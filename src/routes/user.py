from flask import Blueprint, request, jsonify
from .utils import check_atributs, status_code, db_connection

user_routes = Blueprint("user_routes", __name__)


@user_routes.route('/dbproject/user', methods=["POST"])
def add_user():
	"""
	Criar um novo utilizador, inserindo os dados requeridos pelo modelo de dados.
	Qualquer pessoa se pode registar como comprador, mas apenas administradores podem
	criar novos administradores/vendedores (i.e., será necessário passar um token para validar o administrador).
	"""
	payload = request.get_json()

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


@user_routes.route('/dbproject/user', methods=["PUT"])
def loggin_user():
	"""
	Login com username e password, recebendo um token (e.g., Json Web Token (JWT)) 
	de autenticação em caso de sucesso. Este token deve ser incluído no header de todas 
	as chamadas subsequentes.
	"""
