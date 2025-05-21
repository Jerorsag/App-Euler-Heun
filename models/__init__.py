"""
Módulo de métodos numéricos para resolver ecuaciones diferenciales ordinarias.

Este módulo contiene implementaciones de:
- Método de Euler
- Método de Heun (Euler mejorado)
"""

from .euler import EulerMethod
from .heun import HeunMethod

__all__ = ['EulerMethod', 'HeunMethod']