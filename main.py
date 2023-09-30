import csv
import re
import pandas as pd
import networkx as nx
import json

from networkx.algorithms import node_classification


def dicionario_csv(arquivo):
    # Abre o arquivo CSV em modo de leitura
    with open(arquivo, mode='r', newline='', encoding='UTF-8') as arquivo_csv:
        # Cria um leitor CSV
        leitor_csv = csv.DictReader(arquivo_csv)
        dicionario_de_dados = {}

        # Itera sobre as linhas do arquivo CSV
        for linha in leitor_csv:
            # Obtém a chave e o valor da linha
            chave = linha['HASHTAG']
            valor = linha['ORIENTATION']

            # Adiciona a chave e o valor ao dicionário
            dicionario_de_dados[chave] = valor

    # Agora, dicionario_de_dados contém os dados do CSV como um dicionário
    # onde as chaves são da primeira coluna e os valores são da segunda coluna
    return dicionario_de_dados


def ler_json_e_transformar_em_lista(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            if isinstance(dados, list):
                return dados
            else:
                print("O arquivo JSON não contém uma lista.")
                return []
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return []
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo JSON '{nome_arquivo}'.")
        return []


# Função para identificar e separar hashtags em um tweet
def extrair_hashtags(tweet_text):
    # Usando uma expressão regular para encontrar todas as hashtags começando com "#"
    hashtags_list = re.findall(r'#\w+', tweet_text)
    return hashtags_list


def data_set():
    # Lista com todos os tweets
    lista1 = ler_json_e_transformar_em_lista('data-set-twitter-elections/scraped_tweets_09_16_22.json')
    lista2 = ler_json_e_transformar_em_lista('data-set-twitter-elections/scraped_tweets_09_23_22.json')
    lista3 = ler_json_e_transformar_em_lista('data-set-twitter-elections/scraped_tweets_09_30_22.json')
    lista4 = ler_json_e_transformar_em_lista('data-set-twitter-elections/scraped_tweets_10_07_22.json')
    lista5 = ler_json_e_transformar_em_lista('data-set-twitter-elections/scraped_tweets_10_14_22.json')
    lista6 = ler_json_e_transformar_em_lista('data-set-twitter-elections/scraped_tweets_10_21_22.json')
    lista7 = ler_json_e_transformar_em_lista('data-set-twitter-elections/scraped_tweets_10_28_22.json')
    lista8 = ler_json_e_transformar_em_lista('data-set-twitter-elections/scraped_tweets_11_04_22.json')
    lista9 = ler_json_e_transformar_em_lista('data-set-twitter-elections/scraped_tweets_11_11_22.json')
    lista_total = lista1 + lista2 + lista3 + lista4 + lista5 + lista6 + lista7 + lista8 + lista9
    lista_csv = []

    for tweet in lista_total:
        if len(extrair_hashtags(tweet['full_text'])) >= 1:
            hashtags_ = extrair_hashtags(tweet['full_text'])
            hashtag = []

            if len(hashtags_) >= 1:
                for item_ in hashtags_:
                    item_ = item_.replace('#', '')
                    hashtag.append(item_)

            lista_csv.append([tweet['full_text'], ' '.join(hashtag)])

    # Nome do arquivo CSV de destino
    nome_arquivo = "dados.csv"

    # Escreva a lista de dados em um arquivo CSV
    with open(nome_arquivo, mode="w", encoding="utf-8") as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv, delimiter=",")

        # Escreva cada linha da lista como uma linha no arquivo CSV
        for linha in lista_csv:
            if any(linha):
                escritor_csv.writerow(linha)

    print(f"Arquivo CSV '{nome_arquivo}' criado com sucesso.")


# Carregue seus dados de hashtags (substitua isso pelo seu próprio conjunto de dados)
data = pd.read_csv('dados.csv')

# Crie um objeto de grafo direcionado (para representar as co-ocorrências)
G = nx.DiGraph()
caracterized_hashtags = dicionario_csv('hashtags_populares.csv')
lista_hashtags = []

# Itere sobre cada linha do seu conjunto de dados
for index, row in data.iterrows():
    hashtags = row['HASHTAG'].split()  # Supondo que suas hashtags estejam em uma única coluna separada por espaços

    # Adicione as hashtags como nós do grafo
    for item in hashtags:
        lista_hashtags.append(item)
        if item in caracterized_hashtags:
            G.add_node(item, label=caracterized_hashtags[item])
        else:
            G.add_node(item)

    # Crie arestas entre todas as combinações de hashtags em um único tweet
    for i in range(len(hashtags)):
        for j in range(i + 1, len(hashtags)):
            # Verifique se a aresta já existe e, se existir, aumente o peso
            if G.has_edge(hashtags[i], hashtags[j]):
                G[hashtags[i]][hashtags[j]]['weight'] += 1
            else:
                G.add_edge(hashtags[i], hashtags[j], weight=1)


G_undirected = G.to_undirected()
predicted = node_classification.harmonic_function(G_undirected)

# Imprima os nós com seus rótulos previstos
for node, label in zip(G.nodes, predicted):
    print(f"Hashtag: {node}, Orientation: {label}")
