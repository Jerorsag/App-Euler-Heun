from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json
from datetime import datetime
from config import Config

# Importar modelos de métodos numéricos
from models.euler import EulerMethod
from models.heun import HeunMethod
from models.runge_kutta import RungeKuttaMethod

# Importar utilidades
from utils.plotter import create_ode_plot
from utils.parser import validate_function, evaluate_function

app = Flask(__name__)
app.config.from_object(Config)

# Configurar directorio de sesiones
if not os.path.exists('flask_session'):
    os.makedirs('flask_session')

# Configurar directorio de gráficas
if not os.path.exists('static/plots'):
    os.makedirs('static/plots')


@app.route('/')
def index():
    """Página principal con formulario para ingresar ecuación diferencial."""
    return render_template('index.html', title='Solver EDO - Métodos de Euler y Heun')


@app.route('/solve_euler', methods=['POST'])
def solve_euler():
    """Resolver ecuación diferencial usando método de Euler."""
    try:
        # Obtener datos del formulario
        data = request.get_json() if request.is_json else request.form

        function_str = data['function']
        x0 = float(data['x0'])
        y0 = float(data['y0'])
        xn = float(data['xn'])

        # Determinar si es por número de pasos o tamaño de paso
        if 'num_steps' in data and data['num_steps']:
            num_steps = int(data['num_steps'])
            h = (xn - x0) / num_steps
        else:
            h = float(data['step_size'])
            num_steps = int((xn - x0) / h)

        # Validar función
        if not validate_function(function_str):
            return jsonify({'error': 'Función inválida. Use sintaxis Python válida.'}), 400

        # Resolver usando método de Euler
        euler = EulerMethod(function_str, x0, y0, h, num_steps)
        results = euler.solve()

        # Generar gráfica
        plot_filename = f"euler_plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plot_path = create_ode_plot(results, "Método de Euler", plot_filename)

        # Guardar en historial
        save_to_history({
            'method': 'Euler',
            'function': function_str,
            'x0': x0, 'y0': y0, 'xn': xn,
            'h': h, 'steps': num_steps,
            'timestamp': datetime.now().isoformat(),
            'plot': plot_filename
        })

        return render_template('results.html',
                               results=results,
                               method_name="Método de Euler",
                               plot_url=f"static/plots/{plot_filename}",
                               function=function_str,
                               parameters={'x0': x0, 'y0': y0, 'xn': xn, 'h': h})

    except Exception as e:
        return jsonify({'error': f'Error en el cálculo: {str(e)}'}), 500


@app.route('/solve_heun', methods=['POST'])
def solve_heun():
    """Resolver ecuación diferencial usando método de Heun."""
    try:
        # Obtener datos del formulario
        data = request.get_json() if request.is_json else request.form

        function_str = data['function']
        x0 = float(data['x0'])
        y0 = float(data['y0'])
        xn = float(data['xn'])

        # Determinar si es por número de pasos o tamaño de paso
        if 'num_steps' in data and data['num_steps']:
            num_steps = int(data['num_steps'])
            h = (xn - x0) / num_steps
        else:
            h = float(data['step_size'])
            num_steps = int((xn - x0) / h)

        # Validar función
        if not validate_function(function_str):
            return jsonify({'error': 'Función inválida. Use sintaxis Python válida.'}), 400

        # Resolver usando método de Heun
        heun = HeunMethod(function_str, x0, y0, h, num_steps)
        results = heun.solve()

        # Generar gráfica
        plot_filename = f"heun_plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plot_path = create_ode_plot(results, "Método de Heun", plot_filename)

        # Guardar en historial
        save_to_history({
            'method': 'Heun',
            'function': function_str,
            'x0': x0, 'y0': y0, 'xn': xn,
            'h': h, 'steps': num_steps,
            'timestamp': datetime.now().isoformat(),
            'plot': plot_filename
        })

        return render_template('results.html',
                               results=results,
                               method_name="Método de Heun",
                               plot_url=f"static/plots/{plot_filename}",
                               function=function_str,
                               parameters={'x0': x0, 'y0': y0, 'xn': xn, 'h': h})

    except Exception as e:
        return jsonify({'error': f'Error en el cálculo: {str(e)}'}), 500

@app.route('/solve_runge_kutta', methods=['POST'])
def solve_runge_kutta():
    """Resolver ecuación diferencial usando método de Runge-Kutta."""
    try:
        # Obtener datos del formulario
        data = request.get_json() if request.is_json else request.form

        function_str = data['function']
        x0 = float(data['x0'])
        y0 = float(data['y0'])
        xn = float(data['xn'])

        # Determinar si es por número de pasos o tamaño de paso
        if 'num_steps' in data and data['num_steps']:
            num_steps = int(data['num_steps'])
            h = (xn - x0) / num_steps
        else:
            h = float(data['step_size'])
            num_steps = int((xn - x0) / h)

        # Validar función
        if not validate_function(function_str):
            return jsonify({'error': 'Función inválida. Use sintaxis Python válida.'}), 400

        # Resolver usando método de Runge-Kutta
        rk = RungeKuttaMethod(function_str, x0, y0, h, num_steps)
        results = rk.solve()

        # Generar gráfica
        plot_filename = f"runge_kutta_plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plot_path = create_ode_plot(results, "Método de Runge-Kutta", plot_filename)

        # Guardar en historial
        save_to_history({
            'method': 'Runge-Kutta',
            'function': function_str,
            'x0': x0, 'y0': y0, 'xn': xn,
            'h': h, 'steps': num_steps,
            'timestamp': datetime.now().isoformat(),
            'plot': plot_filename
        })

        return render_template('results.html',
                               results=results,
                               method_name="Método de Runge-Kutta",
                               plot_url=f"static/plots/{plot_filename}",
                               function=function_str,
                               parameters={'x0': x0, 'y0': y0, 'xn': xn, 'h': h})

    except Exception as e:
        return jsonify({'error': f'Error en el cálculo: {str(e)}'}), 500


@app.route('/history')
def history():
    """Mostrar historial de cálculos."""
    try:
        with open('history.json', 'r') as f:
            history_data = json.load(f)
        return render_template('history.html', history=history_data)
    except FileNotFoundError:
        return render_template('history.html', history=[])


@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Limpiar historial de cálculos."""
    try:
        with open('history.json', 'w') as f:
            json.dump([], f)
        return redirect(url_for('history'))
    except Exception as e:
        return jsonify({'error': f'Error al limpiar historial: {str(e)}'}), 500


def save_to_history(calculation_data):
    """Guardar cálculo en historial."""
    try:
        # Cargar historial existente
        try:
            with open('history.json', 'r') as f:
                history = json.load(f)
        except FileNotFoundError:
            history = []

        # Agregar nuevo cálculo
        history.append(calculation_data)

        # Mantener solo los últimos 50 cálculos
        if len(history) > 50:
            history = history[-50:]

        # Guardar historial actualizado
        with open('history.json', 'w') as f:
            json.dump(history, f, indent=2)

    except Exception as e:
        print(f"Error guardando en historial: {e}")


if __name__ == '__main__':
    app.run(debug=True)