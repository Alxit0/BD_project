from flask import jsonify
from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
import psycopg2

SECRET = "Hello World"
status_code = {
	'sucess': 200,
	'api_error': 400,
	'internal_error': 500
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

def write_token(data: dict):
	expier_date = lambda time: datetime.now() + timedelta(minutes=time)
	
	token = encode(payload={**data, "exp": expier_date(30)}, key=SECRET, algorithm="HS256")
	return token.encode("UTF-8")

def validate_token(token, output=False):
	try:
		if output:
			return decode(token, key=SECRET, algorithms=["HS256"])
		decode(token, key=SECRET, algorithms=["HS256"])
	except exceptions.DecodeError:
		return jsonify({"message": "Invalid Token", "status": 401})
	except exceptions.ExpiredSignatureError:
		return jsonify({"message": "Expired Token", "status": 401})

def check_atributs(payload:dict, *args):
	falta = []
	for i in args:
		if i not in payload:
			falta.append(i)
	
	return falta
