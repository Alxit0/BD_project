from flask import jsonify
import psycopg2
from datetime import datetime, timedelta
from jwt import encode, decode, exceptions

SECRET = "Hello World"

status_code = {
	'sucess': 200,
	'api_error': 400,
	'internal_error': 500
}


def db_connection():
	db = psycopg2.connect(
		user='postgres',
		password='postgres',
		host='127.0.0.1',
		port='8000',
		database='proj'
	)

	# db = psycopg2.connect(
	# 	user='postgres',
	# 	password='postgres',
	# 	host='127.0.0.1',
	# 	port='5432',
	# 	database='porjtemp'
	# )

	return db


def make_response(status, message, *, message_title="message"):
	"""
	sucess | api_error | internal_error
	"""
	return jsonify({"status": status_code[status], message_title: message})


def check_atributes(payload:dict, *atributes):
	temp = []
	for i in atributes:
		if i not in payload:
			temp.append(i)
	
	return temp


def write_token(data:dict):
	expier_date = lambda time: datetime.now() + timedelta(minutes=time)
	
	token = encode(payload={**data, "exp": expier_date(30)}, key=SECRET, algorithm="HS256")
	return token.encode("UTF-8")


def check_if_creds(token, lvl):
	tipo = ["comprador", "vendedor", "admnistrador"][lvl-1]

	_id = decode(token, key=SECRET, algorithms=["HS256"])["id"]

	con = db_connection()
	cur = con.cursor()

	cur.execute(f"SELECT * FROM {tipo}"+" WHERE utilizador_id=%s", (_id,))
	
	priv = cur.fetchone()
	if priv is None:
		return False

	con.rollback()
	con.close()
	# print(priv)
	return True


def verify_header(headers, output=False):
	if 'Authorization' not in headers.keys():
		return make_response(
			"api_error",
			"Not logged in (no token passed). Please log in."
		)
	token = headers['Authorization'].split()[1]
	try:
		if output:
			return decode(token, key=SECRET, algorithms=["HS256"])
		decode(token, key=SECRET, algorithms=["HS256"])
	except exceptions.DecodeError:
		print(token)
		return jsonify({"message": "Invalid Token", "status": 401})
	except exceptions.ExpiredSignatureError:
		return jsonify({"message": "Expired Token", "status": 401})


def get_id_from_token(token):
	"""
	get_id_from_token(request.headers['Authorization'].split()[1])
	"""
	return decode(token, key=SECRET, algorithms=["HS256"])["id"]
