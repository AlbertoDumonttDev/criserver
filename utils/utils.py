#!/usr/bin/env python3

import openai
import os
import glob


from datetime import datetime

openai.api_key = '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'



#                           get_gpt4_response
# -------------------------------------------------------------------------
# Função para fazer chamada na API da openai com GPT-4
# Também irá chamar outra função "create_log_gpt4" para criar arquivo de log
# -------------------------------------------------------------------------
#                        Bibliotecas a importar
# import openai - para usar api da OPENAI
# from datetime import datetime - para variaveis de horario e data

def get_gpt4_response(promptUser ,attachmentUser, pathFile):

    prompt = f"{promptUser} {attachmentUser}"

    initNow = datetime.now()
    initData = initNow.strftime("%d/%m/%Y")
    initHour = initNow.strftime("%H:%M:%S")

    try:
        # Notice the use of openai.ChatCompletion here
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Example of a chat-based model
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": prompt},
            ]
        )

        create_log_gpt4(response, initData, initHour, pathFile)
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return str(e)



#                           create_log_gpt4
# -------------------------------------------------------------------------
# Função para criar arquivo de log com dados de consumo da API do GPT-4 
# -------------------------------------------------------------------------
#                        Bibliotecas a importar
# import os
# from datetime import datetime - para variaveis de horario e data

def create_log_gpt4(response, initData, initHour, pathFile):

        finishNow = datetime.now()
        finishData = finishNow.strftime("%d/%m/%Y")
        finishHour = finishNow.strftime("%H:%M:%S")

        format = "%H:%M:%S"
        initHour_dt = datetime.strptime(initHour, format)
        finishHour_dt = datetime.strptime(finishHour, format)
        diferrenceHour = round((finishHour_dt - initHour_dt).total_seconds() / 60, 2)  

        prompt_tokens = response["usage"]["prompt_tokens"]
        completion_tokens = response["usage"]["completion_tokens"]

        
        tokenCalculatorInput = (prompt_tokens / 1000) * 0.3
        tokenCalculatorOutput = (completion_tokens / 1000) * 0.6
        totalPrincingToken = round((tokenCalculatorInput + tokenCalculatorOutput) * 4.93, 2)
        

        dataTXT = f"ARQUIVO DE LOG {pathFile}\n\ndata de inicio: {initData}\nhora de inicio: {initHour}\nErros: 0\ndata de conclusão: {finishData}\nhora de conclusão: {finishHour}\ntempo para conclusão: {diferrenceHour} minutos\nquantidade de tokens de entrada: {prompt_tokens}\nquantidade de tokens de saída: {completion_tokens}\ncusto de IA estimado em tokens: R$ {totalPrincingToken} (Dolar atual R$ 4,93)"
        print(f"{dataTXT}")

        with open(pathFile, 'w') as arquivo_novo:
            arquivo_novo.write(dataTXT)



#                           get_prompt_drive
# -------------------------------------------------------------------------
# Função para ler prompt que está em yaml do drive e armazenar em string
# -------------------------------------------------------------------------
#                        Bibliotecas a importar
# import glob
#  

def get_prompt_drive(pathFile):

        path = pathFile 

        inUse = '* EM USO.yml'

        # Usando glob para encontrar arquivos que correspondam ao padrão
        fileSearch = glob.glob(path + inUse)
        
        # Checando se algum arquivo foi encontrado e lendo o primeiro que corresponder
        if fileSearch:
            fileSearchReady = fileSearch[0]  # Pegando o primeiro arquivo encontrado
            with open(fileSearchReady, 'r', encoding='utf-8') as file:
                prompt = file.read()
            return prompt
        else:
            return "Nenhum prompt foi encontrado"  
        


# conv = "Olá"
# data = get_gpt4_response(conv, "/home/dev/resources/googledrive/arquivo.txt")
# print(f"{data}")






