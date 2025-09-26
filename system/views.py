# dashboard/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal
from .models import *

def aplicar_conversion_precios(productos_list, configuracionStr):
    """
    Calcula el precio de visualización para cada producto basado en la moneda de referencia.

    :param productos_list: QuerySet o lista de objetos Producto.
    :param configuracionStr: Lista con [Factor_BS, Moneda_Display, Factor_COP, ...].
    :return: Lista de objetos Producto con el atributo 'precio_display' añadido.
    """
    
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
        producto.precio_display = producto.precio * factor_conversion 
        
    return productos_list


@login_required
def page_info(request):
    return render(request, 'dashboard/page_info.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

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

    except:
        print("Error")

    return render(request, 'inventario/productos_categoria.html', {
        'categoria': categoriaDB,
        'productosList': productos_list,
        "configuracion": configuracionStr,
    })


def guardar_configuracion(request):
    if request.method == 'POST':
        # 1. Obtener el único registro (asumiendo que siempre hay uno)
        config_id = request.POST.get('config_id')
        
        try:
            config = configuraciones_admin.objects.get(pk=config_id)
        except configuraciones_admin.DoesNotExist:
            config = configuraciones_admin.objects.create() # Crea uno si no existe

        # 2. Actualizar los campos
        try:
            config.tasa_cambio_cop = Decimal(request.POST['tasa_cambio_cop'])
            config.tasa_cambio_bs = Decimal(request.POST['tasa_cambio_bs'])
            config.mostrar_precios = request.POST['mostrar_precios']
            
            config.save()
            messages.success(request, "Configuración de precios actualizada con éxito.")
            
        except (ValueError, KeyError):
            messages.error(request, "Error: Los valores de las tasas de cambio son inválidos.")
            
    # Redirige a la página anterior o a la lista de productos
    referer_url = request.META.get('HTTP_REFERER', redirect('productos').url)
        
    # 2. Redirige a la URL obtenida (recarga la página actual)
    return redirect(referer_url)