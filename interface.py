import tkinter as tk
from tkinter import filedialog
import main as m


# CRIAR A JANELA ======================================
Window = tk.Tk()
Window.geometry("800x600")
Window.config(bg="white")
Window.resizable(False, False)
Window.title("SLQLite Terminal")

# VARIAVEIS ===========================================
user_file = ""
user_command = ""
# DEFS ================================================
def SelectFile():
    global name_of_file_text, user_file
    user_file = filedialog.askopenfilename(filetypes=(("Bases de Dados SQLite", "*.db *.sqlite *.sqlite3 *.s3db"),
                                                      ("Todos os ficheiros", "*.*")))
    
    if not user_file.lower().endswith((".db", ".sqlite", ".sqlite3" ,".s3db")):
        user_file = ""
    name_of_file_text.config(text=f"{user_file}")

def SendCommand(event):
    global user_command
    user_command = Text_Box.get("1.0", "end").strip() # 1.0 = Primeira linha e coluna / end = final 
    if user_command != "":
        resposta = m.conexao(user_file, user_command)
        if resposta == True:
            resposta = "Operacão concluida com sucesso!"
        response_display.config(state="normal")
        response_display.delete("1.0", "end")
        response_display.insert("1.0", f"{resposta}")
        response_display.config(state="disabled")
        Text_Box.delete("1.0", "end")
        return "break"
# CRIAR OS ITENS DA JANELA ============================

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
frame_resposta.place(x=2, y=240, width=680, height=340)

# Criar a barra de rolagem (Scrollbar)
scrollbar_y = tk.Scrollbar(frame_resposta)
scrollbar_y.pack(side="left", fill="y")

# Criar o widget de texto para a resposta
# state="disabled" faz com que o usuário não consiga digitar nele
response_display = tk.Text(frame_resposta, bg="white", fg="black", 
                           yscrollcommand=scrollbar_y.set, state="disabled",
                           border=0, wrap="word")
response_display.pack(side="left", fill="both", expand=True)

# Configurar a barra de rolagem para controlar o texto
scrollbar_y.config(command=response_display.yview)

# Nome do ficheiro ===
name_of_file_text = tk.Label(Window, text=f"{user_file}", bg="white", fg="black", font=("Consolas, 13"))
name_of_file_text.place(x=80, y= 4)

Window.bind("<Return>", SendCommand)
Window.mainloop()
