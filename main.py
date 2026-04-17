#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Integral de Energía y Combustible - ESPAÑA
Generador de datos: Electricidad (OMIE) + Gas (TUR) + Gasolina + Presupuesto + Recomendaciones
"""

import json
import os
import pandas as pd
import math
from datetime import datetime, timedelta
import random

# =========================
# CONFIGURACIÓN
# =========================
DOCS = "docs"
os.makedirs(DOCS, exist_ok=True)

# Parámetros configurables
CONSUMO_DIARIO_KWH = 25  # kWh por día (luz)
PRESUPUESTO_GASOLINA = 100  # € mensuales
PRECIO_LITRO_GASOLINA = 1.769  # € (referencia)

# =========================
# GENERAR PRECIOS HORARIOS ELECTRICIDAD (OMIE simulado)
# =========================
def generar_precios_electricidad():
    """
    Simula precios horarios OMIE (Operador del Mercado Ibérico de Energía)
    Patrón realista: bajo de noche (2-6h), medio día, alto atardecer (19-21h)
    """
    precios_base = [
        0.065, 0.058, 0.052, 0.048, 0.055, 0.072,  # 00-05: Muy baratos
        0.095, 0.135, 0.165, 0.158, 0.142, 0.128,  # 06-11: Caros (mañana)
        0.115, 0.125, 0.138, 0.155, 0.198, 0.215,  # 12-17: Medio-Caros
        0.235, 0.245, 0.228, 0.185, 0.145, 0.085   # 18-23: Muy caros (tarde-noche)
    ]
    
    # Añadir variación realista
    precios = []
    for precio_base in precios_base:
        variacion = random.uniform(0.95, 1.05)
        precios.append(round(precio_base * variacion, 4))
    
    # Calcular estadísticas
    precio_minimo = min(precios)
    precio_maximo = max(precios)
    precio_promedio = round(sum(precios) / len(precios), 4)
    
    # Encontrar mejor ventana de 4h
    mejores_ventanas = []
    for i in range(len(precios) - 3):
        ventana_sum = sum(precios[i:i+4])
        mejores_ventanas.append({
            'inicio': f"{i:02d}:00",
            'fin': f"{(i+4):02d}:00",
            'promedio': round(ventana_sum / 4, 4)
        })
    mejores_ventanas.sort(key=lambda x: x['promedio'])
    mejor_ventana = mejores_ventanas[0]
    
    # Generar detalle por hora
    horas = []
    for h, precio in enumerate(precios):
        if precio <= precio_minimo * 1.1:
            estado = "🟢 Barata"
            categoria = "cheap"
        elif precio >= precio_maximo * 0.85:
            estado = "🔴 Cara"
            categoria = "expensive"
        else:
            estado = "🟡 Media"
            categoria = "medium"
        
        horas.append({
            'hora': f"{h:02d}:00",
            'precio': precio,
            'estado': estado,
            'categoria': categoria
        })
    
    return {
        'horas': horas,
        'precio_minimo': precio_minimo,
        'precio_maximo': precio_maximo,
        'precio_promedio': precio_promedio,
        'mejor_ventana': mejor_ventana,
        'coste_diario_estimado': round(CONSUMO_DIARIO_KWH * precio_promedio, 2),
        'coste_mensual_estimado': round(CONSUMO_DIARIO_KWH * precio_promedio * 30, 2)
    }

# =========================
# GENERAR TARIFA GAS (TUR Naturgy simulada)
# =========================
def generar_tarifa_gas():
    """
    Simula tarifa TUR (Tarifa de Último Recurso) de Naturgy
    Componentes: término fijo + término variable
    """
    # Datos realistas para T1 (residencial)
    precio_kwh = round(random.uniform(0.038, 0.052), 4)  # €/kWh
    termino_fijo = 0.35  # € por día
    
    # Consumo estimado
    consumo_diario_gas = 8  # kWh/día (estimado residencial)
    consumo_mensual_gas = consumo_diario_gas * 30
    
    # Costes
    coste_variable_diario = round(consumo_diario_gas * precio_kwh, 2)
    coste_fijo_diario = termino_fijo
    coste_diario_total = round(coste_variable_diario + coste_fijo_diario, 2)
    coste_mensual_total = round(coste_diario_total * 30, 2)
    
    # Alerta de cambios
    cambio_tarifa = random.choice([True, False])
    alerta_tarifa = "⚠️ Cambio de tarifa detectado" if cambio_tarifa else "✅ Tarifa estable"
    
    return {
        'precio_kwh': precio_kwh,
        'termino_fijo_diario': termino_fijo,
        'consumo_estimado_diario': consumo_diario_gas,
        'consumo_estimado_mensual': consumo_mensual_gas,
        'coste_variable_diario': coste_variable_diario,
        'coste_fijo_diario': coste_fijo_diario,
        'coste_diario_total': coste_diario_total,
        'coste_mensual_total': coste_mensual_total,
        'alerta': alerta_tarifa,
        'tarifa_type': 'T1 - Residencial',
        'unidad': '€/kWh'
    }

# =========================
# CARGAR Y ANALIZAR GASOLINA
# =========================
def cargar_datos_gasolina():
    """Carga datos del CSV principal"""
    csv_path = "precios_gasolina.csv"
    
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
            return df
        except Exception as e:
            print(f"⚠️ Error cargando CSV: {e}")
    
    # Datos de ejemplo
    return pd.DataFrame({
        'estacion': ['Gasolina Express', 'Shell Premium', 'Repsol Slover', 'BP Energía', 'Cepsa Plus'],
        'precio': [1.749, 1.789, 1.769, 1.799, 1.759],
    })

# =========================
# ANALIZAR GASOLINA CON PRESUPUESTO
# =========================
def analizar_gasolina(df):
    """Analiza datos de gasolina e integra presupuesto mensual"""
    if df.empty or 'precio' not in df.columns:
        return None
    
    df_clean = df.dropna(subset=['precio']).copy()
    
    if df_clean.empty:
        return None
    
    min_row = df_clean.loc[df_clean['precio'].idxmin()]
    max_row = df_clean.loc[df_clean['precio'].idxmax()]
    avg_price = float(df_clean['precio'].mean())
    
    precio_min = float(min_row['precio'])
    precio_max = float(max_row['precio'])
    
    # Determinar alerta de precio
    if precio_min < 1.75:
        alerta = "🟢 MUY BARATA"
        estado = "ok"
    elif precio_min < 1.85:
        alerta = "🟡 Buen precio"
        estado = "warn"
    else:
        alerta = "🔴 Caro"
        estado = "bad"
    
    # Cálculo de presupuesto mensual
    litros_mensuales = PRESUPUESTO_GASOLINA / precio_min
    consumo_diario = litros_mensuales / 30
    gasto_diario = precio_min * consumo_diario
    
    # Simular consumo del mes (aleatorio 40-90% del presupuesto)
    porcentaje_mes = random.uniform(0.4, 0.9)
    gasto_acumulado = PRESUPUESTO_GASOLINA * porcentaje_mes
    saldo_restante = PRESUPUESTO_GASOLINA - gasto_acumulado
    
    alerta_presupuesto = ""
    if saldo_restante < PRESUPUESTO_GASOLINA * 0.1:
        alerta_presupuesto = "⚠️ Te quedan pocos fondos"
    elif saldo_restante > PRESUPUESTO_GASOLINA * 0.7:
        alerta_presupuesto = "✅ Presupuesto saludable"
    
    # Top 3
    top3 = df_clean.nsmallest(3, 'precio')
    top3_list = [
        {
            'posicion': i + 1,
            'estacion': str(row['estacion']),
            'precio': float(row['precio'])
        }
        for i, (_, row) in enumerate(top3.iterrows())
    ]
    
    return {
        'mejor': {
            'estacion': str(min_row.get('estacion', '?')),
            'precio': precio_min,
            'alerta': alerta,
            'estado': estado
        },
        'peor': {
            'estacion': str(max_row.get('estacion', '?')),
            'precio': precio_max
        },
        'promedio': round(avg_price, 3),
        'total': len(df_clean),
        'top3': top3_list,
        'presupuesto': {
            'mensual': PRESUPUESTO_GASOLINA,
            'gasto_acumulado': round(gasto_acumulado, 2),
            'saldo_restante': round(saldo_restante, 2),
            'dias_restantes': 30 - int(porcentaje_mes * 30),
            'alerta': alerta_presupuesto
        }
    }

# =========================
# GENERAR RECOMENDACIONES INTELIGENTES
# =========================
def generar_recomendaciones(electricidad, gas, gasolina):
    """Crea recomendaciones personalizadas de ahorro"""
    recomendaciones = []
    
    # Recomendaciones de electricidad
    if electricidad['mejor_ventana']['inicio'] < '08:00':
        recomendaciones.append({
            'tipo': 'electricidad',
            'icono': '⚡',
            'titulo': 'Mejor horario para consumo',
            'detalle': f"Usa lavadora y lavavajillas entre {electricidad['mejor_ventana']['inicio']}-{electricidad['mejor_ventana']['fin']}",
            'ahorro_estimado': round(electricidad['coste_mensual_estimado'] * 0.15, 2)
        })
    
    # Recomendaciones de gas
    if gas['alerta'] == "✅ Tarifa estable":
        recomendaciones.append({
            'tipo': 'gas',
            'icono': '🔥',
            'titulo': 'Tarifa estable',
            'detalle': 'Tu tarifa de gas se mantiene sin cambios',
            'ahorro_estimado': 0
        })
    
    # Recomendaciones de gasolina
    if gasolina['presupuesto']['saldo_restante'] < gasolina['presupuesto']['mensual'] * 0.2:
        recomendaciones.append({
            'tipo': 'gasolina',
            'icono': '⛽',
            'titulo': 'Control de presupuesto',
            'detalle': f"Te quedan {gasolina['presupuesto']['saldo_restante']:.2f}€ para este mes",
            'ahorro_estimado': 0
        })
    
    recomendaciones.append({
        'tipo': 'general',
        'icono': '💡',
        'titulo': 'Consejo del día',
        'detalle': 'Cargar el coche en horas valle (02:00-06:00) te ayuda a ahorrar con tarifa variable',
        'ahorro_estimado': 5.00
    })
    
    return recomendaciones

# =========================
# GENERAR DATOS JSON COMPLETO
# =========================
def generar_datos():
    """Genera datos completos y los guarda como JSON"""
    
    print("🔄 Iniciando procesamiento de datos...")
    
    # Generar todos los datos
    df = cargar_datos_gasolina()
    gasolina_data = analizar_gasolina(df)
    electricidad_data = generar_precios_electricidad()
    gas_data = generar_tarifa_gas()
    
    # Calcular resumen financiero
    total_electricidad_mes = electricidad_data['coste_mensual_estimado']
    total_gas_mes = gas_data['coste_mensual_total']
    total_gasolina_mes = gasolina_data['presupuesto']['gasto_acumulado']
    
    total_mes = round(total_electricidad_mes + total_gas_mes + total_gasolina_mes, 2)
    
    # Estructura completa
    datos = {
        'timestamp': datetime.now().isoformat(),
        'status': 'ok',
        'resumen_financiero': {
            'electricidad': total_electricidad_mes,
            'gas': total_gas_mes,
            'gasolina': total_gasolina_mes,
            'total_mensual': total_mes,
            'moneda': 'EUR'
        },
        'gasolina': gasolina_data,
        'electricidad': electricidad_data,
        'gas': gas_data,
        'recomendaciones': generar_recomendaciones(electricidad_data, gas_data, gasolina_data)
    }
    
    # Guardar JSON
    json_path = os.path.join(DOCS, 'datos.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Datos generados en {json_path}")
    print(f"   - Gasolina: {gasolina_data['total']} estaciones")
    print(f"   - Mejor gasolina: {gasolina_data['mejor']['estacion']} @ {gasolina_data['mejor']['precio']}€")
    print(f"   - Electricidad: {electricidad_data['coste_diario_estimado']}€/día")
    print(f"   - Gas: {gas_data['coste_diario_total']}€/día")
    print(f"   - Total mensual: {total_mes}€")
    print(f"   - Timestamp: {datos['timestamp']}")
    
    return datos

# =========================
# MAIN
# =========================
if __name__ == '__main__':
    generar_datos()
    print("✨ Proceso completado")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Integral de Energía y Combustible - ESPAÑA
Generador de datos: Electricidad (OMIE) + Gas (TUR) + Gasolina + Presupuesto + Recomendaciones
"""

