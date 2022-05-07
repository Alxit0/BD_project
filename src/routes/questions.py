from flask import Blueprint

questions_routes = Blueprint("questions_routes", __name__)


@questions_routes.route('/dbproject/questions/<product_id>', methods=["POST"])
def make_question(product_id):
	"""
	Deve ser possível fazer uma pergunta num produto.
	"""


@questions_routes.route('/dbproject/questions/<product_id>/<parent_question_id>', methods=["POST"])
def answer_question(product_id, parent_question_id):
	"""
	Deve ser possível responder a uma pergunta num produto.
	"""
 
