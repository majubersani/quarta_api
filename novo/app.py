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
    """
    API para listar todos os clientes cadastrados.

    ## Endpoint:
        /clientes

        "clientes": [
            {
                "id": 1,
                "nome": "Nome do Cliente",
                "cpf": "123.456.789-00",
                "telefone": "(11) 98765-4321",
                "endereco": "Rua Exemplo, 123"'
            }

    ### Erros Possíveis (JSON):

    #### Erro Interno do Servidor
    """
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
    """
    API para criar cliente.

    ## Endpoint:
        /criar_cliente

    ## Requisições (POST):
        - **Campos (JSON):**
            - "nome"
            - "cpf"
            - "telefone"
            - "endereco"

    ## Respostas (JSON):
            "id": 1,
            "nome": "Nome do Cliente",
            "cpf": "123.456.789-00",
            "telefone": "(11) 98765-4321",
            "endereco": "Rua Exemplo, 123"


    ### Erros Possíveis:
        - Nenhum erro específico é tratado neste exemplo.
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
    """
    API para atualizar os dados de um cliente existente.

    ## Endpoint:
        /clientes

    ## Métodos:
        - **PUT**: atualizar os dados de um cliente, identificados

    ## Requisições (PUT):
        - **Campos (JSON):**
            - "nome"
            - "cpf"
            - "telefone"
            - "endereco"


    ### Sucesso:
        "id": 1,
        "nome": "Nome Atualizado",
        "cpf": "987.654.321-00",
        "telefone": "(22) 11111-2222",
        "endereco": "Novo Endereço"

    ### Erros Possíveis:
        - **Cliente não encontrado
        - **Erro Interno do Servidor - Em caso de falha na atualização.
    """
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
    """
    API para deletar um cliente.

    ## Endpoint:
        /clientes>

    ### Sucesso (200 OK):
        "mensagem": "Cliente deletado com sucesso!"


    ### Erros Possíveis:
        - **Cliente não encontrado **
            "erro": "Cliente não encontrado"

    """
    cliente = db_session.execute(select(Cliente).where(Cliente.id == id)).scalar()
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404
    cliente.delete()
    return jsonify({'mensagem': 'Cliente deletado com sucesso!'})



#VEÍCULOS
@app.route('/veiculos', methods=['GET'])
def listar_veiculos():
    """
    API para listar todos os veículos.

    ## Endpoint:
        /veiculos

    ## Métodos:
        - **GET**: Volta uma lista de todos os veículos cadastrados.

    ### Sucesso:
                "id": 1,
                "cliente_id": 10,
                "marca": "Fusca",
                "modelo": "blabla",
                "placa": "ABC-1234",
                "ano_fabricacao": "2020"

    ### Erros Possíveis:
     "error": "Descrição do erro ocorrido"
    """
    try:
        veiculos = select(Veiculo)
        result = db_session().execute(veiculos).scalars().all()
        listar_veiculos = [veiculo.serialize() for veiculo in result]
        return jsonify({'veiculos': listar_veiculos})
    except Exception as e:
        return jsonify({'error': str(e)})



@app.route('/veiculos', methods=['POST'])
def criar_veiculo():
    """
    API para criar um veículo.

    ## Endpoint:
        /veiculos

    ## Requisições (POST):
        - **Campos (JSON):**
            - "cliente_id"
            - "marca"
            - "modelo"
            - "placa"
            - "ano_fabricacao"

    ### Erros Possíveis:
           - "error": "Descrição do erro ocorrido"
    """
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
    """
    API para buscar um veículo específico.

    ## Métodos:
        - **GET**: Volta os dados de um veículo, identificado.

    ### Erros Possíveis:
            "mensagem": "Veículo não encontrado"

    """
    try:
        veiculo = db_session().execute(select(Veiculo).where(Veiculo.id == id)).scalar_one_or_none()
        if veiculo:
            return jsonify(veiculo.serialize())
        return jsonify({'mensagem': 'Veículo não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/veiculos/<int:id>', methods=['PUT'])
def atualizar_veiculo(id):
    """
    API para atualizar os dados de um veículo existente.

    ## Endpoint:
        /veiculos

    ## Requisições (PUT):
        - **Campos (JSON):**
            - "cliente_id"
            - "marca"
            - "modelo"
            - "placa"
            - "ano_fabricacao"

    ## Respostas (JSON):
    '''json

    ### Erros Possíveis:
            "mensagem": "Veículo não encontrado"
            "error": "Descrição do erro ocorrido"
    """
    try:
        veiculo = db_session().execute(select(Veiculo).where(Veiculo.id == id)).scalar_one_or_none()
        if not veiculo:
            return jsonify({'mensagem': 'Veículo não encontrado'}), 404
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
    """
    API para deletar um veículo.

    ## Endpoint:
        /veiculos

    ### Sucesso (200 OK):
    '''json

    ### Erros Possíveis:
        - **Veículo não encontrado**
        - **Erro Interno do Servidor**
    """
    try:
        veiculo = db_session().execute(select(Veiculo).where(Veiculo.id == id)).scalar_one_or_none()
        if not veiculo:
            return jsonify({'mensagem': 'Veículo não encontrado'}), 404

        db_session().delete(veiculo)
        db_session().commit()
        return jsonify({'mensagem': 'Veículo deletado com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)})


#ORDENS DE SERVIÇO
@app.route('/ordens', methods=['GET'])
def listar_ordens():
    """
    API para listar todas as ordens de serviço.

    ## Endpoint:
        /ordens

    ### Sucesso:
    '''json

        "ordens":
                "id": 1,
                "veiculo_id": 10,
                "descricao": "Troca de óleo",
                "data_abertura": "2024-05-20",
                "status": "aberta"

    ### Erros Possíveis:
            "error": "Descrição do erro ocorrido"
    """
    try:
        ordens = select(OrdemServico)
        result = db_session().execute(ordens).scalars().all()
        listar_ordens = [ordem.serialize() for ordem in result]
        return jsonify({'ordens': listar_ordens})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/ordens', methods=['POST'])
def criar_ordem():
    """
    API para criar uma ordem de servico

    ## Endpoint:
        /ordens

    ## Requisições (POST):
        - **Campos (JSON):**
            - "veiculo_id"
            - "data_abertura"
            - "descricao_servico"
            - "status"
            - "valor_estimado"

    ### Sucesso:
    '''json

    ### Erros Possíveis:
            "error": "Descrição do erro ocorrido"

    """
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
    """
    API para buscar uma ordem de serviço específica pelo ID.

    ## Endpoint:
        /ordens

    ## Métodos:
        - **GET**: Volta os dados de uma ordem de serviço.

    ### Sucesso:
    '''json

    ### Erros Possíveis:
            "mensagem": "Ordem de serviço não encontrada"
            "error": "Descrição do erro ocorrido"
    """
    try:
        ordem = db_session().execute(select(OrdemServico).where(OrdemServico.id == id)).scalar_one_or_none()
        if ordem:
            return jsonify(ordem.serialize())
        return jsonify({'mensagem': 'Ordem de serviço não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/ordens/<int:id>', methods=['PUT'])
def atualizar_ordem(id):
    """
    API para atualizar os dados de uma ordem de serviço existente.

    ## Endpoint:
        /ordens

    ## Requisições (PUT):
        - **Campos (JSON):**
            - "veiculo_id"
            - "data_abertura"
            - "descricao_servico"
            - "status"
            - "valor_estimado"

    ### Sucesso:
    '''json

    ### Erros Possíveis:
        '''json
            "mensagem": "Ordem de serviço não encontrada"
            "error": "Descrição do erro ocorrido"

    """
    try:
        ordem = db_session().execute(select(OrdemServico).where(OrdemServico.id == id)).scalar_one_or_none()
        if not ordem:
            return jsonify({'mensagem': 'Ordem de serviço não encontrada'}), 404

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
    """
    API para deletar uma ordem de serviço.

    ## Endpoint:
        /ordens

    ## Respostas (JSON):
        "mensagem": "Ordem de serviço deletada com sucesso!"

    ### Erros Possíveis:
            "mensagem": "Ordem de serviço não encontrada"
            "error": "Descrição do erro ocorrido"
    """
    try:
        ordem = db_session().execute(select(OrdemServico).where(OrdemServico.id == id)).scalar_one_or_none()
        if not ordem:
            return jsonify({'message': 'Ordem de serviço não encontrada'}), 404

        db_session().delete(ordem)
        db_session().commit()
        return jsonify({'mensagem': 'Ordem de serviço deletada com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)


# POST recebe a informação
# GET mostra
# PUT atualiza