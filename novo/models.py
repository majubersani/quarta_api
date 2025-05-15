from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

engine = create_engine('sqlite:///oficina.db')
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

class Cliente(Base):
        __tablename__ = 'clientes'
        id = Column(Integer, primary_key=True)
        nome = Column(String)
        cpf = Column(String, unique=True)
        telefone = Column(String)
        endereco = Column(String)

        def save(self):
            db_session.add(self)
            db_session.commit()

        def delete(self):
            db_session.delete(self)
            db_session.commit()

        def serialize(self):
            return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "telefone": self.telefone,
            "endereco": self.endereco
            }

class Veiculo(Base):
    __tablename__ = 'veiculos'
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    marca = Column(String)
    modelo = Column(String)
    placa = Column(String, unique=True)
    ano_fabricacao = Column(Integer)
    cliente = relationship("Cliente", backref="veiculos")

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        return {
        "id": self.id,
        "cliente_id": self.cliente_id,
        "marca": self.marca,
        "modelo": self.modelo,
        "placa": self.placa,
        "ano_fabricacao": self.ano_fabricacao
        }

class OrdemServico(Base):
    __tablename__ = 'ordens_servico'
    id = Column(Integer, primary_key=True)
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'))
    data_abertura = Column(Date)
    descricao_servico = Column(String)
    status = Column(String)
    valor_estimado = Column(Float)
    veiculo = relationship("Veiculo", backref="ordens")

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        return {
        "id": self.id,
        "veiculo_id": self.veiculo_id,
        "data_abertura": self.data_abertura.isoformat(),
        "descricao_servico": self.descricao_servico,
        "status": self.status,
        "valor_estimado": self.valor_estimado
        }

def init_db():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()