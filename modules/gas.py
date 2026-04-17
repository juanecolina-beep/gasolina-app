import random

def generar_tarifa_gas():
    precio_kwh = round(random.uniform(0.038, 0.052), 4)
    termino_fijo = 0.35
    consumo_diario_gas = 8
    coste_variable_diario = round(consumo_diario_gas * precio_kwh, 2)
    coste_fijo_diario = termino_fijo
    coste_diario_total = round(coste_variable_diario + coste_fijo_diario, 2)
    coste_mensual_total = round(coste_diario_total * 30, 2)
    tendencia = random.choice(['sube', 'baja', 'estable'])
    alerta = {'sube': '⚠️ Cambio de tarifa detectado', 'baja': '✅ Tarifa en descenso', 'estable': '✅ Tarifa estable'}[tendencia]
    return {'precio_kwh': precio_kwh, 'termino_fijo_diario': termino_fijo, 'consumo_estimado_diario': consumo_diario_gas, 'consumo_estimado_mensual': consumo_diario_gas * 30, 'coste_variable_diario': coste_variable_diario, 'coste_fijo_diario': coste_fijo_diario, 'coste_diario_total': coste_diario_total, 'coste_mensual_total': coste_mensual_total, 'alerta': alerta, 'tendencia': tendencia, 'tarifa_type': 'T1 - Residencial', 'unidad': '€/kWh'}
