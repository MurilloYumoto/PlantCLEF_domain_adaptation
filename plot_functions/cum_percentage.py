import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_cumulative_percentage(df, column, color="#533e2d"):
    """
    Gera um gráfico de linha da porcentagem acumulativa de uma variável categórica.

    Parâmetros:
        df (DataFrame): dataframe com a coluna categórica
        column (str): nome da coluna categórica
        color (str): cor da linha no gráfico (hex)

    Retorna:
        cumulative_df (DataFrame): dataframe com contagem, % individual e % acumulada
        fig (plotly Figure): figura do gráfico de linha gerado
    """
    value_counts = df[column].value_counts(ascending=True)
    total = value_counts.sum()
    individual_percentage = (value_counts / total) * 100
    cumulative_percentage = individual_percentage.cumsum()

    cumulative_df = pd.DataFrame({
        column: value_counts.index,
        'individual_percentage': individual_percentage.values,
        'cumulative_percentage': cumulative_percentage.values,
        'value_counts': value_counts.values,
        'index': range(len(value_counts))
    }).reset_index(drop=True)

    fig = px.line(
        cumulative_df,
        x="index",
        y="cumulative_percentage",
        hover_data={
            column: True,
            "value_counts": True,
            "cumulative_percentage": ':.2f',
            "index": False
        },
        labels={"cumulative_percentage": "Cumulative %",
                "index": f"{column} Rank (ascending)"},
        title=f"Cumulative Percentage of {column} Frequency",
        color_discrete_sequence=[color],
    )

    n_cats = len(value_counts)
    perfect_balanced = [(i+1)/n_cats*100 for i in range(n_cats)]

    fig.add_trace(
        go.Scatter(
            x=cumulative_df['index'],
            y=perfect_balanced,
            mode='lines',
            name="Perfect Balanced Distribution",
            line=dict(dash='dash', color='gray')
        )
    )

    fig.update_layout(
        template='plotly_white',
        title_x = 0.43,
        yaxis_title="Cumulative Percentage (%)",
        xaxis_title=f"{column} Rank (ascending)",
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        xaxis=dict(
            tickfont=dict(color="black"),
            title=dict(text=f"{column} Rank (ascending)", font=dict(color="black"))
        ),
        yaxis=dict(
            tickfont=dict(color="black"),
            title=dict(text="Cumulative Percentage (%)", font=dict(color="black"))
        ),
        # width=1100,
        height=500
    )
    return cumulative_df, fig