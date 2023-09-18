from database import DatabaseConnection
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)  

def start(host, database, user, password):
    connection = DatabaseConnection(host, database, user, password)
    connection.start_connection()
    
    @app.route('/pessoas', methods=['GET', 'POST'])
    def pessoas():
        if (request.method == 'GET'):
            result = connection.selectAll()
            response = jsonify(result)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        elif (request.method == 'POST'):
            body = request.get_json(silent=True)
            nome = body['nome']
            rg = body['rg']
            cpf = body['cpf']
            data_nascimento = body['data_nascimento']
            data_admissao = body['data_admissao']
            result = connection.create(f"""'{nome}', '{rg}', '{cpf}', '{data_nascimento}', '{data_admissao}', ''""")
            response = jsonify(result)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

    @app.route('/pessoas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def pessoa_id(id):
        if (request.method == 'GET'):
            result = connection.select(id)
            response = jsonify(result)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
        elif (request.method == 'PUT'):
            body = request.get_json(silent=True)
            str = """"""
            for key, value in body.items():
                str += f"""`{key}`='{value}',"""
            result = connection.update(id, str[0:str.rfind(',')])
            response = jsonify(result)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

        elif (request.method == 'DELETE'):
            result = connection.delete(id)
            response = jsonify(result)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response           
    
    
    app.run()
    
   
    

if __name__ == '__main__':
    start('jobs.visie.com.br', 'joaorollbusch', 'joaorollbusch', 'am9hb3JvbGxi')
