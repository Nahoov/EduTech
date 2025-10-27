import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import Error

# carrega as variaveis do arquivo .env
load_dotenv()

senha = os.getenv("senha")

""" 
psycopg2: Biblioteca para integração do python com o postegres
os: 
dotenv: Biblioteca que carrega variáveis de ambiente no arquivo .env.

"""

def conecta():
    # def para fazer conexão
    try:
        conn = psycopg2.connect(
            user="postgres",
            password= senha,
            host="localhost",
            port="5432",
            database="dbase_edutech")
    
        print("conectado no postgres com sucesso!!")

        return conn
    
    except Error as e:
        print(f"Ocorreu um erro ao tentar conectar ao banco de dados: {e}")                                                                                                                                             

def encerra_conexao(conn):
    if conn:
        conn.close()
    print("conexao encerrada com sucesso!")


