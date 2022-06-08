from flask import Blueprint, request
from psycopg2 import errors

if __name__ == "__main__":
	from utils import *
else:
	from .utils import *

unique_routes = Blueprint("unique_routes", __name__)
campanha_atrs = ["descricao", "date_start", "date_end", "coupons", "discount", "validade_cupao_dias"]

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
	
	desconto = 1.0
	if "coupon" in payload:
		cur.execute(
			"SELECT discount FROM cupoes WHERE id = %s;",
			(payload["coupon"],)
		)

	temp = cur.fetchone()
	if cur.fetchone() is None:
		return make_response(
			"api_error",
			"No coupond found. Plese use another or eliminate the field 'coupon'."
		)

	desconto = temp[0]/100

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
		"DELETE FROM cupoes WHERE id = %s AND comprador_id = %s;",
		(payload["coupon"], get_id_from_token(request.headers['Authorization'].split()[1]))
	)

	cur.execute(
		"INSERT INTO orders (total, num_orders, _date, comprador_id) VALUES (%s, %s, %s, %s) RETURNING id;",
		(total*desconto, num, get_cur_month(), get_id_from_token(request.headers['Authorization'].split()[1]))
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

@unique_routes.route('/campaign', methods=["POST"])
def create_campaign():
	if not check_if_creds(request.headers['Authorization'].split()[1], 3):
		return make_response(
			"api_error",
			"Not enough privileges. Please log in with and admin acount."
		)
	
	payload: dict = request.get_json()

	checker = check_atributes(payload, *campanha_atrs)
	if checker != []:
		return make_response("api_error", "Missing atributs: " + ', '.join(checker))
	
	if to_date(payload["date_start"]) > to_date(payload["date_end"]):
			return make_response(
				"internal_error",
				"Start date < End date"
			)
	con = db_connection()
	cur = con.cursor()

	start, end = payload["date_start"], payload["date_end"]
	cur.execute(
		"SELECT id FROM campanha WHERE\
		(%s <= date_end AND %s >= date_start);",
		(start, end)
	)
	if len(cur.fetchall())!= 0:
		return make_response(
			"api_error",
			"Campanha subreposta com outra"
		)

	cur.execute(
		f"INSERT INTO campanha ({', '.join(campanha_atrs + ['cupoes_generated'])}) VALUES (" + 
		"%s, "*(len(campanha_atrs)) + "%s) RETURNING id;",
		tuple(map(payload.__getitem__, campanha_atrs)) + (payload['coupons'],)
	)
	########################
	camp_id = cur.fetchone()[0]
	
	con.commit()
	con.close()
	return make_response(
		"sucess",
		camp_id,
		message_title="results"
	)

@unique_routes.route('/subscribe/<campaign_id>', methods=["PUT"])
def subscribe_acmp(campaign_id):
	if not check_if_creds(request.headers['Authorization'].split()[1], 1):
		return make_response(
			"api_error",
			"Not enough privileges. Please log in with and admin acount."
		)
	con = db_connection()
	cur = con.cursor()

	try:
		cur.execute(
			"UPDATE campanha SET coupons = coupons - 1 WHERE id = %s RETURNING date_start, date_end, coupons, discount;",
			(campaign_id, )
		)
		start, end, coupons, discount = cur.fetchone()
		
		if not (start < date.today() <= end):
			con.rollback()
			con.close()
			return make_response(
				"sucess",
				f"Campaign fora do prazo: {start} ate {end}."
			)
		
		if coupons < 0:
			con.rollback()
			con.close()
			return make_response(
				"sucess",
				"Campaign ended due to all coupons selled."
			)
		
		cur.execute(
			"INSERT INTO cupoes (campanha_id, comprador_id, discount) VALUES (%s, %s, %s) RETURNING id;",
			(campaign_id, get_id_from_token(request.headers['Authorization'].split()[1]), discount)
		)

		cupon_id = cur.fetchone()[0]
		
		con.commit()
		con.close()
		
		return make_response(
			"sucess",
			{"campaign_id": cupon_id, "expiration_date": get_expire_date(get_cur_date(), 1)}
		)

	except errors.UniqueViolation:
		con.rollback()
		con.close()
		return make_response(
			"sucess",
			"You have already subscribed in this campign."
		)