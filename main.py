import sqlite3
from interface import user_command, user_file

def conexao(user_f, user_c):
    dados = None
    try:
        conn = sqlite3.connect(user_f)
        cursor = conn.cursor()
        cursor.execute(str(user_c))
        if user_c.upper().startswith(("INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER", "REPLACE")):
            conn.commit()
        else:
            dados = cursor.fetchall()
        cursor.close()
        conn.close()
    except sqlite3.Error as e: return str(e)
    return e, dados