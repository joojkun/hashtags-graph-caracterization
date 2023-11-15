import pandas as pd
import math
import matplotlib.pyplot as plt

# Suponha que você tenha uma lista de mensagens em forma de dicionários
# Cada dicionário possui as chaves "message" e "ideologia"
# Aqui, estou criando um exemplo fictício; substitua pelo seu próprio conjunto de dados reais
ideologia = {
    'central da esquerda': 'Esquerda',
    'notícias brasil patriota': 'Direita',
    'política pragmática': 'Direita',
    'bolsonaro presidente 2026': 'Direita',
    'manicômio libertário': 'Direita',
    'pátria amada brasil': 'Direita',
    'antibolsonaro': 'Esquerda',
    'diretademocratica': 'Direita',
    'canal guilherme boulos': 'Esquerda',
    'memes esquerdistas': 'Esquerda',
    'politicapragmatica': 'Direita',
    'blog do blasse': 'Centro',
    'nadireitabrasil': 'Direita',
    'Direita Patriota': 'Direita',
    'nova direita brasileira': 'Direita',
    'liberte_do_sistema': 'Direita',
    'canalboulostelegram': 'Direita',
    'carlos bolsonaro': 'Direita',
    'direitademocratica': 'Direita',
    'unica via': 'Direita',
    'agoraecirosupergrupo': 'Centro',
    'antiboisonaro': 'Esquerda',
    'jairbolsonarbrasil': 'Direita',
    'CLiberalBrasileiro': 'Centro',
    'blogblasse': 'Centro',
    'geopolítica': 'Centro',
    'DireitaPatriota': 'Direita',
    'socialismos - canal': 'Esquerda',
    'cirogomes': 'Centro',
    'direitas_am_2022': 'Direita',
    'bolsonarocarlos': 'Direita',
    'jones manoel': 'Centro',
    'maringá politica': 'Centro',
    'maringá política': 'Centro',
    'socialismos – canal': 'Esquerda',
    'marxismo': 'Esquerda',
    'jonesmanoel': 'Centro',
    'única via 👊🇧🇷': 'Direita',
    'geopoliticagrupo': 'Centro',
    'marxismoBR': 'Esquerda',
    'independencia goiana(based)': 'Direita',
    'independência goiana ( based )': 'Direita',
    'pátria clube – telegram': 'Direita',
    'ciro gomes oficial': 'Centro',
    'memesesquerdistas': 'Esquerda',
    'unicavia2022': 'Direita',
    'pdt 12': 'Esquerda',
    'pátria clube - telegram': 'Direita',
    'ciro gomes militância organizada': 'Centro',
    'politicageral2020': 'Centro',
    'socialismos': 'Esquerda',
    'pdt_oficial': 'Esquerda',
    'cuesta livre brasil': 'Direita',
    'direita patriota': 'Direita',
    'rafael primo': 'Centro'
}

all_messages = []


def find_link(message: str):
    # Fatiando as palavras da string
    message = message.split()

    # Procurando em todas as palavras da string para encontrar um link
    for palavra in message:
        # Procurando pela palavra 'https'
        if palavra.startswith('https'):
            palavra = palavra[8:palavra[8:].find('/') + 8]
            if '.com' in palavra:
                palavra = palavra[:palavra.find('.com')]
            if 'www.' in palavra:
                palavra = palavra.replace('www.', '')
            return palavra


# Função para extrair o domínio de uma URL em uma mensagem
def extrair_dominio(mensagem):
    # Esta é uma implementação simples; você pode aprimorá-la se necessário
    if '@' in mensagem:
        palavras = mensagem.split()
        for c in palavras:
            if c.startswith('@'):
                dominio = c
                return dominio
    else:
        return None


# Carregue seus dados de hashtags (substitua isso pelo seu próprio conjunto de dados)
data = pd.read_csv('dados.csv')
hashtags = pd.read_csv('caracterized_hashtags.csv')
orientation = {}

# Itere sobre cada linha do seu conjunto de dados
for index, row in hashtags.iterrows():
    orientation[row['HASHTAG']] = row['ORIENTATION']

# Itere sobre cada linha do seu conjunto de dados
for index, row in data.iterrows():
    tweet = row['TWEET']
    if extrair_dominio(tweet) is not None:
        all_messages.append({'Dominio': extrair_dominio(tweet), 'Ideologia': orientation[row['HASHTAG'].split()[0]]})

# Converter a lista de mensagens em um DataFrame do Pandas
df = pd.DataFrame(all_messages)

# Mapear as ideologias para valores numéricos (-1 para esquerda, 0 para centro, 1 para direita)
ideologia_map = {"L": -1, "N": 0, "R": 1}
df['score_ideologia'] = df['Ideologia'].map(ideologia_map)

# Calcular a cor com base no score
df['cor'] = df['score_ideologia'].apply(lambda score: plt.cm.RdBu((score + 1) / 2))

# Agrupar e contar a frequência dos domínios
contagem_dominios = df['Dominio'].value_counts().reset_index()
contagem_dominios.columns = ['Dominio', 'frequencia']

# Calcular o score de ideologia para cada domínio
score_dominios = df.groupby('Dominio')['score_ideologia'].mean().reset_index()

# Combinar os DataFrames
dados_scatter = contagem_dominios.merge(score_dominios, on='Dominio')
# Remover duplicatas com base nas colunas 'score_ideologia' e 'frequencia'
dados_scatter = dados_scatter.drop_duplicates(subset=['score_ideologia', 'frequencia'])


# Ordenar os domínios por frequência (do maior para o menor)
dados_scatter = dados_scatter.sort_values(by='frequencia', ascending=False)

# Selecionar os 20 domínios mais relevantes
dados_scatter = dados_scatter

# Calcular a cor com base no score
dados_scatter['cor'] = dados_scatter['score_ideologia'].apply(lambda score: plt.cm.RdBu((score + 1) / 2))

# Plotar o scatter plot com pontos maiores (altere o valor em s conforme necessário)
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    dados_scatter['score_ideologia'],
    dados_scatter['frequencia'],
    alpha=0.6,
    s=1000,  # Ajuste o valor em "s" para controlar o tamanho dos pontos
    c=dados_scatter['cor']
)

# Selecionar os 20 domínios mais relevantes
dados_scatter = dados_scatter.sort_values(by='frequencia', ascending=False)
top_n = 10
for i, row in dados_scatter.head(top_n).iterrows():
    plt.annotate(row['Dominio'], (row['score_ideologia'], row['frequencia']), fontsize=11)

pular_cada_n = 7
for i, row in dados_scatter[12:].iloc[::pular_cada_n].iterrows():
    if row['Dominio'] == '@FlavioBolsonaro' or row['Dominio'] == '@LulaOficial,':
        continue
    else:
        plt.annotate(row['Dominio'], (row['score_ideologia'], row['frequencia']), fontsize=11)

# Personalizar o gráfico
plt.title('Perfis mais relevantes nos Tweets Analisados', fontsize=12)
plt.xlabel('Polaridade', fontsize=12)
plt.ylabel('Frequência', fontsize=12)

# Definir barra de cores
sm = plt.cm.ScalarMappable(cmap=plt.cm.RdBu, norm=plt.Normalize(vmin=-1, vmax=1))
sm.set_array([])
cbar = plt.colorbar(sm)
cbar.set_label('Polaridade', fontsize=12)

# Exibir o gráfico
plt.grid(True)
plt.show()
