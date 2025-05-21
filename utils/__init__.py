"""
Módulo de utilidades para la aplicación de métodos numéricos.

Contiene:
- parser.py: Evaluación segura de funciones matemáticas
- plotter.py: Generación de gráficas interactivas
"""

try:
    from .parser import validate_function, evaluate_function, get_allowed_functions
    from .plotter import create_ode_plot, create_comparison_plot

    __all__ = [
        'validate_function',
        'evaluate_function',
        'get_allowed_functions',
        'create_ode_plot',
        'create_comparison_plot'
    ]
except ImportError as e:
    print(f"Warning: Could not import some utilities: {e}")
    __all__ = []