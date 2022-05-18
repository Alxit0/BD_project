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

	total = 0
	num = 0
	valores_nao_reconhecidos = []
	for i in payload["cart"]:
		try:
			product_id, quantity = i
		except TypeError:
			con.rollback()
			con.close()
			return wrong_cart_config_response
		temp = get_cur_preco(product_id, cur)

		if temp is None:
			valores_nao_reconhecidos.append(product_id)
			continue
		
		# print(product_id, temp, quantity)
		total += temp * quantity
		num += 1

	if len(valores_nao_reconhecidos) == len(payload["cart"]):
		print(valores_nao_reconhecidos, num)
		con.rollback()
		con.close()
		return make_response(
			"api_error",
			"Nenhum valor reconhecido."
		)

	cur.execute(
		"INSERT INTO orders (total, num_orders) VALUES (%s, %s) RETURNING id;",
		(total, num)
	)
	order_id = cur.fetchone()[0]
	# print(total)
	con.commit()
	con.close()

	if valores_nao_reconhecidos:
		return jsonify({"status": 200, "errors": valores_nao_reconhecidos, "results": order_id})
	
	return make_response(
		"sucess",
		order_id,
		message_title="results"
	)

def get_cur_preco(prod_id, cur):
	cur.execute(
		"SELECT preco FROM equipamentos_versions WHERE id = (SELECT cur_version FROM equipamentos WHERE id = %s)",
		(prod_id,)
	)
	data = cur.fetchone()
	if data is None:
		return
	
	preco = data[0]
	return preco
