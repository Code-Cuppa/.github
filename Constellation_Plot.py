import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import astropy.units as u
from astropy.coordinates import SkyCoord
import os


## Make a bunch of RA, Dec, and Flux
ra   = [168.2, 168.21, 168.205, 168.211, 168.25, 168.08, 168.12, 168.23, 168.17]
dec  = [68.21, 68.2, 68.205, 68.211, 68.08, 68.12, 68.25, 68.23, 68.17]
flux = [1024,  8201, 4450,   1231,   9912,  3621,  8362,  4222,  3124]

## Turn it into a dictionary, then dataframe
df_dict = {'RA': ra, 'Dec': dec, 'flux': flux}
df = pd.DataFrame(df_dict)

## Miscellaneous Fixing and Definitions
df['flux'] = df['flux']**(1/3)
min_flux = min(df['flux'])
max_flux = max(df['flux'])
min_ra  = min(df['RA'])
max_ra  = max(df['RA'])
min_dec = min(df['Dec'])
max_dec = max(df['Dec'])

## ----- PLOTTING (With Plotly Go) -----

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x = df['RA'],
        y = df['Dec'],
        mode = 'markers',
        marker=dict(
            size = df['flux'],
            color="White",
            opacity=1,
            line = dict(
                width=1,
                color="navy"
            ),
        ),
        hovertemplate   =
            'RA: %{x:.3f}<br>' +
            'Dec: %{y:.3f}<br>' +
            'Flux: %{customdata[2]:.0f}<br>'
            ,
        customdata      =  [(df['RA'].iloc[i], df["Dec"].iloc[i], df["flux"].iloc[i]) for i in range(len(df['flux']))],
    )
)



## Add a white rectangle around all the points that's always visible, so that the plot limits remain the same
fig.add_shape(type="rect",
    x0=min_ra-0.05,
    x1=max_ra+0.05,
    y0=min_dec-0.05,
    y1=max_dec+0.05,
    line=dict(color="White"),
)

## Update the layout, including creating the slider
fig.update_layout(width=600, height=530,
    margin=dict(t=0, l=0, r=0, b=100),  # Set margins to reduce whitespace
    xaxis_title="RA",
    yaxis_title="Dec",
    plot_bgcolor='navy',
    showlegend=False,
    sliders=[{
        'active': 0,
        'currentvalue': {'prefix': 'Flux > '},
        'pad': {'t': 50},
        'steps': [
            {
                'method': 'update',
                'label': str(threshold),
                'args': [
                    {
                        'x': [
                            df["RA"][df["flux"] >= threshold],
                        ],
                        'y': [
                            df["Dec"][df["flux"] >= threshold],
                        ],
                        'hovertemplate': [
                            'RA: %{x:.3f}<br>' +
                            'Dec: %{y:.3f}<br>' +
                            'Flux: %{customdata[2]:.0f}<br>',
                        ],
                        'customdata': [
                            [(df['RA'].iloc[i], df["Dec"].iloc[i], df["flux"][df["flux"] >= threshold].iloc[i]) for i in range(len(df['flux'][df["flux"] >= threshold]))],
                        ],
                        'marker' : [
                            dict(
                                size = df['flux'][df["flux"] >= threshold],
                                color="White",
                                opacity=1,
                                line = dict(
                                    width=1,
                                    color="navy"
                                ),
                            ),
                        ],
                    },
                ]
            } for threshold in range(int(np.floor(min_flux)), int(np.ceil(max_flux)), 1)  # Adjust slider granularity as needed
        ]
    }],
)

fig.update_xaxes(gridcolor='darkslateblue')
fig.update_yaxes(gridcolor='darkslateblue')
fig.update_xaxes(autorange="reversed")

fig['layout']['sliders'][0]['pad']=dict(t=20,)

fig.write_html("../Outputs/Constellation_Plot.html")
