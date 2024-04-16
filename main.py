from flask import Flask, jsonify, request
import mysql.connector
import random

app = Flask(__name__)

# Conexão com o banco de dados
svdb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1106",
    database="stardewdb"
)

# Cursor para executar consultas SQL
mycursor = svdb.cursor()

# Consulta SQL para selecionar uma linha aleatória
def get_random_collectible():
    mycursor.execute("SELECT * FROM coletaveis ORDER BY RAND() LIMIT 1")
    return mycursor.fetchone()

# Consulta SQL para obter uma dica relacionada ao item colecionável
def get_collectible_hint(collectible_id):
    mycursor.execute("SELECT dica FROM dicas WHERE id_coletavel = %s", (collectible_id,))
    hint = mycursor.fetchone()
    return hint[0] if hint else "Desculpe, nenhuma dica disponível."

# Rota para obter um item colecionável aleatório com dica
@app.route('/get_random_collectible', methods=['GET'])
def get_random_collectible_route():
    collectible = get_random_collectible()
    hint = get_collectible_hint(collectible[0])
    return jsonify({"collectible": collectible, "hint": hint})

# Rota para verificar a resposta do usuário
@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    guess = data['guess'].lower()
    collectible_name = data['collectible_name'].lower()

    if guess == collectible_name:
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "incorrect"})

if __name__ == '__main__':
    app.run(debug=True)
