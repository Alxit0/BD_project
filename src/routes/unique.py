from flask import Blueprint, request

if __name__ == "__main__":
	from utils import *
else:
	from .utils import *

unique_routes = Blueprint("unique_routes", __name__)

@unique_routes.before_request
def verify_token():
	return verify_header(request.headers)

@unique_routes.route('/order', methods=["POST"])
def make_order():
	# verify credentials
	if not check_if_creds(request.headers['Authorization'].split()[1], 1):
		return make_response(
			"sucess",
			"Wrong credentials. Must be comprador."
		)
	
	payload = request.get_json()
	wrong_cart_config_response = make_response(
			"internal_error", 
			"Wrong type (car): “cart”: [[product_id_1, quantity], [product_id_2, quantity], ...]"
		)
		
	if "cart" not in payload:
		return make_response(
			"api_error",
			"Missing atribute: cart"
		)
	elif type(payload['cart']) != list:
		return wrong_cart_config_response

	con = db_connection()
	cur = con.cursor()

	for i in payload["cart"]:
		try:
			porduct_id, qunatity = i
		except TypeError:
			con.rollback()
			con.close()
			return wrong_cart_config_response
		
		cur.execute("UPDATE ")

	return "Ola"