from flask import Flask, request, jsonify
from models import Cliente, Veiculo, OrdemServico, init_db, db_session
from flask_pydantic_spec import FlaskPydanticSpec

app = Flask(__name__)

spec = FlaskPydanticSpec(
                        'flask',
                        title='First API - SENAI',
                        version='1.0.0')
spec.register(app)
init_db()

#CLIENTES
@app.route('/clientes', methods=['GET'])
def listar_clientes():
    try:
        clientes = select(Cliente)
        result = db_session().execute(clientes).scalars().all()
        listar_clientes = []
        for cliente in result:
            listar_clientes.append({cliente.serialize()})
            return jsonify({'clientes': listar_clientes})
    except ValueError as e:
        return  jsonify({'error': str(e)})

@app.route('/clientes', methods=['POST'])
def criar_cliente():
    """
    Api para criar cliente
    :return:
    """
    data = request.get_json()
    cliente = Cliente(
        nome=data['nome'],
        cpf=data['cpf'],
        telefone=data['telefone'],
        endereco=data['endereco'],
    )
    cliente.save()
    return jsonify(cliente.serialize()), 201

@app.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    cliente = db_session.execute(select(Cliente).where(Cliente.id == id)).scalar()
    data = request.get_json()
    cliente.nome = data('nome')
    cliente.cpf =data('cpf', cliente.cpf)
    cliente.telefone = data('telefone', cliente.telefone)
    cliente.endereco = data('endereco', cliente.endereco)
    cliente.save()
    return jsonify(cliente.serialize())

@app.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = db_session.execute(select(Cliente).where(Cliente.id == id)).scalar()
    cliente.delete()
    return jsonify({'message': 'Cliente deletado'})


#VEÍCULOS
@app.route('/veiculos', methods=['GET'])
def listar_veiculos():
    """
    Api para listar veiculos
    :return:
    """
    return jsonify([v.serialize() for v in Veiculo.query.all()])

@app.route('/veiculos', methods=['POST'])
def criar_veiculo():
    """
    Api para criar veiculo
    :return:
    """
    data = request.json()
    veiculo = Veiculo(
        cliente_id=data['cliente_id'],
        marca=data['marca'],
        modelo=data['modelo'],
        placa=data['placa'],
        ano_fabricacao=data['ano_fabricacao'],
    )
    veiculo.save()
    return jsonify(veiculo.serialize()), 201

@app.route('/veiculos/<int:id>', methods=['GET'])
def buscar_veiculo(id):
    """
    Api para buscar veiculo
    :param id:
    :return:
    """
    veiculo = Veiculo.query.get_or_404(id)
    return jsonify(veiculo.serialize())

@app.route('/veiculos/<int:id>', methods=['PUT'])
def atualizar_veiculo(id):
    """
    Api para atualizar veiculo
    :param id:
    :return:
    """
    veiculo = Veiculo.query.get_or_404(id)
    data = request.json()
    veiculo.cliente_id = data.get['cliente_id'] = data.get('cliente_id', veiculo.cliente_id)
    veiculo.marca = data.get('marca', veiculo.marca)
    veiculo.modelo = data.get('modelo', veiculo.modelo)
    veiculo.ano_fabricacao = data.get('ano_fabricacao', veiculo.ano_fabricacao)
    veiculo.save()
    return jsonify(veiculo.serialize())

@app.route('/veiculos/<int:id>', methods=['DELETE'])
def deletar_veiculo(id):
    """
    Api para deletar veiculo
    :param id:
    :return:
    """
    veiculo = Veiculo.query.get_or_404(id)
    veiculo.delete()
    return jsonify({'messagem': 'Veículo deletado com sucesso!'})


#ORDENS DE SERVIÇO
@app.route('/ordens' , methods=['GET'])
def listar_ordens():
    """
    Api para listar ordens
    :return:
    """
    return jsonify([o.serialize() for o in OrdemServico.query.all()])

@app.route('/ordens' , methods=['GET'])
def criar_ordens():
    """

    :return:
    """
    data = request.get_json()
    ordens = OrdemServico(
        veiculo_id=data['veiculo_id'],
        data_abertura=data['data_abertura'],
        descricao_servico=data['descricao_servico'],
        status=data['status'],
        valor_estimada=data['valor_estimada'],
    )
    ordens.save()
    return jsonify(ordens.serialize()), 201

@app.route('/ordens/<int:id>', methods=['GET'])
def buscar_ordens(id):
    """
    Api para buscar ordens
    :param id:
    :return:
    """
    ordem = OrdemServico.query.get_or_404(id)
    return jsonify(ordem.serialize())

@app.route('/ordens/<int:id>', methods=['PUT'])
def atualizar_ordens(id):
    """
    Api para atualizar ordens
    :param id:
    :return:
    """
    ordem = OrdemServico.query.get_or_404(id)
    data = request.json()
    ordem.veiculo_id = data.get('veiculo_id', ordem.veiculo_id)
    ordem.data_abertura = data.get('data_abertura', ordem.data_abertura)
    ordem.descricao_servico = data.get('descricao_servico', ordem.descricao_servico)
    ordem.status = data.get('status', ordem.status)
    ordem.valor_estimada = data.get('valor_estimada', ordem.valor_estimada)
    ordem.save()
    return jsonify(ordem.serialize())

@app.route('/ordens/<int:id>', methods=['DELETE'])
def deletar_ordens(id):
    """
    Api para deletar ordens
    :param id:
    :return:
    """
    ordem = OrdemServico.query.get_or_404(id)
    ordem.delete()
    return jsonify({'messagem': 'Ordem deletada com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)

# POST recebe a informação
# GET mostra
# PUT atualiza