from flask import Blueprint, request
from psycopg2 import errors

if __name__ == "__main__":
	from utils import *
else:
	from .utils import *


report_route = Blueprint("report_route", __name__)

@report_route.before_request
def verify_token():
	return verify_header(request.headers)


@report_route.route('/proj/report/year', methods=["GET"])
def year_report():
	con = db_connection()
	cur = con.cursor()

	cur.execute(
		"SELECT _date, SUM(total), SUM(num_orders) FROM orders GROUP BY _date ORDER BY _date DESC LIMIT 12;"
	)

	data = cur.fetchall()
	results = []
	for i, j, k in data:
		results.append({"month": i, "total_value": j, "orders": k})

	return make_response(
		"sucess",
		results,
		message_title="results"
	)