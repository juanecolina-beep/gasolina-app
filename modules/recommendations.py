def generar_recomendaciones(electricidad_data, gas_data, gasolina_data, comparador_data):
    recomendaciones = []
    if electricidad_data:
        mejor_ventana = electricidad_data.get('mejor_ventana', {})
        precio_promedio = electricidad_data.get('precio_promedio', 0)
        precio_minimo = electricidad_data.get('precio_minimo', 0)
        diferencia_pct = ((precio_promedio - precio_minimo) / precio_promedio * 100) if precio_promedio > 0 else 0
        if diferencia_pct > 15:
            ahorro_estimado = round(electricidad_data.get('coste_mensual_estimado', 0) * 0.15, 2)
            recomendaciones.append({'tipo': 'Electricidad', 'titulo': '⚡ Ahorro en horas valle', 'descripcion': f"Usa lavadora entre {mejor_ventana.get('inicio', '02:00')}-{mejor_ventana.get('fin', '06:00')}", 'ahorro_estimado': ahorro_estimado, 'urgencia': 'media'})
    if gas_data:
        tendencia = gas_data.get('tendencia', 'estable')
        if tendencia == 'sube':
            recomendaciones.append({'tipo': 'Gas', 'titulo': '🔥 Cambio de tarifa detectado', 'descripcion': 'Revisa contrato Naturgy. Tarifa al alza', 'ahorro_estimado': 0, 'urgencia': 'media'})
    if comparador_data:
        diferencia = comparador_data.get('diferencia_precio', 0)
        ahorro_mensual = comparador_data.get('ahorro_mensual_estimado', 0)
        mejor_ciudad = 'Aranjuez' if diferencia > 0 else 'Seseña'
        if abs(diferencia) > 0.02:
            urgencia = 'alta' if ahorro_mensual > 50 else 'media'
            recomendaciones.append({'tipo': 'Gasolina', 'titulo': '⛽ Mejor gasolinera encontrada', 'descripcion': f'Dirígete a {mejor_ciudad} - Ahorra {ahorro_mensual}€/mes', 'ahorro_estimado': ahorro_mensual, 'urgencia': urgencia})
    recomendaciones.append({'tipo': 'General', 'titulo': '💡 Consejo del día', 'descripcion': 'Recuerda revisar tus consumos mensuales', 'ahorro_estimado': 0, 'urgencia': 'baja'})
    orden_urgencia = {'alta': 0, 'media': 1, 'baja': 2}
    recomendaciones.sort(key=lambda x: (orden_urgencia.get(x['urgencia'], 3), -x['ahorro_estimado']))
    return recomendaciones
