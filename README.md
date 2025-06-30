## Classificação Multi-rótulo de Espécies Vegetais a Partir da Adaptação de Domínio Multi-classe

Este repositório contém a implementação e visualizações relacionadas ao projeto de classificação multi-rótulo de espécies vegetais com adaptação de domínio a partir de uma tarefa originalmente multi-classe.

#### Como Rodar o Aplicativo Dash

Para executar o aplicativo Dash, siga os passos abaixo:

Clone este repositório localmente:

git clone <URL_DO_REPOSITÓRIO>
cd <DIRETÓRIO_DO_REPOSITÓRIO>

Instale as dependências necessárias:

Certifique-se de que possui o Python instalado (recomendado Python 3.9+). Em seguida, instale as bibliotecas necessárias com o seguinte comando:

pip install -r requirements.txt

Execute o aplicativo Dash:

python dashapp.py

Após executar o comando acima, o aplicativo estará disponível em:

http://127.0.0.1:8050

#### Dados do Aplicativo Dash

O aplicativo Dash utiliza dois arquivos de dados principais:

train_metadata (1).csv:

Uma subamostra aleatória com aproximadamente 140 mil exemplares (cerca de 10% da base total original). A subamostragem foi realizada devido à limitação de tamanho para upload de arquivos no GitHub.

embeddings_zip.csv:

Contém embeddings gerados para uma pequena parcela de espécies vegetais específicas, escolhidas por possuírem exemplares com todos os órgãos representados. Esse dataset é usado exclusivamente para a visualização UMAP presente no relatório.
