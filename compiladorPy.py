import tkinter as tk  # Importa o Tkinter para criar a interface gráfica
from tkinter import filedialog  # Importa o filedialog para abrir janelas de seleção de arquivos
import subprocess  # Importa subprocess para executar comandos do sistema

# Cria a janela principal
root = tk.Tk()
root.title("Compilador Python para Executável")  # Define o título da janela

# Variáveis para armazenar os caminhos selecionados
caminho_arquivo = tk.StringVar()   # Caminho do arquivo .py
caminho_destino = tk.StringVar()   # Caminho da pasta de destino

# Função para selecionar o arquivo Python
def selecionar_arquivo():
    arquivo = filedialog.askopenfilename(
        filetypes=[("Python Files", "*.py")],
        title="Selecione o arquivo Python"
    )
    if arquivo:
        caminho_arquivo.set(arquivo)  # Atualiza o campo com o caminho selecionado

# Função para selecionar a pasta de destino
def selecionar_destino():
    pasta = filedialog.askdirectory(
        title="Selecione a pasta de destino"
    )
    if pasta:
        caminho_destino.set(pasta)  # Atualiza o campo com o caminho selecionado

# Campo e botão para selecionar o arquivo Python
tk.Label(root, text="Arquivo Python:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Entry(root, textvariable=caminho_arquivo, width=40).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="🔍", command=selecionar_arquivo).grid(row=0, column=2, padx=5, pady=5)

# Campo e botão para selecionar a pasta de destino
tk.Label(root, text="Destino do Executável:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Entry(root, textvariable=caminho_destino, width=40).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="🔍", command=selecionar_destino).grid(row=1, column=2, padx=5, pady=5)

# Função para compilar o arquivo Python selecionado
def compilar():
    arquivo = caminho_arquivo.get()      # Obtém o caminho do arquivo .py
    destino = caminho_destino.get()      # Obtém o caminho da pasta de destino
    if not arquivo or not destino:
        tk.messagebox.showerror("Erro", "Selecione o arquivo Python e o destino!")  # Mostra erro se faltar algum campo
        return
    comando = [
        "pyinstaller",
        "--onefile",
        "--noconsole",                   # Não abre janela preta ao executar o .exe gerado
        "--distpath", destino,           # Define a pasta de destino do executável
        arquivo
    ]
    subprocess.run(comando)              # Executa o comando do PyInstaller

# Botão para compilar
tk.Button(root, text="Compilar", command=compilar).grid(row=2, column=1, pady=15)

# Inicia o loop principal da interface
root.mainloop()