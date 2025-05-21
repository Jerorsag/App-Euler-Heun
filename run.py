#!/usr/bin/env python3
"""
run.py - Archivo principal para ejecutar la aplicación ODE Solver

Este archivo proporciona una forma sencilla de ejecutar la aplicación
con diferentes configuraciones y manejo de errores.
"""

import os
import sys
import argparse
from pathlib import Path

# Agregar el directorio actual al path para imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))


def create_directories():
    """Crear directorios necesarios si no existen."""
    directories = [
        'flask_session',
        'static/plots',
        'logs'
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directorio '{directory}' verificado/creado")


def check_dependencies():
    """Verificar que las dependencias estén instaladas."""
    required_packages = [
        'flask',
        'numpy',
        'matplotlib',
        'sympy'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} instalado")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} NO instalado")

    if missing_packages:
        print(f"\n⚠️  Faltan dependencias: {', '.join(missing_packages)}")
        print("Instálalas con: pip install -r requirements.txt")
        return False

    print("✓ Todas las dependencias están instaladas")
    return True


def initialize_history():
    """Inicializar archivo de historial si no existe."""
    history_file = 'history.json'
    if not os.path.exists(history_file):
        import json
        with open(history_file, 'w') as f:
            json.dump([], f)
        print(f"✓ Archivo de historial '{history_file}' creado")
    else:
        print(f"✓ Archivo de historial '{history_file}' existe")


def run_app(debug=True, host='127.0.0.1', port=5000):
    """Ejecutar la aplicación Flask."""
    try:
        from app import app

        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    🚀 ODE SOLVER APP                        ║
╠══════════════════════════════════════════════════════════════╣
║  Aplicación web para resolver ecuaciones diferenciales      ║
║  Métodos disponibles: Euler y Heun                          ║
╠══════════════════════════════════════════════════════════════╣
║  🌐 URL: http://{host}:{port}                     ║
║  🛠️  Modo: {'Desarrollo' if debug else 'Producción'}                                  ║
║  📋 Presiona Ctrl+C para detener                            ║
╚══════════════════════════════════════════════════════════════╝
        """)

        app.run(
            debug=debug,
            host=host,
            port=port,
            use_reloader=debug,
            threaded=True
        )

    except ImportError as e:
        print(f"❌ Error al importar la aplicación: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al ejecutar la aplicación: {e}")
        sys.exit(1)


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='ODE Solver - Aplicación web para resolver ecuaciones diferenciales',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python run.py                    # Ejecutar en modo desarrollo
  python run.py --prod             # Ejecutar en modo producción  
  python run.py --port 8080        # Ejecutar en puerto 8080
  python run.py --host 0.0.0.0     # Permitir conexiones externas
        """
    )

    parser.add_argument('--prod', action='store_true',
                        help='Ejecutar en modo producción (debug=False)')
    parser.add_argument('--host', default='127.0.0.1',
                        help='Host para el servidor (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000,
                        help='Puerto para el servidor (default: 5000)')
    parser.add_argument('--skip-checks', action='store_true',
                        help='Saltar verificaciones de dependencias')

    args = parser.parse_args()

    print("🔧 Inicializando ODE Solver App...")

    # Crear directorios necesarios
    create_directories()

    # Verificar dependencias (opcional)
    if not args.skip_checks:
        if not check_dependencies():
            print("\n❌ No se puede ejecutar la aplicación sin las dependencias requeridas")
            sys.exit(1)

    # Inicializar archivos necesarios
    initialize_history()

    # Ejecutar aplicación
    debug_mode = not args.prod

    try:
        run_app(
            debug=debug_mode,
            host=args.host,
            port=args.port
        )
    except KeyboardInterrupt:
        print("\n\n👋 Aplicación detenida por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()