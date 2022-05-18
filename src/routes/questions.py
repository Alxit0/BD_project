from flask import Blueprint, request
from psycopg2 import errors

if __name__ == "__main__":
	from utils import *
else:
	from .utils import *

questions_routes = Blueprint("questions_routes", __name__)

@questions_routes.before_request
def verify_token():
	return verify_header(request.headers)

@questions_routes.route('/<product_id>', methods=["POST"])
def make_question(product_id):
	payload = request.get_json()

	if "question" not in payload:
		make_response(
			"internal_error",
			"Missing arguments: question"
		)
	
	con = db_connection()
	cur = con.cursor()

	utilizador_id = get_id_from_token(request.headers['Authorization'].split()[1])

	cur.execute(
		"INSERT INTO questions (equipamento_id, utilizador_id, question) VALUES " +
		"(%s, %s, %s) RETURNING id;",
		(product_id, utilizador_id, payload['question'])
	)

	question_id = cur.fetchone()[0]

	con.commit()
	con.close()

	return make_response(
		"sucess",
		question_id,
		message_title="results"
	)

@questions_routes.route('/<product_id>/<parent_question_id>', methods=["POST"])
def respond_question(product_id, parent_question_id):
	payload = request.get_json()

	if "question" not in payload:
		make_response(
			"internal_error",
			"Missing arguments: question"
		)
	
	con = db_connection()
	cur = con.cursor()

	utilizador_id = get_id_from_token(request.headers['Authorization'].split()[1])

	try:
		cur.execute(
			"INSERT INTO questions (equipamento_id, utilizador_id, question, parent_question) VALUES " +
			"(%s, %s, %s, %s) RETURNING id;",
			(product_id, utilizador_id, payload['question'], parent_question_id)
		)
	except errors.ForeignKeyViolation:
		con.rollback()
		con.close()
		return make_response(
			"api_error",
			"Parent question does not exist."
		)

	question_id = cur.fetchone()[0]

	con.commit()
	con.close()

	return make_response(
		"sucess",
		question_id,
		message_title="results"
	)
