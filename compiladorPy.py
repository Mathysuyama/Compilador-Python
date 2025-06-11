import subprocess                # Importa o módulo para executar comandos do sistema
import tkinter as tk             # Importa o módulo tkinter para interfaces gráficas
from tkinter import filedialog   # Importa o filedialog para abrir janelas de seleção de arquivos

def escolher_arquivo():
    root = tk.Tk()               # Cria uma janela principal do tkinter
    root.withdraw()              # Oculta a janela principal (não queremos que ela apareça)
    arquivo = filedialog.askopenfilename(
        filetypes=[("Python Files", "*.py")],  # Limita a seleção para arquivos .py
        title="Selecione o arquivo Python"     # Título da janela de seleção
    )
    return arquivo               # Retorna o caminho do arquivo selecionado

def compilar_para_executavel(arquivo_py):
    # Gera o executável usando PyInstaller
    subprocess.run(['pyinstaller', '--onefile', arquivo_py])  # Executa o comando do PyInstaller para criar um executável único

if __name__ == "__main__":       # Verifica se o script está sendo executado diretamente
    arquivo = escolher_arquivo() # Chama a função para escolher o arquivo Python
    if arquivo:                  # Se um arquivo foi selecionado
        compilar_para_executavel(arquivo)  # Compila o arquivo selecionado para executável
        print("Compilação finalizada. O executável está na pasta 'dist'.")  # Mensagem de sucesso
    else:
        print("Nenhum arquivo selecionado.")  # Mensagem caso nenhum arquivo seja escolhido