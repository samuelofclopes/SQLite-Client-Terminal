import sqlite3

def conexao(user_f, user_c):
    
    try:
        with sqlite3.connect(user_f) as conn:
            cursor = conn.cursor()
            cursor.execute(user_c)
            
            # Se for uma consulta, busca os dados.
            if cursor.description:
                dados = cursor.fetchall()
                return dados if dados else "Nenhum dado encontrado.", False
            
            # Para INSERT, UPDATE, DELETE, o 'with' faz o commit automaticamente.
            return f"Sucesso: {conn.total_changes} linha(s) alterada(s).", True

    except sqlite3.OperationalError as e:    return f"Erro de sintaxe/arquivo: {e}", True
    except sqlite3.IntegrityError as e:      return f"Erro de integridade: {e}", True
    except Exception as e:                   return f"Erro desconhecido: {e}", True

#RETURNS ===========
# RETORNA SEMPRE UM SET.
#   PRIMEIRO VALOR: SET DE LISTAS OU UMA STRING
#   SEGUNDO VALOR: VARIAVEL BOOLEANA
#   SE O SEGUNDO VALOR FOR:
#       TRUE: A PRIMEIRA É UMA STRING
#       FALSE: A PRIMEIRA É UM SET DE LISTASS