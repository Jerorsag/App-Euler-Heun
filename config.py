import os
from datetime import timedelta


class Config:
    """Configuración de la aplicación Flask."""

    # Configuración básica de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-super-segura-para-desarrollo'

    # Configuración de sesiones
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = './flask_session'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_FILE_THRESHOLD = 100
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    # Configuración de archivos
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo

    # Configuración de plots
    PLOT_DPI = 150
    PLOT_FIGSIZE = (10, 6)
    PLOT_STYLE = 'seaborn-v0_8'  # Estilo de matplotlib

    # Configuración de métodos numéricos
    MAX_STEPS = 10000  # Máximo número de pasos permitidos
    MIN_STEP_SIZE = 1e-8  # Tamaño mínimo de paso
    MAX_STEP_SIZE = 10.0  # Tamaño máximo de paso

    # Configuración de funciones permitidas (seguridad)
    ALLOWED_FUNCTIONS = [
        'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan',
        'sinh', 'cosh', 'tanh', 'exp', 'log', 'log10', 'log2',
        'sqrt', 'abs', 'pow', 'pi', 'e'
    ]

    # Configuración de desarrollo
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

    @staticmethod
    def init_app(app):
        """Inicializar configuración específica de la aplicación."""
        pass


class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True


class TestingConfig(Config):
    """Configuración para testing."""
    TESTING = True
    WTF_CSRF_ENABLED = False


# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}