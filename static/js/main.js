/**
 * main.js - JavaScript principal para la aplicación ODE Solver
 * Funcionalidades: validación de formularios, manejo de eventos,
 * comunicación con servidor, animaciones y utilidades
 */

// ===== CONFIGURACIÓN GLOBAL =====
const Config = {
    endpoints: {
        euler: '/solve_euler',
        heun: '/solve_heun',
        history: '/history'
    },
    validation: {
        maxSteps: 1000,
        minSteps: 1,
        maxStepSize: 10.0,
        minStepSize: 0.0001,
        maxInterval: 100,
        minInterval: 0.01
    },
    animation: {
        duration: 300,
        easing: 'ease-in-out'
    }
};

// ===== CLASE PRINCIPAL DE LA APLICACIÓN =====
class ODESolverApp {
    constructor() {
        this.form = null;
        this.isLoading = false;
        this.init();
    }

    /**
     * Inicializar la aplicación
     */
    init() {
        this.bindEvents();
        this.initializeForm();
        this.loadURLParameters();
        this.setupMathJax();
        console.log('ODE Solver App initialized');
    }

    /**
     * Vincular eventos globales
     */
    bindEvents() {
        // Eventos del DOM
        document.addEventListener('DOMContentLoaded', () => {
            this.onDOMContentLoaded();
        });

        // Eventos de formulario
        this.setupFormEvents();

        // Eventos de teclado
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });

        // Eventos de ventana
        window.addEventListener('beforeunload', (e) => {
            if (this.isLoading) {
                e.preventDefault();
                e.returnValue = 'Hay un cálculo en progreso. ¿Estás seguro de que quieres salir?';
            }
        });
    }

    /**
     * Configurar eventos del formulario
     */
    setupFormEvents() {
        // Radio buttons para método de paso
        const stepMethodRadios = document.querySelectorAll('input[name="step_method"]');
        stepMethodRadios.forEach(radio => {
            radio.addEventListener('change', () => {
                this.toggleStepMethod(radio.value);
            });
        });

        // Validación en tiempo real
        const inputs = document.querySelectorAll('input[type="number"], input[type="text"]');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                this.validateField(input);
            });
            input.addEventListener('blur', () => {
                this.validateField(input);
            });
        });

        // Función matemática
        const functionInput = document.getElementById('function');
        if (functionInput) {
            functionInput.addEventListener('input', () => {
                this.validateFunction(functionInput.value);
            });
        }
    }

    /**
     * Configurar MathJax
     */
    setupMathJax() {
        if (window.MathJax) {
            MathJax.typesetPromise().catch((err) => {
                console.error('Error rendering math:', err);
            });
        }
    }

    /**
     * Acciones cuando el DOM está listo
     */
    onDOMContentLoaded() {
        // Animaciones de entrada
        this.animatePageLoad();

        // Inicializar tooltips y popovers
        this.initializeBootstrapComponents();

        // Configurar autocompletado
        this.setupAutoComplete();
    }

    /**
     * Inicializar formulario principal
     */
    initializeForm() {
        this.form = document.getElementById('odeForm');
        if (this.form) {
            this.form.noValidate = true;

            // Configurar valores por defecto
            this.setDefaultValues();
        }
    }

    /**
     * Establecer valores por defecto del formulario
     */
    setDefaultValues() {
        const defaults = {
            'function': 'x + y',
            'x0': '0',
            'y0': '1',
            'xn': '2',
            'num_steps': '10'
        };

        Object.keys(defaults).forEach(key => {
            const element = document.getElementById(key);
            if (element && !element.value) {
                element.value = defaults[key];
            }
        });
    }

    /**
     * Cargar parámetros de URL
     */
    loadURLParameters() {
        const urlParams = new URLSearchParams(window.location.search);

        if (urlParams.has('function')) {
            const params = {
                'function': urlParams.get('function'),
                'x0': urlParams.get('x0'),
                'y0': urlParams.get('y0'),
                'xn': urlParams.get('xn'),
                'num_steps': urlParams.get('num_steps')
            };

            Object.keys(params).forEach(key => {
                const element = document.getElementById(key);
                if (element && params[key]) {
                    element.value = params[key];
                }
            });

            // Limpiar URL
            window.history.replaceState({}, document.title, window.location.pathname);
        }
    }

    /**
     * Cambiar entre métodos de configuración de paso
     */
    toggleStepMethod(method) {
        const stepsInput = document.getElementById('steps_input');
        const sizeInput = document.getElementById('size_input');

        if (method === 'steps') {
            stepsInput.style.display = 'block';
            sizeInput.style.display = 'none';
            this.animateElement(stepsInput, 'fadeIn');
        } else {
            stepsInput.style.display = 'none';
            sizeInput.style.display = 'block';
            this.animateElement(sizeInput, 'fadeIn');
        }
    }

    /**
     * Validar campo individual
     */
    validateField(field) {
        const value = field.value.trim();
        const fieldName = field.name || field.id;
        let isValid = true;
        let message = '';

        // Validaciones específicas por campo
        switch (fieldName) {
            case 'function':
                isValid = this.validateFunction(value);
                message = isValid ? '' : 'Función matemática inválida';
                break;

            case 'x0':
            case 'y0':
            case 'xn':
                isValid = !isNaN(value) && value !== '';
                message = isValid ? '' : 'Debe ser un número válido';
                break;

            case 'num_steps':
                const steps = parseInt(value);
                isValid = !isNaN(steps) && steps >= Config.validation.minSteps && steps <= Config.validation.maxSteps;
                message = isValid ? '' : `Debe estar entre ${Config.validation.minSteps} y ${Config.validation.maxSteps}`;
                break;

            case 'step_size':
                const size = parseFloat(value);
                isValid = !isNaN(size) && size >= Config.validation.minStepSize && size <= Config.validation.maxStepSize;
                message = isValid ? '' : `Debe estar entre ${Config.validation.minStepSize} y ${Config.validation.maxStepSize}`;
                break;
        }

        // Aplicar estilos de validación
        this.setFieldValidation(field, isValid, message);
        return isValid;
    }

    /**
     * Validar función matemática
     */
    validateFunction(functionStr) {
        if (!functionStr.trim()) return false;

        // Verificar caracteres permitidos
        const allowedPattern = /^[x y \+\-\*/\(\)\.\d\s\w]*$/;
        if (!allowedPattern.test(functionStr)) return false;

        // Verificar balanceo de paréntesis
        const openParens = (functionStr.match(/\(/g) || []).length;
        const closeParens = (functionStr.match(/\)/g) || []).length;
        if (openParens !== closeParens) return false;

        return true;
    }

    /**
     * Establecer estado de validación del campo
     */
    setFieldValidation(field, isValid, message) {
        field.classList.remove('is-valid', 'is-invalid');

        if (isValid) {
            field.classList.add('is-valid');
        } else {
            field.classList.add('is-invalid');
        }

        // Mostrar mensaje de error
        const feedback = field.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.textContent = message;
        }
    }

    /**
     * Validar formulario completo
     */
    validateForm() {
        if (!this.form) return false;

        const requiredFields = this.form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        // Validación adicional de intervalo
        const x0 = parseFloat(document.getElementById('x0').value);
        const xn = parseFloat(document.getElementById('xn').value);

        if (xn <= x0) {
            this.showAlert('El valor final debe ser mayor que el inicial', 'danger');
            isValid = false;
        }

        return isValid;
    }

    /**
     * Resolver EDO con método específico
     */
    async solveODE(method) {
        if (!this.validateForm()) {
            this.form.classList.add('was-validated');
            return;
        }

        this.setLoading(true);

        try {
            const formData = this.getFormData();
            const endpoint = Config.endpoints[method];

            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Error del servidor');
            }

            // Reemplazar contenido de la página con los resultados
            const html = await response.text();
            document.documentElement.innerHTML = html;

            // Reinicializar MathJax en la nueva página
            this.setupMathJax();

        } catch (error) {
            console.error('Error solving ODE:', error);
            this.showAlert(`Error al resolver la ecuación: ${error.message}`, 'danger');
        } finally {
            this.setLoading(false);
        }
    }

    /**
     * Obtener datos del formulario
     */
    getFormData() {
        const formData = new FormData();

        formData.append('function', document.getElementById('function').value);
        formData.append('x0', document.getElementById('x0').value);
        formData.append('y0', document.getElementById('y0').value);
        formData.append('xn', document.getElementById('xn').value);

        const stepMethod = document.querySelector('input[name="step_method"]:checked').value;
        if (stepMethod === 'steps') {
            formData.append('num_steps', document.getElementById('num_steps').value);
        } else {
            formData.append('step_size', document.getElementById('step_size').value);
        }

        return formData;
    }

    /**
     * Establecer estado de carga
     */
    setLoading(loading) {
        this.isLoading = loading;
        const spinner = document.getElementById('loadingSpinner');
        const buttons = document.querySelectorAll('#btnEuler, #btnHeun, #btnCompare');

        if (loading) {
            spinner?.classList.remove('d-none');
            buttons.forEach(btn => {
                btn.disabled = true;
                btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Calculando...';
            });
        } else {
            spinner?.classList.add('d-none');
            buttons.forEach(btn => {
                btn.disabled = false;
            });

            // Restaurar textos originales
            const eulerBtn = document.getElementById('btnEuler');
            const heunBtn = document.getElementById('btnHeun');
            const compareBtn = document.getElementById('btnCompare');

            if (eulerBtn) eulerBtn.innerHTML = '<i class="fas fa-arrow-right me-2"></i>Resolver con <strong>Euler</strong>';
            if (heunBtn) heunBtn.innerHTML = '<i class="fas fa-arrows-alt-h me-2"></i>Resolver con <strong>Heun</strong>';
            if (compareBtn) compareBtn.innerHTML = '<i class="fas fa-balance-scale me-2"></i>Comparar Ambos Métodos';
        }
    }

    /**
     * Mostrar alerta
     */
    showAlert(message, type = 'info') {
        const alertContainer = document.createElement('div');
        alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
        alertContainer.innerHTML = `
            <i class="fas fa-${type === 'danger' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insertar antes del contenido principal
        const main = document.querySelector('main');
        if (main && main.firstChild) {
            main.insertBefore(alertContainer, main.firstChild);
        }

        // Auto-eliminar después de 5 segundos
        setTimeout(() => {
            if (alertContainer.parentNode) {
                alertContainer.remove();
            }
        }, 5000);
    }

    /**
     * Cargar ejemplo predefinido
     */
    loadExample(type) {
        const examples = {
            'simple': {
                function: 'y',
                x0: 0,
                y0: 1,
                xn: 2,
                num_steps: 10,
                description: 'Crecimiento exponencial simple'
            },
            'linear': {
                function: 'x + y',
                x0: 0,
                y0: 1,
                xn: 1,
                num_steps: 10,
                description: 'Ecuación diferencial lineal'
            },
            'nonlinear': {
                function: 'x**2 - y**2',
                x0: 0,
                y0: 0,
                xn: 2,
                num_steps: 20,
                description: 'Comportamiento no lineal'
            }
        };

        const example = examples[type];
        if (!example) return;

        // Cargar valores
        document.getElementById('function').value = example.function;
        document.getElementById('x0').value = example.x0;
        document.getElementById('y0').value = example.y0;
        document.getElementById('xn').value = example.xn;
        document.getElementById('num_steps').value = example.num_steps;

        // Configurar método de pasos
        document.getElementById('by_steps').checked = true;
        this.toggleStepMethod('steps');

        // Validar campos
        const inputs = [
            document.getElementById('function'),
            document.getElementById('x0'),
            document.getElementById('y0'),
            document.getElementById('xn'),
            document.getElementById('num_steps')
        ];

        inputs.forEach(input => this.validateField(input));

        // Mostrar notificación
        this.showAlert(`Ejemplo cargado: ${example.description}`, 'success');

        // Animar campos
        inputs.forEach((input, index) => {
            setTimeout(() => {
                this.animateElement(input, 'pulse');
            }, index * 100);
        });
    }

    /**
     * Animar elemento
     */
    animateElement(element, animation) {
        element.classList.add(`animate-${animation}`);
        setTimeout(() => {
            element.classList.remove(`animate-${animation}`);
        }, Config.animation.duration);
    }

    /**
     * Animar carga de página
     */
    animatePageLoad() {
        const cards = document.querySelectorAll('.card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('animate-fade-in');
            }, index * 100);
        });
    }

    /**
     * Inicializar componentes de Bootstrap
     */
    initializeBootstrapComponents() {
        // Inicializar tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        // Inicializar popovers
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }

    /**
     * Configurar autocompletado de funciones
     */
    setupAutoComplete() {
        const functionInput = document.getElementById('function');
        if (!functionInput) return;

        const suggestions = [
            'x + y', 'x - y', 'x * y', 'x / y',
            'sin(x)', 'cos(x)', 'tan(x)',
            'exp(x)', 'log(x)', 'sqrt(x)',
            'x**2', 'y**2', 'x**2 + y**2',
            'x*sin(y)', 'cos(x)*sin(y)',
            'x**2 - y**2', 'x*y - 2*x'
        ];

        // Implementar autocompletado simple
        functionInput.addEventListener('input', (e) => {
            const value = e.target.value.toLowerCase();
            if (value.length < 2) return;

            const matches = suggestions.filter(s =>
                s.toLowerCase().includes(value)
            );

            // Aquí se podría mostrar una lista desplegable de sugerencias
            console.log('Suggestions:', matches);
        });
    }

    /**
     * Manejar atajos de teclado
     */
    handleKeyboardShortcuts(e) {
        if (e.ctrlKey || e.metaKey) {
            switch (e.key) {
                case 'Enter':
                    e.preventDefault();
                    document.getElementById('btnEuler')?.click();
                    break;
                case '1':
                    e.preventDefault();
                    this.loadExample('simple');
                    break;
                case '2':
                    e.preventDefault();
                    this.loadExample('linear');
                    break;
                case '3':
                    e.preventDefault();
                    this.loadExample('nonlinear');
                    break;
            }
        }
    }
}

// ===== FUNCIONES GLOBALES =====

/**
 * Resolver EDO con método de Euler
 */
window.solveODE = function(method) {
    app.solveODE(method);
};

/**
 * Cargar ejemplo predefinido
 */
window.loadExample = function(type) {
    app.loadExample(type);
};

/**
 * Modal de comparación de métodos (placeholder)
 */
window.compareMethodsModal = function() {
    app.showAlert('La funcionalidad de comparación estará disponible próximamente', 'info');
};

// ===== INICIALIZACIÓN =====
let app;

document.addEventListener('DOMContentLoaded', function() {
    app = new ODESolverApp();
});

// ===== EXPORTAR PARA PRUEBAS =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ODESolverApp, Config };
}