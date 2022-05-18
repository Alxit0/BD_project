from unicodedata import name
from flask import Blueprint, request
from psycopg2 import errors

if __name__ == "__main__":
	from utils import *
else:
	from .utils import *


product_routes = Blueprint("product_routes", __name__)
basic_produt_atributes = ["preco", "descricao", "nome"]
types_of_prods = ['computadores', 'televisoes', 'smartphones']
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
	# verify credentials
	if not check_if_creds(request.headers['Authorization'].split()[1], 2):
		return make_response(
			"sucess",
			"Wrong credentials. Must be vendedor."
		)
	
	payload:dict = request.get_json()

	if len(payload) == 0:
		return make_response(
			"sucess",
			"No atributs changed"
		)
	
	con = db_connection()
	cur = con.cursor()

	if 'stock' in payload:
		cur.execute(
			"UPDATE equipamentos SET stock = %s WHERE id=%s;",
			(payload.pop('stock'), prod_id)
		)
		if len(payload) == 0:
			con.commit()
			con.close()
			return jsonify({"status": 200})
	
	d, nome_of_type = fetch_info_product(prod_id, cur)
	# print(d)
	for i in payload:
		d[i] = payload[i]
	# print(d)

	cur.execute(
		"INSERT INTO equipamentos_versions (" +
		', '.join(basic_produt_atributes+["equipamentos_main"]) +
		") VALUES (%s" + ", %s"*len(basic_produt_atributes) + ") RETURNING id;",
		tuple(map(d.__getitem__, basic_produt_atributes+["equipamentos_main"]))
	)

	version_id = cur.fetchone()[0]
	_, atrs_tipo = product_atributes[nome_of_type]
	cur.execute(
		
		f"INSERT INTO {nome_of_type} (" +
		', '.join(atrs_tipo+["equipamentos_versions_id"]) +
		") VALUES (%s" + ", %s"*len(atrs_tipo) + ");",
		tuple(map(d.__getitem__, atrs_tipo)) + (version_id, )
	)

	cur.execute(
			"UPDATE equipamentos SET cur_version = %s WHERE id=%s;",
			(version_id, prod_id)
		)

	con.commit()
	con.close()
	
	return jsonify({"status": 200})


def create_product_helper(payload:dict, vendedor_id):
	# check if has 'type'
	if 'type' not in payload:
		return make_response(
			"api_error",
			"Tipo ('type') de utilizador nao especificado (computadores | televisoes | smartphones)",
			message_title="error"
		)
	
	# check if has all the needed atributes
	checker = check_atributes(payload, *['stock'] + basic_produt_atributes + product_atributes[payload['type']][1])
	if checker != []:
		return make_response("api_error", "Missing atributs: " + ', '.join(checker))
	
	con = db_connection()
	cur = con.cursor()
	num_tipo, atrs_tipo = product_atributes[payload['type']]
	"""try:
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
	)"""

	cur.execute(
		"INSERT INTO equipamentos_versions (" +
		', '.join(basic_produt_atributes) +
		") VALUES (%s" + ", %s"*(len(basic_produt_atributes) - 1) + ") RETURNING id;",
		tuple(map(payload.__getitem__, basic_produt_atributes))
	)

	version_id = cur.fetchone()[0]
	
	cur.execute(
		"INSERT INTO equipamentos (stock, vendedor_utilizador_id, tipo, cur_version) " +
		"VALUES (%s, %s, %s, %s) RETURNING id;",
		(payload['stock'], vendedor_id, num_tipo, version_id)
	)

	prod_id = cur.fetchone()[0]
	
	cur.execute(
		"UPDATE equipamentos_versions SET equipamentos_main = %s WHERE id = %s",
		(prod_id, version_id)
	)

	cur.execute(
		
		f"INSERT INTO {payload['type']} (" +
		', '.join(atrs_tipo+["equipamentos_versions_id"]) +
		") VALUES (%s" + ", %s"*len(atrs_tipo) + ");",
		tuple(map(payload.__getitem__, atrs_tipo)) + (version_id, )
	)

	con.commit()
	con.close()

	return make_response(
		"sucess",
		prod_id,
		message_title="results"
	)

def fetch_info_product(prod_id, cur):

	cur.execute(
		"SELECT cur_version, tipo FROM equipamentos WHERE id = %s;",
		(prod_id,)
	)

	version_id, tipo = cur.fetchone()
	d = {}

	cur.execute(
		"SELECT " + ', '.join(basic_produt_atributes+["equipamentos_main"]) + " FROM equipamentos_versions WHERE id = %s;",
		(version_id,)
	)
	for i, j in zip(basic_produt_atributes+["equipamentos_main"], cur.fetchone()):
		d[i] = j

	nome_of_type = types_of_prods[tipo - 1]
	cur.execute(
		"SELECT " + ', '.join(product_atributes[nome_of_type][1])+ f" FROM {nome_of_type} "+
		"WHERE equipamentos_versions_id = %s;",
		(version_id,)
	)
	for i, j in zip(product_atributes[nome_of_type][1], cur.fetchone()):
		d[i] = j
	
	return d, nome_of_type

