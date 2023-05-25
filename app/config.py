from loader import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
import os

root_dir = os.path.dirname(os.path.abspath(__file__))


class MainConfig:
    """
    Конфигурационный класс для настроек создаваемого экземпляра класса Flask в основном режиме
    """
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(MainConfig):
    """
    Конфигурационный класс для настроек создаваемого экземпляра класса Flask в тестовом режиме
    """
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{root_dir}/tests/test.db"
    TESTING = True
