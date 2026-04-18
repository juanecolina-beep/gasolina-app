import os
import pandas as pd

def cargar_datos_gasolina():
    csv_path = "precios_gasolina.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path, sep=';')
            df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
            return df
        except:
            pass
    return pd.DataFrame({'estacion': ['REPSOL Aranjuez', 'CEPSA Aranjuez', 'Shell Aranjuez', 'REPSOL Seseña', 'BP Seseña', 'REPSOL Seseña Premium'], 'precio': [1.759, 1.779, 1.789, 1.749, 1.799, 1.769], 'localidad': ['Aranjuez', 'Aranjuez', 'Aranjuez', 'Seseña', 'Seseña', 'Seseña'], 'direccion': ['Calle de la Industria, 23', 'Av. del Príncipe Carlos, 45', 'Carretera Toledo-Cuenca', 'Autovía A-4 KM. 32', 'Ctra. Nacional 430', 'Calle Industrial 56'], 'lat': [40.0, 40.01, 40.02, 40.1, 40.11, 40.12], 'lon': [-3.6, -3.61, -3.62, -3.5, -3.51, -3.52]})

def analizar_gasolina(df, presupuesto=100):
    if df.empty or 'precio' not in df.columns:
        return None
    df_clean = df.dropna(subset=['precio']).copy()
    if df_clean.empty:
        return None
    min_row = df_clean.loc[df_clean['precio'].idxmin()]
    max_row = df_clean.loc[df_clean['precio'].idxmax()]
    avg_price = float(df_clean['precio'].mean())
    presupuesto_dinero = presupuesto
    litros_posibles = round(presupuesto_dinero / avg_price, 1)
    porcentaje_gastado = int((presupuesto_dinero / presupuesto_dinero) * 100)
    alerta_presupuesto = "🟢 OK" if porcentaje_gastado < 80 else ("🟡 Cuidado" if porcentaje_gastado < 90 else "🔴 Límite")
    
    estaciones_list = []
    for _, row in df_clean.iterrows():
        est = {
            'nombre': row.get('estacion', 'No disponible'),
            'precio': float(row['precio']),
            'localidad': row.get('localidad', 'No disponible'),
            'direccion': row.get('direccion', 'No disponible'),
            'lat': float(row.get('lat', 40.0)),
            'lon': float(row.get('lon', -3.6))
        }
        estaciones_list.append(est)
    
    return {
        'mejor': {
            'estacion': min_row.get('estacion', 'No disponible'),
            'precio': float(min_row['precio']),
            'localidad': min_row.get('localidad', 'No disponible'),
            'direccion': min_row.get('direccion', 'No disponible')
        },
        'peor': {
            'estacion': max_row.get('estacion', 'No disponible'),
            'precio': float(max_row['precio']),
            'localidad': max_row.get('localidad', 'No disponible'),
            'direccion': max_row.get('direccion', 'No disponible')
        },
        'promedio': round(avg_price, 3),
        'presupuesto': {
            'total': presupuesto_dinero,
            'litros_posibles': litros_posibles,
            'porcentaje_gastado': porcentaje_gastado,
            'alerta': alerta_presupuesto
        },
        'estaciones': estaciones_list
    }

def calcular_comparador(gasolina_data):
    if not gasolina_data or 'estaciones' not in gasolina_data:
        return None
    estaciones = gasolina_data['estaciones']
    seseña = [e for e in estaciones if e['localidad'].lower() == 'seseña']
    aranjuez = [e for e in estaciones if e['localidad'].lower() == 'aranjuez']
    mejor_seseña = min(seseña, key=lambda x: x['precio']) if seseña else None
    mejor_aranjuez = min(aranjuez, key=lambda x: x['precio']) if aranjuez else None
    if not mejor_seseña or not mejor_aranjuez:
        return None
    diferencia = round(mejor_seseña['precio'] - mejor_aranjuez['precio'], 3)
    ahorro_deposito = round(diferencia * 50, 2)
    ahorro_mensual = round(ahorro_deposito * 8, 2)
    recomendacion = "🟢 ARANJUEZ MEJOR" if diferencia > 0 else "🔴 SESEÑA MEJOR"
    return {
        'seseña': mejor_seseña,
        'aranjuez': mejor_aranjuez,
        'diferencia_precio': diferencia,
        'ahorro_deposito': ahorro_deposito,
        'ahorro_mensual_estimado': ahorro_mensual,
        'recomendacion': recomendacion
    }
