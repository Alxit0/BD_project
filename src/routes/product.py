from flask import Blueprint, request
from psycopg2 import errors

if __name__ == "__main__":
	from utils import *
else:
	from .utils import *


product_routes = Blueprint("product_routes", __name__)
basic_produt_atributes = ["preco", "descricao", "stock", "nome"]
product_atributes = {
	'computadores': [1, ["processador", "placa_vidio", "ram", "storage"]],
	'televisoes': [2, ["tamanho", "resolucao", "refresh_rt"]],
	'smartphones': [3, ["tamanho", "ram", "storage", "camera", "processador"]]
}


@product_routes.before_request
def verify_token():
	return verify_header(request.headers)

@product_routes.route("/", methods=["POST"])
def create_product():
	# verify credentials
	if not check_if_creds(request.headers['Authorization'].split()[1], 2):
		return make_response(
			"sucess",
			"Wrong credentials. Must be vendedor."
		)
	
	payload = request.get_json()

	return create_product_helper(payload, get_id_from_token(request.headers['Authorization'].split()[1]))

@product_routes.route("/<prod_id>", methods=["PUT"])
def update_product(prod_id):
	"""
	Tens de adicionar um novo produto no final
	UPDATE informacao na tabela de equipamentos retornando o id e o tipo

	Ir a tabela desse tipo e UPADTE a informacao especifica
	"""
	# verify credentials
	if not check_if_creds(request.headers['Authorization'].split()[1], 2):
		return make_response(
			"sucess",
			"Wrong credentials. Must be vendedor."
		)
	
	d, vendedor_id, tipo, code = fetch_info_product(prod_id)

	payload = request.get_json()
	for i in payload:
		if i in d:
			d[i] = payload[i]

	create_product_helper({**d, "type": tipo}, vendedor_id, prod_code=code)
	return jsonify({"status": 200})


def create_product_helper(payload:dict, vendedor_id, *, prod_code=None):
	# check if has 'type'
	if 'type' not in payload:
		return make_response(
			"api_error",
			"Tipo ('type') de utilizador nao especificado (computadores | televisoes | smartphones)",
			message_title="error"
		)
	
	# check if has all the needed atributes
	checker = check_atributes(payload, *basic_produt_atributes + product_atributes[payload['type']][1])
	if checker != []:
		return make_response("api_error", "Missing atributs: " + ', '.join(checker))
	
	con = db_connection()
	cur = con.cursor()
	num_tipo, atrs_tipo = product_atributes[payload['type']]
	try:
		cur.execute(
			"INSERT INTO equipamentos (" +
			', '.join(basic_produt_atributes+["vendedor_utilizador_id", "tipo"]) +
			") VALUES (%s, %s" + ", %s"*len(basic_produt_atributes) + ") RETURNING id;",
			tuple(map(payload.__getitem__, basic_produt_atributes)) + (vendedor_id, num_tipo)
		)
	except errors.UniqueViolation:
		con.rollback()
		con.close()
		return make_response("internal_error", "Equipamento already exists", message_title="error")

	prod_id = cur.fetchone()[0]

	if prod_code is None:
		prod_code = prod_id

	cur.execute(
		"UPDATE equipamentos SET prod_code=%s WHERE id=%s;", 
		(prod_code, prod_id)
	)
	cur.execute(
		
		f"INSERT INTO {payload['type']} (" +
		', '.join(atrs_tipo+["equipamentos_id"]) +
		") VALUES (%s" + ", %s"*len(atrs_tipo) + ");",
		tuple(map(payload.__getitem__, atrs_tipo)) + (prod_id, )
	)

	con.commit()
	con.close()

	return make_response(
		"sucess",
		prod_id,
		message_title="results"
	)

def fetch_info_product(prod_id):
	con = db_connection()
	cur = con.cursor()

	cur.execute(
		"SELECT " + ', '.join(basic_produt_atributes+["tipo", "vendedor_utilizador_id", "prod_code"]) + 
		" FROM equipamentos WHERE id=%s;",
		prod_id
	)
	# print(cur.fetchone())
	*temp_atrs, tipo_num, vendedor_id, prod_code = cur.fetchone()
	d = {}
	for i, j in zip(basic_produt_atributes, temp_atrs):
		d[i] = j
	
	tipo_str = list(product_atributes.keys())[tipo_num - 1]
	print(tipo_str)

	cur.execute(
		"SELECT " + ', '.join(product_atributes[tipo_str][1]) +
		f" FROM {tipo_str}" + " WHERE equipamentos_id=%s;",
		prod_id
	)
	for i, j in zip(product_atributes[tipo_str][1], cur.fetchone()):
		d[i] = j

	con.commit()
	con.close()

	return d, vendedor_id, tipo_str, prod_code