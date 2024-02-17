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

# ========= Layout ========= #
layout = dbc.Col([
                html.H1("MyBudget", className='text-primary'),
                html.P("by ASIMOV", className='text-info'),
                html.Hr(),
    
    # Seção de Perfil
                dbc.Button(id='botao_avatar',
                           children=[html.Img(src='/assets/img_hom.png', id='avatar_change', alt='Avatar', className='perfil_avatar')
                                     ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
    
    # Seção Lançamento de Receitas/Despesas
                dbc.Row([
                    dbc.Col([dbc.Button(color='success', id='open-novo-receita', children=['+ Receita'])], width=6),
                    dbc.Col([dbc.Button(color='danger', id='open-novo-despesa', children=['- Despesa'])], width=6)
                ]),
                
    # Seção de Navegação
                html.Hr(),
                
                dbc.Nav(
                    [
                        dbc.NavLink("Dashboard", href="/dashboards", active="exact"),
                        dbc.NavLink("Extratos", href="/extratos", active="exact"),
                    ], vertical=True, pills=True, id='nav_buttons', style={"margin-bottom": "50px"}),
                
                #ThemeChangerAIO(aio_id="theme", radio_props={"value":dbc.themes.QUARTZ})
    
            
], id='sidebar_completa')

    
    


# =========  Callbacks  =========== #
# Pop-up receita