import json
import os
import pandas as pd
import math
from datetime import datetime, timedelta
import random

# =========================
# CONFIGURACIÓN
# =========================
DOCS = "docs"
os.makedirs(DOCS, exist_ok=True)

# Parámetros configurables
CONSUMO_DIARIO_KWH = 25  # kWh por día (luz)
PRESUPUESTO_GASOLINA = 100  # € mensuales
PRECIO_LITRO_GASOLINA = 1.769  # € (referencia)

# =========================
# GENERAR PRECIOS HORARIOS ELECTRICIDAD (OMIE simulado)
# =========================
def generar_precios_electricidad():
    """
    Simula precios horarios OMIE (Operador del Mercado Ibérico de Energía)
    Patrón realista: bajo de noche (2-6h), medio día, alto atardecer (19-21h)
    """
    precios_base = [
        0.065, 0.058, 0.052, 0.048, 0.055, 0.072,  # 00-05: Muy baratos
        0.095, 0.135, 0.165, 0.158, 0.142, 0.128,  # 06-11: Caros (mañana)
        0.115, 0.125, 0.138, 0.155, 0.198, 0.215,  # 12-17: Medio-Caros
        0.235, 0.245, 0.228, 0.185, 0.145, 0.085   # 18-23: Muy caros (tarde-noche)
    ]
    
    # Añadir variación realista
    precios = []
    for precio_base in precios_base:
        variacion = random.uniform(0.95, 1.05)
        precios.append(round(precio_base * variacion, 4))
    
    # Calcular estadísticas
    precio_minimo = min(precios)
    precio_maximo = max(precios)
    precio_promedio = round(sum(precios) / len(precios), 4)
    
    # Encontrar mejor ventana de 4h
    mejores_ventanas = []
    for i in range(len(precios) - 3):
        ventana_sum = sum(precios[i:i+4])
        mejores_ventanas.append({
            'inicio': f"{i:02d}:00",
            'fin': f"{(i+4):02d}:00",
            'promedio': round(ventana_sum / 4, 4)
        })
    mejores_ventanas.sort(key=lambda x: x['promedio'])
    mejor_ventana = mejores_ventanas[0]
    
    # Generar detalle por hora
    horas = []
    for h, precio in enumerate(precios):
        if precio <= precio_minimo * 1.1:
            estado = "🟢 Barata"
            categoria = "cheap"
        elif precio >= precio_maximo * 0.85:
            estado = "🔴 Cara"
            categoria = "expensive"
        else:
            estado = "🟡 Media"
            categoria = "medium"
        
        horas.append({
            'hora': f"{h:02d}:00",
            'precio': precio,
            'estado': estado,
            'categoria': categoria
        })
    
    return {
        'horas': horas,
        'precio_minimo': precio_minimo,
        'precio_maximo': precio_maximo,
        'precio_promedio': precio_promedio,
        'mejor_ventana': mejor_ventana,
        'coste_diario_estimado': round(CONSUMO_DIARIO_KWH * precio_promedio, 2),
        'coste_mensual_estimado': round(CONSUMO_DIARIO_KWH * precio_promedio * 30, 2)
    }

