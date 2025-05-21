import numpy as np
from utils.parser import evaluate_function


class HeunMethod:
    """
    Implementación del Método de Heun (Euler mejorado) para resolver ecuaciones
    diferenciales de la forma: dy/dx = f(x, y) con condición inicial y(x0) = y0
    """

    def __init__(self, function_str, x0, y0, h, num_steps):
        """
        Inicializar el método de Heun.

        Args:
            function_str (str): Función f(x,y) como string (ej: "x + y", "x*y - 2*x")
            x0 (float): Valor inicial de x
            y0 (float): Valor inicial de y (condición inicial)
            h (float): Tamaño del paso
            num_steps (int): Número de pasos a realizar
        """
        self.function_str = function_str
        self.x0 = x0
        self.y0 = y0
        self.h = h
        self.num_steps = num_steps

        # Arrays para almacenar resultados
        self.x_values = np.zeros(num_steps + 1)
        self.y_values = np.zeros(num_steps + 1)
        self.k1_values = np.zeros(num_steps + 1)  # Primera pendiente
        self.k2_values = np.zeros(num_steps + 1)  # Segunda pendiente
        self.y_predictor = np.zeros(num_steps + 1)  # Valor predictor (Euler simple)

        # Condiciones iniciales
        self.x_values[0] = x0
        self.y_values[0] = y0

    def solve(self):
        """
        Ejecutar el método de Heun para resolver la ecuación diferencial.

        Returns:
            dict: Diccionario con los resultados organizados para mostrar
        """
        try:
            # Calcular k1 inicial
            self.k1_values[0] = evaluate_function(self.function_str, self.x0, self.y0)

            # Aplicar método de Heun iterativamente
            for i in range(self.num_steps):
                # Valores actuales
                x_current = self.x_values[i]
                y_current = self.y_values[i]

                # PASO 1: Calcular k1 = f(x_i, y_i)
                k1 = evaluate_function(self.function_str, x_current, y_current)
                self.k1_values[i] = k1

                # PASO 2: Predictor usando Euler simple
                # y_predictor = y_i + h * k1
                x_next = x_current + self.h
                y_pred = y_current + self.h * k1
                self.y_predictor[i] = y_pred

                # PASO 3: Calcular k2 = f(x_{i+1}, y_predictor)
                k2 = evaluate_function(self.function_str, x_next, y_pred)
                self.k2_values[i] = k2

                # PASO 4: Corrector (promedio de pendientes)
                # y_{i+1} = y_i + (h/2) * (k1 + k2)
                self.x_values[i + 1] = x_next
                self.y_values[i + 1] = y_current + (self.h / 2) * (k1 + k2)

            # Calcular k1 final para completar la tabla
            self.k1_values[-1] = evaluate_function(
                self.function_str,
                self.x_values[-1],
                self.y_values[-1]
            )

            return self._format_results()

        except Exception as e:
            raise Exception(f"Error en método de Heun: {str(e)}")

    def _format_results(self):
        """
        Formatear resultados para mostrar en la interfaz.

        Returns:
            dict: Resultados formateados
        """
        # Crear tabla de resultados paso a paso
        steps_table = []
        for i in range(len(self.x_values)):
            step_data = {
                'step': i,
                'x': round(self.x_values[i], 6),
                'y': round(self.y_values[i], 6),
                'k1': round(self.k1_values[i], 6) if not np.isnan(self.k1_values[i]) else 'N/A'
            }

            # Para pasos intermedios, agregar cálculos detallados del método de Heun
            if i < len(self.x_values) - 1:
                k1 = self.k1_values[i]
                k2 = self.k2_values[i]
                y_pred = self.y_predictor[i]

                step_data.update({
                    'y_predictor': round(y_pred, 6),
                    'k2': round(k2, 6),
                    'avg_slope': round((k1 + k2) / 2, 6),
                    'calculation': f"y_{i + 1} = {step_data['y']:.6f} + ({self.h}/2) × ({k1:.6f} + {k2:.6f}) = {round(self.y_values[i + 1], 6):.6f}"
                })

            steps_table.append(step_data)

        # Datos para la gráfica
        plot_data = {
            'x_values': self.x_values.tolist(),
            'y_values': self.y_values.tolist(),
            'y_predictor': self.y_predictor[:-1].tolist(),  # Excluir último elemento
            'method': 'Heun'
        }

        # Información del método
        method_info = {
            'name': 'Método de Heun (Euler Mejorado)',
            'formula': 'y_{n+1} = y_n + (h/2) × [f(x_n, y_n) + f(x_{n+1}, y_pred)]',
            'description': 'Método predictor-corrector de segundo orden para resolver EDOs',
            'order': 2,
            'error_type': 'O(h³) por paso, O(h²) global',
            'steps': [
                '1. Predictor: y_pred = y_n + h × f(x_n, y_n)',
                '2. Corrector: y_{n+1} = y_n + (h/2) × [f(x_n, y_n) + f(x_{n+1}, y_pred)]'
            ]
        }

        return {
            'steps_table': steps_table,
            'plot_data': plot_data,
            'method_info': method_info,
            'summary': {
                'initial_value': f"y({self.x0}) = {self.y0}",
                'final_value': f"y({self.x_values[-1]:.6f}) ≈ {self.y_values[-1]:.6f}",
                'total_steps': self.num_steps,
                'step_size': self.h,
                'interval': f"[{self.x0}, {self.x_values[-1]:.6f}]"
            }
        }