import tkinter as tk
from tkinter import filedialog
import main as m


# CRIAR A JANELA ======================================
Window = tk.Tk()
Window.geometry("900x700")
Window.config(bg="white")
Window.resizable(False, False)
Window.title("SLQLite Terminal")

# VARIÁVEIS ===========================================
user_file = None
user_command = None
# DEFS GERAIS =========================================
def SelectFile():
    global name_of_file_text, user_file
    user_file = filedialog.askopenfilename(filetypes=(("Bases de resposta_do_banco[0] SQLite", "*.db *.sqlite *.sqlite3 *.s3db"),
                                                      ("Todos os ficheiros", "*.*")))

    if user_file:
        name_of_file_text.config(text= user_file)
    else:
        name_of_file_text.config(text="Nenhum ficheiro selecionado")

def SendCommand(event):
    global user_command, user_file
    user_command = Text_Box.get("1.0", "end").strip() # 1.0 = Primeira linha e coluna / end = final
    response_display.config(state="normal") # Torna editável
    if not user_command or not user_file: # Verifica se ambos os campos estão preenchidos
        resposta = "Tente executar um comando ou escolher um ficheiro."
        response_display.insert("end", f"\n{resposta}\n") # Envia a resposta
        Text_Box.delete("1.0", "end") # Apaga o comando
        response_display.config(state="disabled") # Torna desiditavel
        return "break" # Sai da caixa de texto

    resposta_do_banco = m.conexao(user_file, user_command) # Pede a resposta, True ou Set de listas

    if not isinstance(resposta_do_banco[0], (list, tuple, set)): # Verifica se a resposta não é lista, tupla ou set
        resposta = str(resposta_do_banco[0])
        response_display.insert("end", f"\n{resposta}\n") # Mostra a mensagem de erro ou de sucesso
    
    else:
        larguras = []
        num_colunas = len(next(iter(resposta_do_banco[0])))

        for i in range(num_colunas):
            # Procura o comprimento do maior texto na coluna

            maior_item_teste = max([len(str(linha[i])) for linha in resposta_do_banco[0]])
            larguras.append(maior_item_teste)
        # 3. Imprimir os resposta_do_banco[0] formatados
        
        for linha in resposta_do_banco[0]:
            linha_formatada = ""
            for x, item in enumerate(linha):
                texto = str(item)
                
                # Se o texto for maior que 30, cortamos e pomos "..." 
                # para o utilizador saber que há mais (e pesquisar pelo ID)
                if len(texto) > min(larguras[x], 30):
                    texto = texto[:min(larguras[x], 27)] + "..."
                else:
                    texto += " " * (min((larguras[x]), 30) - len(texto))

                # Alinha à esquerda com base na largura calculada para aquela coluna
                linha_formatada += texto + "  |  "
            
            response_display.insert("end", f"{linha_formatada}\n")
            

    response_display.config(state="disabled")
    Text_Box.delete("1.0", "end")
    return "break"

# CRIAR OS ITENS DA JANELA ============================
def criar_itens_da_tela():
    global Text_Box, setinha, response_display, name_of_file_text
    # Caixa do texto ===
    Text_Box = tk.Text(Window, bg= "white", fg= "black", border= 0, font=("Consolas, 13"))
    setinha = tk.Label(Window, text=">", bg="white", fg="black", font=("Consolas, 13"))
    setinha.place(x= 2, y= 35)
    Text_Box.place(x= 16, y= 35)


    # Botão de selecionar o ficheiro ===
    Select_file_button = tk.Button(Window, command=SelectFile, text="Select file", bg="white")
    Select_file_button.place(x= 2, y= 2)

    # Resposta do SQLite

    frame_resposta = tk.Frame(Window, bg="white")
    frame_resposta.place(x=2, y=240, width=900, height=460)

    # Criar a barra de rolagem (Scrollbar)
    scrollbar_y = tk.Scrollbar(frame_resposta, orient="vertical")
    scrollbar_y.pack(side="left", fill="y")
    
    scrollbar_x = tk.Scrollbar(frame_resposta, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")

    # Criar o widget de texto para a resposta
    # state="disabled" faz com que o usuário não consiga digitar nele
    response_display = tk.Text(frame_resposta, bg="white", fg="black", 
                                font=("Consolas", 10), # Fonte monoespaçada é vital
                                yscrollcommand=scrollbar_y.set, 
                                xscrollcommand=scrollbar_x.set,
                                state="disabled",
                                border=0, 
                                wrap="none")
    response_display.pack(side="left", fill="both", expand=True)

    # Configurar a barra de rolagem para controlar o texto
    scrollbar_y.config(command=response_display.yview)
    scrollbar_x.config(command=response_display.xview)
    # Nome do ficheiro ===
    name_of_file_text = tk.Label(Window, text="", bg="white", fg="black", font=("Consolas, 13"))
    name_of_file_text.place(x=80, y= 4)
criar_itens_da_tela()

Window.bind("<Return>", SendCommand)
Window.mainloop()
