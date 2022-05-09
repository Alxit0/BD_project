from flask import Blueprint, request
from psycopg2 import errors

if __name__ == "__main__":
	from utils import *
else:
	from .utils import *


user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/", methods=["POST"])
def add_user():
	atribues_needed = ["username", "password"]
	payload = request.get_json()

	# check if has 'type'
	if 'type' not in payload:
		return make_response(
			"api_error",
			"Tipo ('type') de utilizador nao especificado (admin | vendedor | comprador)",
			message_title="error"
		)
	tipo = payload['type']

	# check if has all the needed atributes
	checker = check_atributes(payload, *atribues_needed)
	if checker != []:
		return make_response("api_error", "Missing atributs: " + ', '.join(checker))

	# if is comprador dont need verification
	if tipo == "comprador":
		return add_user_helper(payload, "comprador")
	
	# check if as header
	if 'Authorization' not in request.headers.keys():
		return make_response(
			"api_error",
			"Not logged in (no token passed). Please log in with and admin acount."
		)
	
	# check if as enough privileges
	if not check_if_admin(request.headers['Authorization'].split()[1]):
		return make_response(
			"api_error",
			"Not enough privileges. Please log in with and admin acount."
		)
	
	return add_user_helper(payload, tipo)


@user_routes.route("/", methods=["PUT"])
def loggin_user():
	atribues_needed = ["username", "password"]
	payload = request.get_json()

	# check if has all the needed atributes
	checker = check_atributes(payload, *atribues_needed)
	if checker != []:
		return make_response("api_error", "Missing atributs: " + ', '.join(checker))
	
	# ir buscar a informacao á base de dados
	con = db_connection()
	cur = con.cursor()

	cur.execute(
		"SELECT " + ', '.join(["id", "privileges"] + atribues_needed) +
		" FROM utilizador WHERE username=%s AND password=%s;",
		tuple(map(payload.__getitem__, atribues_needed))
	)

	rows = cur.fetchall()
	
	# fechar ligacao
	con.rollback()
	con.close()

	# Caso nao exista um utlizador com o username e passoword
	if not rows:
		return make_response("sucess", "Utilizador nao encontrado")
	
	# responder com o token
	return make_response(
		"sucess",
		write_token({"id":rows[0][0]}).decode("u8"),
		message_title= "token"
	)


def add_user_helper(payload:dict, tipo):

	# check if has all the needed atributes
	checker = check_atributes(payload, *users_atributes[tipo] + basic_user_atributes)
	if checker != []:
		return make_response("api_error", "Missing atributs: " + ', '.join(checker))

	con = db_connection()
	cur = con.cursor()

	try:
		cur.execute(
			"INSERT INTO utilizador (" + ', '.join(basic_user_atributes + ["privileges"]) + ")\
				VALUES (%s, %s, %s, %s)\
				RETURNING id",
			tuple(map(payload.__getitem__, basic_user_atributes))+(2, )
		)
	except errors.UniqueViolation:
		con.rollback()
		con.close()
		return make_response("internal_error", "User already exists", message_title="error")

	cur_id = cur.fetchone()[0]

	cur.execute(
		f"INSERT INTO {tipo} (" + ', '.join(["utilizador_id"]+users_atributes[tipo]) + ")\
			VALUES (%s" + ", %s" * len(users_atributes[tipo]) + ")",
		(cur_id,)+tuple(map(payload.__getitem__, users_atributes[tipo]))
	)

	con.commit()
	con.close()

	return make_response("sucess", cur_id, message_title="results")
