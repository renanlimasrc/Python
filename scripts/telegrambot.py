#!/usr/bin/python

import telebot
import requests

CHAVE_API = ""
bot = telebot.TeleBot(CHAVE_API)

cities_in_temp = {}


@bot.message_handler(commands=["cep"])
def busca_cep(mensagem):
    bot.send_message(mensagem.chat.id, "Digite o CEP para obter informações sobre a rua:")
    bot.register_next_step_handler(mensagem, handle_cep)


def handle_cep(mensagem):
    cep = mensagem.text
    if cep:
        url = f"https://viacep.com.br/ws/{cep}/json/"
        resposta = requests.get(url)

        if resposta.status_code == 200:
            dados_cep = resposta.json()
            if "erro" not in dados_cep:
                rua = dados_cep["logradouro"]
                bairro = dados_cep["bairro"]
                cidade = dados_cep["localidade"]
                uf = dados_cep["uf"]
                mensagem_resposta = f"Rua: {rua}\nBairro: {bairro}\nCidade: {cidade}\nUF: {uf}"
                bot.send_message(mensagem.chat.id, mensagem_resposta)
            else:
                bot.send_message(mensagem.chat.id, "CEP não encontrado.")
        else:
            bot.send_message(mensagem.chat.id, "Não foi possível obter as informações do CEP.")
    else:
        bot.send_message(mensagem.chat.id, "Por favor, especifique o CEP.")


@bot.message_handler(commands=["seu_id"])
def iduser(mensagem):
    iduser = mensagem.chat.id
    bot.reply_to(mensagem, f"id: {iduser}")


@bot.message_handler(commands=["temp"])
def handle_message(mensagem):
    chat_id = mensagem.chat.id
    bot.send_message(chat_id, "Digite o nome da cidade:")
    cities_in_temp[chat_id] = True


@bot.message_handler(func=lambda mensagem: cities_in_temp.get(mensagem.chat.id, False))
def handle_temp_city(mensagem):
    chat_id = mensagem.chat.id
    cidade = mensagem.text
    if cidade:
        api_key = ''
        url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric"
        resposta = requests.get(url)

        if resposta.status_code == 200:
            dados_clima = resposta.json()
            temperatura = dados_clima["main"]["temp"]
            bot.send_message(chat_id, f"A temperatura atual de {cidade} é: {temperatura}°C")
        else:
            bot.send_message(chat_id, "Não foi possível obter as informações meteorológicas.")
    else:
        bot.send_message(chat_id, "Por favor, especifique o nome da cidade corretamente.")

    del cities_in_temp[chat_id]


@bot.message_handler(commands=["cotacao"])
def cotacao_dolar(mensagem):
    link = "https://economia.awesomeapi.com.br/last/USD-BRL"
    link2 = "https://economia.awesomeapi.com.br/last/BTC-BRL"
    reqdol = requests.get(link)
    reqdol = reqdol.json()
    dolar = reqdol['USDBRL']['bid']
    reqbit = requests.get(link2)
    reqbit = reqbit.json()
    bitcoin = reqbit['BTCBRL']['bid']
    bot.reply_to(mensagem, f"Cotação Dólar: R${dolar}\nCotação Bitcoin: R${bitcoin}.00")


@bot.message_handler(commands=["megasena"])
def get_mega_sena_numbers(mensagem):
    url = "https://loteriascaixa-api.herokuapp.com/api/mega-sena/latest"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados_sorteio = resposta.json()
        conc = dados_sorteio['concurso']
        num_sorteados = ", ".join(dados_sorteio['dezenas'])
        vencedores = dados_sorteio['premiacoes'][0]['vencedores']
        acumul = dados_sorteio['acumulou']
        valacumul = dados_sorteio['acumuladaProxConcurso']
        if acumul:
            result = 'Acumulou!'
            bot.send_message(mensagem.chat.id, f'{result}')
            bot.send_message(mensagem.chat.id, 'Dados:')
            bot.send_message(mensagem.chat.id, f"Concurso: {conc}, Números Sorteados: {num_sorteados}, Valor do próximo sorteio: {valacumul}")
        else:
            result = 'Saiu!'
            premio = dados_sorteio['premiacoes'][0]['premio']
            bot.send_message(mensagem.chat.id, f'{result}')
            bot.send_message(mensagem.chat.id, 'Dados:')
            bot.send_message(mensagem.chat.id, f"Concurso: {conc},Números Sorteados: {num_sorteados}, Número de vencedores:{vencedores}, Prêmio: {premio}, Valor do próximo sorteio: {valacumul}")
    else:
        bot.send_message(mensagem.chat.id, "Não foi possível obter os números do último sorteio da Mega-Sena.")


def verificar(mensagem):
    return True


texto = """
/cep - Busca informações sobre a rua pelo CEP
/temp - Exibe a temperatura atual da cidade
/cotacao - Mostra a cotação do Dólar e do Bitcoin
/megasena - Mostra os números do último sorteio da Mega-Sena
/seu_id - Verificar seu ID
"""


@bot.message_handler(func=verificar)
def responder(mensagem):
    bot.reply_to(mensagem, texto)


bot.polling()  # <- loop do bot
