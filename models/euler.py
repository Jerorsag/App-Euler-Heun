import numpy as np
from utils.parser import evaluate_function


class EulerMethod:
    """
    Implementación del Método de Euler para resolver ecuaciones diferenciales
    de la forma: dy/dx = f(x, y) con condición inicial y(x0) = y0
    """

    def __init__(self, function_str, x0, y0, h, num_steps):
        """
        Inicializar el método de Euler.

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
        self.slope_values = np.zeros(num_steps + 1)

        # Condiciones iniciales
        self.x_values[0] = x0
        self.y_values[0] = y0

    def solve(self):
        """
        Ejecutar el método de Euler para resolver la ecuación diferencial.

        Returns:
            dict: Diccionario con los resultados organizados para mostrar
        """
        try:
            # Calcular pendiente inicial
            self.slope_values[0] = evaluate_function(self.function_str, self.x0, self.y0)

            # Aplicar método de Euler iterativamente
            for i in range(self.num_steps):
                # Valores actuales
                x_current = self.x_values[i]
                y_current = self.y_values[i]

                # Calcular pendiente f(xi, yi)
                slope = evaluate_function(self.function_str, x_current, y_current)
                self.slope_values[i] = slope

                # Fórmula de Euler: y_{i+1} = y_i + h * f(x_i, y_i)
                self.x_values[i + 1] = x_current + self.h
                self.y_values[i + 1] = y_current + self.h * slope

            # Calcular pendiente final
            self.slope_values[-1] = evaluate_function(
                self.function_str,
                self.x_values[-1],
                self.y_values[-1]
            )

            return self._format_results()

        except Exception as e:
            raise Exception(f"Error en método de Euler: {str(e)}")

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
                'slope': round(self.slope_values[i], 6) if not np.isnan(self.slope_values[i]) else 'N/A'
            }

            # Para pasos intermedios, agregar cálculos detallados
            if i < len(self.x_values) - 1:
                step_data[
                    'calculation'] = f"y_{i + 1} = {step_data['y']:.6f} + {self.h} × {step_data['slope']:.6f} = {round(self.y_values[i + 1], 6):.6f}"

            steps_table.append(step_data)

        # Datos para la gráfica
        plot_data = {
            'x_values': self.x_values.tolist(),
            'y_values': self.y_values.tolist(),
            'method': 'Euler'
        }

        # Información del método
        method_info = {
            'name': 'Método de Euler',
            'formula': 'y_{n+1} = y_n + h × f(x_n, y_n)',
            'description': 'Método numérico de primer orden para resolver EDOs',
            'order': 1,
            'error_type': 'O(h²) por paso, O(h) global'
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