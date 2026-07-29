import tkinter as tk
from tkinter import filedialog
import conn as c


class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1200x800")
        self.window.title("SQLite Terminal")
        self.window.config(bg="white")

        self.user_file = None
        self.user_command = None

        self._criar_widgets()
        self._criar_binds()

    def run(self):
        self.window.mainloop()

    # ==================================================
    # AÇÕES
    # ==================================================
    def SelectFile(self):
        self.user_file = filedialog.askopenfilename(
            filetypes=(
                ("Bases de dados SQLite", "*.db *.sqlite *.sqlite3 *.s3db"),
                ("Todos os ficheiros", "*.*"),
            )
        )

        if self.user_file:
            self.name_of_file_text.config(text=self.user_file)
        else:
            self.name_of_file_text.config(text="Nenhum ficheiro selecionado")

    def command_or_file(self):
        if not self.user_command:
            self.resposta = "Tente executar um comando primeiro."
            return False
        if not self.user_file:
            self.resposta = "Tente escolher um ficheiro primeiro."
            return False
        
        return True

    def SendCommand(self, event):
        self.user_command = self.text_box.get("1.0", "end").strip()

        self.response_display.config(state="normal")
        self.response_display.tag_add("old", "1.0", "end")

        if self.user_command == "clear":
            self.response_display.delete("1.0", "end")
            self.text_box.delete("1.0", "end")
            self.response_display.config(state="disabled")
            return "break"

        if not self.command_or_file():
            self._inserir(f"\n{self.resposta}\n", "erro")
            self.text_box.delete("1.0", "end")
            self.response_display.config(state="disabled")
            return "break"

        resposta_do_banco = c.conexao(self.user_file, self.user_command)

        if not isinstance(resposta_do_banco[0], (list, tuple, set)):
            resposta = str(resposta_do_banco[0])
            self._inserir(f"\n{resposta}\n", resposta_do_banco[1])
        else:
            larguras = []
            num_colunas = len(next(iter(resposta_do_banco[0])))

            for i in range(num_colunas):
                maior_item_teste = max([len(str(linha[i])) for linha in resposta_do_banco[0]])
                larguras.append(maior_item_teste)

            for linha in resposta_do_banco[0]:
                linha_formatada = ""
                for x, item in enumerate(linha):
                    texto = str(item)
                    if len(texto) > min(larguras[x], 30):
                        texto = texto[:min(larguras[x], 27)] + "..."
                    else:
                        texto += " " * (min(larguras[x], 30) - len(texto))
                    linha_formatada += texto + "  |  "

                self._inserir(f"{linha_formatada}\n", "norm")

        self.response_display.config(state="disabled")
        self.text_box.delete("1.0", "end")
        return "break"


    def _inserir(self, texto, tag):
        """Insere texto e garante que fica só com a tag nova, sem herdar 'old'."""
        inicio = self.response_display.index("end-1c")
        self.response_display.insert("end", texto)
        for t in (self.response_display.tag_names()):
            if t != "sel":
                self.response_display.tag_remove(t, inicio, "end")
        self.response_display.tag_add(tag, inicio, "end")

    # ==================================================
    # CONSTRUÇÃO DA JANELA
    # ==================================================
    def _criar_widgets(self):
        # ---- FRAME DO TOPO: botão + nome do ficheiro ----
        self.top_frame = tk.Frame(self.window, bg="white")
        self.top_frame.pack(side="top", fill="x", padx=8, pady=8)

        self.select_file_button = tk.Button(
            self.top_frame, command=self.SelectFile, text="Select file", bg="white"
        )
        self.select_file_button.pack(side="left")

        self.name_of_file_text = tk.Label(
            self.top_frame, text="Nenhum ficheiro selecionado",
            bg="white", fg="black", font=("Consolas", 13), anchor="w"
        )
        self.name_of_file_text.pack(side="left", padx=10, fill="x", expand=True)

        # ---- FRAME DO COMANDO: seta + caixa de texto ----
        self.command_frame = tk.Frame(self.window, bg="white")
        self.command_frame.pack(side="top", fill="x", padx=8, pady=(0, 8))

        self.setinha = tk.Label(
            self.command_frame, text=">", bg="white", fg="black", font=("Consolas", 13)
        )
        self.setinha.pack(side="left")

        self.text_box = tk.Text(
            self.command_frame, bg="white", fg="black", border=0,
            font=("Consolas", 13), height=2, wrap="word"
        )
        self.text_box.pack(side="left", fill="x", expand=True, padx=(6, 0))

        # ---- FRAME DA RESPOSTA: texto + scrollbars ----
        self.frame_resposta = tk.Frame(self.window, bg="white")
        self.frame_resposta.pack(side="top", fill="both", expand=True, padx=8, pady=(0, 8))

        # grid em vez de pack aqui, para a scrollbar vertical ficar
        # sempre encostada à direita e a horizontal no fundo, sem sobrepor o texto
        self.frame_resposta.grid_rowconfigure(0, weight=1)
        self.frame_resposta.grid_columnconfigure(0, weight=1)

        self.scrollbar_y = tk.Scrollbar(self.frame_resposta, orient="vertical")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.scrollbar_x = tk.Scrollbar(self.frame_resposta, orient="horizontal")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.response_display = tk.Text(
            self.frame_resposta, bg="white", fg="black",
            font=("Consolas", 10),
            yscrollcommand=self.scrollbar_y.set,
            xscrollcommand=self.scrollbar_x.set,
            state="disabled",
            border=0,
            wrap="none",
        )
        self.response_display.grid(row=0, column=0, sticky="nsew")

        self.response_display.tag_config("norm", foreground="black")
        self.response_display.tag_config("erro", foreground="red")
        self.response_display.tag_config("old", foreground="gray")

        self.scrollbar_y.config(command=self.response_display.yview)
        self.scrollbar_x.config(command=self.response_display.xview)

    def _criar_binds(self):
        self.window.bind("<Return>", self.SendCommand)


if __name__ == "__main__":
    app = App()
    app.run()