import numpy as np
import plotly.graph_objects as go
import plotly.express as px 
import umap


def plot_umap(embeddings: np.array,
              organs: np.array,
              labels: np.array,
              random_state=None):
  
  
  colors = px.colors.qualitative.Dark24
  reducer = umap.UMAP(n_components=2, random_state=random_state)
  emb_2d = reducer.fit_transform(embeddings)

  fig = go.Figure()

  unique_labels = np.unique(labels)
  for i, lbl in enumerate(unique_labels):
        mask = (labels == lbl)
        fig.add_trace(go.Scatter(
            x=emb_2d[mask, 0],
            y=emb_2d[mask, 1],
            mode='markers',
            name=str(lbl),
            text=organs[mask],
            hoverinfo='text+name',
            marker=dict(
                color=colors[i % len(colors)],
            ),
        ))

    # 4) Layout básico
  fig.update_layout(
      title="UMAP 2D Embedding Projection",
      template="plotly_white",
      xaxis_title="UMAP-1",
      yaxis_title="UMAP-2",
      
  )

  return fig