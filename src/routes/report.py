from flask import Blueprint

reports_routes = Blueprint("reports_routes", __name__)

@reports_routes.route('/proj/report/year', methods=["GET"])
def year_status():
	"""
	Deve ser possível obter os detalhes das vendas
	(e.g., número de vendas, valor) por mês nos últimos 12 meses.
	No servidor deve ser usada apenas uma query SQL para obter esta informação.
	"""


@reports_routes.route('/dbproject/report/campaign')
def campaign_report():
	"""
	Deve ser possível obter uma lista das diversas campanhas, número de 
	cupões emitidos e utilizados, bem como o valor total dos descontos aplicados. 
	Campanhas sem cupões utilizados/atribuídos também devem ser devolvidas. 
	No servidor deve ser usada apenas uma query SQL para obter esta informação.
	"""
 
