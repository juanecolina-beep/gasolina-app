#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script generador de datos gasolina + energía
Genera JSON con datos actualizados para el dashboard
"""

import json
import os
import pandas as pd
import math
from datetime import datetime
import requests

# =========================
# CONFIGURACIÓN
# =========================
DOCS = "docs"
os.makedirs(DOCS, exist_ok=True)

# =========================
# CARGAR DATOS GASOLINA
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