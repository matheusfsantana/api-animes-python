from flask import Flask, Response, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{USER}:{SENHA}@{ADDRESS}/{NOMEDOBANCO}'

db = SQLAlchemy(app)


class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    epAtual = db.Column(db.Integer)
    epTotal = db.Column(db.Integer)
    urlImagem = db.Column(db.String(255))
    status = db.Column(db.String(20)) #assistindo/completo/à assistir



    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'epAtual': self.epAtual,
            'epTotal': self.epTotal,
            'urlImagem': self.urlImagem,
            'status': self.status
            }

    def __init__(self,nome,epAtual,epTotal,urlImagem):
        self.nome = nome
        self.epAtual = epAtual
        self.epTotal = epTotal
        self.urlImagem = urlImagem

        if(epAtual == epTotal):
            self.status = "Completed"
        elif(epAtual == 0):
            self.status = "Plan to watch"
        else:
            self.status = "Watching"



@app.route('/')
def hello_world():
    return 'Hello from Flask is working!'

@app.route('/animes', methods=['GET'])
def buscarTodos():
    anime = db.session.query(Anime).all()
    anime_json = json.dumps([a.to_json() for a in anime])
    return anime_json

@app.route('/buscar/<id>', methods=['GET'])
def buscarAnimes(id):
    anime = Anime.query.get(id)
    anime_json = anime.to_json();
    return anime_json;


@app.route('/inserirAnime', methods=['POST'])
def inserirAnime():
    body = request.get_json()

    try:
        novo_anime = Anime(nome=body["nome"],
                         epAtual=body["epAtual"],
                         epTotal=body["epTotal"],
                         urlImagem=body["urlImagem"]
                         )

        db.session.add(novo_anime)

        db.session.commit()

        return Response()

    except Exception as e:
        db.session.rollback()
        print(e)
        return "Deu algum erro"
    finally:
        db.session.close()

@app.route('/editar/<id>', methods=['PUT'])
def editarAnime(id):
    anime = Anime.query.get(id)
    body = request.get_json()

    try:
        anime.epAtual=body["epAtual"],
        anime.epTotal=body["epTotal"]

        if(anime.epAtual == anime.epTotal):
            anime.status = "Completed"
        elif(anime.epAtual == 0):
            anime.status = "Plan to watch"
        else:
            anime.status = "Watching"


        db.session.commit()
        return Response()

    except Exception as e:
        db.session.rollback()
        print(e)
        return "Deu algum erro"
    finally:
        db.session.close()

@app.route('/excluir/<id>')
def excluirAnime(id):
    anime = Anime.query.get(id)

    try:
      db.session.delete(anime)
      db.session.commit()
      return Response()

    except Exception as e:
      db.session.rollback()
      print(e)
      return "Deu algum erro"
    finally:
      db.session.close()