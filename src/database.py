import psycopg2
import flask

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

def check_atributs(payload:dict, *args):
	falta = []
	for i in args:
		if i not in payload:
			falta.append(i)
	
	return falta

def insert_comprador(payload:dict):
	needed_atriputs = ["username", "email", "password", "morada"]
	temp = check_atributs(payload, *needed_atriputs)
	
	if temp:
		return flask.jsonify({"status": status_code["api_error"],
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

	return flask.jsonify({"status": status_code["sucess"], "results": cur_id})


def delete_comprador(name):
	con = db_connection()
	cur = con.cursor()

	# parameterized queries, good for security and performance
	statement = f"DELETE FROM utilizador WHERE username = '{name}';"
	cur.execute(statement)
	con.commit()
	con.close()

if __name__ == "__main__":
	insert_comprador({"username":"Alex", "email": "alexandreregalado@hotmail.com", "password": "Alexandre1712", "morada":"gafanha do Carmo"})
	# delete_comprador("Alex")


