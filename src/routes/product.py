from flask import Blueprint, request
from .utils import validate_token

product_routes = Blueprint("product_routes", __name__)

@product_routes.before_request
def verify_token():
	token = request.headers['Authorization'].split()[1]
	return validate_token(token)

@product_routes.route('/dbproject/product', methods=["POST"])
def create_product():
	"""
	Cada vendedor deve poder criar novos produtos para comercializar.
	"""

@product_routes.route('/dbproject/product/<product_id>', methods=["POST"])
def udpate_product(product_id):
	"""
	Deve ser possível atualizar os detalhes de um produto.
	Para efeitos de auditoria é necessário manter as diferentes versões.
	"""

@product_routes.route('/<product_id>', methods=["GET"])
def consult_product_info(product_id):
	return """
	Deve ser possível obter os detalhes genéricos de um produto
	(e.g., título, stock), o histórico de preços, rating médio,
	e comentários (ter em conta que é possível que para um dado 
	produto não haja rating ou comentários, devendo o mesmo ser devolvido). 
	No servidor deve ser usada apenas uma query SQL para obter esta informação.
	"""