# =========================
# GENERAR TARIFA GAS (TUR Naturgy simulada)
# =========================
def generar_tarifa_gas():
    """
    Simula tarifa TUR (Tarifa de Último Recurso) de Naturgy
    Componentes: término fijo + término variable
    """
    # Datos realistas para T1 (residencial)
    precio_kwh = round(random.uniform(0.038, 0.052), 4)  # €/kWh
    termino_fijo = 0.35  # € por día
    
    # Consumo estimado
    consumo_diario_gas = 8  # kWh/día (estimado residencial)
    consumo_mensual_gas = consumo_diario_gas * 30
    
    # Costes
    coste_variable_diario = round(consumo_diario_gas * precio_kwh, 2)
    coste_fijo_diario = termino_fijo
    coste_diario_total = round(coste_variable_diario + coste_fijo_diario, 2)
    coste_mensual_total = round(coste_diario_total * 30, 2)
    
    # Alerta de cambios
    cambio_tarifa = random.choice([True, False])
    alerta_tarifa = "⚠️ Cambio de tarifa detectado" if cambio_tarifa else "✅ Tarifa estable"
    
    return {
        'precio_kwh': precio_kwh,
        'termino_fijo_diario': termino_fijo,
        'consumo_estimado_diario': consumo_diario_gas,
        'consumo_estimado_mensual': consumo_mensual_gas,
        'coste_variable_diario': coste_variable_diario,
        'coste_fijo_diario': coste_fijo_diario,
        'coste_diario_total': coste_diario_total,
        'coste_mensual_total': coste_mensual_total,
        'alerta': alerta_tarifa,
        'tarifa_type': 'T1 - Residencial',
        'unidad': '€/kWh'
    }

    """Carga datos del CSV principal"""
    csv_path = "precios_gasolina.csv"
    
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
            return df
        except Exception as e:
            print(f"⚠️ Error cargando CSV: {e}")
    
    # Datos de ejemplo
    return pd.DataFrame({
        'estacion': ['Gasolina Express', 'Shell Premium', 'Repsol Slover', 'BP Energía', 'Cepsa Plus'],
        'precio': [1.749, 1.789, 1.769, 1.799, 1.759],
    })

