from flask import Blueprint

misclans_routes = Blueprint("misclans_routes", __name__)

@misclans_routes.route('/dbproject/order', methods=["POST"])
def make_order():
	"""Deve ser possível registar uma nova compra, com todos os detalhes associados."""


@misclans_routes.route('/dbproject/rating/<product_id>', methods=["POST"])
def give_rating(product_id):
	"""
	Deve ser possível deixar um rating a um produto comprado.
	"""


@misclans_routes.route('/dbproject/campaign', methods=["POST"])
def create_campaign():
	"""
	Um administrador deverá poder criar novas campanhas.
	Tenha em conta que não poderão existir campanhas ativas em simultâneo.
	"""


@misclans_routes.route('/dbproject/subscribe/<campaign_id>', methods=["PUT"])
def subscribe_campaign():
	"""
	Deve ser possível um comprador subscrever uma campanha de atribuição de cupões.
	Assim que esgotarem os cupões, a campanha termina.
	"""
