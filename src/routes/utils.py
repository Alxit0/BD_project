from flask import jsonify
import psycopg2
from datetime import datetime, timedelta
from jwt import encode, decode

SECRET = "Hello World"

status_code = {
	'sucess': 200,
	'api_error': 400,
	'internal_error': 500
}

basic_user_atributes = ["username", "email", "password"]

users_atributes = {
	'comprador': ["morada"],
	'vendedor': ["morada", "nif"],
	'admin': []
}

def db_connection():
	db = psycopg2.connect(
		user='postgres',
		password='ola',
		host='127.0.0.1',
		port='8000',
		database='proj'
	)

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


def check_if_admin(token):
	_id = decode(token, key=SECRET, algorithms=["HS256"])["id"]

	con = db_connection()
	cur = con.cursor()

	cur.execute("SELECT privileges FROM utilizador WHERE id=%s", (_id,))

	priv = cur.fetchone()

	con.rollback()
	con.close()
	print(priv)
	return priv[0] == 3
