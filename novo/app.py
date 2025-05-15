from flask import Flask, request, jsonify
from models import Cliente, Veiculo, OrdemServico, db_session
from utils import init_db
from flask_pydantic_spec import FlaskPydanticSpec, Request, Response
from pydantic import BaseModel, Field
from sqlalchemy import select
from datetime import datetime

app = Flask(__name__)

spec = FlaskPydanticSpec(
    'flask',
    title='Quarta API - SENAI',
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

@app.route('/criar_cliente', methods=['POST'])
def criar_cliente():
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
    cliente.cpf = data('cpf', cliente.cpf)
    cliente.telefone = data('telefone', cliente.telefone)
    cliente.endereco = data('endereco', cliente.endereco)
    cliente.save()
    return jsonify(cliente.serialize())

@app.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = db_session.execute(select(Cliente).where(Cliente.id == id)).scalar()
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404
    cliente.delete()
    return jsonify({'mensagem': 'Cliente deletado com sucesso!'})


#VEÍCULOS
@app.route('/veiculos', methods=['GET'])
def listar_veiculos():
    try:
        veiculos = select(Veiculo)
        result = db_session().execute(veiculos).scalars().all()
        listar_veiculos = [veiculo.serialize() for veiculo in result]
        return jsonify({'veiculos': listar_veiculos})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/veiculos', methods=['POST'])
def criar_veiculo():
    data = request.get_json()
    try:
        veiculo = Veiculo(
            cliente_id=data['cliente_id'],
            marca=data['marca'],
            modelo=data['modelo'],
            placa=data['placa'],
            ano_fabricacao=data['ano_fabricacao'],
        )
        veiculo.save()
        return jsonify(veiculo.serialize()), 201
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/veiculos/<int:id>', methods=['GET'])
def buscar_veiculo(id):
    try:
        veiculo = db_session().execute(select(Veiculo).where(Veiculo.id == id)).scalar_one_or_none()
        if veiculo:
            return jsonify(veiculo.serialize())
        return jsonify({'message': 'Veículo não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/veiculos/<int:id>', methods=['PUT'])
def atualizar_veiculo(id):
    try:
        veiculo = db_session().execute(select(Veiculo).where(Veiculo.id == id)).scalar_one_or_none()
        if not veiculo:
            return jsonify({'message': 'Veículo não encontrado'}), 404
        data = request.get_json()
        veiculo.cliente_id = data.get('cliente_id', veiculo.cliente_id)
        veiculo.marca = data.get('marca', veiculo.marca)
        veiculo.modelo = data.get('modelo', veiculo.modelo)
        veiculo.placa = data.get('placa', veiculo.placa)
        veiculo.ano_fabricacao = data.get('ano_fabricacao', veiculo.ano_fabricacao)
        veiculo.save()
        return jsonify(veiculo.serialize())
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/veiculos/<int:id>', methods=['DELETE'])
def deletar_veiculo(id):
    try:
        veiculo = db_session().execute(select(Veiculo).where(Veiculo.id == id)).scalar_one_or_none()
        if not veiculo:
            return jsonify({'message': 'Veículo não encontrado'}), 404

        db_session().delete(veiculo)
        db_session().commit()
        return jsonify({'message': 'Veículo deletado com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)})



#ORDENS DE SERVIÇO
@app.route('/ordens', methods=['GET'])
def listar_ordens():
    try:
        ordens = select(OrdemServico)
        result = db_session().execute(ordens).scalars().all()
        listar_ordens = [ordem.serialize() for ordem in result]
        return jsonify({'ordens': listar_ordens})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/ordens', methods=['POST'])
def criar_ordem():
    data = request.get_json()
    try:
        ordem = OrdemServico(
            veiculo_id=data['veiculo_id'],
            data_abertura=data['data_abertura'],
            descricao_servico=data['descricao_servico'],
            status=data['status'],
            valor_estimado=data['valor_estimado'],
        )
        ordem.save()
        return jsonify(ordem.serialize()), 201
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/ordens/<int:id>', methods=['GET'])
def buscar_ordem(id):
    try:
        ordem = db_session().execute(select(OrdemServico).where(OrdemServico.id == id)).scalar_one_or_none()
        if ordem:
            return jsonify(ordem.serialize())
        return jsonify({'message': 'Ordem de serviço não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/ordens/<int:id>', methods=['PUT'])
def atualizar_ordem(id):
    try:
        ordem = db_session().execute(select(OrdemServico).where(OrdemServico.id == id)).scalar_one_or_none()
        if not ordem:
            return jsonify({'message': 'Ordem de serviço não encontrada'}), 404

        data = request.get_json()
        ordem.veiculo_id = data.get('veiculo_id', ordem.veiculo_id)
        ordem.data_abertura = data.get('data_abertura', ordem.data_abertura)
        ordem.descricao_servico = data.get('descricao_servico', ordem.descricao_servico)
        ordem.status = data.get('status', ordem.status)
        ordem.valor_estimado = data.get('valor_estimado', ordem.valor_estimado)
        ordem.save()
        return jsonify(ordem.serialize())
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/ordens/<int:id>', methods=['DELETE'])
def deletar_ordem(id):
    try:
        ordem = db_session().execute(select(OrdemServico).where(OrdemServico.id == id)).scalar_one_or_none()
        if not ordem:
            return jsonify({'message': 'Ordem de serviço não encontrada'}), 404

        db_session().delete(ordem)
        db_session().commit()
        return jsonify({'message': 'Ordem de serviço deletada com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

# POST recebe a informação
# GET mostra
# PUT atualiza