# 🧮 ODE Solver - Métodos Numéricos para Ecuaciones Diferenciales

Una aplicación web educativa desarrollada en **Flask** para resolver ecuaciones diferenciales ordinarias (EDO) utilizando los métodos numéricos de **Euler** y **Heun**.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Características

### 🎯 Funcionalidades Principales
- ✅ **Método de Euler**: Solución numérica de primer orden
- ✅ **Método de Heun**: Método predictor-corrector de segundo orden
- ✅ **Visualización Gráfica**: Gráficas interactivas de las soluciones
- ✅ **Tabla de Resultados**: Resultados paso a paso detallados
- ✅ **Comparación de Métodos**: Análisis comparativo entre métodos
- ✅ **Historial de Cálculos**: Guarda y revisa cálculos anteriores
- ✅ **Ejemplos Predefinidos**: Casos de estudio listos para usar
- ✅ **Interfaz Intuitiva**: Diseño responsive y fácil de usar

### 🔧 Características Técnicas
- **Framework**: Flask con arquitectura MVC
- **Visualización**: Matplotlib + Seaborn para gráficas profesionales
- **Frontend**: Bootstrap 5 + JavaScript ES6
- **Matemáticas**: NumPy + SymPy para cálculos numéricos
- **Seguridad**: Evaluación segura de funciones matemáticas
- **Responsive**: Compatible con dispositivos móviles

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tuusuario/ode-solver-app.git
cd ode-solver-app
```

### 2. Crear Entorno Virtual (Recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación
```bash
# Modo básico
python run.py

# Modo producción
python run.py --prod

# Puerto personalizado
python run.py --port 8080

# Permitir conexiones externas
python run.py --host 0.0.0.0
```

La aplicación estará disponible en: `http://127.0.0.1:5000`

## 📖 Guía de Uso

### 🔢 Resolviendo una Ecuación Diferencial

1. **Ingresa tu función**: Escribe la función f(x,y) de tu ecuación dy/dx = f(x,y)
   - Ejemplo: `x + y`, `sin(x)*cos(y)`, `x**2 - y**2`

2. **Configura las condiciones iniciales**:
   - `x₀`: Valor inicial de x
   - `y₀`: Valor inicial de y (condición inicial)
   - `xₙ`: Valor final del intervalo

3. **Selecciona el método de paso**:
   - Por **número de pasos**: Define cuántos pasos quieres
   - Por **tamaño de paso**: Define el tamaño h directamente

4. **Elige el método**:
   - **Euler**: Más simple, menor precisión
   - **Heun**: Mayor precisión, ligeramente más costoso

### 📝 Funciones Matemáticas Soportadas

| Categoría | Funciones Disponibles |
|-----------|----------------------|
| **Básicas** | `+`, `-`, `*`, `/`, `**`, `()` |
| **Trigonométricas** | `sin()`, `cos()`, `tan()`, `arcsin()`, `arccos()`, `arctan()` |
| **Exponenciales** | `exp()`, `log()`, `ln()`, `sqrt()` |
| **Constantes** | `pi`, `e` |
| **Variables** | `x`, `y` |

### 💡 Ejemplos Predefinidos

La aplicación incluye tres ejemplos listos para usar:

1. **Crecimiento Simple**: `dy/dx = y`
   - Solución exacta: y = e^x
   - Ideal para comparar precisión

2. **Ecuación Lineal**: `dy/dx = x + y`
   - Problema clásico de EDO lineal
   - Bueno para entender el comportamiento

3. **No Lineal**: `dy/dx = x² - y²`
   - Comportamiento no lineal interesante
   - Muestra limitaciones de métodos simples

## 🏗️ Arquitectura del Proyecto

```
ode_solver_app/
├── 📁 models/              # Métodos numéricos
│   ├── euler.py           # Implementación de Euler
│   ├── heun.py            # Implementación de Heun
│   └── __init__.py
├── 📁 templates/           # Templates HTML
│   ├── base.html          # Template base
│   ├── index.html         # Formulario principal
│   ├── results.html       # Página de resultados
│   └── history.html       # Historial
├── 📁 static/             # Archivos estáticos
│   ├── css/style.css      # Estilos personalizados
│   ├── js/main.js         # JavaScript principal
│   └── plots/             # Gráficas generadas
├── 📁 utils/              # Utilidades
│   ├── parser.py          # Evaluador de funciones
│   ├── plotter.py         # Generador de gráficas
│   └── __init__.py
├── 📄 app.py              # Aplicación Flask principal
├── 📄 config.py           # Configuración
├── 📄 run.py              # Script de ejecución
├── 📄 requirements.txt    # Dependencias
└── 📄 README.md           # Este archivo
```

## 🧪 Métodos Numéricos Implementados

### Método de Euler
- **Orden**: 1
- **Fórmula**: `y_{n+1} = y_n + h × f(x_n, y_n)`
- **Error local**: O(h²)
- **Error global**: O(h)
- **Características**: Simple, rápido, menos preciso

### Método de Heun (Euler Mejorado)
- **Orden**: 2
- **Fórmula**: 
  - Predictor: `y_pred = y_n + h × f(x_n, y_n)`
  - Corrector: `y_{n+1} = y_n + (h/2) × [f(x_n, y_n) + f(x_{n+1}, y_pred)]`
- **Error local**: O(h³)
- **Error global**: O(h²)
- **Características**: Más preciso, predictor-corrector

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Opcional: configurar clave secreta
export SECRET_KEY="tu-clave-secreta-super-segura"

# Configurar modo de ejecución
export FLASK_ENV=development  # o production
```

### Personalización
- **Estilos**: Modifica `static/css/style.css`
- **Comportamiento**: Ajusta `static/js/main.js`
- **Configuración**: Edita `config.py`

## 📊 Capturas de Pantalla

### Interfaz Principal
![Interfaz Principal](docs/images/main-interface.png)

### Resultados y Gráficas
![Resultados](docs/images/results-page.png)

### Historial de Cálculos
![Historial](docs/images/history-page.png)

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### 🐛 Reportar Bugs
Si encuentras algún error, por favor abre un issue con:
- Descripción del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Información del sistema (OS, Python version, etc.)

## 📚 Recursos Educativos

### 📖 Teoría de Métodos Numéricos
- [Método de Euler - Wikipedia](https://es.wikipedia.org/wiki/M%C3%A9todo_de_Euler)
- [Métodos de Runge-Kutta](https://es.wikipedia.org/wiki/M%C3%A9todos_de_Runge-Kutta)
- [Análisis Numérico - Burden & Faires](http://www.amazon.com/Numerical-Analysis-Richard-Burden/dp/1305253663)

### 🎓 Casos de Uso Académico
Esta aplicación es ideal para:
- Cursos de Métodos Numéricos
- Análisis Numérico
- Ecuaciones Diferenciales
- Programación Científica
- Proyectos de ingeniería

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@tuusuario](https://github.com/tuusuario)
- Email: tu.email@ejemplo.com
- LinkedIn: [Tu Perfil](https://linkedin.com/in/tuperfil)

## 🙏 Agradecimientos

- [Flask](https://flask.palletsprojects.com/) - Framework web
- [NumPy](https://numpy.org/) - Computación científica
- [Matplotlib](https://matplotlib.org/) - Visualización de datos
- [Bootstrap](https://getbootstrap.com/) - Framework CSS
- [MathJax](https://www.mathjax.org/) - Renderizado de ecuaciones

---

**⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub!**