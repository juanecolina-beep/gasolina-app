#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os, pandas as pd
from datetime import datetime
import random

DOCS = "docs"
os.makedirs(DOCS, exist_ok=True)
CONSUMO_DIARIO_KWH = 25
PRESUPUESTO_GASOLINA = 100

def generar_precios_electricidad():
    precios_base = [0.065, 0.058, 0.052, 0.048, 0.055, 0.072, 0.095, 0.135, 0.165, 0.158, 0.142, 0.128, 0.115, 0.125, 0.138, 0.155, 0.198, 0.215, 0.235, 0.245, 0.228, 0.185, 0.145, 0.085]
    precios = [round(p * random.uniform(0.95, 1.05), 4) for p in precios_base]
    precio_minimo, precio_maximo = min(precios), max(precios)
    precio_promedio = round(sum(precios) / len(precios), 4)
    mejores = sorted([{'inicio': f"{i:02d}:00", 'fin': f"{(i+4):02d}:00", 'promedio': round(sum(precios[i:i+4]) / 4, 4)} for i in range(len(precios) - 3)], key=lambda x: x['promedio'])
    horas = [{'hora': f"{h:02d}:00", 'precio': p, 'estado': "🟢 Barata" if p <= precio_minimo * 1.1 else ("🔴 Cara" if p >= precio_maximo * 0.85 else "🟡 Media"), 'categoria': "cheap" if p <= precio_minimo * 1.1 else ("expensive" if p >= precio_maximo * 0.85 else "medium")} for h, p in enumerate(precios)]
    return {'horas': horas, 'precio_minimo': precio_minimo, 'precio_maximo': precio_maximo, 'precio_promedio': precio_promedio, 'mejor_ventana': mejores[0], 'coste_diario_estimado': round(CONSUMO_DIARIO_KWH * precio_promedio, 2), 'coste_mensual_estimado': round(CONSUMO_DIARIO_KWH * precio_promedio * 30, 2)}

def generar_tarifa_gas():
    precio_kwh = round(random.uniform(0.038, 0.052), 4)
    termino_fijo = 0.35
    consumo_diario_gas = 8
    coste_variable_diario = round(consumo_diario_gas * precio_kwh, 2)
    coste_fijo_diario = termino_fijo
    coste_diario_total = round(coste_variable_diario + coste_fijo_diario, 2)
    coste_mensual_total = round(coste_diario_total * 30, 2)
    alerta = "⚠️ Cambio de tarifa detectado" if random.choice([True, False]) else "✅ Tarifa estable"
    return {'precio_kwh': precio_kwh, 'termino_fijo_diario': termino_fijo, 'consumo_estimado_diario': consumo_diario_gas, 'consumo_estimado_mensual': consumo_diario_gas * 30, 'coste_variable_diario': coste_variable_diario, 'coste_fijo_diario': coste_fijo_diario, 'coste_diario_total': coste_diario_total, 'coste_mensual_total': coste_mensual_total, 'alerta': alerta, 'tarifa_type': 'T1 - Residencial', 'unidad': '€/kWh'}

def cargar_datos_gasolina():
    csv_path = "precios_gasolina.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path, sep=';')
            df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
            return df
        except:
            pass
    return pd.DataFrame({'estacion': ['REPSOL Aranjuez', 'CEPSA Aranjuez', 'Shell Aranjuez', 'REPSOL Seseña', 'BP Seseña', 'REPSOL Seseña Premium'], 'precio': [1.759, 1.779, 1.789, 1.749, 1.799, 1.769], 'localidad': ['Aranjuez', 'Aranjuez', 'Aranjuez', 'Seseña', 'Seseña', 'Seseña']})

