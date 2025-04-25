from models import Cliente, Veiculo, OrdemServico, db_session
from sqlalchemy import select


# inserir dados na tabela
def inserir_cliente():
    cliente = Cliente(nome=str(input('nome: ')),
                      endereco=str(input("endereco: ")),
                      telefone=str(input('telefone: ')),
                      cpf=int(input('cpf: ')))
    print(cliente)
    cliente.save()


def consultar_cliente():
    var_cliente = select(Cliente)
    var_cliente = db_session.execute(var_cliente).all()
    print(var_cliente)


def atualizar_cliente():
    # Seleciona o item a ser alterado
    var_cliente = select(Cliente).where(str(input('Nome: ')) == Cliente.nome)
    var_cliente = db_session.execute(var_cliente).scalar()
    # Nova informação
    var_cliente.nome = str(input('Novo Nome: '))
    var_cliente.save()


# remove pessoas
def deletar_cliente():
    cliente_delete = input('Quem você deseja deletar?: ')
    var_cliente = select(Cliente).where(cliente_delete == Cliente.nome)
    var_cliente = db_session.execute(var_cliente).scalar()
    var_cliente.delete()


def inserir_veiculo():
    veiculo = Veiculo(
        cliente_id=int(input('Cliente: ')),
        marca=str(input('Marca: ')),
        modelo=str(input('Modelo: ')),
        placa=str(input('Placa: ')),
        ano_fabricacao=int(input('Ano de fabricacao: ')),
    )
    print(veiculo)
    veiculo.save()


def consultar_veiculo():
    var_veiculo = select(Veiculo)
    var_veiculo = db_session.execute(var_veiculo).all()
    print(var_veiculo)


def atualizar_veiculo():
    # Seleciona o item a ser alterado
    var_veiculo = select(Veiculo).where(str(input('Placa: ')) == Veiculo.placa)
    var_veiculo = db_session.execute(var_veiculo).scalar()
    # Nova informação
    var_veiculo.placa = str(input('Nova placa: '))
    var_veiculo.save()


# remove pessoas
def deletar_veiculo():
    veiculo_delete = input('Qual veiculo você deseja deletar?: ')
    var_veiculo = select(Veiculo).where(veiculo_delete == Veiculo.placa)
    var_veiculo = db_session.execute(var_veiculo).scalar()
    var_veiculo.delete()


def inserir_ordem_servico():
    ordem_servico = OrdemServico(
        veiculo_id=int(input('ID Veiculo: ')),
        data_abertura=str(input('Data abertura: ')),
        descricao_servico=str(input('Descricao servico: ')),
        status=str(input('Status: ')),
        valor_estimado=float(input('Valor estimado: ')),
    )
    print(ordem_servico)
    ordem_servico.save()


def consultar_ordem_servico():
    var_ordem_servico = select(OrdemServico)
    var_ordem_servico = db_session.execute(var_ordem_servico).all()
    print(var_ordem_servico  )


def atualizar_ordem_servico():
    # Seleciona o item a ser alterado
    var_ordem_servico = select(OrdemServico).where(str(input('Atividade: ')) == OrdemServico.nome)
    var_ordem_servico = db_session.execute(var_ordem_servico  ).scalar()
    # Nova informação
    var_ordem_servico.nome = str(input('Nova Atividade: '))
    var_ordem_servico.save()


# remove movimentações
def deletar_ordem_servico():
    ordem_servico_delete = input('Qual emprestimo você deseja deletar?: ')
    var_ordem_servico = select(OrdemServico).where(ordem_servico_delete == OrdemServico.id)
    var_ordem_servico = db_session.execute(var_ordem_servico).scalar()
    var_ordem_servico.delete()


if __name__ == '__main__':

    while True:
        print("--" * 50)
        print("Qual tabela você quer editar? \n 0 - sair \n 1 - cliente \n 2 - veiculo \n 3 - ordem_servico")


        escolha = input("Escolha: ")
        if escolha == "1":
            print("O que você quer fazer na tabela cliente?")
            print("0 - sair")
            print("1 - inserir dados")
            print("2 - atualizar dados")
            print("3 - excluir dados")
            print("4 - consultar dados")

            escolha2 = input("Escolha: ")
            if escolha2 == "1":
                inserir_cliente()
            elif escolha2 == "2":
                atualizar_cliente()
            elif escolha2 == "3":
                deletar_cliente()
            elif escolha2 == "4":
                consultar_cliente()
            elif escolha == "0":
                break

        elif escolha == "2":
            print("O que você quer fazer na tabela veiculo?")
            print("0 - sair")
            print("1 - inserir dados")
            print("2 - atualizar dados")
            print("3 - excluir dados")
            print("4 - consultar dados")

            escolha2 = input("Escolha: ")
            if escolha2 == "1":
                inserir_veiculo()
            elif escolha2 == "2":
                atualizar_veiculo()
            elif escolha2 == "3":
                deletar_veiculo()
            elif escolha2 == "4":
                consultar_veiculo()
            elif escolha == "0":
                break

        elif escolha == "3":
            print("O que você quer fazer na tabela ordem de serviço?")
            print("0 - sair")
            print("1 - inserir dados")
            print("2 - atualizar dados")
            print("3 - excluir dados")
            print("4 - consultar dados")

            escolha2 = input("Escolha: ")
            if escolha2 == "1":
                inserir_ordem_servico()
            elif escolha2 == "2":
                atualizar_ordem_servico()
            elif escolha2 == "3":
                deletar_ordem_servico()
            elif escolha2 == "4":
                consultar_ordem_servico()
            elif escolha == "0":
                break

        elif escolha == "0":
            break

        else:
            print("ERRO")