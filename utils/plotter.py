import matplotlib

matplotlib.use('Agg')  # Backend no interactivo para servidor
import matplotlib.pyplot as plt
import numpy as np
import os
from typing import Dict, List, Optional, Tuple
import seaborn as sns

# Configurar estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class ODEPlotter:
    """
    Generador de gráficas para métodos de solución de ecuaciones diferenciales.
    """

    def __init__(self, figsize=(12, 8), dpi=150):
        """
        Inicializar el graficador.

        Args:
            figsize (tuple): Tamaño de la figura
            dpi (int): Resolución de la imagen
        """
        self.figsize = figsize
        self.dpi = dpi
        self.colors = {
            'Euler': '#FF6B6B',
            'Heun': '#4ECDC4',
            'exact': '#45B7D1',
            'grid': '#E8E8E8',
            'predictor': '#FFA726'
        }

    def create_solution_plot(self, results: Dict, title: str, filename: str,
                             compare_with: Optional[Dict] = None) -> str:
        """
        Crear gráfica de la solución de una ecuación diferencial.

        Args:
            results (dict): Resultados del método numérico
            title (str): Título de la gráfica
            filename (str): Nombre del archivo de salida
            compare_with (dict, optional): Resultados de otro método para comparar

        Returns:
            str: Ruta del archivo generado
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.figsize, dpi=self.dpi)
        fig.suptitle(title, fontsize=16, fontweight='bold')

        # Datos principales
        plot_data = results['plot_data']
        x_vals = plot_data['x_values']
        y_vals = plot_data['y_values']
        method = plot_data['method']

        # GRÁFICA 1: Solución principal
        ax1.plot(x_vals, y_vals, 'o-',
                 color=self.colors.get(method, '#FF6B6B'),
                 linewidth=2, markersize=4,
                 label=f'Solución {method}')

        # Si es Heun, mostrar también el predictor
        if method == 'Heun' and 'y_predictor' in plot_data:
            x_pred = x_vals[:-1]  # Excluir último punto
            y_pred = plot_data['y_predictor']
            ax1.plot(x_pred, y_pred, 's--',
                     color=self.colors['predictor'],
                     linewidth=1, markersize=3, alpha=0.7,
                     label='Predictor (Euler)')

        # Comparación con otro método si se proporciona
        if compare_with:
            comp_data = compare_with['plot_data']
            ax1.plot(comp_data['x_values'], comp_data['y_values'],
                     '^-', linewidth=2, markersize=4, alpha=0.8,
                     label=f"Comparación {comp_data['method']}")

        ax1.set_xlabel('x', fontsize=12)
        ax1.set_ylabel('y', fontsize=12)
        ax1.set_title('Solución Numérica de la EDO', fontsize=14)
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # GRÁFICA 2: Campo de pendientes (si es útil)
        self._add_slope_field(ax2, results, x_vals, y_vals)

        plt.tight_layout()

        # Guardar archivo
        filepath = os.path.join('static', 'plots', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        return filepath

    def create_comparison_plot(self, euler_results: Dict, heun_results: Dict,
                               filename: str) -> str:
        """
        Crear gráfica comparativa entre métodos de Euler y Heun.

        Args:
            euler_results (dict): Resultados del método de Euler
            heun_results (dict): Resultados del método de Heun
            filename (str): Nombre del archivo de salida

        Returns:
            str: Ruta del archivo generado
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10), dpi=self.dpi)
        fig.suptitle('Comparación: Método de Euler vs Método de Heun',
                     fontsize=16, fontweight='bold')

        # Datos
        euler_data = euler_results['plot_data']
        heun_data = heun_results['plot_data']

        # GRÁFICA 1: Soluciones superpuestas
        ax1.plot(euler_data['x_values'], euler_data['y_values'],
                 'o-', color=self.colors['Euler'], linewidth=2,
                 markersize=4, label='Euler')
        ax1.plot(heun_data['x_values'], heun_data['y_values'],
                 '^-', color=self.colors['Heun'], linewidth=2,
                 markersize=4, label='Heun')
        ax1.set_title('Comparación de Soluciones')
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # GRÁFICA 2: Diferencia absoluta
        x_common = euler_data['x_values']
        diff = np.abs(np.array(heun_data['y_values']) - np.array(euler_data['y_values']))
        ax2.plot(x_common, diff, 's-', color='red', linewidth=2, markersize=3)
        ax2.set_title('Diferencia Absoluta |Heun - Euler|')
        ax2.set_xlabel('x')
        ax2.set_ylabel('|Diferencia|')
        ax2.grid(True, alpha=0.3)
        ax2.set_yscale('log')

        # GRÁFICA 3: Euler con detalles
        self._plot_method_details(ax3, euler_results, 'Euler')

        # GRÁFICA 4: Heun con detalles
        self._plot_method_details(ax4, heun_results, 'Heun')

        plt.tight_layout()

        # Guardar archivo
        filepath = os.path.join('static', 'plots', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        return filepath

    def _add_slope_field(self, ax, results: Dict, x_vals: List, y_vals: List):
        """
        Agregar campo de pendientes a la gráfica.

        Args:
            ax: Axes de matplotlib
            results (dict): Resultados del método
            x_vals (list): Valores de x
            y_vals (list): Valores de y
        """
        # Crear malla para campo de pendientes
        x_min, x_max = min(x_vals), max(x_vals)
        y_min, y_max = min(y_vals), max(y_vals)

        # Expandir un poco el rango
        x_range = x_max - x_min
        y_range = y_max - y_min
        x_min -= 0.1 * x_range
        x_max += 0.1 * x_range
        y_min -= 0.1 * y_range
        y_max += 0.1 * y_range

        # Crear malla (reducida para mejor visualización)
        nx, ny = 15, 12
        x_mesh = np.linspace(x_min, x_max, nx)
        y_mesh = np.linspace(y_min, y_max, ny)
        X, Y = np.meshgrid(x_mesh, y_mesh)

        # Calcular pendientes usando la función del problema
        try:
            from utils.parser import evaluate_function
            # Obtener función del primer resultado
            steps = results['steps_table']
            if steps:
                # Usar la función implícita en los cálculos
                # (En una implementación completa, guardaríamos la función original)
                DX = np.ones_like(X)
                DY = np.zeros_like(Y)

                # Placeholder: usar pendientes calculadas como referencia
                for i, step in enumerate(steps[:min(len(steps), nx)]):
                    if 'slope' in step and step['slope'] != 'N/A':
                        if i < len(x_mesh):
                            DY[:, i] = step['slope']

                # Normalizar vectores
                N = np.sqrt(DX ** 2 + DY ** 2)
                DX, DY = DX / N, DY / N

                ax.quiver(X, Y, DX, DY, alpha=0.5, scale=20, width=0.003, color='gray')
        except:
            pass  # Si no se puede crear el campo, continuar sin él

        # Plotear la solución
        ax.plot(x_vals, y_vals, 'o-', linewidth=3, markersize=5)
        ax.set_title('Solución con Campo de Direcciones')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, alpha=0.3)

    def _plot_method_details(self, ax, results: Dict, method_name: str):
        """
        Plotear detalles específicos del método.

        Args:
            ax: Axes de matplotlib
            results (dict): Resultados del método
            method_name (str): Nombre del método
        """
        plot_data = results['plot_data']
        x_vals = plot_data['x_values']
        y_vals = plot_data['y_values']

        ax.plot(x_vals, y_vals, 'o-',
                color=self.colors.get(method_name, '#FF6B6B'),
                linewidth=2, markersize=4)

        # Mostrar algunos pasos intermedios
        step_indices = np.linspace(0, len(x_vals) - 1, min(6, len(x_vals))).astype(int)
        for i in step_indices:
            ax.annotate(f'({x_vals[i]:.2f}, {y_vals[i]:.2f})',
                        (x_vals[i], y_vals[i]),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=8, alpha=0.8)

        ax.set_title(f'Detalles - {method_name}')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, alpha=0.3)


# Instancia global del graficador
_plotter = ODEPlotter()


def create_ode_plot(results: Dict, title: str, filename: str) -> str:
    """
    Crear gráfica de la solución de una EDO.

    Args:
        results (dict): Resultados del método numérico
        title (str): Título de la gráfica
        filename (str): Nombre del archivo

    Returns:
        str: Ruta del archivo generado
    """
    return _plotter.create_solution_plot(results, title, filename)


def create_comparison_plot(euler_results: Dict, heun_results: Dict, filename: str) -> str:
    """
    Crear gráfica comparativa entre métodos.

    Args:
        euler_results (dict): Resultados de Euler
        heun_results (dict): Resultados de Heun
        filename (str): Nombre del archivo

    Returns:
        str: Ruta del archivo generado
    """
    return _plotter.create_comparison_plot(euler_results, heun_results, filename)