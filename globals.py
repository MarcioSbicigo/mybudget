import datetime
from pymongo import MongoClient
import pandas as pd

# URL do banco de dados MongoDb
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

# Buscando categorias de receitas e armazenando em um dataframe
categorias_receitas = list(db['categorias_receitas'].find({}, {'_id': 0, 'nome': 1}))
df_cat_receita = pd.DataFrame(categorias_receitas)

# Buscando categorias de despesas e armazenando em um dataframe
categorias_despesas = list(db['categorias_despesas'].find({}, {'_id': 0, 'nome': 1}))
df_cat_despesa = pd.DataFrame(categorias_despesas)
    
cat_receita = df_cat_receita.values.tolist()
cat_despesa = df_cat_despesa.values.tolist()

# Carrega as receitas do MongoDB
try:
    if 'receitas' in db.list_collection_names():
        # Buscar os dados das coleções
        cursor_receitas = db['receitas'].find({}, {'_id': 0})
        #cursor_receitas = db['receitas'].find({'Data': {'$gte': '1900-01-02'}}, {'_id': 0})
        
        # Converter os dados em DataFrames
        df_receitas = pd.DataFrame(list(cursor_receitas))
        
        # Converte a coluna 'Data' para datetime, assumindo que 'Data' é o nome da coluna
        df_receitas['Data'] = pd.to_datetime(df_receitas['Data'])
        
        # Ajusta para manter apenas a data
        df_receitas['Data'] = df_receitas['Data'].dt.date
        
        #df_receitas["Data"] = pd.to_datetime(df_receitas["Data"])
        #df_receitas["Data"] = df_receitas["Data"].apply(lambda x: x.date())
        
        insereLog('Dados de receitas carregados.', 'log_aplicacao')
except Exception as error:
    print(f'ERRO: {error}')
    insereLog(error, 'log_errors')

# Carrega as despesas do MongoDB
try:
    if 'despesas' in db.list_collection_names():
        # Buscar os dados das coleções
        cursor_despesas = db['despesas'].find({}, {'_id': 0})
        #cursor_despesas = db['despesas'].find({'Data': {'$gte': '1900-01-02'}}, {'_id': 0})
        
        # Converter os dados em DataFrames
        df_despesas = pd.DataFrame(list(cursor_despesas))
        
        # Converte a coluna 'Data' para datetime, assumindo que 'Data' é o nome da coluna
        df_despesas['Data'] = pd.to_datetime(df_despesas['Data'])
        
        # Ajusta para manter apenas a data
        df_despesas['Data'] = df_despesas['Data'].dt.date
        
        #df_despesas["Data"] = pd.to_datetime(df_despesas["Data"])
        #df_despesas["Data"] = df_despesas["Data"].apply(lambda x: x.date())
        
        insereLog('Dados de despesas carregados.', 'log_aplicacao')

except Exception as error:
    print(f'ERRO: {error}')
    insereLog(error, 'log_errors')

