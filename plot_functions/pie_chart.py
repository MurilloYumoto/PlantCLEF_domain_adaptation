import plotly.graph_objects as go

def plot_organ_distribution_by_species(df, species=None, species_col="species"):
    """
    Gera um gráfico de pizza da distribuição dos órgãos para uma espécie específica,
    ou para o dataset inteiro se nenhuma espécie for informada.

    Parâmetros:
        df (pd.DataFrame): dataframe com as colunas 'organ' e 'species'
        species (str, opcional): nome da espécie a ser filtrada
        species_col (str): nome da coluna com os identificadores de espécie

    Retorna:
        fig (plotly.graph_objects.Figure): gráfico de pizza
    """
    
    colors = ['#242331', "#533e2d", "#a27035",
              "#b88b4a", "#ddca7d", "#735751", "#c6a677"]

    # Filtra se species for passada
    if species:
        df_filtered = df[df[species_col] == species]
    else:
        df_filtered = df

    # Conta os órgãos
    organ_counts = df_filtered['organ'].value_counts()

    # Cria a figura
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=organ_counts.index,
        values=organ_counts.values,
        hole=0.5,
        textinfo='percent+label',
        domain=dict(x=[0, 1], y=[0, 1]),
        marker=dict(colors=colors, line=dict(color='white', width=1)),
        textfont=dict(color='black')
    ))

    fig.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        height=500,
        margin=dict(t=50, b=50, l=0, r=0),
        
    )

    return fig