import flask
import logging
import psycopg2

app = flask.Flask(__name__)

status_code = {
    'sucess': 200,
    'api_error': 400,
    'internal_error': 500
}


def db_connection():
    db = psycopg2.connect(
        user='aulaspl',
        password='aulaspl',
        host='127.0.0.1',
        port='5000',
        database='dbfichas'
    )

    return db


@app.route('/dbproject', methods=["GET"])
def landing_page():
    """Base"""

    return "INICIO"


@app.route('/dbproject/user', methods=["POST"])
def add_user():
    """
    Criar um novo utilizador, inserindo os dados requeridos pelo modelo de dados.
    Qualquer pessoa se pode registar como comprador, mas apenas administradores podem
    criar novos administradores/vendedores (i.e., será necessário passar um token para validar o administrador).
    """
    pass


@app.route('/dbproject/user', methods=["PUT"])
def loggin_user():
    """
    Login com username e password, recebendo um token (e.g., Json Web Token (JWT)) 
    de autenticação em caso de sucesso. Este token deve ser incluído no header de todas 
    as chamadas subsequentes.
    """


@app.route('/dbproject/product', methods=["POST"])
def create_product():
    """
    Cada vendedor deve poder criar novos produtos para comercializar.
    """


@app.route('/dbproject/product/<product_id>', methods=["POST"])
def udpate_product(product_id):
    """
    Deve ser possível atualizar os detalhes de um produto.
    Para efeitos de auditoria é necessário manter as diferentes versões.
    """


@app.route('/dbproject/order', methods=["POST"])
def make_order():
    """Deve ser possível registar uma nova compra, com todos os detalhes associados."""


@app.route('/dbproject/rating/<product_id>', methods=["POST"])
def give_rating(product_id):
    """
    Deve ser possível deixar um rating a um produto comprado.
    """


@app.route('/dbproject/questions/<product_id>', methods=["POST"])
def make_question(product_id):
    """
    Deve ser possível fazer uma pergunta num produto.
    """


@app.route('/dbproject/questions/<product_id>/<parent_question_id>', methods=["POST"])
def answer_question(product_id, parent_question_id):
    """
    Deve ser possível responder a uma pergunta num produto.
    """


@app.route('/dbproject/product/<product_id>', methods=["GET"])
def consult_product_info(product_id):
    """
    Deve ser possível obter os detalhes genéricos de um produto
    (e.g., título, stock), o histórico de preços, rating médio,
    e comentários (ter em conta que é possível que para um dado 
    produto não haja rating ou comentários, devendo o mesmo ser devolvido). 
    No servidor deve ser usada apenas uma query SQL para obter esta informação.
    """


@app.route('/proj/report/year', methods=["GET"])
def year_status():
    """
    Deve ser possível obter os detalhes das vendas
    (e.g., número de vendas, valor) por mês nos últimos 12 meses.
    No servidor deve ser usada apenas uma query SQL para obter esta informação.
    """


@app.route('/dbproject/campaign', methods=["POST"])
def create_campaign():
    """
    Um administrador deverá poder criar novas campanhas.
    Tenha em conta que não poderão existir campanhas ativas em simultâneo.
    """


@app.route('/dbproject/subscribe/<campaign_id>', methods=["PUT"])
def subscribe_campaign():
    """
    Deve ser possível um comprador subscrever uma campanha de atribuição de cupões.
    Assim que esgotarem os cupões, a campanha termina.
    """


@app.route('/dbproject/report/campaign')
def campaign_report():
    """
    Deve ser possível obter uma lista das diversas campanhas, número de 
    cupões emitidos e utilizados, bem como o valor total dos descontos aplicados. 
    Campanhas sem cupões utilizados/atribuídos também devem ser devolvidas. 
    No servidor deve ser usada apenas uma query SQL para obter esta informação.
    """


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8080
    app.run(host=host, port=port)
