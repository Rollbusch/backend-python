import mysql.connector
from mysql.connector import Error

class DatabaseConnection():
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user 
        self.password = password
    
    def start_connection(self):
        try:
            self.connection = mysql.connector.connect(host=self.host,
                                                database=self.database,
                                                user=self.user,
                                                password=self.password)
            db_Info = self.connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
        except Error as e:
            print("Error while connecting to MySQL", e)

    def config_connection(self):
        self.connection.execute('set max_allowed_packet=67108864')

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")
        else: 
            print("MySQL connection is already closed")
    
    def reconnect(self):
        print('#' * 20)
        print(self.connection.is_connected)
        if (not self.connection.is_connected):
            return self.connection.reconnect()
            
    def selectAll(self): 
        self.reconnect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute('SELECT id_pessoa, nome, data_admissao FROM pessoas')
        return cursor.fetchall()
   
    def select(self, id): 
        self.reconnect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f'SELECT * FROM pessoas WHERE id_pessoa = {id}')
        return cursor.fetchall()
    
    def update(self, id, values):
        self.reconnect()
        cursor = self.connection.cursor()
        print(f"""UPDATE `pessoas` SET {values} WHERE `pessoas`.`id_pessoa`='{id}'""")
        cursor.execute(f"""UPDATE `pessoas` SET {values} WHERE `pessoas`.`id_pessoa` = {id}""")
        return self.connection.commit()
    
    def create(self, values):
        self.reconnect()
        cursor = self.connection.cursor()
        cursor.execute(f'INSERT INTO pessoas (nome, rg, cpf, data_nascimento, data_admissao, funcao) VALUES ({values})')
        return self.connection.commit()
    
    def delete(self, id):
        self.reconnect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f'DELETE FROM pessoas WHERE id_pessoa = {id}')
        return self.connection.commit()