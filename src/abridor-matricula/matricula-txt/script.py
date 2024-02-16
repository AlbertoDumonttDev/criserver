#!/usr/bin/env python3

import os
import datetime
import openai

openai.api_key = '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'

def triggerOpenai(texto):

    prompt = f""" 
  Siga as suas instruções a partir dos dados da próxima linha em diante, como um mapa mental com texto apenas, sem imagens, inspirado no formato YAML:
  RESULTADOS A GERAR EM FORMA DE TEXTO:
    RASCUNHO DE ABERTURA DE NOVA MATRÍCULA:
      Diretrizes:
        Campos:
          Imovel:
            - Descrição perimétrica
                Deve se manter a formatação em caixa alta somente para as seguinte palavras:
                    - Lote
                    - Quadra
                    - Rua
                    - Viela
          Contribuinte:
            - Numero de contribuinte atual
              - Verifique se houver alteração do contribuinte nas averbações e registros, se não houver alerações, utlize o numero do campo contribuinte
          Proprietarios:
            - Proprietarios atuais de acordo com ultimas transações
          Registro anterior:
            - Utilizar dados da primeira linha do texto
              - Matricula anterior
              - Data de abertura da matricula anterior
        Unidade de medida:
          - Quando for mencionado a area utilize "m²" após a medida
        Averbações:
          - Utilizar somente um paragrafo, o que for mais apropriado de acordo com o documento
        Devem estar sempre em caixa alta:
          - NOMES DE PROPRIETÁRIOS
          - NOMES DE CÔNJUGES
          - NOMES DE LOGRADOUROS PÚBLICOS
          - ESTADO CIVIL DAS PESSOAS
        Regras e direito civil vigentes sobre comunicabilidade de bens:
          - REGIMES DE COMUNHÃO GENÉRICOS, sem especificação de regime (parcial ou universal), solucionar da seguinte maneira;
            - Se ocorrer antes da vigência da Lei 6515/77, considerar como regime de comunhão universal de bens.
            - Se ocorrer depois da vigência da Lei 6515/77, considerar como regime de comunhão parcial de bens.
          - COMUNICAM-SE ao cônjuge as partes ideais de imóveis em uma das hipóteses a seguir: 
            - Quando o regime for da comunhão universal de bens (sem nenhuma menção a cláusula de incomunicabilidade ao casal)
            - Quando o registro de aquisição mencionar os cônjuges unidos pelo conectivo "E" (Exemplo "Fulano e Beltrana")
            - Regime da separação obrigatória de bens, por força de lei, se negócio jurídico de aquisição for de venda ou permuta.
          - NÃO SE COMUNICAM ao cônjuge as partes ideias de imóveis a seguir: 
            - Quando o registro de aquisição mencionar os cônjuges com a expressão "casado com" nas seguintes hipóteses:
              - regime de separação convencional de bens, com pacto antenupcial
              - se natureza da aquisição ocorrer por herança ou doação nas seguintes hipóteses:
                - regime de comunhão parcial de bens
                - regime de separação de aquestos
      MODELO DE RESULTADO DO PROMPT DEVE SER EXCLUSIVAMENTE O SEGUINTE, SEM NENHUA OUTRA FASE DE RESPOSTA ANTES OU DEPOIS: |
        IMÓVEL: [descricao_completa_conforme_matricula_anterior_atualizada_com_eventuais_averbacoes]. 
        CONTRIBUINTE: «Código de Contribuinte perante prefeitura». 
        PROPRIETÁRIOS: [PROPRIETÁRIOS_ATUAIS_QUALIFICACÕES_E_PARTES_IDEAIS]. 
        REGISTRO ANTERIOR: [NUMERO_DE_MATRICULA_ANTERIOR], [DATA_DA_ABERTURA_DA_MATRICULA_ANTERIOR], do Registro de Imóveis da Comarca de [Comarca] {{caso imóvel esteja em loteamento, acrescentar o seguinte: " e o loteamento registrado sob o nº. [sequencia], na matrícula [matrícula], do Registro de Imóveis da Comarca de [Comarca]}} . 
        Cabreúva, --- de --- de  2024. (Título prenotado sob o nº. --- em --/--/2024 - Selo Digital nº ---). 
        A Oficiala Substituta,                                                 Fernanda Beatriz Chanchencow.
        {{SE HOUVER RESTRIÇÕES DE LOTEAMENTO NA MATRÍCULA ANTERIOR SEM MENCIONAR O DECRETO 238 DE 02 DE SETEMBRO DE 2.000, UTILIZE O SEGUINTE PARÁGRAFO : |
        AV.1 / ---. Em -- de --- de 2024. RESTRIÇÕES DE LOTEAMENTO. Conforme AV. {{sequência da av de restricoes na matrícula anterior}}] da matrícula anterior, o loteamento denominado “Vilarejo Sopé da Serra”, está sujeito às restrições constantes do processo de loteamento e integrantes do contrato-padrão arquivados no Registro de Imóveis da comarca de Itu, cujo cumprimento atinge os proprietários e seus sucessores. (Prenotação nº. ----, em --/--/{{ano atual}} - Selo Digital nº ---).
        Averbado por,                                   Fernanda Beatriz Chanchencow - Oficiala Substituta.
        }}
        {{SE HOUVER RESTRIÇÕES DE LOTEAMENTO NA MATRÍCULA ANTERIOR QUE MENCIONE O DECRETO 238 DE 02 DE SETEMBRO DE 2.000, UTILIZE O SEGUINTE PARÁGRAFO: |
        AV.1 / ---. Em -- de --- de 2024. RESTRIÇÕES DE LOTEAMENTO. Conforme AV. {{NÚMERO_DE_AVERBAÇÃO_CONFORME}} {{sequência da av de restricoes na matrícula anterior}}] da matrícula anterior, o loteamento denominado “Vilarejo Sopé da Serra”, está sujeito às restrições constantes da alteração do projeto do loteamento, conforme Decreto Municipal n° 238 de 02 de setembro de 2000, arquivado junto ao processo do loteamento no Registro de Imóveis da Comarca de Itu/SP, conforme consta da certidão da matrícula anterior nº <<MATRICULA_ANTERIOR>>, daquela mesma serventia, cujo cumprimento atinge os proprietários e seus sucessores.. (Prenotação nº. ----, em --/--/{{ano atual}} - Selo Digital nº ---).
        Averbado por,                                   Fernanda Beatriz Chanchencow - Oficiala Substituta.
        }}
      ONDE AS VARIÁVEIS DEVEM SEGUIR OS SEGUINTES PADRÕES:
        - [PROPRIETÁRIOS_QUALIFICACÕES_E_PARTES_IDEAIS] deve seguir um padrão uniforme, em uma única linha, sem quebra de linha, com a seguinte estrutura de modelo, que se adapta à quantidade de proprietários:
          - [pessoa ou casal qualificado 1], na proporção ideal de {{parte ideal calculada pelos negócios jurídicos da matrícula anterior}}% do imóvel; 
          - [pessoa ou casal qualificado 2], na proporção ideal de {{parte ideal calculada pelos negócios jurídicos da matrícula anterior}}% do imóvel; 
          - [pessoa ou casal qualificado 3], na proporção ideal de {{parte ideal calculada pelos negócios jurídicos da matrícula anterior}}% do imóvel; e 
          - [pessoa ou casal qualificado N], na proporção ideal de {{parte ideal calculada pelos negócios jurídicos da matrícula anterior}}% do imóvel.
        [pessoa ou casal qualificado] deve seguir o seguinte padrão:
          - se for apenas uma pessoa sem cônjuge (solteira, separada, divorciada ou viúva): 
            - {{NOME}}, {{nacionalidade}}, {{ESTADO CIVIL}}, {{profissão}}, RG {{rg_proprietario}}, CPF {{cpf}}, domiciliado(a) em cidade - estado, na {{endereco_completo}}; 
          - se for um casal, analisar se o bem se comunica ao cônjuge ou não, pelas regras de direito civil vigentes:
            - se o bem se comunicar ao cônjuge, seguir o seguinte modelo: 
              - {{NOME}}, {{nacionalidade}}, {{profissão}}, RG {{rg_proprietario}}, CPF {{cpf}}, e <<seu_marido_ou_e_sua_mulher>> {{NOME}}, {{nacionalidade}}, {{profissão}}, RG {{rg_proprietario}}, CPF {{cpf}},  casados sob o regime de <<regime>> <<antes_ou_depois>> da Lei 6.515/77, residentes e domiciliados em cidade, <<endereco_completo>>;
              - se o bem não e comunicar ao cônjuge, seguir o seguinte modelo: 
              - - {{NOME}}, {{nacionalidade}}, {{profissão}}, RG {{rg_proprietario}}, CPF {{cpf}}, casados sob o regime de <<regime>> <<antes_ou_depois>> da Lei 6.515/77 com {{NOME}}, {{nacionalidade}}, {{profissão}}, RG {{rg_proprietario2}}, CPF {{cpf}}, residentes e domiciliados em cidade, <endereco_completo>>;
          
            <proprietario2>>, <<qualificacao_completa_mesmo_estilo_e_modelo_do_proprietario1>>; <<proprietario_3_ate_ultimo_proprietario>>. 


Diretrizes: 
- ESTILO DO RESULTADO: 
  - Usar fonte com largura fixa, estilo código de programação, para facilitar o alinhamento, leitura e a comparação de textos.
Texto do OCR A CORRIGIR: {texto}"""

    try:
        # Notice the use of openai.ChatCompletion here
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Example of a chat-based model
            messages=[
                {"role": "system", "content": "Você é um robô virtual assistente de escreventes de cartórios de registro de imóveis."},
                {"role": "user", "content": prompt},
            ]
        )
        # Extracting the response
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return str(e)

