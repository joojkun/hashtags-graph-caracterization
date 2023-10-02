# Caracterização de Hashtags

## Introdução

Este código tem como objetivo criar um grafo de co-ocorrência de hashtags a partir de um conjunto de dados de tweets e, em seguida, caracterizar as hashtags não caracterizadas usando o algoritmo de Harmonic Function. Além disso, ele salva as hashtags caracterizadas em um arquivo CSV.

## Bibliotecas Utilizadas

O código utiliza várias bibliotecas Python, incluindo:

- `csv`: Para leitura e escrita de arquivos CSV.
- `re`: Para o uso de expressões regulares na extração de hashtags.
- `pandas`: Para a manipulação de dados em formato de tabela.
- `networkx`: Para criar e manipular grafos.
- `json`: Para leitura de dados em formato JSON.

## Funções Principais

O código é dividido em várias partes, incluindo a leitura de dados, a criação do grafo, a caracterização das hashtags e a escrita dos resultados em um arquivo CSV. Aqui estão as principais funções e o fluxo do código:

1. **`dicionario_csv(arquivo)`:** Esta função lê um arquivo CSV e retorna os dados em formato de dicionário, onde as chaves são da primeira coluna e os valores são da segunda coluna.

2. **`ler_json_e_transformar_em_lista(nome_arquivo)`:** Esta função lê um arquivo JSON e retorna os dados como uma lista. Verifica se os dados no arquivo JSON são uma lista antes de retornar.

3. **`extrair_hashtags(tweet_text)`:** Esta função extrai hashtags de um texto de tweet usando expressões regulares e retorna uma lista de hashtags encontradas.

4. **`data_set()`:** Esta função lê dados de vários arquivos JSON contendo tweets, extrai as hashtags de cada tweet e as armazena em um arquivo CSV chamado "dados.csv".

5. **Criação do Grafo:**
   - Um objeto `Graph` da NetworkX é criado para representar o grafo de co-ocorrência de hashtags.

6. **Iteração sobre os Dados:**
   - O código itera sobre cada linha do arquivo CSV "dados.csv", que contém tweets e suas hashtags associadas.
   - As hashtags são adicionadas como nós do grafo. Se uma hashtag já foi caracterizada manualmente, seu rótulo é atribuído ao nó.
   - Arestas são criadas entre todas as combinações de hashtags em um único tweet, e seus pesos são atualizados.

7. **Caracterização de Hashtags:**
   - O algoritmo de Harmonic Function é aplicado ao grafo para caracterizar as hashtags que ainda não foram caracterizadas manualmente.
   - Os rótulos previstos para as hashtags são armazenados na lista `predicted`.

8. **Salvando as Hashtags Caracterizadas em um CSV:**
   - As hashtags caracterizadas junto com seus rótulos são armazenadas na lista `lista_csv`.
   - Essas hashtags são escritas em um arquivo CSV chamado "nome_arquivo.csv".

## Uso do Código

Para utilizar o código, siga os seguintes passos:

1. Certifique-se de ter as bibliotecas necessárias instaladas em seu ambiente Python, como `csv`, `re`, `pandas`, `networkx`, e `json`.

2. Coloque os arquivos JSON contendo os tweets no mesmo diretório do código ou forneça os caminhos corretos para esses arquivos.

3. Execute a função `data_set()` para criar o arquivo CSV "dados.csv" a partir dos dados dos tweets.

4. Execute o restante do código para criar o grafo, caracterizar as hashtags e salvar os resultados em um arquivo CSV.

## Conclusão

Este código permite criar um grafo de co-ocorrência de hashtags a partir de tweets, caracterizar hashtags usando o algoritmo de Harmonic Function e salvar os resultados em um arquivo CSV. É útil para análises de redes sociais e classificação de hashtags com base em suas co-ocorrências em tweets. Certifique-se de personalizar o código de acordo com seus próprios dados e requisitos específicos.
