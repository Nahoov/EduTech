from conexao_banco import conecta, encerra_conexao
import os

connection = conecta()
cursor = connection.cursor()

# FUNÇÕES PARA EXPORTAR CSV (pois os dados já estão no banco de dados)


def exportar_tabela_copy(table_name: str, output_path: str):

    """
    Exporta a tabela do banco para um CSV local usando COPY TO STDOUT.
    Rápido e eficiente — grava diretamente no arquivo local a partir do servidor.
    """

    with open(output_path, "w", encoding="utf-8") as f:
        sql = f"COPY {table_name} TO STDOUT WITH CSV HEADER DELIMITER ','"

        # copy_expert executa o COPY e escreve no arquivo f (lado cliente)
        
        cursor.copy_expert(sql, f)
    print(f"Export concluída (COPY): {table_name} -> {output_path}")



def exportar_varias_tabelas_copy(tabelas: list, pasta_destino: str = "."):
    """
    Exporta várias tabelas usando COPY TO STDOUT, cada uma em arquivo separado.
    """
    os.makedirs(pasta_destino, exist_ok=True)

    for t in tabelas:
        filename = os.path.join(pasta_destino, f"{t}.csv")
        exportar_tabela_copy(t, filename)



# Lista de tabelas que você quer exportar
tabelas_para_exportar = [
    "alunos",
    "instrutores",
    "cursos",
    "modulos",
    "aulas",
    "matriculas",
    "avaliacoes",
    "progresso_aulas",
    "especialidades",
    "categoria_cursos",
    "instrutor_especialidades"
]

# Chama a função e exporta tudo de uma vez
exportar_varias_tabelas_copy(tabelas_para_exportar, pasta_destino="exports_csv")

encerra_conexao(connection)



