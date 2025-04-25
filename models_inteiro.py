from flask import Flask, jsonify, request, session
from flask_pydantic_spec import FlaskPydanticSpec, Request, Response
from pydantic import BaseModel
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oficina.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = session(app)
spec = FlaskPydanticSpec('flask', title='API Oficina Mecânica')
spec.register(app)

# ========== MODELOS ==========

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(11))
    telefone = db.Column(db.String(15))
    endereco = db.Column(db.String(200))

class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(50))
    placa = db.Column(db.String(10))
    ano_fabricacao = db.Column(db.Integer)

class OrdemServico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'))
    data_abertura = db.Column(db.String(10))  # YYYY-MM-DD
    descricao = db.Column(db.Text)
    status = db.Column(db.String(20))  # pendente, em andamento, concluído
    valor_estimado = db.Column(db.Float)

# ========== SCHEMAS ==========

class ClienteSchema(BaseModel):
    nome: str
    cpf: str
    telefone: str
    endereco: str

class VeiculoSchema(BaseModel):
    cliente_id: int
    marca: str
    modelo: str
    placa: str
    ano_fabricacao: int

class OSSchema(BaseModel):
    veiculo_id: int
    data_abertura: str
    descricao: str
    status: str
    valor_estimado: float

# ========== ROTAS ==========

@app.route('/clientes', methods=['POST'])
@spec.validate(body=Request(ClienteSchema), resp=Response(HTTP_201=ClienteSchema))
def add_cliente():
    dados = request.context.body.dict()
    cliente = Cliente(**dados)
    db.session.add(cliente)
    db.session.commit()
    return jsonify(dados), 201

@app.route('/veiculos', methods=['POST'])
@spec.validate(body=Request(VeiculoSchema), resp=Response(HTTP_201=VeiculoSchema))
def add_veiculo():
    dados = request.context.body.dict()
    veiculo = Veiculo(**dados)
    db.session.add(veiculo)
    db.session.commit()
    return jsonify(dados), 201

@app.route('/os', methods=['POST'])
@spec.validate(body=Request(OSSchema), resp=Response(HTTP_201=OSSchema))
def add_ordem_servico():
    dados = request.context.body.dict()
    os = OrdemServico(**dados)
    db.session.add(os)
    db.session.commit()
    return jsonify(dados), 201

@app.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([{
        "id": c.id, "nome": c.nome, "cpf": c.cpf,
        "telefone": c.telefone, "endereco": c.endereco
    } for c in clientes])

@app.route('/veiculos/cliente/<int:cliente_id>', methods=['GET'])
def listar_veiculos_por_cliente(cliente_id):
    veiculos = Veiculo.query.filter_by(cliente_id=cliente_id).all()
    return jsonify([{
        "id": v.id, "marca": v.marca, "modelo": v.modelo,
        "placa": v.placa, "ano_fabricacao": v.ano_fabricacao
    } for v in veiculos])

@app.route('/os/status/<status>', methods=['GET'])
def listar_os_por_status(status):
    ordens = OrdemServico.query.filter_by(status=status).all()
    return jsonify([{
        "id": o.id, "veiculo_id": o.veiculo_id,
        "data_abertura": o.data_abertura, "descricao": o.descricao,
        "status": o.status, "valor_estimado": o.valor_estimado
    } for o in ordens])

@app.route('/os/veiculo/<int:veiculo_id>', methods=['GET'])
def listar_os_por_veiculo(veiculo_id):
    ordens = OrdemServico.query.filter_by(veiculo_id=veiculo_id).all()
    return jsonify([{
        "id": o.id, "data_abertura": o.data_abertura,
        "descricao": o.descricao, "status": o.status,
        "valor_estimado": o.valor_estimado
    } for o in ordens])

# ========== INICIALIZA BANCO ==========

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)



























@app.route('/validade_produto', methods=['POST'])
def calcular_validade():
    """
    API para Cálculo de Validade de Produtos

    ## Endpoint:
    `GET /data/quantidade

    ## Parâmetros:
    - ** Data no formato "DD/MM/YYYY" ** (exemplo: "20/11/2025").
    - ** Qualquer outro formato resultará em erro. **

    ## Resposta (JSON):
    {
        "validade_fornecida": "0"
        "data_validade": "%Y/%m/%d"
        "unidade": "0"
        }

    ## Erros possíveis:
    - Se não estiver no formato correto(data), retorna erro ** 400 **
    Bad Request
    "json"

    :return: "validade_fornecida": 0
            "data_validade": "%Y/%m/%d"
    """

    dados = request.get_json()
    data_fabricacao = datetime.strptime('data_fabricacao', "%Y/%m/%d")
    validade = dados['validade']
    unidade = dados['unidade'].lower()


    if unidade == "dias":
        data_validade = data_fabricacao + relativedelta(days=validade)
    elif unidade == "semanas":
        data_validade = data_fabricacao + relativedelta(weeks=validade)
    elif unidade == "meses":
        data_validade = data_fabricacao + relativedelta(months=validade)
    elif unidade == "anos":
        data_validade = data_fabricacao + relativedelta(years=validade)
    else:
        return jsonify({"Use dias, semanas, meses ou anos."}), 400

    resposta = {
        "validade_fornecida": f"{validade} {unidade}",
        "data_validade": data_validade.strftime("%Y/%m/%d")
    }
    return jsonify(resposta)