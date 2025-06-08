import numpy as np
from utils.parser import evaluate_function


class RungeKuttaMethod:
    """
    Implementación del Método de Runge-Kutta de 4to orden para resolver ecuaciones
    diferenciales de la forma: dy/dx = f(x, y) con condición inicial y(x0) = y0
    """

    def __init__(self, function_str, x0, y0, h, num_steps):
        """
        Inicializar el método de Runge-Kutta.

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
        self.k1_values = np.zeros(num_steps + 1)  # k1 = f(x_i, y_i)
        self.k2_values = np.zeros(num_steps + 1)  # k2 = f(x_i + h/2, y_i + k1*h/2)
        self.k3_values = np.zeros(num_steps + 1)  # k3 = f(x_i + h/2, y_i + k2*h/2)
        self.k4_values = np.zeros(num_steps + 1)  # k4 = f(x_i + h, y_i + k3*h)

        # Condiciones iniciales
        self.x_values[0] = x0
        self.y_values[0] = y0

    def solve(self):
        """
        Ejecutar el método de Runge-Kutta para resolver la ecuación diferencial.

        Returns:
            dict: Diccionario con los resultados organizados para mostrar
        """
        try:
            # Calcular k1 inicial
            self.k1_values[0] = evaluate_function(self.function_str, self.x0, self.y0)

            # Aplicar método de Runge-Kutta iterativamente
            for i in range(self.num_steps):
                # Valores actuales
                x_current = self.x_values[i]
                y_current = self.y_values[i]

                # PASO 1: Calcular k1 = f(x_i, y_i)
                k1 = evaluate_function(self.function_str, x_current, y_current)
                self.k1_values[i] = k1

                # PASO 2: Calcular k2 = f(x_i + h/2, y_i + k1*h/2)
                x_mid1 = x_current + self.h/2
                y_mid1 = y_current + k1 * self.h/2
                k2 = evaluate_function(self.function_str, x_mid1, y_mid1)
                self.k2_values[i] = k2

                # PASO 3: Calcular k3 = f(x_i + h/2, y_i + k2*h/2)
                x_mid2 = x_current + self.h/2
                y_mid2 = y_current + k2 * self.h/2
                k3 = evaluate_function(self.function_str, x_mid2, y_mid2)
                self.k3_values[i] = k3

                # PASO 4: Calcular k4 = f(x_i + h, y_i + k3*h)
                x_next = x_current + self.h
                y_next_approx = y_current + k3 * self.h
                k4 = evaluate_function(self.function_str, x_next, y_next_approx)
                self.k4_values[i] = k4

                # PASO 5: Calcular y_{i+1} usando la fórmula de RK4
                # y_{i+1} = y_i + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
                self.x_values[i + 1] = x_next
                self.y_values[i + 1] = y_current + (self.h/6) * (k1 + 2*k2 + 2*k3 + k4)

            # Calcular k1 final para completar la tabla
            self.k1_values[-1] = evaluate_function(
                self.function_str,
                self.x_values[-1],
                self.y_values[-1]
            )

            return self._format_results()

        except Exception as e:
            raise Exception(f"Error en método de Runge-Kutta: {str(e)}")

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

            # Para pasos intermedios, agregar cálculos detallados del método de Runge-Kutta
            if i < len(self.x_values) - 1:
                k1 = self.k1_values[i]
                k2 = self.k2_values[i]
                k3 = self.k3_values[i]
                k4 = self.k4_values[i]
                weighted_avg = (k1 + 2*k2 + 2*k3 + k4) / 6

                step_data.update({
                    'k2': round(k2, 6),
                    'k3': round(k3, 6),
                    'k4': round(k4, 6),
                    'weighted_slope': round(weighted_avg, 6),
                    'calculation': f"y_{i + 1} = {step_data['y']:.6f} + ({self.h}/6) × ({k1:.6f} + 2×{k2:.6f} + 2×{k3:.6f} + {k4:.6f}) = {round(self.y_values[i + 1], 6):.6f}"
                })

            steps_table.append(step_data)

        # Datos para la gráfica
        plot_data = {
            'x_values': self.x_values.tolist(),
            'y_values': self.y_values.tolist(),
            'method': 'Runge-Kutta'
        }

        # Información del método
        method_info = {
            'name': 'Método de Runge-Kutta (4to Orden)',
            'formula': 'y_{n+1} = y_n + (h/6) × (k_1 + 2k_2 + 2k_3 + k_4)',
            'description': 'Método de cuarto orden para resolver EDOs con alta precisión',
            'order': 4,
            'error_type': 'O(h⁵) por paso, O(h⁴) global',
            'steps': [
                '1. k₁ = f(xₙ, yₙ)',
                '2. k₂ = f(xₙ + h/2, yₙ + k₁h/2)',
                '3. k₃ = f(xₙ + h/2, yₙ + k₂h/2)',
                '4. k₄ = f(xₙ + h, yₙ + k₃h)',
                '5. yₙ₊₁ = yₙ + (h/6)(k₁ + 2k₂ + 2k₃ + k₄)'
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