import datetime
from pymongo import MongoClient
import pandas as pd

class MyBudgetDatabase:
    def __init__(self, mongo_url='mongodb://localhost:27017/', database_name='myBudget'):
        self.mongo_url = mongo_url
        self.database_name = database_name
        self.client = MongoClient(self.mongo_url)
        self.db = self.client[self.database_name]
        
    def insert_log(self, event, collection):
        app_log = self.db[collection]
        datetime_log = datetime.datetime.now()
        log = {'Evento': event, 'timestamp': datetime_log}
        app_log.insert_one(log)
        
    def load_categories(self, collection):
        categories_data = list(self.db[collection].find({}, {'_id': 0, 'nome': 1}))
        categories_df = pd.DataFrame(categories_data)
        return categories_df
    
    def insert_category(self, collection, category):
        try:
            self.db[collection].insert_one({'nome': category})
                
            if collection=='categorias_receita':
                self.insert_log(f'Categoria de receita "{category}" inserida.', 'log_operacoes')
            elif collection=='categorias_despesa':
                self.insert_log(f'Categoria de despesa "{category}" inserida.', 'log_operacoes')
                
        except Exception as error:
            print(f'ERRO: {error}')
            self.insert_log(str(error), 'log_errors')
    
    def remove_category(self, collection, category):
        try:
            self.db[collection].delete_one({'nome': category})
            
            if collection=='categorias_receita':
                self.insert_log(f'Categoria de receita "{category}" removida.', 'log_operacoes')
            elif collection=='categorias_despesa':
                self.insert_log(f'Categoria de despesa "{category}" removida.', 'log_operacoes')

        except Exception as error:
            print(f'ERRO: {error}')
            self.insert_log(str(error), 'log_errors')
    
    def load_data(self, collection):
        data = None
        if collection in self.db.list_collection_names():
            cursor = self.db[collection].find({}, {'_id': 0})
            data = pd.DataFrame(list(cursor))
            if 'Data' in data.columns:
                data['Data'] = pd.to_datetime(data['Data'])
                data['Data'] = data['Data'].dt.date
                
                data = data[data['Descrição'] != '*transacao-inicial*']
            
            self.insert_log(f'Dados de {collection} carregados.', 'log_aplicacao')
        return data
            
    def insert_data(self, collection, valor, recebido, fixo, date, categoria, descricao):
        dados = {
            'Valor': valor, 
            'Recebido': recebido, 
            'Fixo': fixo, 
            'Data': date,
            'Categoria': categoria, 
            'Descrição': descricao
        }
        
        try:
            self.db[collection].insert_one(dados)
            
            if collection=='receitas':
                self.insert_log(f'Nova receita inserida.', 'log_operacoes')
            elif collection=='despesas':
                self.insert_log(f'Nova despesa inserida.', 'log_operacoes')
                
        except Exception as error:
            print(f'ERRO: {error}')
            self.insert_log(str(error), 'log_errors')