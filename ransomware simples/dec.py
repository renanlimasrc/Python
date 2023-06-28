#!/usr/bin/env python
# Arquivo de decriptar pasta
# by n1nr0d

import os
from cryptography.fernet import Fernet
import tkinter as tk
import time

# Descriptografar os arquivos de um diretório
def descriptografar_arquivos(diretorio, chave):
    fernet = Fernet(chave)

    # Percorrer todos os arquivos no diretório
    for raiz, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)

            # Verificar se o arquivo possui a extensão .encrypted
            if arquivo.endswith(".encrypted"):
                # Ler o conteúdo do arquivo criptografado
                with open(caminho_completo, "rb") as f:
                    conteudo_criptografado = f.read()

                # Descriptografar o conteúdo do arquivo
                conteudo_descriptografado = fernet.decrypt(conteudo_criptografado)

                # Remover a extensão .encrypted do nome do arquivo descriptografado
                novo_nome = arquivo[:-10]
                caminho_descriptografado = os.path.join(raiz, novo_nome)

                # Gravar o conteúdo descriptografado no novo arquivo
                with open(caminho_descriptografado, "wb") as f:
                    f.write(conteudo_descriptografado)

                # Remover o arquivo criptografado
                os.remove(caminho_completo)


    # Remover o arquivo senha
    os.remove("senha.txt")

    # Remover o arquivo horareal
    os.remove("horareal.txt")

# Nome do diretório que será descriptografado
diretorio = "./p"

# Ler a chave de criptografia do arquivo
with open("senha.txt", "r") as arquivo:
    chave_base64 = arquivo.read()
# Converter a chave base64 de volta para bytes
chave = chave_base64.encode()

# Descriptografar os arquivos do diretório
descriptografar_arquivos(diretorio, chave)

# Criar a janela de conclusão da descriptografia
root = tk.Tk()
root.title("Descriptografar Arquivos")
root.geometry("350x70")

conclusao_label = tk.Label(root, font=("Arial", 12), text="Descriptografado com sucesso! \U0001F600")
conclusao_label.pack(pady=10)

root.mainloop()