def analizar_gasolina(df):
    if df.empty or 'precio' not in df.columns:
        return None
    df_clean = df.dropna(subset=['precio']).copy()
    if df_clean.empty:
        return None
    min_row, max_row = df_clean.loc[df_clean['precio'].idxmin()], df_clean.loc[df_clean['precio'].idxmax()]
    avg_price = float(df_clean['precio'].mean())
    precio_min, precio_max = float(min_row['precio']), float(max_row['precio'])
    alerta = "🟢 MUY BARATA" if precio_min < 1.75 else ("🟡 Buen precio" if precio_min < 1.85 else "🔴 Caro")
    estado = "ok" if precio_min < 1.75 else ("warn" if precio_min < 1.85 else "bad")
    porcentaje_mes = random.uniform(0.4, 0.9)
    gasto_acumulado = PRESUPUESTO_GASOLINA * porcentaje_mes
    saldo_restante = PRESUPUESTO_GASOLINA - gasto_acumulado
    alerta_presupuesto = "⚠️ Te quedan pocos fondos" if saldo_restante < PRESUPUESTO_GASOLINA * 0.1 else ("✅ Presupuesto saludable" if saldo_restante > PRESUPUESTO_GASOLINA * 0.7 else "")
    top3 = df_clean.nsmallest(3, 'precio')
    top3_list = [{'posicion': i + 1, 'estacion': str(row['estacion']), 'precio': float(row['precio']), 'localidad': str(row.get('localidad', ''))} for i, (_, row) in enumerate(top3.iterrows())]
    return {'mejor': {'estacion': str(min_row.get('estacion', '?')), 'precio': precio_min, 'alerta': alerta, 'estado': estado, 'localidad': str(min_row.get('localidad', ''))}, 'peor': {'estacion': str(max_row.get('estacion', '?')), 'precio': precio_max, 'localidad': str(max_row.get('localidad', ''))}, 'promedio': round(avg_price, 3), 'total': len(df_clean), 'top3': top3_list, 'presupuesto': {'mensual': PRESUPUESTO_GASOLINA, 'gasto_acumulado': round(gasto_acumulado, 2), 'saldo_restante': round(saldo_restante, 2), 'dias_restantes': 30 - int(porcentaje_mes * 30), 'alerta': alerta_presupuesto}}

def generar_recomendaciones(electricidad, gas, gasolina):
    recomendaciones = []
    if electricidad['mejor_ventana']['inicio'] < '08:00':
        recomendaciones.append({'tipo': 'electricidad', 'icono': '⚡', 'titulo': 'Mejor horario', 'detalle': f"Entre {electricidad['mejor_ventana']['inicio']}-{electricidad['mejor_ventana']['fin']}", 'ahorro_estimado': round(electricidad['coste_mensual_estimado'] * 0.15, 2)})
    if gas['alerta'] == "✅ Tarifa estable":
        recomendaciones.append({'tipo': 'gas', 'icono': '🔥', 'titulo': 'Tarifa estable', 'detalle': 'Sin cambios', 'ahorro_estimado': 0})
    if gasolina['presupuesto']['saldo_restante'] < gasolina['presupuesto']['mensual'] * 0.2:
        recomendaciones.append({'tipo': 'gasolina', 'icono': '⛽', 'titulo': 'Control de presupuesto', 'detalle': f"Te quedan {gasolina['presupuesto']['saldo_restante']:.2f}€", 'ahorro_estimado': 0})
    recomendaciones.append({'tipo': 'general', 'icono': '💡', 'titulo': 'Consejo', 'detalle': 'Cargar en horas valle', 'ahorro_estimado': 5.00})
    return recomendaciones

def generar_datos():
    print("🔄 Iniciando...")
    df = cargar_datos_gasolina()
    gasolina_data = analizar_gasolina(df)
    electricidad_data = generar_precios_electricidad()
    gas_data = generar_tarifa_gas()
    total_mes = round(electricidad_data['coste_mensual_estimado'] + gas_data['coste_mensual_total'] + gasolina_data['presupuesto']['gasto_acumulado'], 2)
    datos = {'timestamp': datetime.now().isoformat(), 'status': 'ok', 'resumen_financiero': {'electricidad': electricidad_data['coste_mensual_estimado'], 'gas': gas_data['coste_mensual_total'], 'gasolina': gasolina_data['presupuesto']['gasto_acumulado'], 'total_mensual': total_mes, 'moneda': 'EUR'}, 'gasolina': gasolina_data, 'electricidad': electricidad_data, 'gas': gas_data, 'recomendaciones': generar_recomendaciones(electricidad_data, gas_data, gasolina_data)}
    json_path = os.path.join(DOCS, 'datos.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"✅ {gasolina_data['total']} estaciones - Mejor: {gasolina_data['mejor']['estacion']} @ {gasolina_data['mejor']['precio']}€ - Total: {total_mes}€")

if __name__ == '__main__':
    generar_datos()
    print("✨ Listo")
