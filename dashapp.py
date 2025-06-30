import dash
from dash import Dash, html, dcc, Output, Input, callback_context, State
import dash_bootstrap_components as dbc
from plot_functions.cum_percentage import plot_cumulative_percentage
from plot_functions.pie_chart import plot_organ_distribution_by_species
from plot_functions.display_images import _get_species_images_by_organ, plot_images
from plot_functions.projection import plot_umap
import pandas as pd

import numpy as np
import ast

from io import BytesIO
import base64

TRAIN_PATH_CSV = "datasource/train_metadata (1).csv"
EMBEDDINGS_PATH = "datasource/embeddings_zip.csv"

df = pd.read_csv(f"{TRAIN_PATH_CSV}", index_col=0)

embeddings_df = pd.read_csv(f"{EMBEDDINGS_PATH}")

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY]
)
server = app.server

p1 = dbc.Container(fluid=True, children=[
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='cumulative-fig', style={"marginBottom": '0px',  'maxWidth': '800px'}, config={'displayModeBar': False}),
            html.Div([
                dbc.Button("Genus", id="btn-genus", n_clicks=0, style={"marginRight": "10px", 'marginTop': '0px', "marginLeft": "60px"}),
                dbc.Button("Family", id="btn-family", n_clicks=0, style={"marginRight": "10px", 'marginTop': '0px'}),
                dbc.Button("Species", id="btn-species", n_clicks=0, style={'marginTop': '0px'}),
            ], className='d-flex flex-wrap justify-content-start', style={"marginTop": '5px'}),
        ],xs=12, md=12, lg={"size": 7, "offset": 1}),
        
        dbc.Col([
            html.Div(
                id='table-container',
                style={"maxHeight": "500px", "overflowY": "auto", 'marginTop': "15px", "paddingLeft": '10px', "maxWidth": '300px'},
            )
        ], xs=12, md=12, lg=4), 
    ], className='g-0', style={"marginBottom": "30px"}),
])

@app.callback(
    Output("cumulative-fig", "figure"),
    Output("table-container", "children"),
    Input("btn-genus", "n_clicks"),
    Input("btn-family", "n_clicks"),
    Input("btn-species", "n_clicks")
)

def update_outputs(btn_genus, btn_family, btn_species):
    
    triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]
    if triggered_id == "btn-genus":
        col = "genus"
    elif triggered_id == "btn-family":
        col = "family"
    elif triggered_id == "btn-species":
        col = "species"
    else:
        col = "species"
        
    cumulative_df, fig = plot_cumulative_percentage(df, col)
    view = cumulative_df[[col, 'value_counts']].sort_values(by='value_counts', ascending=False)

    table = dbc.Table.from_dataframe(
        view,
        striped=True,
        bordered=True,
        hover=True
    )
    
    return fig, table

p2 = dbc.Container(fluid=True, children=[
    dbc.Row([
        
        dbc.Col([
            
            html.Div([
                dcc.Store(id='species-store', data=[{"label": s, "value": s} for s in sorted(df["species"].unique())]),
                dbc.Input(
                    id="species-search-input",
                    placeholder="Input Species name...",
                    type="text",
                    debounce=False,
                    autoComplete="off",
                    style={"width": "80%", "margin": "0 auto", "marginBottom": "10px"}
                ),
                html.Div(id="species-suggestions", style={"width": "80%", "margin": "0 auto"}),
                
                dcc.Graph(
                id='organ-pie-chart',
                figure=plot_organ_distribution_by_species(df),
                style={'height': '450px'},
                config={'displayModeBar': False}        
            )
            
            ], style={'width': '100%', "textAlign": "center", "marginTop": "20px"}),
                

        ],  width={"size": 12, "offset": 1}, lg=4),
        
        dbc.Col([
            html.Div(
                id='images-organ-container',
                style={'maxHeight': '500px', 'overFlowY': 'auto', 'textAlign': 'center'}
            )
        ], width=12, lg=6),
        
    ], className='g-0', style={"marginTop": "70px"}),
        
])

@app.callback(
    Output("species-suggestions", "children"),
    Input("species-search-input", "value"),
    State("species-store", "data")
)

def update_suggestions(query, species_data):
    if not query:
        return ""
    
    # Filtrando as sugestões no cliente (bem mais rápido!)
    matches = [s for s in species_data if query.lower() in s['label'].lower()]
    
    # Limite de 5 sugestões
    return html.Ul([html.Li(s['label'], style={"cursor": "pointer"}) for s in matches[:5]])

@app.callback(
    Output("organ-pie-chart", "figure"),
    Output("images-organ-container", "children"),
    Input("species-search-input", "value")
)

def update_organ_section(selected_species):
    # 1) Gera fig do gráfico de torta
    fig_pie = plot_organ_distribution_by_species(df, species=selected_species)
    
    # 2) Se não há espécie, não mostra imagens
    if not selected_species:
        return fig_pie, "Nenhuma espécie selecionada"

    # 3) Se há espécie, gerar dataframe e figura matplotlib
    df_links = _get_species_images_by_organ(df, selected_species)
    fig_matplotlib = plot_images(df_links)

    # Converte fig_matplotlib em base64
    png_buffer = BytesIO()
    fig_matplotlib.savefig(png_buffer, format='png', bbox_inches='tight')
    png_buffer.seek(0)
    encoded_png = base64.b64encode(png_buffer.getvalue()).decode()

    # Monta um <img>
    img_component = html.Img(
        src=f"data:image/png;base64,{encoded_png}",
        style={"width": "90%", "maxHeight": "1000px"}
    )

    return fig_pie, img_component

embeddings_df['embeddings'] = embeddings_df['embeddings'].apply(lambda s: np.array(ast.literal_eval(s)).reshape(-1))
organs = embeddings_df['organ']
embeddings_array = np.stack(embeddings_df['embeddings'].values)
labels = np.array(embeddings_df['species'])

umap_fig = plot_umap(embeddings_array,
          organs,
          labels)

p3 = dbc.Container(fluid=True, children=[
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id="umap-static-fig",
                figure=umap_fig,
                style={'height': '500px'},
                config={'displayModeBar': False}
            )
        ], width={"size": 10, "offset": 1})
    ], className="g-0", style={"marginTop": "40px"})
])

# Layout principal
app.layout = html.Div([
    html.H1("PlantCLEF2025. CVPR-FGCV ", style={"textAlign": "center", "marginBottom": "30px"}),
    p1,
    p2,
    p3
])

if __name__ == "__main__":
    app.run(debug=False)
