# dashboard/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Count, Q
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.db import transaction
from .forms import ProductoForm, InformacionAdicionalFormSet
from decimal import Decimal
from .models import *

@login_required
def aplicar_conversion_precios(productos_list, configuracionStr):
    # --- 1. Inicializar el factor y la moneda de referencia ---
    moneda_referencia = configuracionStr[1] 
    factor_conversion = Decimal('1.0') # Por defecto, no hay conversión

    # --- 2. Determinar el factor de conversión basado en la moneda ---
    try:
        if moneda_referencia == 'COP':
            # Asume: Precio del producto está en USD, lo convertimos a COP
            factor_conversion = Decimal(configuracionStr[2]) 
        
        elif moneda_referencia == 'BS':
            # Asume: Precio del producto está en USD, lo convertimos a BS
            factor_conversion = Decimal(configuracionStr[0]) 
            
        # Para cualquier otra moneda (ej. 'USD'), el factor_conversion se mantiene en 1.0

    except (TypeError, IndexError, ValueError):
        # Manejo de errores si la configuración es inválida
        print("Advertencia: El factor de conversión no es válido. Usando precio original.")
        factor_conversion = Decimal('1.0')

    # --- 3. Aplicar el cálculo y añadir el atributo 'precio_display' ---
    for producto in productos_list:
        producto.precio_display = producto.precio_venta * factor_conversion 
        
    return productos_list

@login_required
def page_info(request):
    return render(request, 'dashboard/page_info.html')

# @login_required
# def get_date_range(periodo):
#     # ... (tu implementación de get_date_range)
#     # Ya la tienes definida, solo asegúrate de que esté en el ámbito correcto.
#     now = timezone.now()
#     if periodo == 'mensual':
#         start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#         label = f"Mensual. Desde el {start_date.strftime('%d-%m-%Y')} hasta el {now.strftime('%d-%m-%Y')}"
#     elif periodo == 'anual':
#         start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
#         label = f"Anual. Desde el {start_date.strftime('%d-%m-%Y')} hasta el {now.strftime('%d-%m-%Y')}"
#     else: # Por defecto: Diario
#         start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
#         label = f"Diario. Desde el {start_date.strftime('%d-%m-%Y %H:%M')} hasta Ahora ({now.strftime('%d-%m-%Y %H:%M')})"
        
#     return start_date, now, label


@login_required
def dashboard(request):
    # Obtener el período (usando GET si es desde el filtro de tiempo, POST si es recarga normal)
    periodo_seleccionado = request.POST.get('periodo') or request.GET.get('periodo', 'diario')
    # start_date, end_date, periodo_label = get_date_range(periodo_seleccionado)
    
    # ----------------------------------------------
    # 1. Configuración Administrativa (Solo Lectura)
    # ----------------------------------------------
    try:
        config = configuraciones_admin.objects.get(pk=1)
    except configuraciones_admin.DoesNotExist:
        config = None
        
    # ----------------------------------------------
    # 2. Balance y Resumen General (De momento, ceros)
    # ----------------------------------------------
    ventas_totales = 0.00
    compras_totales = 0.00
    balance_neto = 0.00
    
    # ----------------------------------------------
    # 5. Contexto para el Template
    # ----------------------------------------------
    context = {
        'config': config,
        'periodo_seleccionado': periodo_seleccionado,
        # 'periodo_label': periodo_label,
        'ventas_totales': ventas_totales,
        'compras_totales': compras_totales,
        'balance_neto': balance_neto,
        
        # Necesitamos variables para el buscador global (añadidas en el paso 3)
        'search_query': '',
        'search_results': [],
    }

    return render(request, 'dashboard/dashboard.html', context)

@login_required
def productos(request):
    return render(request, 'inventario/productos.html')

@login_required
def productosCategoria(request, categoria):
    configuraciones = configuraciones_admin.objects.all()

    configuracionStr = []

    for con in configuraciones:
        configuracionStr.append(con.tasa_cambio_bs)
        configuracionStr.append(con.mostrar_precios)
        configuracionStr.append(con.tasa_cambio_cop)

    # Obtener los parámetros de la URL (filtros)
    search_query = request.GET.get('search', '')

    categoriaDB = AreaAlmacen.objects.get(nombre=categoria)

    try:
        productos_list = Producto.objects.filter(area=categoriaDB)

        # Aplicar el filtro de búsqueda
        if search_query:
            # Usa Q objects para combinar múltiples campos en una búsqueda OR
            productos_list = productos_list.filter(
                Q(nombre__icontains=search_query) |
                Q(codigoProducto__icontains=search_query) |
                Q(codigoBarras__icontains=search_query) |
                Q(etiquetas__nombre__icontains=search_query)
            ).distinct()

        productos_list = aplicar_conversion_precios(productos_list, configuracionStr)

    # ❌ CAMBIO CLAVE: Capturar la excepción (e) y registrarla
    except Exception as e:
        # O para una simple impresión en la consola:
        print(f"Ocurrió un error inesperado: {e}")
        import traceback
        traceback.print_exc()

    return render(request, 'inventario/productos_categoria.html', {
        'categoria': categoriaDB,
        'productosList': productos_list,
        "configuracion": configuracionStr,
    })

