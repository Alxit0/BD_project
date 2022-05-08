from flask import Blueprint, request, jsonify
from .utils import status_code, db_connection, validate_token, check_atributs, write_token

user_routes = Blueprint("user_routes", __name__)


@user_routes.route('/', methods=["POST"])
def add_user():
	"""
	Criar um novo utilizador, inserindo os dados requeridos pelo modelo de dados.
	Qualquer pessoa se pode registar como comprador, mas apenas administradores podem
	criar novos administradores/vendedores (i.e., será necessário passar um token para validar o administrador).
	"""
	payload = request.get_json()

	if "type" not in payload:
		return jsonify({"status": status_code["internal_error"],
			"errors": "Tipo (type) de utilizador nao especificado (admin | vendedor | comprador)"})

	tipo = payload["type"]
	
	response = jsonify({"status": status_code["api_error"],
			"errors": "Tipo de utilizador nao existe (admin | vendedor | comprador)"})
	
	if tipo in ("admin", "vendedor"):
		if 'Authorization' not in request.headers.keys():
			return jsonify({"status": status_code["sucess"],
			"results": "Token required"})

		validade = validate_token(request.headers['Authorization'].split()[1], output=False)

		if validade:
			return validade

		if tipo == "admin":
			response = add_admin(payload)
		elif tipo == "vendedor":
			response = add_vendedor(payload)
	
	if tipo == "comprador":
		response = add_comprador(payload)

	return response

@user_routes.route('/', methods=["PUT"])
def loggin_user():
	"""
	Login com username e password, recebendo um token (e.g., Json Web Token (JWT)) 
	de autenticação em caso de sucesso. Este token deve ser incluído no header de todas 
	as chamadas subsequentes.
	"""
	payload = request.get_json()

	needed_atriputs = ["username", "password"]
	temp = check_atributs(payload, *needed_atriputs)
	
	if temp:
		return jsonify({"status": status_code["api_error"],
			"errors": "Missing atributs: " + ', '.join(temp)})

	con = db_connection()
	cur = con.cursor()

	cur.execute("SELECT username, password FROM utilizador WHERE username=%s AND password=%s;",
			tuple(map(payload.__getitem__, needed_atriputs)))

	rows = cur.fetchone()
	if rows is None:
		return jsonify({{"status": status_code["sucess"],
			"results": "User not found"}})
	
	return write_token({**payload, "lvl": "admin"})
	return jsonify({"status": status_code["sucess"], "results": write_token({**payload, "lvl": "admin"})})


def add_comprador(payload):

	needed_atriputs = ["username", "email", "password", "morada"]
	temp = check_atributs(payload, *needed_atriputs)
	
	if temp:
		return jsonify({"status": status_code["api_error"],
			"errors": "Missing atributs: " + ', '.join(temp)})
		

	con = db_connection()
	cur = con.cursor()

	# parameterized queries, good for security and performance
	cur.execute(
		"INSERT INTO utilizador (username, email, password)\
			VALUES (%s, %s, %s)\
			RETURNING id", tuple(map(payload.__getitem__, needed_atriputs[:-1]))
	)

	cur_id = cur.fetchall()[0][0] # sacar do id que foi gerado automaticamente

	cur.execute(
		"INSERT INTO comprador (morada, utilizador_id)\
			VALUES (%s, %s)", (payload["morada"], cur_id)
	)

	con.commit()
	con.close()

	response = jsonify({"status": status_code["sucess"], "results": cur_id})
	return response

def add_admin(payload):

	needed_atriputs = ["username", "email", "password"]
	temp = check_atributs(payload, *needed_atriputs)
	
	if temp:
		return jsonify({"status": status_code["api_error"],
			"errors": "Missing atributs: " + ', '.join(temp)})
		

	con = db_connection()
	cur = con.cursor()

	# parameterized queries, good for security and performance
	cur.execute(
		"INSERT INTO utilizador (username, email, password)\
			VALUES (%s, %s, %s)\
			RETURNING id", tuple(map(payload.__getitem__, needed_atriputs))
	)

	cur_id = cur.fetchall()[0][0] # sacar do id que foi gerado automaticamente

	cur.execute(
		"INSERT INTO admnistrador (utilizador_id)\
			VALUES (%s)", (cur_id,)
	)

	con.commit()
	con.close()

	response = jsonify({"status": status_code["sucess"], "results": cur_id})
	return response

def add_vendedor(payload):

	needed_atriputs = ["username", "email", "password", "morada", "nif"]
	temp = check_atributs(payload, *needed_atriputs)
	
	if temp:
		return jsonify({"status": status_code["api_error"],
			"errors": "Missing atributs: " + ', '.join(temp)})
		

	con = db_connection()
	cur = con.cursor()

	# parameterized queries, good for security and performance
	cur.execute(
		"INSERT INTO utilizador (username, email, password)\
			VALUES (%s, %s, %s)\
			RETURNING id", tuple(map(payload.__getitem__, needed_atriputs[:-2]))
	)

	cur_id = cur.fetchall()[0][0] # sacar do id que foi gerado automaticamente

	cur.execute(
		"INSERT INTO vendedor (morada, nif, utilizador_id)\
			VALUES (%s, %s, %s)", (payload["morada"], payload["nif"], cur_id)
	)

	con.commit()
	con.close()

	response = jsonify({"status": status_code["sucess"], "results": cur_id})
	return response

if __name__ == "__main__":
	add_admin({"username": "Alex", "email": "alexandrerassxegalado@hotmail.com", "password": "Ola123"})
	print("Ola")