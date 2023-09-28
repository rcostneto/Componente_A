from pydantic import BaseModel
from typing import Optional, List
from model.pecas import Peca


class PecaSchema(BaseModel):
    """ Define como uma nova peça deve ser inserido e representada
    """
    id: int = 1
    nome_peca: str = "Nome da Peça"
    modelo_peca: str = "Identificação do tipo de peça"
    cod_peca: str = "Identificação da Peça"



class ListagemPecaSchema(BaseModel):
    """ Define como uma listagem de peças será retornada.
    """
    materiais:List[PecaSchema]


class PecaBuscaPorIDSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no ID da mercadoria.
    """
    id: int = 1


def apresenta_materiais(materiais: List[Peca]):
    """ Retorna uma representação da peça seguindo o schema definido em
        ListagemPecaSchema.
    """
    result = []
    for peca in materiais:
        result.append({
            
            "nome_peca": peca.nome_peca,
            "modelo_peca": peca.modelo_peca,
            "cod_peca": peca.cod_peca,
        })

    return {"pecas": result}


class PecaViewSchema(BaseModel):
    """ Define como uma Peça será retornada: Peça.
    """
    id: int = 1
    nome_peca: str = "Nome da Peça"
    modelo_peca: str = "Identificação do tipo de peça"
    cod_peca: str = "Identificação da Peça"


class PecaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int



def apresenta_material(pecas: Peca):
    """ Retorna uma representação da Peça seguindo o schema definido em
        PeçaViewSchema.
    """
    return {
        "id": pecas.id,
        "nome_peca": pecas.nome_peca,
        "modelo_peca": pecas.modelo_peca,
        "cod_peca": pecas.cod_peca,
    }