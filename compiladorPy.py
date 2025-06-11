import subprocess                # Importa o módulo para executar comandos do sistema
import tkinter as tk             # Importa o módulo tkinter para interfaces gráficas
from tkinter import filedialog   # Importa o filedialog para abrir janelas de seleção de arquivos
from tkinter import ttk          # Importa o ttk para widgets modernos do tkinter
from tkinter import messagebox   # Importa o messagebox para mostrar diálogos de mensagem
import threading                 # Importa threading para rodar a compilação em paralelo à interface

class CompiladorApp:
    def __init__(self, master):
        self.master = master
        master.title("Compilador Python para Executável")  # Define o título da janela

        # Variáveis para armazenar caminhos
        self.caminho_arquivo = tk.StringVar()              # Variável para o caminho do arquivo .py
        self.caminho_destino = tk.StringVar()              # Variável para o caminho de destino

        # Linha para escolher o arquivo .py
        tk.Label(master, text="Arquivo Python:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_arquivo = tk.Entry(master, textvariable=self.caminho_arquivo, width=40)
        self.entry_arquivo.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(master, text="🔍", command=self.selecionar_arquivo).grid(row=0, column=2, padx=5, pady=5)

        # Linha para escolher o destino
        tk.Label(master, text="Destino do Executável:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_destino = tk.Entry(master, textvariable=self.caminho_destino, width=40)
        self.entry_destino.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(master, text="🔍", command=self.selecionar_destino).grid(row=1, column=2, padx=5, pady=5)

        # Botão de compilar
        self.btn_compilar = tk.Button(master, text="Compilar", command=self.iniciar_compilacao)
        self.btn_compilar.grid(row=2, column=1, pady=10)

        # Barra de progresso
        self.progress = ttk.Progressbar(master, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Caixa de texto para logs
        self.texto_log = tk.Text(master, height=10, width=60)
        self.texto_log.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

    def selecionar_arquivo(self):
        arquivo = filedialog.askopenfilename(
            filetypes=[("Python Files", "*.py")],
            title="Selecione o arquivo Python"
        )
        if arquivo:
            self.caminho_arquivo.set(arquivo)             # Atualiza o caminho do arquivo na caixa de texto

    def selecionar_destino(self):
        pasta = filedialog.askdirectory(
            title="Selecione a pasta de destino"
        )
        if pasta:
            self.caminho_destino.set(pasta)               # Atualiza o caminho de destino na caixa de texto

    def iniciar_compilacao(self):
        # Desabilita o botão para evitar múltiplos cliques
        self.btn_compilar.config(state="disabled")
        self.progress["value"] = 0                        # Reseta a barra de progresso
        self.texto_log.delete(1.0, tk.END)                # Limpa o log
        # Inicia a compilação em uma thread separada para não travar a interface
        threading.Thread(target=self.compilar).start()

    def compilar(self):
        arquivo_py = self.caminho_arquivo.get()
        pasta_destino = self.caminho_destino.get()
        if not arquivo_py or not pasta_destino:
            self.log("Selecione o arquivo e o destino antes de compilar.")
            self.btn_compilar.config(state="normal")
            return

        comando = [
            'pyinstaller',
            '--onefile',
            '--distpath', pasta_destino,
            arquivo_py
        ]
        self.log(f"Compilando: {arquivo_py}")
        self.log(f"Destino: {pasta_destino}")
        self.progress["value"] = 10                       # Atualiza a barra de progresso

        # Executa o comando e captura a saída em tempo real
        processo = subprocess.Popen(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for linha in processo.stdout:
            self.log(linha.strip())                       # Mostra cada linha do log na caixa de texto
            self.progress["value"] += 1                   # Atualiza a barra de progresso (simples)
            self.master.update_idletasks()                # Atualiza a interface

        processo.wait()                                   # Aguarda o término do processo
        self.progress["value"] = 100                      # Barra de progresso completa

        if processo.returncode == 0:
            self.log("Compilação finalizada com sucesso!")
            messagebox.showinfo("Finalizado", "Compilação finalizada com sucesso!")  # Mostra diálogo de sucesso
        else:
            self.log("Erro na compilação.")
            messagebox.showerror("Erro", "Ocorreu um erro durante a compilação.")    # Mostra diálogo de erro

        self.btn_compilar.config(state="normal")          # Reabilita o botão de compilar

    def log(self, mensagem):
        self.texto_log.insert(tk.END, mensagem + "\n")    # Insere mensagem na caixa de texto
        self.texto_log.see(tk.END)                        # Rola para o final

if __name__ == "__main__":                                # Verifica se o script está sendo executado diretamente
    root = tk.Tk()                                        # Cria a janela principal do tkinter
    app = CompiladorApp(root)                             # Cria a aplicação
    root.mainloop()                                       # Inicia o loop principal da interface