@login_required
def registrar_producto(request):
    if request.method == 'POST':
        # 1. Crear instancias de los formularios con los datos POST
        producto_form = ProductoForm(request.POST, request.FILES) 
        
        if producto_form.is_valid():
            try:
                # Usar transaction.atomic para asegurar que si falla uno, falla todo
                with transaction.atomic():
                    # 1. Guardar el Producto principal
                    producto_instance = producto_form.save(commit=False)
                    producto_instance.save()
                    
                    # 2. PROCESAR Y ASOCIAR ETIQUETAS EXISTENTES
                    etiquetas_seleccionadas = producto_form.cleaned_data.get('etiquetas')
                    producto_instance.etiquetas.set(etiquetas_seleccionadas)
                    
                    # 3. PROCESAR Y CREAR NUEVAS ETIQUETAS
                    nuevas_etiquetas_str = producto_form.cleaned_data.get('nuevas_etiquetas')
                    if nuevas_etiquetas_str:
                        # Separa la cadena por comas y elimina espacios
                        nombres_etiquetas = [
                            nombre.strip() 
                            for nombre in nuevas_etiquetas_str.split(',') 
                            if nombre.strip()
                        ]

                        for nombre in nombres_etiquetas:
                            # Intenta obtener la etiqueta; si no existe, la crea
                            etiqueta, created = Etiqueta.objects.get_or_create(
                                nombre=nombre
                            )
                            # Asocia la etiqueta (existente o nueva) al producto
                            producto_instance.etiquetas.add(etiqueta)

                    # 4. Manejar el FormSet de Información Adicional
                    info_adicional_formset = InformacionAdicionalFormSet(
                        request.POST, 
                        request.FILES, 
                        instance=producto_instance
                    )
                    
                    if info_adicional_formset.is_valid():
                        info_adicional_formset.save()
                        return redirect('productos') 
                    else:
                        # Si falla el FormSet, eleva el error (la transacción se revertirá)
                        raise Exception("Error al guardar la información adicional") 

            except Exception as e:
                # Manejar errores de base de datos o de transacción
                print(f"Error al guardar el producto y la info adicional: {e}")
                # Re-renderizar con el error
        
    else:
        # Inicializar formularios vacíos para el método GET
        producto_form = ProductoForm()
        # Inicializar el FormSet sin instancia para que esté vacío
        info_adicional_formset = InformacionAdicionalFormSet(instance=Producto()) 

    context = {
        'producto_form': producto_form,
        'info_adicional_formset': info_adicional_formset,
        'titulo': 'Registrar Nuevo Producto',
    }
    return render(request, 'inventario/registrar_producto.html', context)

@login_required
def guardar_configuracion(request):
    if request.method == 'POST':
        
        # 1. Obtener el registro o crear uno
        # Asume pk=1 como convención si config_id no está en el POST
        config_id = request.POST.get('config_id', 1) 
        
        try:
            # Intenta obtener por PK, si no existe, levanta DoesNotExist
            config = configuraciones_admin.objects.get(pk=config_id)
        except configuraciones_admin.DoesNotExist:
            # Si no existe, crea un nuevo registro
            config = configuraciones_admin.objects.create(pk=1) 

        # 2. Actualizar los campos
        try:
            # Obtener los valores del POST
            tasa_cop_str = request.POST.get('tasa_cambio_cop', '').strip()
            tasa_bs_str = request.POST.get('tasa_cambio_bs', '').strip()
            
            # NOTA: Tu vista original buscaba 'mostrar_precios', no 'mostrar_precios_en'
            moneda_principal = request.POST.get('mostrar_precios_en') 
            
            # --- Conversión Robusta y Asignación ---
            
            # Tasa COP: Reemplaza coma por punto y solo convierte si hay valor
            if tasa_cop_str:
                # 💡 SOLUCIÓN CLAVE: Reemplazar la coma (,) por el punto (.)
                # Esto previene el error 'ConversionSyntax'
                config.tasa_cambio_cop = Decimal(tasa_cop_str.replace(',', '.'))
            
            # Tasa BS: Reemplaza coma por punto y solo convierte si hay valor
            if tasa_bs_str:
                # 💡 SOLUCIÓN CLAVE: Reemplazar la coma (,) por el punto (.)
                config.tasa_cambio_bs = Decimal(tasa_bs_str.replace(',', '.'))
                
            # Moneda principal
            if moneda_principal:
                # Asume que el campo del modelo es 'mostrar_precios'
                config.mostrar_precios = moneda_principal
            
            config.save()
            messages.success(request, "Configuración de precios actualizada con éxito.")
        
        # Capturamos el error de conversión (ValueError, ConversionSyntax)
        except (ValueError, KeyError, TypeError, Exception):
            # Usar 'Exception' al final es una buena práctica si la lógica es compleja
            messages.error(request, "Error: Los valores de las tasas de cambio son inválidos. Asegúrese de que son números y use el punto o coma decimal de forma correcta.")
            
    # Redirige a la página anterior (usa un nombre de URL por defecto más seguro)
    referer_url = request.META.get('HTTP_REFERER')
    if referer_url:
        return redirect(referer_url)
    else:
        # Fallback a una URL conocida si no hay HTTP_REFERER (ej. tu dashboard)
        # Reemplaza 'nombre_del_dashboard' por la URL name real de tu dashboard
        return redirect('nombre_del_dashboard')