import tkinter as tk  # Importa o Tkinter para criar a interface gráfica

# Cria a janela principal
root = tk.Tk()
root.title("Teste de Programa")  # Define o título da janela

# Adiciona um texto na janela
label = tk.Label(root, text="Esta é uma janela de teste do programa!")
label.pack(padx=20, pady=20)

# Inicia o loop principal da interface
root.mainloop()