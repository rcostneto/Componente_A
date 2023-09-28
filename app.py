import json
from urllib import response
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from numpy import indices
import requests
import pprint
import pandas
from sqlalchemy.exc import IntegrityError

from model import Session, Usuario, Veiculo, Peca
from logger import logger
from schemas import *
from flask_cors import CORS



info = Info(title="Principal_A", version="1.0.1")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
usuario_tag = Tag(name="Usuario", description="Adicao, visualizacao e remoção de usuarios a base de dados")
veiculo_tag = Tag(name="Veiculo", description="Adicao, visualizacao e remoção de veículos a base de dados")
peca_tag = Tag(name="Peca", description="Adicao, visualizacao e remoção de peças a base de dados")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/usuario', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_usuario(form: UsuarioSchema):
    """Adiciona um novo Usuario à base de dados

    Retorna uma representação dos usuarios.
    """
    usuario = Usuario(
        nome = form.nome,
        sobrenome = form.sobrenome,
        cpf = form.cpf,
        data_nascimento = form.data_nascimento,
        email = form.email,
        veiculo = form.veiculo,
        placa = form.placa)
    logger.debug(f"Adicionando usuario de nome: '{usuario.nome}'")
    try:
        # criando conexão com o banco
        session = Session()
        # adicionando usuario
        session.add(usuario)
        # efetivando o comando de adição de novo usuario na tabela
        session.commit()
        logger.debug(f"Adicionado usuario de nome: '{usuario.nome}'")
        return apresenta_usuario(usuario), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Esse usuário ja existe no banco :/"
        logger.warning(f"Erro ao adicionar usuario '{usuario.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "O usuário não foi salvo no banco :/"
        logger.warning(f"Erro ao adicionar usuario '{usuario.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    

@app.delete('/usuario', tags=[usuario_tag],
            responses={"200": UsuarioDelSchema, "404": ErrorSchema})
def del_usuario(query: UsuarioBuscaSchema):
    """Deleta um Usuario a partir do nome informado

    Retorna uma mensagem de confirmação da remoção.
    """
    usuario_nome = unquote(unquote(query.nome))
    print(usuario_nome)
    logger.debug(f"Deletando dados sobre usuario #{usuario_nome}")
    # criando conexão com o banco
    session = Session()
    # fazendo a remoção
    count = session.query(Usuario).filter(Usuario.nome == usuario_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado usuario #{usuario_nome}")
        return {"mesage": "Usuario foi removido", "id": usuario_nome}
    else:
        # se o fornecedor não foi encontrado
        error_msg = "Usuario não foi encontrado no banco :/"
        logger.warning(f"Erro ao deletar o usuario #'{usuario_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    

@app.get('/usuario', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def get_usuarios(query: UsuarioBuscaSchema):
    """Faz a busca por um Usuario a partir do seu nome.

    Retorna uma representação dos usuarios.
    """
    usuario_nome = query.nome
    logger.debug(f"Coletando dados sobre usuario #{usuario_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuario = session.query(Usuario).filter(Usuario.nome == usuario_nome).first()

    if not usuario:
        # se o fornecedor não foi encontrado
        error_msg = "Usuario não localizado no banco :/"
        logger.warning(f"Erro ao buscar o usuario '{usuario_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Usuarios encontrados: '{usuario.nome}'")
        # retorna a representação de fornecedor
        return apresenta_usuario(usuario), 200
    

@app.get('/usuarios', tags=[usuario_tag],
         responses={"200": ListagemUsuariosSchema, "404": ErrorSchema})
def get_usuario():
    """Faz a busca por todos os Usuarios cadastrados no banco de dados.

    Retorna uma representação da lista de usuarios.
    """
    
    logger.debug(f"Coletando usuarios ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuarios = session.query(Usuario).order_by(Usuario.nome.asc()).all()

    if not usuarios:
        # se não há usuarios cadastrados
        return {"usuarios": []}, 200
    else:
        logger.debug(f"%d Usuarios encontrados" % len(usuarios))
        # retorna a representação do usuário
        print(usuarios)
        return apresenta_usuarios(usuarios), 200
    

@app.get('/usuarioTopCar', tags=[usuario_tag],
         responses={"200": ListagemUsuariosSchema, "404": ErrorSchema})
def get_topcar():     
    """Faz a busca por todas os usuarios pertencentes a empresa na API externa(TopCar_d.)

    Retorna uma representação da lista de usuarios.
    """

    headers = {
    "accept": "application/json"
    }

    # fazendo uma requisição get a API externa com peças cadastradas
    request = requests.get("http://peca-usuario:7000/usuariotopcar", headers=headers)
    d = request.json()
    # http://peca:8000/pecasapi
    # http://127.0.0.1:8000/pecasapi
    # imprime de forma organizada os dados
    pprint.pprint(d)

    # Recurso do Pandas que estrutura os dados em tabela 
    tabelas = pandas.DataFrame(d['usuarios'])
    print(tabelas)

    if __name__ == '__main__':
        get_topcar()
    
    # se status_code ok
    if request.status_code == 200:

        # posição dos dados que serão armazenados
        indice1 = 0
        indice2 = 1
        indice3 = 2
        indice4 = 3
        indice5 = 4
        indice6 = 5
        indice7 = 6
        indice8 = 7
        indice9 = 8
        indice10 = 9
        indice11 = 10
        indice12 = 11
    
       
        # variável de identificação e inclusão dos dados  
        nome1 = d['usuarios'][indice1]['nome']
        sobrenome1 = d['usuarios'][indice1]['sobrenome']
        cpf1 = d['usuarios'][indice1]['cpf']
        data_nascimento1 = d['usuarios'][indice1]['data_nascimento']
        email1 = d['usuarios'][indice1]['email']
        veiculo1 = d['usuarios'][indice1]['veiculo']
        placa1 = d['usuarios'][indice1]['placa']
            
        top1 = Usuario(
            nome=nome1,
            sobrenome=sobrenome1,
            cpf=cpf1,
            data_nascimento=data_nascimento1,
            email=email1,
            veiculo=veiculo1,
            placa=placa1,
            )
        
        nome2 = d['usuarios'][indice2]['nome']
        sobrenome2 = d['usuarios'][indice2]['sobrenome']
        cpf2 = d['usuarios'][indice2]['cpf']
        data_nascimento2 = d['usuarios'][indice2]['data_nascimento']
        email2 = d['usuarios'][indice2]['email']
        veiculo2 = d['usuarios'][indice2]['veiculo']
        placa2 = d['usuarios'][indice2]['placa']
            
        top2 = Usuario(
            nome=nome2,
            sobrenome=sobrenome2,
            cpf=cpf2,
            data_nascimento=data_nascimento2,
            email=email2,
            veiculo=veiculo2,
            placa=placa2,
            )
        
        nome3 = d['usuarios'][indice3]['nome']
        sobrenome3 = d['usuarios'][indice3]['sobrenome']
        cpf3 = d['usuarios'][indice3]['cpf']
        data_nascimento3 = d['usuarios'][indice3]['data_nascimento']
        email3 = d['usuarios'][indice3]['email']
        veiculo3 = d['usuarios'][indice3]['veiculo']
        placa3 = d['usuarios'][indice3]['placa']
            
        top3 = Usuario(
            nome=nome3,
            sobrenome=sobrenome3,
            cpf=cpf3,
            data_nascimento=data_nascimento3,
            email=email3,
            veiculo=veiculo3,
            placa=placa3,
            )
        
        nome4 = d['usuarios'][indice4]['nome']
        sobrenome4 = d['usuarios'][indice4]['sobrenome']
        cpf4 = d['usuarios'][indice4]['cpf']
        data_nascimento4 = d['usuarios'][indice4]['data_nascimento']
        email4 = d['usuarios'][indice4]['email']
        veiculo4 = d['usuarios'][indice4]['veiculo']
        placa4 = d['usuarios'][indice4]['placa']
            
        top4 = Usuario(
            nome=nome4,
            sobrenome=sobrenome4,
            cpf=cpf4,
            data_nascimento=data_nascimento4,
            email=email4,
            veiculo=veiculo4,
            placa=placa4,
            )
        
        nome5 = d['usuarios'][indice5]['nome']
        sobrenome5 = d['usuarios'][indice5]['sobrenome']
        cpf5 = d['usuarios'][indice5]['cpf']
        data_nascimento5 = d['usuarios'][indice5]['data_nascimento']
        email5 = d['usuarios'][indice5]['email']
        veiculo5 = d['usuarios'][indice5]['veiculo']
        placa5 = d['usuarios'][indice5]['placa']
            
        top5 = Usuario(
            nome=nome5,
            sobrenome=sobrenome5,
            cpf=cpf5,
            data_nascimento=data_nascimento5,
            email=email5,
            veiculo=veiculo5,
            placa=placa5,
            )
        
        nome6 = d['usuarios'][indice6]['nome']
        sobrenome6 = d['usuarios'][indice6]['sobrenome']
        cpf6 = d['usuarios'][indice6]['cpf']
        data_nascimento6 = d['usuarios'][indice6]['data_nascimento']
        email6 = d['usuarios'][indice6]['email']
        veiculo6 = d['usuarios'][indice6]['veiculo']
        placa6 = d['usuarios'][indice6]['placa']
            
        top6 = Usuario(
            nome=nome6,
            sobrenome=sobrenome6,
            cpf=cpf6,
            data_nascimento=data_nascimento6,
            email=email6,
            veiculo=veiculo6,
            placa=placa6,
            )
        
        nome7 = d['usuarios'][indice7]['nome']
        sobrenome7 = d['usuarios'][indice7]['sobrenome']
        cpf7 = d['usuarios'][indice7]['cpf']
        data_nascimento7 = d['usuarios'][indice7]['data_nascimento']
        email7 = d['usuarios'][indice7]['email']
        veiculo7 = d['usuarios'][indice7]['veiculo']
        placa7 = d['usuarios'][indice7]['placa']
            
        top7 = Usuario(
            nome=nome7,
            sobrenome=sobrenome7,
            cpf=cpf7,
            data_nascimento=data_nascimento7,
            email=email7,
            veiculo=veiculo7,
            placa=placa7,
            )
        
        nome8 = d['usuarios'][indice8]['nome']
        sobrenome8 = d['usuarios'][indice8]['sobrenome']
        cpf8 = d['usuarios'][indice8]['cpf']
        data_nascimento8 = d['usuarios'][indice8]['data_nascimento']
        email8 = d['usuarios'][indice8]['email']
        veiculo8 = d['usuarios'][indice8]['veiculo']
        placa8 = d['usuarios'][indice8]['placa']
            
        top8 = Usuario(
            nome=nome8,
            sobrenome=sobrenome8,
            cpf=cpf8,
            data_nascimento=data_nascimento8,
            email=email8,
            veiculo=veiculo8,
            placa=placa8,
            )
        
        nome9 = d['usuarios'][indice9]['nome']
        sobrenome9 = d['usuarios'][indice9]['sobrenome']
        cpf9 = d['usuarios'][indice9]['cpf']
        data_nascimento9 = d['usuarios'][indice9]['data_nascimento']
        email9 = d['usuarios'][indice9]['email']
        veiculo9 = d['usuarios'][indice9]['veiculo']
        placa9 = d['usuarios'][indice9]['placa']
            
        top9 = Usuario(
            nome=nome9,
            sobrenome=sobrenome9,
            cpf=cpf9,
            data_nascimento=data_nascimento9,
            email=email9,
            veiculo=veiculo9,
            placa=placa9,
            )
        
        nome10 = d['usuarios'][indice10]['nome']
        sobrenome10 = d['usuarios'][indice10]['sobrenome']
        cpf10 = d['usuarios'][indice10]['cpf']
        data_nascimento10 = d['usuarios'][indice10]['data_nascimento']
        email10 = d['usuarios'][indice10]['email']
        veiculo10 = d['usuarios'][indice10]['veiculo']
        placa10 = d['usuarios'][indice10]['placa']
            
        top10 = Usuario(
            nome=nome10,
            sobrenome=sobrenome10,
            cpf=cpf10,
            data_nascimento=data_nascimento10,
            email=email10,
            veiculo=veiculo10,
            placa=placa10,
            )
        
        nome11 = d['usuarios'][indice11]['nome']
        sobrenome11 = d['usuarios'][indice11]['sobrenome']
        cpf11 = d['usuarios'][indice11]['cpf']
        data_nascimento11 = d['usuarios'][indice11]['data_nascimento']
        email11 = d['usuarios'][indice11]['email']
        veiculo11 = d['usuarios'][indice11]['veiculo']
        placa11 = d['usuarios'][indice11]['placa']
            
        top11 = Usuario(
            nome=nome11,
            sobrenome=sobrenome11,
            cpf=cpf11,
            data_nascimento=data_nascimento11,
            email=email11,
            veiculo=veiculo11,
            placa=placa11,
            )
        
        nome12 = d['usuarios'][indice12]['nome']
        sobrenome12 = d['usuarios'][indice12]['sobrenome']
        cpf12 = d['usuarios'][indice12]['cpf']
        data_nascimento12 = d['usuarios'][indice12]['data_nascimento']
        email12 = d['usuarios'][indice12]['email']
        veiculo12 = d['usuarios'][indice12]['veiculo']
        placa12 = d['usuarios'][indice12]['placa']
            
        top12 = Usuario(
            nome=nome12,
            sobrenome=sobrenome12,
            cpf=cpf12,
            data_nascimento=data_nascimento12,
            email=email12,
            veiculo=veiculo12,
            placa=placa12,
            )
        
        
        # criando conexão com a base
        session = Session()

        # adicionando as Peças
        session.add(top1)
        session.add(top2)
        session.add(top3)
        session.add(top4)
        session.add(top5)
        session.add(top6)
        session.add(top7)
        session.add(top8)
        session.add(top9)
        session.add(top10)
        session.add(top11)
        session.add(top12)

        # efetivando o camando de adição de nova peça na tabela
        session.commit()
 
        logger.debug(f"Informações da API externa(TopCar_d) adicionada na base de dados: '{Usuario.id}'")

        # fazendo leitura do dado em json e imprimindo
        print(request.json())
        print(request.text)
        print(request.status_code)
        print(request.content)

        print('------------------------------------------------------------------')
        print('Requisição feita com sucesso e dados de usuarios salvo no banco')
        print('------------------------------------------------------------------')
    else:
        print('Não foi possível se conectar com a API externa(TopCar_d).')
    
    logger.debug(f"Coletando usuarios")

    # criando conexão com a base
    session = Session()
    topcar = session.query(Usuario).order_by(Usuario.nome.asc()).all()
    
    if not topcar:
        # se não há usuarios cadastrados
        return {"usuarios": []}, 200
    else:
        logger.debug(f"%d usuarios encontradas" % len(topcar))
        # retorna a representação do usuario
        print(topcar)
        return apresenta_usuarios(topcar), 200


@app.post('/veiculo', tags=[veiculo_tag],
          responses={"200": VeiculoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_veiculo(form: VeiculoSchema):
    """Adiciona um novo veículo à base de dados

    Retorna uma representação dos veículos.
    """
    
    veiculo = Veiculo(
        nome_veiculo = form.nome_veiculo,
        modelo = form.modelo,
        placa = form.placa)
    logger.debug(f"Adicionando veículo de nome: '{veiculo.nome_veiculo}'")
    try:
        # criando conexão com o banco
        session = Session()
        # adicionando veículo
        session.add(veiculo)
        # efetivando o comando de adição de novo veículo na tabela
        session.commit()
        logger.debug(f"Adicionado veículo de nome: '{veiculo.nome_veiculo}'")
        return apresenta_veiculo(veiculo), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Esse veículo ja existe no banco :/"
        logger.warning(f"Erro ao adicionar veículo '{veiculo.nome_veiculo}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "O veículo não foi salvo no banco :/"
        logger.warning(f"Erro ao adicionar veículo '{veiculo.nome_veiculo}', {error_msg}")
        return {"mesage": error_msg}, 400
    
@app.get('/veiculosapi', tags=[veiculo_tag],
         responses={"200": ListagemVeiculoSchema, "404": ErrorSchema})
def get_veiculo():     
    """Faz a busca por todos os veículos cadastrados na API externa (Componente_B).

    Retorna uma representação da lista de veículos.
    """

    headers = {
    "accept": "application/json",
    "cobli-api-key": "WKNPnuj.67557cb1-0ed7-4b39-8999-8bcc798fc69c"
    }

    # fazendo uma requisição get a API externa com veículos cadastrados
    request = requests.get("https://api.cobli.co/public/v1/vehicles?limit=2000&page=1", headers=headers)
    d = request.json()
    # imprime de forma organizada os dados
    pprint.pprint(d)

    # Recurso do Pandas que estrutura os dados em tabela 
    tabela = pandas.DataFrame(d['data'])
    print(tabela)

    if __name__ == '__main__':
        get_veiculo()
    
    # se status_code ok
    if request.status_code == 200:

        # posição dos dados
        indice1 = 0
        indice2 = 1 
        indice3 = 2
        indice4 = 3
        indice5 = 4
        indice6 = 5
        indice7 = 6
        indice8 = 7
        indice9 = 8
        indice10 = 9
        indice11 = 10
        indice12 = 11
           
        # variável de identificação e inclusão dos dados   
        marca = d['data'][indice1]['brand']
        modelo = d['data'][indice1]['model']
        placa = d['data'][indice1]['license_plate']
        
        veiculo1 = Veiculo(
            nome_veiculo=marca,
            modelo=modelo,
            placa=placa,
            )

        marca = d['data'][indice2]['brand']
        modelo = d['data'][indice2]['model']
        placa = d['data'][indice2]['license_plate']

        veiculo2 = Veiculo(
            nome_veiculo=marca,
            modelo=modelo,
            placa=placa,
            )
        
        marca = d['data'][indice3]['brand']
        modelo = d['data'][indice3]['model']
        placa = d['data'][indice3]['license_plate']
            
        veiculo3 = Veiculo(
            nome_veiculo=marca,
            modelo=modelo,
            placa=placa,
            )

        marca = d['data'][indice4]['brand']
        modelo = d['data'][indice4]['model']
        placa = d['data'][indice4]['license_plate']

        veiculo4 = Veiculo(
            nome_veiculo=marca,
            modelo=modelo,
            placa=placa,
            )
        
        marca = d['data'][indice5]['brand']
        modelo = d['data'][indice5]['model']
        placa = d['data'][indice5]['license_plate']

        veiculo5 = Veiculo(
            nome_veiculo=marca,
            modelo=modelo,
            placa=placa,
            )
        
        marca = d['data'][indice6]['brand']
        modelo = d['data'][indice6]['model']
        placa = d['data'][indice6]['license_plate']
            
        veiculo6 = Veiculo(
            nome_veiculo=marca,
            modelo=modelo,
            placa=placa,
            )

        marca = d['data'][indice7]['brand']
        modelo = d['data'][indice7]['model']
        placa = d['data'][indice7]['license_plate']

        veiculo7 = Veiculo(
            nome_veiculo=marca,
            modelo=modelo,
            placa=placa,
            )
        
        marca = d['data'][indice8]['brand']
        modelo = d['data'][indice8]['model']
        placa = d['data'][indice8]['license_plate']

        veiculo8 = Veiculo(
            nome_veiculo=marca,
            modelo=modelo,
            placa=placa,
            )
        
        marca = d['data'][indice9]['brand']
        modelo = d['data'][indice9]['model']
        placa = d['data'][indice9]['license_plate']
            
        veiculo9 = Veiculo(
            nome_veiculo=marca,
            modelo=modelo,
            placa=placa,
            )

        marca = d['data'][indice10]['brand']
        modelo = d['data'][indice10]['model']
        placa = d['data'][indice10]['license_plate']

        veiculo10 = Veiculo(
            nome_veiculo=marca,
            modelo=modelo,
            placa=placa,
            )
        
        marca = d['data'][indice11]['brand']
        modelo = d['data'][indice11]['model']
        placa = d['data'][indice11]['license_plate']
            
        veiculo11 = Veiculo(
            nome_veiculo=marca,
            modelo=modelo,
            placa=placa,
            )

        marca = d['data'][indice12]['brand']
        modelo = d['data'][indice12]['model']
        placa = d['data'][indice12]['license_plate']

        veiculo12 = Veiculo(
            nome_veiculo=marca,
            modelo=modelo,
            placa=placa,
            )
        
        
        # criando conexão com a base
        session = Session()

        # adicionando dados de veículos
        session.add(veiculo1)
        session.add(veiculo2)
        session.add(veiculo3)
        session.add(veiculo4)
        session.add(veiculo5)
        session.add(veiculo6)
        session.add(veiculo7)
        session.add(veiculo8)
        session.add(veiculo9)
        session.add(veiculo10)
        session.add(veiculo11)
        session.add(veiculo12)

        # efetivando o comando de adição de novo veículo na tabela
        session.commit()
        
        
        logger.debug(f"Informações da API externa(Componente_B) adicionada na base de dados: '{Veiculo.id}'")

        print('==================================================================')
        print('Requisição feita com sucesso e dados de veículos salvo no banco')
        print('==================================================================')
    else:
        print('Não foi possível se conectar com a API externa(Componente_B).')
    
    logger.debug(f"Coletando veículos ")
    # criando conexão com a base
    session = Session()
    veiculos = session.query(Veiculo).order_by(Veiculo.nome_veiculo.asc()).all()
    

    if not veiculos:
        # se não há veículos cadastrados
        return {"veiculos": []}, 200
    else:
        logger.debug(f"%d veiculos econtrados" % len(veiculos))
        # retorna a representação do veículo
        print(veiculos)
        return apresenta_veiculos(veiculos), 200
    


@app.get('/veiculos', tags=[veiculo_tag],
         responses={"200": ListagemVeiculoSchema, "404": ErrorSchema})
def get_veiculos():     
    """Faz a busca por todos os veículos cadastrados no banco de dados.

    Retorna uma representação da lista de veículos.
    """

    logger.debug(f"Coletando veículos ")
    # criando conexão com a base
    session = Session()
    veiculos = session.query(Veiculo).order_by(Veiculo.nome_veiculo.asc()).all()
    

    if not veiculos:
        # se não há veículos cadastrados
        return {"veiculos": []}, 200
    else:
        logger.debug(f"%d usuarios econtrados" % len(veiculos))
        # retorna a representação do veículo
        print(veiculos)
        return apresenta_veiculos(veiculos), 200
    


@app.put('/updateVeiculo', tags=[veiculo_tag],
          responses={"200": UpdateVeiculoSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_veiculo(form: UpdateVeiculoSchema):
    """Edita um veículo já salvo na base de dados

    Retorna uma representação dos veículos.
    """
    nome_veiculo = form.id
    session = Session()

    try:
        query = session.query(Veiculo).filter(Veiculo.id == nome_veiculo)
        print(query)
        db_veiculo = query.first()
        if not db_veiculo:
            # se veículo não for encontrado
            error_msg = "Veículo não encontrado na base :/"
            logger.warning(f"Erro ao buscar o veículo '{nome_veiculo}', {error_msg}")
            return {"mesage": error_msg}, 404
        else:
            if form.nome_veiculo:
                db_veiculo.nome_veiculo = form.nome_veiculo
            if form.modelo:  
                db_veiculo.modelo = form.modelo
            if form.placa:
                db_veiculo.placa=form.placa
            
            session.add(db_veiculo)
            session.commit()
            logger.debug(f"Editando veículo de id: '{db_veiculo.id}'")
            return apresenta_veiculo(db_veiculo), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo veículo :/"
        logger.warning(f"Erro ao adicionar o veículo '{db_veiculo.id}', {error_msg}")
        return {"mesage": error_msg}, 400
    

@app.delete('/veiculo', tags=[veiculo_tag],
            responses={"200": VeiculoDelSchema, "404": ErrorSchema})
def del_veiculo(query: VeiculoBuscaPorIDSchema):
    """Deleta um veículo a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    veiculo_id = query.id
    logger.info(f"Deletando dados sobre veículo #{veiculo_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Veiculo).filter(Veiculo.id == veiculo_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.info(f"Deletado produto #{veiculo_id}")
        return {"mesage": "Produto removido", "id": veiculo_id}
    else:
        # se o veículo não foi encontrado
        error_msg = "Veículo não encontrado na base :/"
        logger.warning(f"Erro ao deletar o veículo #'{veiculo_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    


@app.get('/pecasapi', tags=[peca_tag],
         responses={"200": ListagemPecaSchema, "404": ErrorSchema})
def get_pecas():     
    """Faz a busca por todas as peças cadastradas na API externa(Componente_C.)

    Retorna uma representação da lista de peças.
    """

    headers = {
    "accept": "application/json"
    }

    # fazendo uma requisição get a API externa com peças cadastradas
    request = requests.get("http://peca:8000/pecasapi", headers=headers)
    d = request.json()
    # http://peca:8000/pecasapi
    # http://127.0.0.1:8000/pecasapi
    # imprime de forma organizada os dados
    pprint.pprint(d)

    # Recurso do Pandas que estrutura os dados em tabela 
    tabelas = pandas.DataFrame(d['pecas'])
    print(tabelas)

    if __name__ == '__main__':
        get_pecas()
    
    # se status_code ok
    if request.status_code == 200:

        # posição dos dados que serão armazenados
        indice1 = 0
        indice2 = 1
        indice3 = 2
        indice4 = 3
        indice5 = 4
        indice6 = 5
        indice7 = 6
        indice8 = 7
        indice9 = 8
        indice10 = 9
        indice11 = 10
        indice12 = 11
    
       
        # variável de identificação e inclusão dos dados  
        nome1 = d['pecas'][indice1]['nome_peca']
        modelo1 = d['pecas'][indice1]['modelo_peca']
        codigo1 = d['pecas'][indice1]['cod_peca']
            
        peca1 = Peca(
            nome_peca=nome1,
            modelo_peca=modelo1,
            cod_peca=codigo1,
            )
        
        nome2 = d['pecas'][indice2]['nome_peca']
        modelo2 = d['pecas'][indice2]['modelo_peca']
        codigo2 = d['pecas'][indice2]['cod_peca']
            
        peca2 = Peca(
            nome_peca=nome2,
            modelo_peca=modelo2,
            cod_peca=codigo2,
            )
        
        nome3 = d['pecas'][indice3]['nome_peca']
        modelo3 = d['pecas'][indice3]['modelo_peca']
        codigo3 = d['pecas'][indice3]['cod_peca']
            
        peca3 = Peca(
            nome_peca=nome3,
            modelo_peca=modelo3,
            cod_peca=codigo3,
            )
        
        nome4 = d['pecas'][indice4]['nome_peca']
        modelo4 = d['pecas'][indice4]['modelo_peca']
        codigo4 = d['pecas'][indice4]['cod_peca']
            
        peca4 = Peca(
            nome_peca=nome4,
            modelo_peca=modelo4,
            cod_peca=codigo4,
            )
        
        nome5 = d['pecas'][indice5]['nome_peca']
        modelo5 = d['pecas'][indice5]['modelo_peca']
        codigo5 = d['pecas'][indice5]['cod_peca']
            
        peca5 = Peca(
            nome_peca=nome5,
            modelo_peca=modelo5,
            cod_peca=codigo5,
            )
        
        nome6 = d['pecas'][indice6]['nome_peca']
        modelo6 = d['pecas'][indice6]['modelo_peca']
        codigo6 = d['pecas'][indice6]['cod_peca']
            
        peca6 = Peca(
            nome_peca=nome6,
            modelo_peca=modelo6,
            cod_peca=codigo6,
            )
        
        nome7 = d['pecas'][indice7]['nome_peca']
        modelo7 = d['pecas'][indice7]['modelo_peca']
        codigo7 = d['pecas'][indice7]['cod_peca']
            
        peca7 = Peca(
            nome_peca=nome7,
            modelo_peca=modelo7,
            cod_peca=codigo7,
            )
        
        nome8 = d['pecas'][indice8]['nome_peca']
        modelo8 = d['pecas'][indice8]['modelo_peca']
        codigo8 = d['pecas'][indice8]['cod_peca']
            
        peca8 = Peca(
            nome_peca=nome8,
            modelo_peca=modelo8,
            cod_peca=codigo8,
            )
        
        nome9 = d['pecas'][indice9]['nome_peca']
        modelo9 = d['pecas'][indice9]['modelo_peca']
        codigo9 = d['pecas'][indice9]['cod_peca']
            
        peca9 = Peca(
            nome_peca=nome9,
            modelo_peca=modelo9,
            cod_peca=codigo9,
           )
        
        nome10 = d['pecas'][indice10]['nome_peca']
        modelo10 = d['pecas'][indice10]['modelo_peca']
        codigo10 = d['pecas'][indice10]['cod_peca']
            
        peca10 = Peca(
            nome_peca=nome10,
            modelo_peca=modelo10,
            cod_peca=codigo10,
            )
        
        nome11 = d['pecas'][indice11]['nome_peca']
        modelo11 = d['pecas'][indice11]['modelo_peca']
        codigo11 = d['pecas'][indice11]['cod_peca']
            
        peca11 = Peca(
            nome_peca=nome11,
            modelo_peca=modelo11,
            cod_peca=codigo11,
            )
        
        nome12 = d['pecas'][indice12]['nome_peca']
        modelo12 = d['pecas'][indice12]['modelo_peca']
        codigo12 = d['pecas'][indice12]['cod_peca']
            
        peca12 = Peca(
            nome_peca=nome12,
            modelo_peca=modelo12,
            cod_peca=codigo12,
            )
        
        
        # criando conexão com a base
        session = Session()

        # adicionando as Peças
        session.add(peca1)
        session.add(peca2)
        session.add(peca3)
        session.add(peca4)
        session.add(peca5)
        session.add(peca6)
        session.add(peca7)
        session.add(peca8)
        session.add(peca9)
        session.add(peca10)
        session.add(peca11)
        session.add(peca12)

        # efetivando o camando de adição de nova peça na tabela
        session.commit()
 
        logger.debug(f"Informações da API externa(Componente_C) adicionada na base de dados: '{Peca.id}'")

        # fazendo leitura do dado em json e imprimindo
        print(request.json())
        print(request.text)
        print(request.status_code)
        print(request.content)

        print('------------------------------------------------------------------')
        print('Requisição feita com sucesso e dados de veículos salvo no banco')
        print('------------------------------------------------------------------')
    else:
        print('Não foi possível se conectar com a API externa(Componente_C).')
    
    logger.debug(f"Coletando peças")

    # criando conexão com a base
    session = Session()
    pecas = session.query(Peca).order_by(Peca.nome_peca.asc()).all()
    
    if not pecas:
        # se não há veiculos cadastrados
        return {"pecas": []}, 200
    else:
        logger.debug(f"%d peças encontradas" % len(pecas))
        # retorna a representação do veiculo
        print(pecas)
        return apresenta_materiais(pecas), 200
    

@app.get('/pecas', tags=[peca_tag],
         responses={"200": ListagemPecaSchema, "404": ErrorSchema})
def get_peca():     
    """Faz a busca por todas as peças cadastradas no banco de dados.

    Retorna uma representação da lista de peças.
    """

    logger.debug(f"Coletando peças")
    # criando conexão com a base
    session = Session()
    peca = session.query(Peca).order_by(Peca.nome_peca.asc()).all()
    

    if not peca:
        # se não há veículos cadastrados
        return {"pecas": []}, 200
    else:
        logger.debug(f"%d peças encontradas" % len(peca))
        # retorna a representação da peça
        print(peca)
        return apresenta_materiais(peca), 200
    

@app.delete('/peca', tags=[peca_tag],
            responses={"200": PecaDelSchema, "404": ErrorSchema})
def del_peca(query: PecaBuscaPorIDSchema):
    """Deleta uma peça a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    peca_id = query.id
    logger.info(f"Deletando dados sobre a peça #{peca_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Peca).filter(Peca.id == peca_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.info(f"Deletado peça #{peca_id}")
        return {"mesage": "Peça removida", "id": peca_id}
    else:
        # se a peça não for encontradada
        error_msg = "Peça não encontrada na base :/"
        logger.warning(f"Erro ao deletar a peça #'{peca_id}', {error_msg}")
        return {"mesage": error_msg}, 404