# =========================
# ANALIZAR GASOLINA
# =========================
def analizar_gasolina(df):
    """Analiza datos de gasolina"""
    if df.empty or 'precio' not in df.columns:
        return None
    
    df_clean = df.dropna(subset=['precio']).copy()
    
    if df_clean.empty:
        return None
    
    min_row = df_clean.loc[df_clean['precio'].idxmin()]
    max_row = df_clean.loc[df_clean['precio'].idxmax()]
    avg_price = float(df_clean['precio'].mean())
    
    precio_min = float(min_row['precio'])
    precio_max = float(max_row['precio'])
    
    # Determinar alerta
    if precio_min < 1.75:
        alerta = "🚨 MUY BARATA"
        estado = "ok"
    elif precio_min < 1.85:
        alerta = "⚠️ Buen precio"
        estado = "warn"
    else:
        alerta = "🔥 Caro"
        estado = "bad"
    
    # Top 3
    top3 = df_clean.nsmallest(3, 'precio')
    top3_list = [
        {
            'posicion': i + 1,
            'estacion': str(row['estacion']),
            'precio': float(row['precio'])
        }
        for i, (_, row) in enumerate(top3.iterrows())
    ]
    
    return {
        'mejor': {
            'estacion': str(min_row.get('estacion', '?')),
            'precio': precio_min,
            'alerta': alerta,
            'estado': estado
        },
        'peor': {
            'estacion': str(max_row.get('estacion', '?')),
            'precio': precio_max
        },
        'promedio': round(avg_price, 3),
        'total': len(df_clean),
        'top3': top3_list
    }

