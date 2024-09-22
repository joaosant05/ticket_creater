import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.host = 'ip our localhost'
        self.database = 'schema'
        self.user = 'user'
        self.password = 'password'

    def conectar_banco(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None

    def salvar_dados(self, dados):
        connection = self.conectar_banco()
        if connection is not None:
            try:
                cursor = connection.cursor()
                query = """INSERT INTO relatorios (tier, ambiente, frequencia, usuario, navegador, organizacao, marca, log, como_reproduzir, o_que_acontece, o_que_deveria_acontecer)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, dados)
                connection.commit()
                print("Dados inseridos com sucesso no banco de dados.")
                return cursor.lastrowid
            except Error as e:
                print(f"Erro ao inserir dados no MySQL: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("Conexão ao MySQL encerrada.")
        return None

    def salvar_anexo(self, ticket_id, anexo_blob):
        connection = self.conectar_banco()
        if connection is not None:
            try:
                cursor = connection.cursor()
                query = "INSERT INTO anexos (ticket_id, anexo) VALUES (%s, %s)"
                cursor.execute(query, (ticket_id, anexo_blob))
                connection.commit()
                print("Anexo inserido com sucesso no banco de dados.")
            except Error as e:
                print(f"Erro ao salvar anexo no MySQL: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("Conexão ao MySQL encerrada.")
