import datetime
from pymongo import MongoClient
import pandas as pd

mongo_url = 'mongodb://localhost:27017/'

# Conectando ao MongoDB
client = MongoClient(mongo_url)
db = client['myBudget']

# Definindo logs
def insereLog(evento, collection):
    app_log = db[collection]

    datetime_log = datetime.datetime.now()
    
    log = {
        'evento': evento,
        'timestamp': datetime_log
    }
    
    app_log.insert_one(log)

# Inicializando categorias de receitas
try:
    # Populando categorias iniciais de receitas
    if db['categorias_receita'].count_documents({}) == 0:
        list_cat_receitas = ["Salário", "Rendimentos", "Vendas", "Cashback"]
        
        for categoria in list_cat_receitas:
            # Verificando se a categoria já existe na coleção
            if db['categorias_receita'].count_documents({'nome': categoria}) == 0:
                cat_receita = {
                    'nome': categoria
                }
                db['categorias_receita'].insert_one(cat_receita)
                
        insereLog('Categorias iniciais de receitas inseridas.', 'log_aplicacao')
except Exception as error:
    print(f'Ocorreu o seguinte erro: {error}')
    insereLog(error, 'log_errors')

# Inicializando categorias de despesas
try:
    # Populando categorias iniciais de despesas
    if db['categorias_despesa'].count_documents({}) == 0:
        list_cat_despesas = ["Alimentação", "Aluguel", "Água", "Luz", "Combustível", "Saúde", "Lazer"]
        
        for categoria in list_cat_despesas:
            # Verificando se a categoria já existe na coleção
            if db['categorias_despesa'].count_documents({'nome': categoria}) == 0:
                cat_despesa = {
                    'nome': categoria
                }
                db['categorias_despesa'].insert_one(cat_despesa)
                
        insereLog('Categorias iniciais de despesas inseridas.', 'log_aplicacao')
except Exception as error:
    print(f'Ocorreu o seguinte erro: {error}')
    insereLog(error, 'log_errors')

# Inicializando collection de receitas
try:
    # Criando DataFrames vazios
    data_structure = {'Valor': [0], 'Recebido': [1], 'Fixo': [0], 'Data': [datetime.datetime.strptime('1900-01-01', '%Y-%m-%d')], 'Categoria': [''], 'Descrição': ['*transacao-inicial*']}
        
    df_receitas = pd.DataFrame(data_structure)
        
    # Salvando o DataFrame de despesas no MongoDB
    db['receitas'].insert_many(df_receitas.to_dict('records'))
        
    insereLog('Coleção de receitas criada.', 'log_aplicacao')
except Exception as error:
    print(f'Erro ao criar collection de receitas: {error}')
    insereLog(error, 'log_errors')

# Inicializando collection de despesas   
try:
    # Criando DataFrames vazios
    data_structure = {'Valor': [0], 'Recebido': [1], 'Fixo': [0], 'Data': [datetime.datetime.strptime('1900-01-01', '%Y-%m-%d')], 'Categoria': [''], 'Descrição': ['*transacao-inicial*']}
        
    df_despesas = pd.DataFrame(data_structure)
        
    # Salvando o DataFrame de despesas no MongoDB
    db['despesas'].insert_many(df_despesas.to_dict('records'))
        
    insereLog('Coleção de despesas criada.', 'log_aplicacao')  
    
except Exception as error:
    print(f'Erro ao criar collection de despesas: {error}')
    insereLog(error, 'log_errors')
    
insereLog('Aplicação inicializada!', 'log_aplicacao')