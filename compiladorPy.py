import tkinter as tk  # Importa o Tkinter para criar a interface gráfica
from tkinter import filedialog  # Importa o filedialog para abrir janelas de seleção de arquivos
from tkinter import messagebox  # Importa messagebox para mostrar mensagens ao usuário
from tkinter import ttk         # Importa ttk para a barra de progresso
import subprocess  # Importa subprocess para executar comandos do sistema
import threading   # Importa threading para não travar a interface
import os          # Importa os para manipulação de caminhos

# Cria a janela principal
root = tk.Tk()
root.title("Compilador Python para Executável")  # Define o título da janela

# Define o ícone da janela para o emblema do Python (usa caminho absoluto para evitar erro)
icon_path = os.path.join(os.path.dirname(__file__), "python.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Frame principal para os controles do compilador
frame_principal = tk.Frame(root)
frame_principal.grid(row=0, column=0, padx=10, pady=10, sticky="n")

# Frame lateral para instruções de uso
frame_ajuda = tk.Frame(root, relief=tk.GROOVE, borderwidth=2)
frame_ajuda.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

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
tk.Label(frame_principal, text="Arquivo Python:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Entry(frame_principal, textvariable=caminho_arquivo, width=40).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_principal, text="🔍", command=selecionar_arquivo).grid(row=0, column=2, padx=5, pady=5)

# Campo e botão para selecionar a pasta de destino
tk.Label(frame_principal, text="Destino do Executável:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Entry(frame_principal, textvariable=caminho_destino, width=40).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame_principal, text="🔍", command=selecionar_destino).grid(row=1, column=2, padx=5, pady=5)

# Barra de progresso
progress = ttk.Progressbar(frame_principal, orient="horizontal", length=400, mode="determinate")  # Modo determinate
progress.grid(row=3, column=0, columnspan=3, padx=5, pady=10)
progress["value"] = 0  # Garante que a barra inicia zerada e sem cor

# Caixa de texto para logs
log_text = tk.Text(frame_principal, height=8, width=60)
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
tk.Button(frame_principal, text="Compilar", command=compilar_thread).grid(row=2, column=1, pady=15)

# Frame lateral de instruções de uso
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
label_autor = tk.Label(frame_ajuda, text="Idealizado por: Rivaldo", font=("Arial", 9, "italic"))
label_autor.pack(side=tk.BOTTOM, pady=10)

# Inicia o loop principal da interface
root.mainloop()