from sqlalchemy import Column, String, Integer

from model import Base

class Veiculo(Base):
    __tablename__ = 'veiculo'

    id = Column("pk_veiculo", Integer, primary_key=True)
    nome_veiculo = Column(String(20))
    modelo = Column(String(50))
    placa = Column(String(20))


    def __init__(self, nome_veiculo:str, modelo:str, placa: str):
        """
        Cria um veiculo

        Arguments:
            
            nome_veiculo: Nome do veiculo a ser cadastrado.
            modelo: Identificação do fabricante do veiculo.
            placa: Código de identificação de trânsito do veiculo.
           
        """
        self.nome_veiculo = nome_veiculo
        self.modelo = modelo
        self.placa = placa
        
    