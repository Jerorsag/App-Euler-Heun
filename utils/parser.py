import ast
import operator
import numpy as np
import math
from typing import Union, Dict, Any


class FunctionEvaluator:
    """
    Evaluador seguro de funciones matemáticas para ecuaciones diferenciales.
    Permite evaluar expresiones como "x + y", "x*sin(y)", etc. de forma segura.
    """

    # Operadores permitidos
    ALLOWED_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    # Funciones matemáticas permitidas
    ALLOWED_FUNCTIONS = {
        # Funciones trigonométricas
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
        'arcsin': np.arcsin,
        'arccos': np.arccos,
        'arctan': np.arctan,
        'asin': np.arcsin,
        'acos': np.arccos,
        'atan': np.arctan,

        # Funciones hiperbólicas
        'sinh': np.sinh,
        'cosh': np.cosh,
        'tanh': np.tanh,
        'arcsinh': np.arcsinh,
        'arccosh': np.arccosh,
        'arctanh': np.arctanh,

        # Funciones exponenciales y logarítmicas
        'exp': np.exp,
        'log': np.log,
        'ln': np.log,
        'log10': np.log10,
        'log2': np.log2,

        # Funciones de potencia y raíz
        'sqrt': np.sqrt,
        'pow': np.power,
        'abs': np.abs,
        'fabs': np.abs,

        # Funciones de redondeo
        'floor': np.floor,
        'ceil': np.ceil,
        'round': np.round,

        # Funciones especiales
        'factorial': math.factorial,
    }

    # Constantes permitidas
    ALLOWED_CONSTANTS = {
        'pi': np.pi,
        'e': np.e,
        'euler': np.e,
        'inf': np.inf,
    }

    def __init__(self):
        self.variables = {}

    def evaluate(self, expression: str, x: float = 0, y: float = 0) -> float:
        """
        Evaluar una expresión matemática de forma segura.

        Args:
            expression (str): Expresión matemática (ej: "x + y", "sin(x)*cos(y)")
            x (float): Valor de la variable x
            y (float): Valor de la variable y

        Returns:
            float: Resultado de la evaluación

        Raises:
            ValueError: Si la expresión no es segura o contiene errores
        """
        # Preparar variables
        self.variables = {'x': x, 'y': y}

        try:
            # Parsear la expresión
            tree = ast.parse(expression, mode='eval')

            # Evaluar el árbol AST
            result = self._eval_node(tree.body)

            # Verificar que el resultado sea un número válido
            if isinstance(result, (int, float, np.integer, np.floating)):
                if np.isfinite(result):
                    return float(result)
                else:
                    raise ValueError(f"Resultado no finito: {result}")
            else:
                raise ValueError(f"Resultado no numérico: {type(result)}")

        except Exception as e:
            raise ValueError(f"Error evaluando '{expression}': {str(e)}")

    def _eval_node(self, node: ast.AST) -> Union[float, int]:
        """
        Evaluar un nodo del árbol AST de forma recursiva.

        Args:
            node: Nodo del AST

        Returns:
            Valor numérico del nodo
        """
        if isinstance(node, ast.Constant):  # Python 3.8+
            return node.value

        elif isinstance(node, ast.Num):  # Compatibilidad con versiones anteriores
            return node.n

        elif isinstance(node, ast.Name):
            # Variable o constante
            var_name = node.id
            if var_name in self.variables:
                return self.variables[var_name]
            elif var_name in self.ALLOWED_CONSTANTS:
                return self.ALLOWED_CONSTANTS[var_name]
            else:
                raise ValueError(f"Variable no permitida: {var_name}")

        elif isinstance(node, ast.BinOp):
            # Operación binaria
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)

            if op_type in self.ALLOWED_OPERATORS:
                # Manejar división por cero
                if op_type == ast.Div and right == 0:
                    raise ValueError("División por cero")
                return self.ALLOWED_OPERATORS[op_type](left, right)
            else:
                raise ValueError(f"Operador no permitido: {op_type.__name__}")

        elif isinstance(node, ast.UnaryOp):
            # Operación unaria
            operand = self._eval_node(node.operand)
            op_type = type(node.op)

            if op_type in self.ALLOWED_OPERATORS:
                return self.ALLOWED_OPERATORS[op_type](operand)
            else:
                raise ValueError(f"Operador unario no permitido: {op_type.__name__}")

        elif isinstance(node, ast.Call):
            # Llamada a función
            func_name = node.func.id if isinstance(node.func, ast.Name) else None

            if func_name in self.ALLOWED_FUNCTIONS:
                func = self.ALLOWED_FUNCTIONS[func_name]
                args = [self._eval_node(arg) for arg in node.args]

                try:
                    return func(*args)
                except Exception as e:
                    raise ValueError(f"Error en función {func_name}: {str(e)}")
            else:
                raise ValueError(f"Función no permitida: {func_name}")

        else:
            raise ValueError(f"Tipo de nodo no soportado: {type(node).__name__}")


# Instancia global del evaluador
_evaluator = FunctionEvaluator()


def validate_function(expression: str) -> bool:
    """
    Validar que una expresión sea segura para evaluar.

    Args:
        expression (str): Expresión a validar

    Returns:
        bool: True si es segura, False en caso contrario
    """
    try:
        # Intentar evaluar con valores de prueba
        _evaluator.evaluate(expression, x=1.0, y=1.0)
        return True
    except:
        return False


def evaluate_function(expression: str, x: float, y: float) -> float:
    """
    Evaluar una función f(x, y) de forma segura.

    Args:
        expression (str): Expresión matemática
        x (float): Valor de x
        y (float): Valor de y

    Returns:
        float: f(x, y)

    Raises:
        ValueError: Si la expresión no es válida
    """
    return _evaluator.evaluate(expression, x, y)


def get_allowed_functions() -> Dict[str, Any]:
    """
    Obtener diccionario de funciones permitidas para mostrar al usuario.

    Returns:
        dict: Funciones organizadas por categoría
    """
    return {
        'trigonométricas': ['sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan'],
        'hiperbólicas': ['sinh', 'cosh', 'tanh', 'arcsinh', 'arccosh', 'arctanh'],
        'exponenciales': ['exp', 'log', 'ln', 'log10', 'log2'],
        'potencias': ['sqrt', 'pow', 'abs'],
        'constantes': ['pi', 'e'],
        'variables': ['x', 'y'],
        'operadores': ['+', '-', '*', '/', '**', '()']
    }