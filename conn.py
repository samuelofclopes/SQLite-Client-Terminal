import sqlite3

def conexao(user_f, user_c):
    """
    PRIMEIRO VALOR: SET DE LISTAS OU UMA STRING
    SEGUNDO VALOR: VARIAVEL BOOLEANA
       SE O SEGUNDO VALOR FOR:
        TRUE: A PRIMEIRA É UMA STRING
        FALSE: A PRIMEIRA É UM SET DE LISTASS
    """
    try:
        with sqlite3.connect(user_f) as conn:
            cursor = conn.cursor()
            cursor.execute(user_c)
            
            # Se for uma consulta, busca os dados.
            if cursor.description:
                dados = cursor.fetchall()
                if dados:     return dados, "norm"
                else:         return "Nenhum dado encontrado.", "erro"
            
            # Para INSERT, UPDATE, DELETE, o 'with' faz o commit automaticamente.
            return f"Sucesso: {conn.total_changes} linha(s) alterada(s).", "norm"

    except Exception as e: return f"Erro: {e}", "erro" # Exception já vem com o tipo de erro.

