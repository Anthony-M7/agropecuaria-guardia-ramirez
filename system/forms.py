from django import forms
from .models import Producto, InformacionAdicional, Proveedor, AreaAlmacen, UnidadMedida, Etiqueta
from django.forms.models import inlineformset_factory

# Formulario principal para el modelo Producto
class ProductoForm(forms.ModelForm):
    # Campo M2M (ManyToManyField) para seleccionar etiquetas existentes
    etiquetas = forms.ModelMultipleChoiceField(
        queryset=Etiqueta.objects.all(),
        # APLICAMOS LA CLASE AL WIDGET AQUÍ, NO EN EL TEMPLATE
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}), 
        required=False,
        label="Etiquetas Existentes" 
    )
    
    # Campo para crear nuevas etiquetas (ya tiene 'form-control')
    nuevas_etiquetas = forms.CharField(
        required=False, 
        label="Crear Nuevas Etiquetas (separadas por comas)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Producto
        # Excluye la foto_producto, que a menudo se maneja por separado si se usa un formulario más simple
        exclude = ('foto_producto',) 
        fields = [
            'nombre', 'codigoBarras', 'codigoProducto', 'descripcion', 
            'area', 'proveedor_principal', 'unidad_medida', 
            'precio_venta', 'costo_promedio_referencia', 'stock_minimo', 
            'etiquetas'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class InformacionAdicionalBaseForm(forms.ModelForm):
    class Meta:
        model = InformacionAdicional
        fields = '__all__'

    # Sobreescribe el constructor para forzar que todos los campos sean opcionales
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Recorre todos los campos del formulario y los hace no requeridos
        for field in self.fields.values():
            field.required = False

InformacionAdicionalFormSet = inlineformset_factory(
    Producto, 
    InformacionAdicional, 
    form=InformacionAdicionalBaseForm,  # 👈 Usa tu formulario base aquí
    fields='__all__',
    extra=1, 
    max_num=1, 
    can_delete=False
)