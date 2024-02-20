import pandas as pd
import os

# Caminhos dos diretórios de dados (receitas/despesas e categorias de receitas/despesas)
dir_receitas = os.path.join('data', 'receitas')
dir_despesas = os.path.join('data', 'despesas')

dir_cat_receita = os.path.join('data', 'categorias-receita')
dir_cat_despesa = os.path.join('data', 'categorias-despesa')

diretorios = [dir_receitas, dir_despesas, dir_cat_receita, dir_cat_despesa]

# Cria os diretórios se não existirem
for diretorio in diretorios:
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

# Se os arquivos de receitas/despesas já existirem, faz a leitura.
if ('df_receitas.csv' in os.listdir('data') and ('df_despesas.csv' in os.listdir('data'))):
    df_receitas = pd.read_csv(os.path.join(dir_receitas, 'df_receitas.csv'), index_col=0, parse_dates=True)
    df_despesas = pd.read_csv(os.path.join(dir_despesas, 'df_despesas.csv'), index_col=0, parse_dates=True)

# Se não existirem, faz a criação.
else:
    # Estrutura de dados contendo dicionários com listas vazias 
    data_structure = {
        'Valor': [],
        'Efetuado': [],
        'Fixo': [],
        'Data': [],
        'Categoria': [],
        'Descricao': []
    }
    # Cria um dataFrame de receitas/despesas
    df_receitas = pd.DataFrame(data_structure)
    df_despesas = pd.DataFrame(data_structure)

    # Exporta o dataFrame de receitas/despesas para .CSV
    df_receitas.to_csv(os.path.join(dir_receitas, 'df_receitas.csv'))
    df_despesas.to_csv(os.path.join(dir_despesas, 'df_despesas.csv'))
    
    # Exporta o dataFrame de receitas/despesas para .JSON
    df_receitas.to_json(os.path.join(dir_receitas, 'df_receitas.json'))
    df_despesas.to_json(os.path.join(dir_despesas, 'df_despesas.json'))
    
    # Exporta o dataFrame receitas/despesas para .SQL
    # df_receitas.to_sql(os.path.join(dir_receitas, 'df_receitas.sql'))
    # df_despesas.to_sql(os.path.join(dir_despesas, 'df_despesas.sql'))  

# Se o arquivo de categorias já existir, faz a leitura.
if ('df_cat_receita.csv' in os.listdir('data') and ('df_cat_despesa.csv' in os.listdir('data'))):
    df_cat_receitas = pd.read_csv(os.path.join(dir_cat_receita, 'df_cat_receitas.csv'), index_col=0, parse_dates=True)
    df_cat_despesas = pd.read_csv(os.path.join(dir_cat_despesa, 'df_cat_despesas.csv'), index_col=0, parse_dates=True)
    
    # cat_receita = df_cat_receita.values.tolist()
    # cat_despesa = df_cat_despesa.values.tolist()
    
# Se não existir, faz a criação de um dicionário de categorias para receitas/despesas.
else:
    cat_receita = {'Categoria': ['Salário', 'Venda', 'Investimentos', 'Cashback']}
    cat_despesa = {'Categoria': ['Alimentação', 'Aluguel', 'Água', 'Luz', 'Saúde', 'Lazer']}
    
    # Cria um dataframe de categorias de receitas/despesas.
    df_cat_receita = pd.DataFrame(cat_receita)
    df_cat_despesa = pd.DataFrame(cat_despesa)
    
    # Exporta o dataFrame de categorias para .CSV
    df_cat_receita.to_csv(os.path.join(dir_cat_receita, 'df_cat_receita.csv'))
    df_cat_despesa.to_csv(os.path.join(dir_cat_despesa, 'df_cat_despesa.csv'))
    
    # Exporta o dataFrame de categorias para .JSON
    df_cat_receita.to_json(os.path.join(dir_cat_receita, 'df_cat_receita.json'))
    df_cat_despesa.to_json(os.path.join(dir_cat_despesa, 'df_cat_despesa.json'))
    
    # Exporta o dataFrame de categorias para .SQL
    # df_cat_receita.to_sql(os.path.join(dir_cat_receita, 'df_cat_receita.sql'))
    # df_cat_despesa.to_sql(os.path.join(dir_cat_despesa, 'df_cat_despesa.sql')) 