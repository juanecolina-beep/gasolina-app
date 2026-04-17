#!/usr/bin/env python3
"""
Script para instalar todas las dependencias necesarias
Ejecutar: python setup_fase2.py
"""

import subprocess
import sys
import os

def run_command(cmd, description=""):
    """Ejecuta un comando y muestra resultado"""
    if description:
        print(f"\n📦 {description}")
        print("=" * 60)
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=False)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("  🚀 FASE 2: Setup de Backend + Frontend")
    print("=" * 60)
    
    # Cambiar a directorio gasolina-app
    os.chdir(r"c:\Users\USER\Documents\gasolina-app")
    
    # 1. Instalar dependencias Python
    print("\n1️⃣ Instalando dependencias Python...")
    if not run_command(
        "pip install --upgrade pip && pip install -r requirements.txt",
        "Installing Python packages..."
    ):
        return False
    
    # 2. Instalar dependencias Node.js
    print("\n2️⃣ Instalando dependencias Node.js...")
    os.chdir(r"c:\Users\USER\Documents\gasolina-nextjs")
    if not run_command(
        "npm install",
        "Installing NPM packages..."
    ):
        return False
    
    print("\n" + "=" * 60)
    print("  ✅ Setup completado!")
    print("=" * 60)
    print("\n📋 Próximos pasos:\n")
    print("  Terminal 1 (Backend):")
    print("    cd c:\\Users\\USER\\Documents\\gasolina-app")
    print("    python backend/main.py")
    print()
    print("  Terminal 2 (Frontend):")
    print("    cd c:\\Users\\USER\\Documents\\gasolina-nextjs")
    print("    npm run dev")
    print()
    print("  Browser:")
    print("    http://localhost:3000")
    print()

if __name__ == "__main__":
    main()
