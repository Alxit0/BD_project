from flask import Blueprint, request
from psycopg2 import errors

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
	quantidade_insuficiente = []
	for i in payload["cart"]:
		try:
			product_id, quantity = i
		except TypeError:
			con.rollback()
			con.close()
			return wrong_cart_config_response
		temp = get_cur_preco(product_id, cur)

		try:
			cur.execute(
				"BEGIN TRANSACTION;UPDATE equipamentos SET stock = stock - %s WHERE id = %s;",
				(quantity, product_id)
			)
		except errors.CheckViolation:
			cur.execute("ROLLBACK;")
			quantidade_insuficiente.append(product_id)
			continue
		
		cur.execute("COMMIT;")
		if temp is None:
			valores_nao_reconhecidos.append(product_id)
			continue
	
		# print(product_id, temp, quantity)
		total += temp * quantity
		num += 1

	if len(valores_nao_reconhecidos) == len(payload["cart"]):
		# print(valores_nao_reconhecidos, num)
		con.rollback()
		con.close()
		return make_response(
			"api_error",
			"Nenhum valor reconhecido."
		)
	if len(quantidade_insuficiente) == len(payload['cart']):
		con.rollback()
		con.close()
		return make_response(
			"api_error",
			"Nenhuma quantidade suficiente."
		)

	cur.execute(
		"INSERT INTO orders (total, num_orders, _date) VALUES (%s, %s, %s) RETURNING id;",
		(total, num, get_cur_month())
	)
	order_id = cur.fetchone()[0]
	# print(total)
	con.commit()
	con.close()

	temp_erros = {"errors": {}}
	if valores_nao_reconhecidos:
		temp_erros["errors"]['Produto nao existe'] = valores_nao_reconhecidos
		# return jsonify({"status": 200, "errors": valores_nao_reconhecidos, "results": order_id})
	if quantidade_insuficiente:
		temp_erros["errors"]["Quantidades insuficientes"] = quantidade_insuficiente

	if temp_erros['errors']:
		return jsonify({**temp_erros, "status": 200, "results": order_id})
	
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

@unique_routes.route('/rating/<product_id>', methods=["POST"])
def give_rating(product_id):
	# verify credentials
	if not check_if_creds(request.headers['Authorization'].split()[1], 1):
		return make_response(
			"sucess",
			"Wrong credentials. Must be comprador."
		)
	
	payload = request.get_json()

	checker = check_atributes(payload, "valor", "comment")
	if checker != []:
		return make_response("api_error", "Missing atributs: " + ', '.join(checker))
	
	valor = payload['valor']
	comment = payload["comment"]

	if valor < 0 or valor > 5:
		return make_response(
			"api_error",
			"valor must be between 0 and 5 including"
		)
	if not (0 < len(comment) < 151):
		return make_response(
			"api_error",
			"comment must contain 150 chars at max"
		)
	
	con = db_connection()
	cur = con.cursor()

	comprador_id = get_id_from_token(request.headers['Authorization'].split()[1])

	try:
		cur.execute(
			"INSERT INTO ratings (equipamento_id, comprador_id, valor, comment) VALUES (%s, %s, %s, %s);",
			(product_id, comprador_id, valor, comment)
		)
	except errors.ForeignKeyViolation:
		con.rollback()
		con.close()
		return make_response(
			"internal_error",
			"Product doesnt exist."
		)
	except errors.UniqueViolation:
		con.rollback()
		con.close()
		return make_response(
			"internal_error",
			"You already gave a rating to dis product."
		)
	
	con.commit()
	con.close()
	return jsonify({"status": 200})