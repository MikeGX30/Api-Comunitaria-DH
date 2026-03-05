"""
Extensiones de Flask centralizadas.
Patrón: Inicialización diferida para evitar dependencias circulares.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def configure_extensions(app):
    """
    Configura todas las extensiones de Flask.
    """
    db.init_app(app)
    migrate.init_app(app, db)
    app.logger.info("✅ Extensiones configuradas correctamente")
