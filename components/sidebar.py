import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd

from myBudgetDB import *

my_budget_db = MyBudgetDatabase()

cat_receita = my_budget_db.load_categories("categorias_receita")
cat_receita = cat_receita['nome'].tolist()

cat_despesa = my_budget_db.load_categories("categorias_despesa")
cat_despesa = cat_despesa['nome'].tolist()

# ========= Layout ========= #
layout = dbc.Col([
    
    # Seção Logo
    dcc.Link(html.Img(src='assets/myBudget-logo.png', className='imagem-classe', style={'text-align': 'center'}), href='/'),
    
    # Separador
    html.Hr(), 
    
    # Seção imagem de perfil
    dbc.Row([
        html.Img(src="/assets/img_hom.png", id="avatar_change", alt="Avatar", className='perfil_avatar')
    ]),
    
    html.Div([
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                html.A('Alterar imagem')
            ]),
             style={
                 'textAlign': 'center',
                 'text-decoration': 'underline'
             },
            multiple=False
        ),
    ]),
    
    # Separador
    html.Hr(),
    
    # Seção de Navegação
    dbc.Nav([
        dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
        dbc.NavLink("Extratos de Receitas", href="/extratos-receitas", active="exact"),
        dbc.NavLink("Extratos de Despesas", href="/extratos-despesas", active="exact"),
        ], vertical=True, pills=True, id='nav_buttons'),
    
    # Separador
    html.Hr(style={"margin-bottom": "20px"}),
    
    # Seção Lançamento de Receitas/Despesas
    dbc.Row([
        dbc.Col([dbc.Button(color='success', id='open-novo-receita', children=['+ Receita'])], width=6, className='d-flex justify-content-center'),
        dbc.Col([dbc.Button(color='danger', id='open-novo-despesa', children=['- Despesa'])], width=6, className='d-flex justify-content-center')
        ]),
    
    # Modal Receita
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Adicionar receita')),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Descrição'),
                    dbc.Input(placeholder='Ex.: Salário, Rendimentos, etc...', id='txt-receita'),
                    ], width=6),
                dbc.Col([
                    dbc.Label('Valor: '),
                    dbc.Input(placeholder='R$100,00', id='valor_receita', value='')
                    ], width=6)
                ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Label("Data: "),
                    dcc.DatePickerSingle(id='date-receitas',
                                         min_date_allowed=date(2020, 1, 1),
                                         max_date_allowed=date(2030, 12, 31),
                                         date=datetime.datetime.today(),
                                         style={"width": "100%"}
                                         ),
                    ], width=4),
                
                dbc.Col([
                    dbc.Label("Extras"),
                    dbc.Checklist(
                        options=[
                            {"label": "Foi recebida", "value": 1},
                            {"label": "Receita Recorrente", "value": 2}],
                        value=[1],
                        id="switches-input-receita",
                        switch=True),
                    ], width=4),
                
                dbc.Col([
                    html.Label("Categoria da receita"),
                    dbc.Select(id="select_receita", options=[{'label': i, 'value': i} for i in cat_receita], value=cat_receita[0])
                    ], width=4)
                
                ], style={"margin-top": "25px"}),
            
            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(children=[
                        dbc.Row([
                            dbc.Col([
                                html.Legend("Adicionar categoria", style={'color': 'green'}),
                                
                                dbc.Input(type="text", placeholder="Nova categoria...", id="input-add-receita", value=""),
                                
                                html.Br(),
                                
                                dbc.Button("Adicionar", className="btn btn-success", id="add-category-receita", style={"margin-top": "20px"}),
                                
                                html.Br(),
                                
                                html.Div(id="category-div-add-receita", style={}),
                                ], width=6),
                            
                            dbc.Col([
                                html.Legend("Excluir categorias", style={'color': 'red'}),
                                
                                dbc.Checklist(
                                    id="checklist-selected-style-receita",
                                    options=[{"label": i, "value": i} for i in cat_receita],
                                    value=[],
                                    label_checked_style={"color": "red"},
                                    input_checked_style={"backgroundColor": "#fa7268", "borderColor": "#ea6258"},
                                    ),
                                
                                dbc.Button("Remover", color="warning", id="remove-category-receita", style={"margin-top": "20px"}),
                                ], width=6)
                            ]),
                        ], title="Adicionar/Remover Categorias"),
                    ], flush=True, start_collapsed=True, id='accordion-receita'),
                
                html.Div(id="id_teste_receita", style={"padding-top": "20px"}),
                dbc.ModalFooter([
                    dbc.Button("Adicionar Receita", id="salvar_receita", color="success"),
                    dbc.Popover(dbc.PopoverBody("Receita Salva!"), target="salvar_receita", placement="left", trigger="click"),
                    ])
                ], style={"margin-top": "25px"}),  
            ])
        ],
              id='modal-novo-receita',
              style={"background-color": "rgba(17, 140, 79, 0.05)"},
              size='lg',
              is_open=False,
              centered=True,
              backdrop=True
              ),
    
    # Modal Despesa
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Adicionar despesa')),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Descrição'),
                    dbc.Input(placeholder='Ex.: Contas de água/luz, cartão de crédito, supermercado, etc...', id='txt-despesa'),
                    ], width=6),
                
                dbc.Col([
                    dbc.Label('Valor: '),
                    dbc.Input(placeholder='R$100,00', id='valor_despesa', value='')
                    ], width=6)
                ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Label("Data: "),
                    dcc.DatePickerSingle(id='date-despesas',
                                         min_date_allowed=date(2020, 1, 1),
                                         max_date_allowed=date(2030, 12, 31),
                                         date=datetime.datetime.today(),
                                         style={"width": "100%"}
                                         ),
                    ], width=4),
                
                dbc.Col([
                    dbc.Label("Extras"),
                    dbc.Checklist(
                        options=[{"label": "Foi recebida", "value": 1}, {"label": "Despesa Recorrente", "value": 2}],
                        value=[1],
                        id="switches-input-despesa",
                        switch=True),
                    
                    ], width=4),
                
                dbc.Col([
                    html.Label("Categoria da despesa"),
                    dbc.Select(id="select_despesa", options=[{'label': i, 'value': i} for i in cat_despesa], value=cat_despesa[0])
                    ], width=4)
                
                ], style={"margin-top": "25px"}),
            
            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(children=[
                        dbc.Row([
                            dbc.Col([
                                html.Legend("Adicionar categoria", style={'color': 'green'}),
                                dbc.Input(type="text", placeholder="Nova categoria...", id="input-add-despesa", value=""),
                                html.Br(),
                                dbc.Button("Adicionar", className="btn btn-success", id="add-category-despesa", style={"margin-top": "20px"}),
                                html.Br(),
                                html.Div(id="category-div-add-despesa", style={}),
                                ], width=6),
                            
                            dbc.Col([
                                html.Legend("Excluir categorias", style={'color': 'red'}),
                                dbc.Checklist(
                                    id="checklist-selected-style-despesa",
                                    options=[{"label": i, "value": i} for i in cat_despesa],
                                    value=[],
                                    label_checked_style={"color": "red"},
                                    input_checked_style={"backgroundColor": "#fa7268", "borderColor": "#ea6258"},
                                    ),
                                
                                dbc.Button("Remover", color="warning", id="remove-category-despesa", style={"margin-top": "20px"}),
                                ], width=6)
                            ]),
                        
                        ], title="Adicionar/Remover Categorias"),
                    
                    ], flush=True, start_collapsed=True, id='accordion-despesa'),
                
                html.Div(id="id_teste_despesa", style={"padding-top": "20px"}),
                dbc.ModalFooter([
                    dbc.Button("Adicionar Despesa", id="salvar_despesa", color="success"),
                    dbc.Popover(dbc.PopoverBody("Despesa Salva!"), target="salvar_despesa", placement="left", trigger="click"),
                    ])
                ], style={"margin-top": "25px"}),
            ])
        ],
              id='modal-novo-despesa',
              style={"background-color": "rgba(17, 140, 79, 0.05)"},
              size='lg',
              is_open=False,
              centered=True,
              backdrop=True
              )
    
    #ThemeChangerAIO(aio_id="theme", radio_props={"value":dbc.themes.QUARTZ})       
], id='sidebar_completa')

