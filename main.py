import sqlite3

def conexao(user_f="defaultdatabase.db", user_c=""):

    try:
        with sqlite3.connect(user_f) as conn:
            cursor = conn.cursor()
            cursor.execute(user_c)
            
            # Se for uma consulta, busca os dados.
            if cursor.description:
                dados = cursor.fetchall()
                return dados if dados else "Nenhum dado encontrado."
            
            # Para INSERT, UPDATE, DELETE, o 'with' faz o commit automaticamente.
            return f"Sucesso: {conn.total_changes} linha(s) alterada(s)."

    except sqlite3.OperationalError as e:    return f"Erro de sintaxe/arquivo: {e}"
    except sqlite3.IntegrityError as e:      return f"Erro de integridade: {e}"
    except Exception as e:                   return f"Erro desconhecido: {e}"