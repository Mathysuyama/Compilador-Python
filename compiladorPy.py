import subprocess                # Importa o módulo para executar comandos do sistema
import tkinter as tk             # Importa o módulo tkinter para interfaces gráficas
from tkinter import filedialog   # Importa o filedialog para abrir janelas de seleção de arquivos
from tkinter import ttk          # Importa o ttk para widgets modernos do tkinter
from tkinter import messagebox   # Importa o messagebox para mostrar diálogos de mensagem
import threading                 # Importa threading para rodar a compilação em paralelo à interface
import sys                       # Importa sys para acessar informações do sistema operacional
import os                        # Importa os para manipulação de caminhos
import shutil                    # Importa shutil para verificar se pyinstaller está no PATH

class CompiladorApp:
    def __init__(self, master):
        self.master = master
        master.title("Compilador Python para Executável")  # Define o título da janela

        # Frame principal para os controles do compilador
        frame_principal = tk.Frame(master)                 # Cria o frame principal para os controles
        frame_principal.pack(side=tk.LEFT, padx=10, pady=10)  # Posiciona à esquerda

        # Frame lateral para instruções de uso
        frame_ajuda = tk.Frame(master, relief=tk.GROOVE, borderwidth=2)  # Cria o frame de ajuda com borda
        frame_ajuda.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)      # Posiciona à direita do principal

        # Variáveis para armazenar caminhos
        self.caminho_arquivo = tk.StringVar()              # Variável para o caminho do arquivo .py
        self.caminho_destino = tk.StringVar()              # Variável para o caminho de destino

        # Linha para escolher o arquivo .py
        tk.Label(frame_principal, text="Arquivo Python:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_arquivo = tk.Entry(frame_principal, textvariable=self.caminho_arquivo, width=40)
        self.entry_arquivo.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame_principal, text="🔍", command=self.selecionar_arquivo).grid(row=0, column=2, padx=5, pady=5)

        # Linha para escolher o destino
        tk.Label(frame_principal, text="Destino do Executável:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_destino = tk.Entry(frame_principal, textvariable=self.caminho_destino, width=40)
        self.entry_destino.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(frame_principal, text="🔍", command=self.selecionar_destino).grid(row=1, column=2, padx=5, pady=5)

        # Botão de compilar
        self.btn_compilar = tk.Button(frame_principal, text="Compilar", command=self.iniciar_compilacao)
        self.btn_compilar.grid(row=2, column=1, pady=10)

        # Barra de progresso
        self.progress = ttk.Progressbar(frame_principal, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Caixa de texto para logs
        self.texto_log = tk.Text(frame_principal, height=10, width=60)
        self.texto_log.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        # Caixa de instruções de uso no frame lateral
        label_ajuda = tk.Label(frame_ajuda, text="Como utilizar o programa:", font=("Arial", 10, "bold"))
        label_ajuda.pack(pady=(10, 5))
        texto_ajuda = (
            "1. Clique na lupa ao lado de 'Arquivo Python' e selecione o arquivo .py que deseja compilar.\n\n"
            "2. Clique na lupa ao lado de 'Destino do Executável' e escolha a pasta onde o executável será salvo.\n\n"
            "3. Clique em 'Compilar' para iniciar o processo.\n\n"
            "4. Acompanhe o progresso e os logs na tela.\n\n"
            "5. Ao finalizar, uma mensagem será exibida informando o sucesso ou erro da operação."
        )
        ajuda_box = tk.Message(frame_ajuda, text=texto_ajuda, width=250)
        ajuda_box.pack(padx=10, pady=10)

        # Label com o nome do idealizador
        label_autor = tk.Label(frame_ajuda, text="Idealizado por: Rivaldo", font=("Arial", 9, "italic"))  # Adiciona a label do autor
        label_autor.pack(side=tk.BOTTOM, pady=10)  # Posiciona no final do frame de ajuda

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

    def instalar_pyinstaller():
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível instalar o PyInstaller automaticamente.\nErro: {e}")
            return False

    def iniciar_compilacao(self):
        if not shutil.which("pyinstaller"):
            resposta = messagebox.askyesno(
                "PyInstaller não encontrado",
                "PyInstaller não está instalado. Deseja instalar automaticamente?"
            )
            if resposta:
                if not instalar_pyinstaller():
                    return
            else:
                return
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
            '--noconsole',  # Adiciona esta linha para não abrir o console (janela preta)
            '--distpath', pasta_destino,
            arquivo_py
        ]
        self.log(f"Compilando: {arquivo_py}")
        self.log(f"Destino: {pasta_destino}")
        self.progress["value"] = 10                       # Atualiza a barra de progresso

        # Executa o comando e captura a saída em tempo real, ocultando a janela preta no Windows
        startupinfo = None                                # Define startupinfo como None por padrão
        if sys.platform == "win32":                       # Se estiver no Windows
            startupinfo = subprocess.STARTUPINFO()        # Cria um objeto STARTUPINFO
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # Define a flag para não mostrar a janela

        processo = subprocess.Popen(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            startupinfo=startupinfo                       # Usa startupinfo para ocultar a janela no Windows
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