from django.db import models
from django.conf import settings # ¡Importante!
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.core.files.storage import FileSystemStorage

# Define el almacenamiento local solo si estás en modo de desarrollo.
# Usa os.path para evitar problemas con las rutas en diferentes sistemas operativos.
if settings.DEBUG:
    from django.conf import settings as settings_file
    fs = FileSystemStorage(location=settings_file.MEDIA_ROOT)
else:
    # Si no estás en modo de depuración, usa Cloudinary.
    fs = MediaCloudinaryStorage()


# Create your models here.
# class Nombre_Modelo(models.Model):
#     campo1 = models.CharField()
#     campo1 = models.DecimalField()
#     campo1 = models.EmailField()

# Modelo de COnfiguraciones Personalizadas
class configuraciones_admin(models.Model):
    tasa_cambio_cop = models.DecimalField(max_digits=10, decimal_places=4)
    tasa_cambio_bs = models.DecimalField(max_digits=10, decimal_places=4)
    mostrar_precios = models.CharField(max_length=10)




# Modelos Para el manejo de la informacion de los productos por lotes
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre

class AreaAlmacen(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    prefijo_codigo = models.CharField(max_length=5, unique=True)
    definicion = models.TextField()

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    def __str__(self):
        return self.nombre

class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=50, unique=True) # Ej: Kilogramo, Unidad, Litro
    abreviatura = models.CharField(max_length=10, unique=True) # Ej: KG, UND, LT

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    # --- Identificación y Descripción ---
    nombre = models.CharField(max_length=200)
    codigoBarras = models.CharField(max_length=100, unique=True, blank=True, null=True)
    codigoProducto = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)
    
    # --- Gestión Operativa y Financiera ---
    area = models.ForeignKey(AreaAlmacen, on_delete=models.PROTECT) # Usar PROTECT para evitar borrar áreas con productos
    proveedor_principal = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, default=1)
    
    # El precio de venta (suele ser el más estable)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Venta Público")
    
    # El costo estándar o promedio (para calcular márgenes rápidos)
    costo_promedio_referencia = models.DecimalField(max_digits=10, decimal_places=4) 
    
    stock_minimo = models.PositiveIntegerField(help_text="Nivel de stock para activar alerta de reorden.")

    # --- Archivos y Fotos ---
    foto_producto = models.ImageField(
        upload_to='products_pictures/',
        storage=fs,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"{self.nombre} ({self.area.prefijo_codigo})"


class Lote(models.Model):
    """
    Representa una compra o entrada específica de un producto, 
    gestionando la cantidad, el costo exacto y la caducidad.
    """
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    
    # Control de Lote
    numero_lote = models.CharField(max_length=100, unique=True, help_text="Número de lote del fabricante o interno.")
    fecha_entrada = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    ubicacion_almacen = models.CharField(max_length=100, blank=True) # Ubicación física (pasillo-estante)

    # Control Financiero y de Cantidad
    cantidad_actual = models.PositiveIntegerField(verbose_name="Stock del Lote")
    costo_unitario_lote = models.DecimalField(max_digits=10, decimal_places=4, help_text="Costo unitario real de esta compra.")
    
    def __str__(self):
        return f"Lote {self.numero_lote} de {self.producto.nombre}"
    
class InformacionAdicional(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    informacion = models.TextField(blank=True)
    recomendaciones = models.TextField(blank=True)
    usos = models.TextField(blank=True)
    contraindicaciones = models.TextField(blank=True)
    advertencias_precauciones = models.TextField(blank=True)
    reaccionesAdversas = models.TextField(blank=True)

    def __str__(self):
        return f"Información adicional para {self.producto.nombre}"

