from flask import Flask, request, jsonify
from gerador_dados import extrair_dados_aluno, delete_do_banco  # espera que gerador_dados.py esteja na mesma pasta

app = Flask(__name__)


# GET para buscar aluno por id (/get-aluno-id?id=123)
@app.route("/get-aluno-id", methods=["GET"])
def get_aluno_by_id():
    #Pegando o parâmetro da URL
    # .get() = pega um valor sem causar erro se a chave não existir.
    aluno_id = request.args.get("id")
    if not aluno_id:
        return jsonify({"error": "Parâmetro 'id' é obrigatório"}), 400

    aluno = extrair_dados_aluno(aluno_id)
    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404

    return (aluno), 200





# POST para adicionar aluno (recebe JSON)
@app.route("/adicionar-aluno", methods=["POST"])
def adicionar_aluno():
    if not request.is_json:
        return jsonify({"error": "Body deve ser JSON"}), 400

    dados = request.get_json()
    # aqui você faria validações / salvar no BD
    # por enquanto só retornamos o que chegou como prova
    return jsonify({"status": "Aluno adicionado", "dados": dados}), 201





@app.route ("/atualizar-aluno", methods=["PUT"])
def atualizar_aluno(aluno_id):
    # 1. verificar se o corpo da requisição é JSON
    if not request.is_json:
        return jsonify({"error": "Body deve ser JSON"}), 400

    # 2. acessar o corpo JSON enviado
    dados = request.get_json()

    # 3. simular consulta no "banco"
    aluno = {"id": aluno_id, "nome": "Antigo", "idade": 20}

    # 4. validar se o aluno existe
    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404

    # 5. atualizar os campos recebidos
    if "nome" in dados:
        aluno["nome"] = dados["nome"]

    if "idade" in dados:
        aluno["idade"] = dados["idade"]

    # 6. retornar o aluno atualizado
    return jsonify({"status": "Atualizado com sucesso", "aluno": aluno}), 200





@app.route("/deletar-aluno", methods=["DELETE"])
def deletar_aluno():
    aluno_para_deletar = request.args.get("id")

    if aluno_para_deletar is None:
        return jsonify({"error": "Parâmetro 'id' é obrigatório"}), 400
        

    aluno = extrair_dados_aluno(aluno_para_deletar)

    if aluno is None:
        return jsonify ({"error": "Não existe esse aluno para deletar"}), 404

    delete_do_banco(aluno)

    return jsonify ({"message": f"Aluno {aluno} deletado"}), 200


# Execute este bloco APENAS se este arquivo for rodado diretamente.
# Não execute se ele for importado."
if __name__ == "__main__":
    # opção direta para desenvolvimento (não usar em produção)
    app.run(debug=True, host="127.0.0.1", port=8000)



"""
FAST API
Para rodar e visualizar em navegador é preciso usar uvicorn main:app --reload.
e visualizar em navegador
Porém se estiver dentro de uma subpasta chamada "routes" seria routes.main:app
"""

# uvicorn python.controlador:app --reload