#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Energy & Fuel Control Center - Orquestador Principal"""

import json
import os
from datetime import datetime

# Importar módulos
from modules import electricity, gas, fuel, recommendations

DOCS = "docs"
os.makedirs(DOCS, exist_ok=True)
PRESUPUESTO_GASOLINA = 100


def main():
    """Orquestador principal - Genera todos los datos"""
    print("\n🔄 Iniciando generación de datos...")
    print("=" * 50)
    
    # 1. Obtener datos de electricidad
    print("  ⚡ Obteniendo precios de electricidad...")
    electricidad_data = electricity.generar_precios_electricidad(usar_api_real=True)
    
    # 2. Obtener tarifa de gas
    print("  🔥 Obteniendo tarifa de gas (TUR)...")
    gas_data = gas.generar_tarifa_gas()
    
    # 3. Cargar y analizar gasolina
    print("  ⛽ Cargando datos de gasolineras...")
    df_gasolina = fuel.cargar_datos_gasolina()
    print(f"     ✓ {len(df_gasolina)} estaciones cargadas")
    
    gasolina_data = fuel.analizar_gasolina(df_gasolina, PRESUPUESTO_GASOLINA)
    comparador_data = fuel.calcular_comparador(gasolina_data)
    
    # 4. Generar recomendaciones
    print("  💡 Generando recomendaciones...")
    recomendaciones = recommendations.generar_recomendaciones(
        electricidad_data, gas_data, gasolina_data, comparador_data
    )
    
    # 5. Construir JSON final
    datos = {
        'timestamp': datetime.now().isoformat(),
        'electricidad': electricidad_data,
        'gas': gas_data,
        'gasolina': gasolina_data,
        'comparador': comparador_data,
        'recomendaciones': recomendaciones
    }
    
    # 6. Guardar JSON
    json_path = os.path.join(DOCS, 'datos.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    # 7. Mostrar resumen
    print("\n✅ DATOS GENERADOS EXITOSAMENTE")
    print("-" * 50)
    mejor_gasolinera = gasolina_data.get('mejor', {}) if gasolina_data else {}
    total_mensual = (
        electricidad_data.get('coste_mensual_estimado', 0) +
        gas_data.get('coste_mensual_total', 0) +
        (gasolina_data.get('presupuesto', {}).get('total', 0) if gasolina_data else 0)
    )
    
    print(f"   📊 Total mensual: {total_mensual}€")
    print(f"   ⚡ Electricidad: {electricidad_data.get('coste_mensual_estimado', 0)}€")
    print(f"   🔥 Gas: {gas_data.get('coste_mensual_total', 0)}€")
    print(f"   ⛽ Gasolina: {gasolina_data.get('presupuesto', {}).get('total', 0) if gasolina_data else 0}€")
    print(f"   ⛽ Mejor gasolinera: {mejor_gasolinera.get('estacion', 'N/A')} @ {mejor_gasolinera.get('precio', 0)}€")
    print(f"   💡 Recomendaciones: {len(recomendaciones)}")
    print(f"   📁 Archivo: {json_path}")
    print("\n✨ Generación completada")
    print("=" * 50 + "\n")


if __name__ == '__main__':
    main()
