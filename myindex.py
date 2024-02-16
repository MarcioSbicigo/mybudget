from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *
from components import dashboards, extratos, sidebar



# =========  Layout  =========== #
content = html.Div(id="page-content")

app.layout = dbc.Container(children=[
    # dcc.Store(id='store-receitas', data=df_receitas_aux),
    # dcc.Store(id="store-despesas", data=df_despesas_aux),
    # dcc.Store(id='stored-cat-receitas', data=list_receitas_aux),
    # dcc.Store(id='stored-cat-despesas', data=list_despesas_aux),
    
    dbc.Row([
        dbc.Col([
            dcc.Location(id="url"),
            sidebar.layout
        ], md=2),

        dbc.Col([
            html.Div(id="page-content")
        ], md=10),
    ])

], fluid=True, style={"padding": "0px"}, className="dbc")


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/" or pathname == "/dashboards":
        return dashboards.layout

    if pathname == "/extratos":
        return extratos.layout
        

if __name__ == '__main__':
    app.run_server(debug=True)