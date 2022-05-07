from flask import Flask
from routes import all_routes

app = Flask(__name__)
app.register_blueprint(all_routes, url_prefix="/dbproject")


status_code = {
	'sucess': 200,
	'api_error': 400,
	'internal_error': 500
}


if __name__ == "__main__":
	host = '127.0.0.1'
	port = 8080
	app.run(host=host, port=port, debug=True)
