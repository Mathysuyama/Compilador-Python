import tkinter as tk  # Importa o Tkinter para criar a interface gráfica
from tkinter import filedialog  # Importa o filedialog para abrir janelas de seleção de arquivos
from tkinter import messagebox  # Importa messagebox para mostrar mensagens ao usuário
from tkinter import ttk         # Importa ttk para a barra de progresso
import subprocess  # Importa subprocess para executar comandos do sistema
import threading   # Importa threading para não travar a interface

# Cria a janela principal
root = tk.Tk()
root.title("Compilador Python para Executável")  # Define o título da janela
root.iconbitmap("python.ico")  # Define o ícone da janela para o emblema do Python

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

# Barra de progresso
progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")  # Modo determinate
progress.grid(row=3, column=0, columnspan=3, padx=5, pady=10)
progress["value"] = 0  # Garante que a barra inicia zerada e sem cor

# Caixa de texto para logs
log_text = tk.Text(root, height=8, width=60)
log_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

# Função para compilar o arquivo Python selecionado (em thread)
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
    progress["value"] = 0           # Garante que a barra inicia zerada ao compilar
    progress.config(mode="indeterminate")  # Muda para animada só durante a compilação
    progress.start()                # Inicia a barra de progresso
    log_text.delete(1.0, tk.END)    # Limpa o log
    try:
        processo = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for linha in processo.stdout:
            log_text.insert(tk.END, linha)
            log_text.see(tk.END)
        processo.wait()
        progress.stop()             # Para a barra de progresso
        progress.config(mode="determinate")  # Volta para determinate (sem cor)
        progress["value"] = 0       # Zera a barra novamente
        if processo.returncode == 0:
            messagebox.showinfo("Sucesso", "Compilação finalizada com sucesso!")  # Mostra mensagem de sucesso
        else:
            messagebox.showerror("Erro", "Ocorreu um erro durante a compilação.") # Mostra mensagem de erro
    except Exception as e:
        progress.stop()
        progress.config(mode="determinate")
        progress["value"] = 0
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Função para rodar a compilação em thread
def compilar_thread():
    threading.Thread(target=compilar).start()

# Botão para compilar
tk.Button(root, text="Compilar", command=compilar_thread).grid(row=2, column=1, pady=15)

# Inicia o loop principal da interface
root.mainloop()