# =========  Callbacks  =========== #
# Pop-up receita
@app.callback(
    Output("modal-novo-receita", "is_open"),
    Input("open-novo-receita", "n_clicks"),
    State("modal-novo-receita", "is_open")
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open

# Pop-up despesa
@app.callback(
    Output("modal-novo-despesa", "is_open"),
    Input("open-novo-despesa", "n_clicks"),
    State("modal-novo-despesa", "is_open")
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open

# Enviar Form receita

@app.callback(
    Output('store-receitas', 'data'),

    Input("salvar_receita", "n_clicks"),

    [
        State("txt-receita", "value"),
        State("valor_receita", "value"),
        State("date-receitas", "date"),
        State("switches-input-receita", "value"),
        State("select_receita", "value"),
        State('store-receitas', 'data')
    ]
)
def save_form_receita(n, descricao, valor, date, switches, categoria, dict_receitas):
    
    if n and not(valor == "" or valor == None):
        valor = round(float(valor), 2)
        date = pd.to_datetime(date)
        categoria = categoria[0] if type(categoria) == list else categoria

        recebido = 1 if 1 in switches else 0
        fixo = 0 if 2 in switches else 0
        
        my_budget_db.insert_data('receitas', valor, recebido, fixo, date, categoria, descricao)
        
    df_receitas = my_budget_db.load_data("receitas").to_dict()
    
    return df_receitas

# Enviar Form despesa
@app.callback(
    Output('store-despesas', 'data'),

    Input("salvar_despesa", "n_clicks"),

    [
        State("txt-despesa", "value"),
        State("valor_despesa", "value"),
        State("date-despesas", "date"),
        State("switches-input-despesa", "value"),
        State("select_despesa", "value"),
        State('store-despesas', 'data')
    ]
)
def save_form_despesa(n, descricao, valor, date, switches, categoria, dict_despesas):
    
    if n and not(valor == "" or valor == None):
        valor = round(float(valor), 2)
        date = pd.to_datetime(date)
        categoria = categoria[0] if type(categoria) == list else categoria

        recebido = 1 if 1 in switches else 0
        fixo = 0 if 2 in switches else 0
        
        my_budget_db.insert_data('despesas', valor, recebido, fixo, date, categoria, descricao)

    df_despesas = my_budget_db.load_data("despesas").to_dict()
    return df_despesas
    
# Adicionar/excluir categorias Receitas
@app.callback(
    [
        Output('select_receita', 'options'),
        Output('checklist-selected-style-receita', 'options'),
        Output('checklist-selected-style-receita', 'value'),
        Output('stored-cat-receitas', 'data')
    ],
    
    [
        Input('add-category-receita', 'n_clicks'),
        Input('remove-category-receita', 'n_clicks')
    ],
    
    [
        State('input-add-receita', 'value'),
        State('checklist-selected-style-receita', 'value'),
        State('stored-cat-receitas', 'data')
    ]
)
def add_category_receita(n, n2, txt, check_delete, data):

    cat_receita = my_budget_db.load_categories("categorias_receita")
    cat_receita = cat_receita['nome'].tolist()
    
    if n and not (txt == '' or txt == None):
        if txt not in cat_receita:
            my_budget_db.insert_category('categorias_receita', txt)
            cat_receita.append(txt)
    
    if n2 and check_delete:
        for categoria in check_delete:
            if categoria in cat_receita:
                my_budget_db.remove_category('categorias_receita', categoria)
                
                cat_receita.remove(categoria)
                
    #Atualizando opções para os componentes de saída    
    opt_receita = [{'label': i, 'value': i} for i in cat_receita]
    
    df_cat_receita = pd.DataFrame(cat_receita, columns=['Categoria'])
    
    data_return = df_cat_receita.to_dict()
    
    return [opt_receita, opt_receita, [], data_return]

# Adicionar/excluir categorias Despesas
@app.callback(
    [
        Output('select_despesa', 'options'),
        Output('checklist-selected-style-despesa', 'options'),
        Output('checklist-selected-style-despesa', 'value'),
        Output('stored-cat-despesas', 'data')
    ],
    
    [
        Input('add-category-despesa', 'n_clicks'),
        Input('remove-category-despesa', 'n_clicks')
    ],
    
    [
        State('input-add-despesa', 'value'),
        State('checklist-selected-style-despesa', 'value'),
        State('stored-cat-despesas', 'data')
    ]
)
def add_category_despesa(n, n2, txt, check_delete, data):
    
    cat_despesa = my_budget_db.load_categories("categorias_despesa")
    cat_despesa = cat_despesa['nome'].tolist()
    
    if n and not (txt == '' or txt == None):
        if txt not in cat_despesa:
            my_budget_db.insert_category('categorias_despesa', txt)
            cat_despesa.append(txt)
    
    if n2 and check_delete:
        for categoria in check_delete:
            if categoria in cat_despesa:
                my_budget_db.remove_category('categorias_despesa', categoria)
                
                cat_despesa.remove(categoria)
                
    #Atualizando opções para os componentes de saída    
    opt_despesa = [{'label': i, 'value': i} for i in cat_despesa]
    
    df_cat_despesa = pd.DataFrame(cat_despesa, columns=['Categoria'])
    
    data_return = df_cat_despesa.to_dict()
    
    return [opt_despesa, opt_despesa, [], data_return]

# Callback para abrir a janela de seleção de arquivo ao clicar no botão
@app.callback(Output('upload-image', 'style'),
              [Input('upload-button', 'n_clicks')])
def display_upload(n_clicks):
    if n_clicks is not None:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# Callback para exibir a imagem carregada
@app.callback(Output('uploaded-image', 'src'),
              [Input('upload-image', 'contents')])
def update_image(content):
    if content is not None:
        return content
    else:
        return '/assets/img_hom.png'
    
# Pop-up perfis
@app.callback(
    Output("modal-perfil", "is_open"),
    Input("botao_avatar", "n_clicks"),
    State("modal-perfil", "is_open")
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open