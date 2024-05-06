#!/usr/bin/python

# By Renan Lima, versão 2.4

import telebot
import requests
import datetime
import locale


CHAVE_API_TELEGRAM = ""  # Gere seu bot do telegram com o @botfather
CHAVE_API_TEMPO = ""  # Vá no site openweather.com e gere seu token para ter acesso a API do tempo

bot = telebot.TeleBot(CHAVE_API_TELEGRAM)
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

# Verificar a hora do dia
def get_time_of_day():
    now = datetime.datetime.now()
    hour = now.hour

    if 6 <= hour < 12:
        return "Bom dia"
    elif 12 <= hour < 18:
        return "Boa tarde"
    else:
        return "Boa noite"


# Executa o comando /cep
@bot.message_handler(commands=["cep"])
def busca_cep(mensagem):
    bot.send_message(mensagem.chat.id, "Digite o CEP para obter informações sobre o local(rua, avenida, etc):")
    bot.register_next_step_handler(mensagem, busca_cep_exec)  # < - parâmetro que pega o conteúdo da próxima mensagem


def busca_cep_exec(mensagem):
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
                bot.reply_to(mensagem, mensagem_resposta)
            else:
                bot.reply_to(mensagem, "CEP não encontrado.")
        else:
            bot.reply_to(mensagem, "Não foi possível obter as informações do CEP.")
    else:
        bot.send_message(mensagem.chat.id , "Por favor, especifique o CEP.")

# Executa o comando /seu_id
@bot.message_handler(commands=["seu_id"])
def iduser(mensagem):
    iduser = mensagem.chat.id
    bot.reply_to(mensagem, f"id: {iduser}")


cidade_temp = {}


# Executa o comando /temp
@bot.message_handler(commands=["temp"])
def handle_message(mensagem):
    chat_id = mensagem.chat.id
    bot.send_message(chat_id, "Digite o nome da cidade:")
    cidade_temp[chat_id] = True


# Busca os dados meteorológicos da cidade
@bot.message_handler(func=lambda mensagem: cidade_temp.get(mensagem.chat.id, False))
def cidade_tempo(mensagem):
    cidade = mensagem.text
    if cidade:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={CHAVE_API_TEMPO}&units=metric"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados_clima = resposta.json()
            temperatura = dados_clima["main"]["temp"]
            bot.send_message(mensagem.chat.id, f"A temperatura atual de {cidade} é: {temperatura}°C")
        else:
            bot.send_message(mensagem.chat.id, "Não foi possível obter as informações meteorológicas.")
    else:
        bot.send_message(mensagem.chat.id, "Por favor, especifique o nome da cidade corretamente.")

    del cidade_temp[mensagem.chat.id]


# Executa o comando cotação
@bot.message_handler(commands=["cotacao"])
def cotacao_dolar(mensagem):
    link = "https://economia.awesomeapi.com.br/last/USD-BRL"
    link2 = "https://economia.awesomeapi.com.br/last/BTC-BRL"
    reqdol = requests.get(link)
    reqdol = reqdol.json()
    dolar = float(reqdol['USDBRL']['bid'])
    dolar = locale.currency(dolar, grouping=True, symbol=True)
    reqbit = requests.get(link2)
    reqbit = reqbit.json()
    bitcoin = float(reqbit['BTCBRL']['bid'])
    bitcoin = locale.currency(bitcoin, grouping=True, symbol=True)
    bot.reply_to(mensagem, f"Cotação Dólar: {dolar}\nCotação Bitcoin: {bitcoin}")


# Executa o comando megasena
@bot.message_handler(commands=["megasena"])
def mega_sena(mensagem):

    conc_num = "latest" # Alterar de latest para algum número para consultador o concurso: Ex: 2510. Irá consultar o concurso 2510

    url = f"https://loteriascaixa-api.herokuapp.com/api/megasena/{conc_num}"
    resposta = requests.get(url)
    if resposta.status_code == 200:
            dados_sorteio = resposta.json()
            #print(dados_sorteio) # < para ver o json
            data = dados_sorteio["data"]
            conc = dados_sorteio["concurso"]
            num_sorteados = ", ".join(dados_sorteio["dezenas"])
            acumul = dados_sorteio['acumulou']
            prox_conc_data = dados_sorteio["dataProximoConcurso"]
            prox_conc_val = dados_sorteio["valorEstimadoProximoConcurso"]
            prox_conc_val = locale.currency(prox_conc_val, grouping=True, symbol=True)

            if acumul is True:
                result = "Ninguém acertou os 6 números!"
                val_acumul = dados_sorteio["valorAcumuladoProximoConcurso"]
                val_acumul = locale.currency(val_acumul, grouping=True, symbol=True)
                # result, data, conc, num_sorteados, val_acumul
                atualizacao = f"{result}\nData do sorteio: {data}\nConcurso: {conc}\nNúmeros sorteados: {num_sorteados}\nValor sorteado: {val_acumul}\nValor estimado no próximo concurso: {prox_conc_val}\nData do próximo concurso: {prox_conc_data}"
                bot.reply_to(mensagem, atualizacao)
            

            elif acumul is False:
                result = "Saiu!"
                premio = dados_sorteio["premiacoes"][0]["valorPremio"]
                premio = locale.currency(premio, grouping=True, symbol=True)
                resultados = []
                ganhadores_qtd = dados_sorteio["premiacoes"][0]["ganhadores"]
                local_ganhadores = dados_sorteio["localGanhadores"]

                for item in local_ganhadores:
                    ganhadores = item["ganhadores"]
                    municipio = item["municipio"]
                    uf = item["uf"]

                    if municipio == "CANAL ELETRONICO" and uf == "--": 
                        resultados.append([f"{ganhadores} ganhador(es) - Aposta feita pela internet"])
                    else:
                        resultados.append([f"{ganhadores} ganhador(es) - Município: {municipio}, Estado: {uf}"])

                string_resultados = "\n".join([", ".join(lista) for lista in resultados])

                atualizacao = f"{result}\nData do sorteio: {data}\nConcurso: {conc}\nNúmeros Sorteados: {num_sorteados}\nValor sorteado: {premio}\nNúmero de pessoas que acertaram a sena: {ganhadores_qtd}\nGanhadores:\n{string_resultados}\nData do próximo concurso: {prox_conc_data}\nValor estimado do próximo concurso: {prox_conc_val}"
                bot.reply_to(mensagem, atualizacao)
                
    else:
        print("Não foi possível obter os números da Mega-Sena!")    


# True, necessário para iniciar o bot
def verificar(mensagem):
    return True


texto = """
/cep - Busca informações sobre a rua pelo CEP
/temp - Exibe a temperatura atual da cidade
/cotacao - Mostra a cotação do Dólar e do Bitcoin
/megasena - Mostra os números do último sorteio da Mega-Sena
/seu_id - Verificar seu ID
"""


# Apresentação: 1° mensagem
@bot.message_handler(func=verificar)
def apresentacao(message):
    user_name = message.from_user.first_name
    time_of_day = get_time_of_day()
    welcome_message = f"{time_of_day}, {user_name}! O que deseja?\n\nOpções disponíveis:\n{texto}"
    bot.send_message(message.chat.id, welcome_message)


# Mostra opções. 2° mensagem
@bot.message_handler(func=verificar)
def responder(mensagem):
    bot.reply_to(mensagem, texto)


# Inicie o bot
bot.polling()
