import dash
from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from app import app

graph_margin = dict(l=25, r=25, t=25, b=0)

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4('Total de despesas', style={'text-align': 'center'}),
                    html.Legend('R$ -', id='valor_despesa_card', style={'font-size': '60px', 'text-align': 'center'})
                    
                ], style={'text-alighn': 'center', 'padding-top': '30px'})
            )
        ], width=12)
    ]),
    dbc.Row([
        #html.Legend('Tabela de Despesas'),
        html.Div(id='tabela-despesas', className='dbc',style={"margin-top": "10px"})
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph', style={'margin-right': '20px'})
        ], width = 12)
    ])
    
                    # #Datepicker de análise por período
                    # html.Legend("Período de Análise", style={"margin-top": "10px"}),
                    # dcc.DatePickerRange(
                    #     month_format='Do MMM, YY',
                    #     end_date_placeholder_text='Data...',
                    #     start_date=start_date,
                    #     end_date=end_date,
                    #     display_format='DD-MM-YYYY',
                    #     with_portal=True,
                    #     updatemode='singledate',
                    #     id='date-picker-config',
                    #     style={'z-index': '100'})
                    # #start_date = datetime(data_atual.year, data_atual.month, 1)
    
], style={'padding': '10px'})

# =========  Callbacks  =========== #
# Tabela
@app.callback(
    Output('tabela-despesas', 'children'),
    Input('store-despesas', 'data')
)
def imprimir_tabela (data):
    df = pd.DataFrame(data)
    df['Data'] = pd.to_datetime(df['Data']).dt.date

    df.loc[df['Recebido'] == 0, 'Recebido'] = 'Não'
    df.loc[df['Recebido'] == 1, 'Recebido'] = 'Sim'

    df.loc[df['Fixo'] == 0, 'Fixo'] = 'Não'
    df.loc[df['Fixo'] == 1, 'Fixo'] = 'Sim'

    df = df.fillna('-')
    
    df['Data'] = pd.to_datetime(df['Data']).dt.strftime('%d-%m-%Y')

    df.sort_values(by='Data', ascending=True)
    
    ordem_colunas = ['Descrição', 'Categoria', 'Data', 'Valor', 'Recebido', 'Fixo']
    
    tabela = dash_table.DataTable(
        id='datatable-interactivity',
        
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": False} for i in ordem_colunas
        ],

        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,           
        page_size=10                       
    ),

    return tabela

# Bar Graph            
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('store-despesas', 'data')
    #Input(ThemeChangerAIO.ids.radio("theme"), "value")
    ]
)
def bar_chart(data):
    df = pd.DataFrame(data)   
    df_grouped = df.groupby("Categoria").sum()[["Valor"]].reset_index()
    
    graph = px.bar(df_grouped, x='Categoria', y='Valor', title="Despesas Gerais")
    
    #graph.update_layout(template=template_from_url(theme))
    graph.update_layout(margin=graph_margin, height=290)
    graph.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    return graph

# Simple card
@app.callback(
    Output('valor_despesa_card', 'children'),
    Input('store-despesas', 'data')
)
def display_desp(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    
    return f"R$ {valor}"