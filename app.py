from database import DatabaseConnection
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from datetime import datetime
from os import getenv
from dotenv import load_dotenv

app = Flask(__name__)  
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# get fields otherwise raise an exception 'Missing `{field}` field'
def get_field(body, field):
    try:
        return body[field]
    except: 
        raise Exception(f'Missing `{field}` field')

def start():
    # load envs from .env file
    load_dotenv()

    def connect_to_db():
        # get envs var from .env file
        host = getenv('DB_HOSTNAME')
        database = getenv('DB_DATABASE')
        user = getenv('DB_USERNAME')
        password = getenv('DB_PASSWORD')

        try:
            connection = DatabaseConnection(host, database, user, password)
            connection.start_connection()
            return connection
        except:
            raise Exception('It was not possible to connect to database.')

    # creating routes /pessoas with methods GET and POST
    @app.route('/api/pessoas', methods=['GET', 'POST'])
    def pessoas():
        if (request.method == 'GET'):
            try:
                connection = connect_to_db()
                result = connection.selectAll()
                response = jsonify(result)
                return response
            except:
                return 'Internal server error', 500
            finally:
                connection.close_connection()
        elif (request.method == 'POST'):
            try:
                connection = connect_to_db()
                body = request.get_json(silent=True)
                nome = get_field(body, 'nome')
                rg = get_field(body, 'rg')
                cpf = get_field(body, 'cpf')
                data_nascimento = get_field(body, 'data_nascimento')
                data_admissao = get_field(body, 'data_admissao')
                result = connection.create(nome, rg, cpf, data_nascimento, data_admissao)
                response = jsonify(result)
                return response
            except Exception as error:
                return str(error), 500
            finally:
                connection.close_connection()

    # creating routes /pessoas/id with methods GET, PUT and DELETE
    @app.route('/api/pessoas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def pessoa_id(id):
        if (request.method == 'GET'):
            try:
                connection = connect_to_db()
                result = connection.select(id)
                response = jsonify(result)
                return response
            except:
                return 'Internal server error', 500
            finally:
                connection.close_connection()
        
        elif (request.method == 'PUT'):
            try:
                connection = connect_to_db()
                body = request.get_json(silent=True)
                nome = get_field(body, 'nome')
                rg = get_field(body, 'rg')
                cpf = get_field(body, 'cpf')
                data_nascimento = get_field(body, 'data_nascimento')
                data_admissao = get_field(body, 'data_admissao')
                result = connection.update(id, nome, rg, cpf, data_nascimento, data_admissao)
                response = jsonify(result)
                return response
            except Exception as error:
                return str(error), 500
            finally:
                connection.close_connection()

        elif (request.method == 'DELETE'):
            try:
                connection = connect_to_db()
                result = connection.delete(id)
                response = jsonify(result)
                return response         
            except:
                return 'Internal server error', 500
            finally:
                connection.close_connection()
          
    app.run()
    

if __name__ == '__main__':
    start()
