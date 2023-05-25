from flask import Blueprint

routes = Blueprint(name='routes', import_name=__name__)

from .record import *
from .user import *
