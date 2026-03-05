"""
Configuración centralizada usando variables de entorno.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración base"""
    PROJECT_NAME = "API Comunitaria Dolores Hidalgo"
    API_VERSION = "v1"
    FLASK_CONFIG = os.getenv('FLASK_CONFIG', 'dev')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-do-not-use-in-production')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/api.log')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://admin:desarrollo123@localhost:5432/api_comunitaria'
    )


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'CHANGE_IN_PRODUCTION')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', '')


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'test': TestingConfig
}

active_config = config_by_name.get(
    os.getenv('FLASK_CONFIG', 'dev'),
    DevelopmentConfig
)