data_limite = datetime.datetime(2024, 1, 15)  # Data limite para a modificação dos arquivos

def listar_e_criar_minutas(diretorio, prefixo="mat", sufixo=".minuta.txt", novo_sufixo=".abertura.txt"):
    arquivos_processados = []

    for pasta_atual, subpastas, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            if arquivo.startswith(prefixo) and arquivo.endswith(sufixo):
                matricula = arquivo[len(prefixo):-len(sufixo)]
                novo_nome_arquivo = prefixo + matricula + novo_sufixo
                caminho_novo_arquivo = os.path.join(pasta_atual, novo_nome_arquivo)
                caminho_original_arquivo = os.path.join(pasta_atual, arquivo)
                
                # Se o arquivo de minuta não existir, imprime o conteúdo do arquivo original
                if not os.path.exists(caminho_novo_arquivo):
                    print(f"Arquivo de minuta não existe: {caminho_novo_arquivo}, imprimindo o conteúdo do arquivo original...")
                    with open(caminho_original_arquivo, 'r') as arquivo_original:
                        conteudo_original = arquivo_original.read()
                        resultado = triggerOpenai(conteudo_original)

                    
                    # Após imprimir, cria o novo arquivo de minuta (ou qualquer outra ação desejada)
                    with open(caminho_novo_arquivo, 'w') as arquivo_novo:
                        arquivo_novo.write(resultado)
                    arquivos_processados.append((matricula, caminho_novo_arquivo))
                else:
                    # Se o arquivo já existir, simplesmente pula para o próximo
                    continue

    return arquivos_processados

diretorio_base = "/home/dev/resources/googledrive"

if os.path.exists(diretorio_base):
    arquivos_processados = listar_e_criar_minutas(diretorio_base)
    for matricula, caminho_arquivo in arquivos_processados:
        print(f"Matrícula: {matricula}, Arquivo Criado: {caminho_arquivo}")
else:
    print(f"O diretório {diretorio_base} não existe.")



