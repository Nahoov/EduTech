import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import Error

""" 
psycopg2 : biblioteca para integração do python com o postegres
os: 
dotenv: biblioteca que carrega variáveis de ambietne no arquivo .env

"""

def conecta():
    # def para fazer conexão
    try:
        conn = psycopg2.connect(
            user="postgres",
            password="root",
            host="localhost",
            database="database_teste_edu")
    
        print("conectado no postgres com sucesso!!")

        return conn
    
    except Error as e:
        print(f"Ocorreu um erro ao tentar conectar ao banco de dados  {e}")

def encerra_conexao(conn):
    if conn:
        conn.close()
    print("conexao encerrada com sucesso!")

conecta()
