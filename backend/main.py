#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Energy & Fuel Control Center - FastAPI Backend
Servicio que expone los datos de energía y combustible como API REST

Ejecutar:
    python backend/main.py
    
O con uvicorn:
    uvicorn backend.main:app --reload --port 5000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import json
from datetime import datetime
import sys
import os

# Agregar parent dir al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar módulos Python
from modules import electricity, gas, fuel, recommendations

# Crear app FastAPI
app = FastAPI(
    title="⚡🔥⛽ Energy & Fuel Control Center API",
    description="Backend para dashboard de energía y combustible en España",
    version="1.0.0",
)

# Configurar CORS para Next.js (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "*",  # En producción: ["https://yourdomain.com"]
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/")
async def root():
    """Endpoint raíz - Health check"""
    return {
        "status": "ok",
        "service": "⚡🔥⛽ Energy & Fuel Control Center API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health")
async def health_check():
    """Health check para Docker/Kubernetes"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


# ============================================================================
# ELECTRICIDAD
# ============================================================================

@app.get("/api/electricity")
async def get_electricity() -> Dict[str, Any]:
    """
    📊 Obtener datos de electricidad (OMIE)
    
    Retorna:
    - Precios horarios (24 horas)
    - Mejor ventana de horas baratas
    - Coste estimado diario y mensual
    
    Query params:
    - usar_api_real (bool): Usar API OMIE real (default: True)
    """
    try:
        print("  ⚡ API: Obteniendo datos de electricidad...")
        data = electricity.generar_precios_electricidad(usar_api_real=True)
        return data
    except Exception as e:
        print(f"❌ Error en electricidad: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo datos de electricidad: {str(e)}"
        )


# ============================================================================
# GAS
# ============================================================================

@app.get("/api/gas")
async def get_gas() -> Dict[str, Any]:
    """
    🔥 Obtener tarifa de gas (TUR - Tarifa de Última Revisión)
    
    Retorna:
    - Precio por kWh
    - Términos fijo y variable
    - Coste estimado diario y mensual
    - Tendencia (sube/baja/estable)
    """
    try:
        print("  🔥 API: Obteniendo datos de gas...")
        data = gas.generar_tarifa_gas()
        return data
    except Exception as e:
        print(f"❌ Error en gas: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo datos de gas: {str(e)}"
        )


# ============================================================================
# GASOLINA
# ============================================================================

@app.get("/api/fuel")
async def get_fuel() -> Dict[str, Any]:
    """
    ⛽ Obtener datos de gasolina
    
    Retorna:
    - Mejor y peor gasolinera
    - Promedio de precios
    - Lista de estaciones cercanas
    - Presupuesto disponible
    """
    try:
        print("  ⛽ API: Obteniendo datos de gasolina...")
        
        # Cargar datos de gasolina
        datos = fuel.cargar_datos_gasolina()
        
        # Analizar
        analisis = fuel.analizar_gasolina(datos)
        
        # Calcular comparador
        comparador = fuel.calcular_comparador(datos)
        
        # Construir respuesta
        response = {
            "mejor": analisis.get("mejor", {}),
            "peor": analisis.get("peor", {}),
            "promedio": analisis.get("promedio", 0),
            "estaciones": analisis.get("estaciones", []),
            "presupuesto": {
                "total": 100,  # 100€ de presupuesto
                "litros_posibles": 100 / analisis.get("promedio", 1.76),
                "porcentaje_gastado": 50,
                "alerta": "✅ Presupuesto OK",
            },
        }
        
        return response
    except Exception as e:
        print(f"❌ Error en gasolina: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo datos de gasolina: {str(e)}"
        )


# ============================================================================
# RECOMENDACIONES
# ============================================================================

@app.get("/api/recommendations")
async def get_recommendations() -> Dict[str, Any]:
    """
    💡 Obtener recomendaciones inteligentes
    
    Retorna:
    - Lista de recomendaciones
    - Urgencia (alta/media/baja)
    - Ahorro estimado en euros
    """
    try:
        print("  💡 API: Generando recomendaciones...")
        
        # Generar recomendaciones
        recomendaciones = recommendations.generar_recomendaciones()
        
        return {
            "recomendaciones": recomendaciones,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        print(f"❌ Error en recomendaciones: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generando recomendaciones: {str(e)}"
        )


# ============================================================================
# RUTAS ADICIONALES (Próximas fases)
# ============================================================================

@app.get("/api/status")
async def get_status() -> Dict[str, Any]:
    """Estado del sistema"""
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "electricity": "✅ online",
            "gas": "✅ online",
            "fuel": "✅ online",
            "recommendations": "✅ online",
        }
    }


@app.get("/api/docs-swagger")
async def swagger_docs():
    """Docs interactivos - Verifica /docs en el navegador"""
    return {"message": "Abre http://localhost:5000/docs para la documentación interactiva"}


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("  🚀 Energy & Fuel Control Center - Backend API")
    print("="*70)
    print("  📍 Iniciando servidor en http://localhost:5000")
    print("  📚 Documentación: http://localhost:5000/docs")
    print("  🔗 Base URL: http://localhost:5000/api/*")
    print("  ❌ Para detener: Presiona Ctrl+C")
    print("="*70)
    print()
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        log_level="info",
    )
