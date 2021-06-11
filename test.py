'''import plotly.graph_objects as go

# Generate example data
import numpy as np
np.random.seed(1)

x = np.random.uniform(low=3, high=6, size=(500,))
y = np.random.uniform(low=3, high=6, size=(500,))

# Build figure
fig = go.Figure()

# Add scatter trace with medium sized markers
fig.add_trace(
    go.Scatter(
        mode='markers',
        x=x,
        y=y,
        marker=dict(
            color='LightSkyBlue',
            size=20,
            
            line=dict(
                color='MediumPurple',
                width=2
            )
        ),
        showlegend=False
    )
)

# Add trace with large marker
fig.add_trace(
    go.Scatter(
        mode='markers',
        x=[2],
        y=[4.5],
        marker=dict(
            color='LightSkyBlue',
            size=120,
            line=dict(
                color='MediumPurple',
                width=12
            )
        ),
        showlegend=False
    )
)

fig.show()'''
    
    