# =========================
# ANALIZAR ENERGÍA
# =========================
def analizar_energia():
    """Obtiene datos de energía (valores por defecto)"""
    precio_luz = 0.135  # €/kWh
    precio_gas = 0.042   # €/kWh
    
    if precio_luz < 0.08:
        estado_luz = "🟢 Barata"
    elif precio_luz < 0.15:
        estado_luz = "🟡 Media"
    else:
        estado_luz = "🔴 Cara"
    
    return {
        'luz': {
            'precio': precio_luz,
            'unidad': '€/kWh',
            'estado': estado_luz
        },
        'gas': {
            'precio': precio_gas,
            'unidad': '€/kWh',
            'estado': '⚖️ Normal'
        }
    }

# =========================
# GENERAR DATOS JSON
# =========================
def generar_datos():
    """Genera datos completos y los guarda como JSON"""
    
    print("🔄 Iniciando procesamiento de datos...")
    
    # Cargar datos
    df = cargar_datos_gasolina()
    gasolina_data = analizar_gasolina(df)
    energia_data = analizar_energia()
    
    # Estructura completa
    datos = {
        'timestamp': datetime.now().isoformat(),
        'status': 'ok' if gasolina_data else 'error',
        'gasolina': gasolina_data,
        'energia': energia_data
    }
    
    # Guardar JSON
    json_path = os.path.join(DOCS, 'datos.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Datos generados en {json_path}")
    print(f"   - Gasolina: {gasolina_data['total'] if gasolina_data else 0} estaciones")
    print(f"   - Mejor: {gasolina_data['mejor']['estacion'] if gasolina_data else 'N/A'} @ {gasolina_data['mejor']['precio'] if gasolina_data else 'N/A'}€")
    print(f"   - Timestamp: {datos['timestamp']}")
    
    return datos

# =========================
# MAIN
# =========================
if __name__ == '__main__':
    generar_datos()
    print("✨ Proceso completado")