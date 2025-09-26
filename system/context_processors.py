# app_name/context_processors.py

from .models import configuraciones_admin # Ajusta la importación a tu modelo
from decimal import Decimal

def global_config(request):
    """
    Inyecta el objeto de configuración único y la lista de factores en el contexto de la plantilla.
    """
    try:
        # 1. Obtener el único registro (o crear uno si no existe, para evitar fallos)
        config_obj = configuraciones_admin.objects.first()
        if not config_obj:
            config_obj = configuraciones_admin.objects.create(
                tasa_cambio_cop=Decimal('3900.0000'), 
                tasa_cambio_bs=Decimal('160.0000'), 
                mostrar_precios='USD'
            )
            
        # 2. Crear la lista configuracionStr para la lógica de la vista
        configuracionStr = [
            str(config_obj.tasa_cambio_bs),   # Factor 0: Tasa BS (usado en la vista)
            config_obj.mostrar_precios,       # Factor 1: Moneda de Display
            str(config_obj.tasa_cambio_cop)    # Factor 2: Tasa COP (usado en la vista)
        ]

    except Exception:
        # Fallback si el modelo o la DB fallan
        config_obj = None
        configuracionStr = [None, 'USD', None] 

    return {
        'configuracion_obj': config_obj,
        'configuracionStr': configuracionStr,
    }