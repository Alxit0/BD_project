from flask import Flask, Blueprint
from routes import user_routes, product_routes, unique_routes, questions_routes

app = Flask(__name__)

app_routes = Blueprint("app_routes", __name__)

app_routes.register_blueprint(unique_routes)
app_routes.register_blueprint(user_routes, url_prefix="/user")
app_routes.register_blueprint(product_routes, url_prefix="/product")
app_routes.register_blueprint(questions_routes, url_prefix="/questions")


app.register_blueprint(app_routes, url_prefix="/dbproject")


if __name__ == '__main__':
	host = '127.0.0.1'
	port = 8080
	app.run(host=host, port=port, debug=True)