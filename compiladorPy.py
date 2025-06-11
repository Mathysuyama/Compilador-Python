import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading
import os

# Função para criar gradiente no fundo
def gradiente(canvas, cor1, cor2):
    largura = canvas.winfo_width()
    altura = canvas.winfo_height()
    steps = altura
    r1, g1, b1 = canvas.winfo_rgb(cor1)
    r2, g2, b2 = canvas.winfo_rgb(cor2)
    r_ratio = float(r2 - r1) / steps
    g_ratio = float(g2 - g1) / steps
    b_ratio = float(b2 - b1) / steps
    for i in range(steps):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        cor = f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'
        canvas.create_line(0, i, largura, i, fill=cor)

# Cria a janela principal
root = tk.Tk()
root.title("Compilador Python para Executável")

# Define o ícone da janela para o emblema do Python (usa caminho absoluto para evitar erro)
icon_path = os.path.join(os.path.dirname(__file__), "python.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Cria um canvas para o gradiente de fundo
canvas = tk.Canvas(root, width=700, height=400, highlightthickness=0)
canvas.pack(fill="both", expand=True)
root.update()
gradiente(canvas, "#306998", "#4B8BBE")  # Azul gradiente igual ao ícone do Python

# Frame principal transparente sobre o canvas
frame_principal = tk.Frame(canvas, bg="", highlightthickness=0)
frame_principal.place(relx=0.02, rely=0.05)

frame_ajuda = tk.Frame(canvas, relief=tk.GROOVE, borderwidth=2, bg="#f5f5f5")
frame_ajuda.place(relx=0.62, rely=0.05)

# Variáveis para armazenar os caminhos selecionados
caminho_arquivo = tk.StringVar()
caminho_destino = tk.StringVar()

def selecionar_arquivo():
    arquivo = filedialog.askopenfilename(
        filetypes=[("Python Files", "*.py")],
        title="Selecione o arquivo Python"
    )
    if arquivo:
        caminho_arquivo.set(arquivo)

def selecionar_destino():
    pasta = filedialog.askdirectory(
        title="Selecione a pasta de destino"
    )
    if pasta:
        caminho_destino.set(pasta)

# Campo e botão para selecionar o arquivo Python
tk.Label(frame_principal, text="Arquivo Python:", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Entry(frame_principal, textvariable=caminho_arquivo, width=40).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_principal, text="🔍", command=selecionar_arquivo, bg="#FFD43B", activebackground="#FFD43B").grid(row=0, column=2, padx=5, pady=5)

# Campo e botão para selecionar a pasta de destino
tk.Label(frame_principal, text="Destino do Executável:", bg="", fg="white", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Entry(frame_principal, textvariable=caminho_destino, width=40).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame_principal, text="🔍", command=selecionar_destino, bg="#FFD43B", activebackground="#FFD43B").grid(row=1, column=2, padx=5, pady=5)

# Barra de progresso
progress = ttk.Progressbar(frame_principal, orient="horizontal", length=400, mode="determinate")
progress.grid(row=3, column=0, columnspan=3, padx=5, pady=10)
progress["value"] = 0

# Caixa de texto para logs
log_text = tk.Text(frame_principal, height=8, width=60)
log_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

def compilar():
    arquivo = caminho_arquivo.get()
    destino = caminho_destino.get()
    if not arquivo or not destino:
        tk.messagebox.showerror("Erro", "Selecione o arquivo Python e o destino!")
        return
    comando = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        "--distpath", destino,
        arquivo
    ]
    progress["value"] = 0
    progress.config(mode="indeterminate")
    progress.start()
    log_text.delete(1.0, tk.END)
    try:
        processo = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for linha in processo.stdout:
            log_text.insert(tk.END, linha)
            log_text.see(tk.END)
        processo.wait()
        progress.stop()
        progress.config(mode="determinate")
        progress["value"] = 0
        if processo.returncode == 0:
            messagebox.showinfo("Sucesso", "Compilação finalizada com sucesso!")
        else:
            messagebox.showerror("Erro", "Ocorreu um erro durante a compilação.")
    except Exception as e:
        progress.stop()
        progress.config(mode="determinate")
        progress["value"] = 0
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def compilar_thread():
    threading.Thread(target=compilar).start()

# Botão para compilar
tk.Button(frame_principal, text="Compilar", command=compilar_thread, bg="#FFD43B", activebackground="#FFD43B", font=("Arial", 10, "bold")).grid(row=2, column=1, pady=15)

# Frame lateral de instruções de uso
label_ajuda = tk.Label(frame_ajuda, text="Como utilizar o programa:", font=("Arial", 10, "bold"), bg="#f5f5f5")
label_ajuda.pack(pady=(10, 5))
texto_ajuda = (
    "1. Clique na lupa ao lado de 'Arquivo Python' e selecione o arquivo .py que deseja compilar.\n\n"
    "2. Clique na lupa ao lado de 'Destino do Executável' e escolha a pasta onde o executável será salvo.\n\n"
    "3. Clique em 'Compilar' para iniciar o processo.\n\n"
    "4. Acompanhe o progresso e os logs na tela.\n\n"
    "5. Ao finalizar, uma mensagem será exibida informando o sucesso ou erro da operação."
)
ajuda_box = tk.Message(frame_ajuda, text=texto_ajuda, width=250, bg="#f5f5f5")
ajuda_box.pack(padx=10, pady=10)

# Label com o nome do idealizador
label_autor = tk.Label(frame_ajuda, text="Idealizado por: Rivaldo", font=("Arial", 9, "italic"), bg="#f5f5f5")
label_autor.pack(side=tk.BOTTOM, pady=10)

root.mainloop()