import random
import requests

CONSUMO_DIARIO_KWH = 25

def generar_precios_electricidad(usar_api_real=True):
    """Obtiene precios de electricidad de OMIE o mock"""
    if usar_api_real:
        try:
            response = requests.get('https://api.esios.ree.es/archives/70', timeout=5)
            if response.status_code == 200:
                datos = response.json()
                return _procesar_precios_electricidad(datos.get('datos', []))
        except:
            pass
    return _generar_mock_electricidad()

def _procesar_precios_electricidad(datos_omie):
    if not datos_omie:
        return _generar_mock_electricidad()
    precios = [float(d) for d in datos_omie[:24]]
    return _calcular_estadisticas(precios)

def _generar_mock_electricidad():
    precios_base = [0.065, 0.058, 0.052, 0.048, 0.055, 0.072, 0.095, 0.135, 0.165, 0.158, 0.142, 0.128, 0.115, 0.125, 0.138, 0.155, 0.198, 0.215, 0.235, 0.245, 0.228, 0.185, 0.145, 0.085]
    precios = [round(p * random.uniform(0.95, 1.05), 4) for p in precios_base]
    return _calcular_estadisticas(precios)

def _calcular_estadisticas(precios):
    precio_minimo = min(precios)
    precio_maximo = max(precios)
    precio_promedio = round(sum(precios) / len(precios), 4)
    mejores = sorted([{'inicio': f"{i:02d}:00", 'fin': f"{(i+4):02d}:00", 'promedio': round(sum(precios[i:i+4]) / 4, 4)} for i in range(len(precios) - 3)], key=lambda x: x['promedio'])
    horas = [{'hora': f"{h:02d}:00", 'precio': p, 'estado': "🟢 Barata" if p <= precio_minimo * 1.1 else ("🔴 Cara" if p >= precio_maximo * 0.85 else "🟡 Media"), 'categoria': 'cheap' if p <= precio_minimo * 1.1 else ('expensive' if p >= precio_maximo * 0.85 else 'medium')} for h, p in enumerate(precios)]
    return {'horas': horas, 'precio_minimo': precio_minimo, 'precio_maximo': precio_maximo, 'precio_promedio': precio_promedio, 'mejor_ventana': mejores[0], 'coste_diario_estimado': round(CONSUMO_DIARIO_KWH * precio_promedio, 2), 'coste_mensual_estimado': round(CONSUMO_DIARIO_KWH * precio_promedio * 30, 2)}
