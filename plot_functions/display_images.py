import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import matplotlib
matplotlib.use('Agg') 

import matplotlib.pyplot as plt


def _get_species_images_by_organ(df, specie, random_choice=False):
    """
    Dado um gbif_species_id, retorna um DataFrame com uma imagem por tipo de organ,
    contendo as colunas 'organ', 'url' e 'image_backup_url'.

    Parâmetros:
        df (DataFrame): dataframe com colunas 'gbif_species_id', 'organ', 'url', 'image_backup_url'
        gbif_species_id (int ou str): ID da espécie a ser buscada
        random_choice (bool): Se True, seleciona uma imagem aleatória por órgão; caso contrário, pega a primeira.

    Retorna:
        DataFrame com colunas: 'organ', 'url', 'image_backup_url'
    """
    # Filtra apenas a espécie desejada
    especie_df = df[df['species'] == specie]

    if random_choice:
        # Seleciona uma amostra aleatória por órgão
        resultado = (
            especie_df
            .groupby('organ', as_index=False)
            .apply(lambda x: x.sample(1))
            .reset_index(drop=True)[['organ', 'url', 'image_backup_url']]
        )
    else:
        # Seleciona a primeira ocorrência por órgão
        resultado = (
            especie_df
            .sort_values('organ')  # opcional: ordena pelos órgãos
            .groupby('organ', as_index=False)[['url', 'image_backup_url']].first()
        )

    return resultado

def plot_images(df_links):
    """
    Recebe um DataFrame com colunas 'organ', 'url', 'image_backup_url',
    baixa as imagens e as exibe em duas linhas (4 imagens na primeira, 3 na segunda).
    """
    imagens = []
    legendas = []

    for _, row in df_links.iterrows():
        organ = row['organ']
        urls = [row['url'], row['image_backup_url']]

        imagem = None
        for url in urls:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    imagem = Image.open(BytesIO(response.content)).convert('RGB')
                    break
            except Exception:
                continue

        if imagem:
            imagens.append(imagem)
            legendas.append(organ)

    n = len(imagens)
    if n == 0:
        print("Nenhuma imagem foi carregada com sucesso.")
        return

    # Define número de colunas por linha
    ncols = [3, 3, 1]  # 4 imagens na primeira linha, 3 na segunda
    nrows = len(ncols)

    fig, axs = plt.subplots(nrows, max(ncols), figsize=(4 * max(ncols), 4 * nrows))

    # Flatten axes para facilitar indexação
    axs = axs.flatten()

    for i in range(len(axs)):
        if i < n:
            axs[i].imshow(imagens[i])
            axs[i].axis('off')
            axs[i].set_title(legendas[i], fontsize=12)
        else:
            axs[i].axis('off')  # esconde eixos vazios

    plt.tight_layout()

    return fig