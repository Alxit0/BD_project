from flask import Blueprint

from .misclans import misclans_routes
from .product import product_routes
from .questions import questions_routes
from .report import reports_routes
from .user import user_routes

all_routes = Blueprint("all_routes", __name__)

all_routes.register_blueprint(misclans_routes)
all_routes.register_blueprint(product_routes, url_prefix="/product")
all_routes.register_blueprint(questions_routes, url_prefix="/questions")
all_routes.register_blueprint(reports_routes, url_prefix="/report")
all_routes.register_blueprint(user_routes, url_prefix="/user")
