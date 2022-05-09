from flask import Blueprint, request
from psycopg2 import errors

if __name__ == "__main__":
	from utils import *
else:
	from .utils import *


product_routes = Blueprint("product_routes", __name__)
basic_produt_atributes = ["preco", "descricao", "stock", "nome"]
product_atributes = {
	'computadores': ["processador", "placa_vidio", "ram", "storage"],
	'televisoes': ["tamanho", "resolucao", "refresh_rt"],
	'smartphones': ["tamanho", "ram", "storage", "camera", "processador"]
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

def create_product_helper(payload:dict, vendedor_id):
	# check if has 'type'
	if 'type' not in payload:
		return make_response(
			"api_error",
			"Tipo ('type') de utilizador nao especificado (computadores | televisoes | smartphones)",
			message_title="error"
		)
	
	# check if has all the needed atributes
	checker = check_atributes(payload, *basic_produt_atributes + product_atributes[payload['type']])
	if checker != []:
		return make_response("api_error", "Missing atributs: " + ', '.join(checker))
	
	con = db_connection()
	cur = con.cursor()

	try:
		cur.execute(
			"INSERT INTO equipamentos (" +
			', '.join(basic_produt_atributes+["vendedor_utilizador_id"]) +
			") VALUES (%s" + ", %s"*len(basic_produt_atributes) + ") RETURNING id;",
			tuple(map(payload.__getitem__, basic_produt_atributes)) + (vendedor_id, )
		)
	except errors.UniqueViolation:
		con.rollback()
		con.close()
		return make_response("internal_error", "Equipamento already exists", message_title="error")

	prod_id = cur.fetchone()[0]

	cur.execute(
		f"INSERT INTO {payload['type']} (" +
		', '.join(product_atributes[payload['type']]+["equipamentos_id"]) +
		") VALUES (%s" + ", %s"*len(product_atributes[payload['type']]) + ");",
		tuple(map(payload.__getitem__, product_atributes[payload['type']])) + (prod_id, )
	)

	con.commit()
	con.close()

	return make_response(
		"sucess",
		prod_id,
		message_title="results"
	)

