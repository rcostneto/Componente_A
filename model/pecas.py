from sqlalchemy import Column, String, Integer, DateTime
from typing import Union

from  model import Base


class Peca(Base):

    __tablename__ = 'pecas'

    id = Column("pk_cod_pecas", Integer, primary_key=True)
    nome_peca = Column(String(50))
    modelo_peca = Column(String(20))
    cod_peca = Column(String(20))
    
    

    def __init__(self, nome_peca:str, modelo_peca:str, cod_peca:str,
                data_insercao:Union[DateTime, None] = None):
        """
        Cria um Produto

        Arguments:
            nome: nome do produto.
            preco: preço atual do produto
            descricao: descrição do produto fornecida pelo fabricante
            marca: identicação da fabricante
            categoria: categoria atribuída ao produto pela loja
            data_insercao: data de quando o produto foi inserido à base
        """
        self.nome_peca = nome_peca
        self.modelo_peca = modelo_peca
        self.cod_peca = cod_peca
        

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao