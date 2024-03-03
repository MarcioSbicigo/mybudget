from dash import html, dcc
import dash
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *
from myBudgetDB import *
from components import dashboard, extratosReceitas, extratosDespesas, sidebar

my_budget_db = MyBudgetDatabase()

df_receitas  = my_budget_db.load_data("receitas")
df_despesas  = my_budget_db.load_data("despesas")
cat_receitas = my_budget_db.load_categories("categorias_receita")
cat_despesas = my_budget_db.load_categories("categorias_despesa")

# =========  Layout  =========== #
content = html.Div(id="page-content")

app.layout = dbc.Container(children=[
    dcc.Store(id='store-receitas', data=df_receitas.to_dict()),
    dcc.Store(id='store-despesas', data=df_despesas.to_dict()),
    dcc.Store(id='stored-cat-receitas', data=cat_receitas.to_dict()),
    dcc.Store(id='stored-cat-despesas', data=cat_despesas.to_dict()),
    
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
    if pathname == "/" or pathname == "/dashboard":
        return dashboard.layout

    if pathname == "/extratos-receitas":
        return extratosReceitas.layout
    
    if pathname == "/extratos-despesas":
        return extratosDespesas.layout

if __name__ == '__main__':
    app.run_server(debug=True)

if __name__ == '__main__':
    #app.run_server(host='0.0.0.0', debug=True)
    app.run_server(debug=True)