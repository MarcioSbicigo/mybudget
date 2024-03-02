from mybudgetDB import *

if __name__ == "__main__":
    # Instanciando a classe MyBudgetDatabase
    my_budget_db = MyBudgetDatabase()

    # Inserindo um log
    my_budget_db.insert_log("Aplicação iniciada.", "log_aplicacao")

    # Carregando categorias de receitas
    categories_revenue = my_budget_db.load_categories("categorias_receitas")
    print("Categorias de Receitas:")
    print(categories_revenue)

    # Carregando categorias de despesas
    categories_expense = my_budget_db.load_categories("categorias_despesas")
    print("Categorias de Despesas:")
    print(categories_expense)

    # Carregando dados de receitas
    revenue_data = my_budget_db.load_data("receitas")
    print("Dados de Receitas:")
    print(revenue_data)

    # Carregando dados de despesas
    expense_data = my_budget_db.load_data("despesas")
    print("Dados de Despesas:")
    print(expense_data)

    # Inserindo novos dados de receitas
    new_revenue_data = [
        {"valor": 100.0, "recebido": 1, "fixo": 0, "Data": datetime.date(2024, 2, 20), "categoria": "Salário", "descricao": "Primeiro salário do mês"}
    ]
    my_budget_db.insert_data("receitas", new_revenue_data)

    # Inserindo novos dados de despesas
    new_expense_data = [
        {"valor": 50.0, "recebido": 0, "fixo": 1, "Data": datetime.date(2024, 2, 15), "categoria": "Aluguel", "descricao": "Aluguel do mês"}
    ]
    my_budget_db.insert_data("despesas", new_expense_data)

    # Exibindo os dados atualizados
    updated_revenue_data = my_budget_db.load_data("receitas")
    updated_expense_data = my_budget_db.load_data("despesas")
    print("Dados de Receitas (Após inserção):")
    print(updated_revenue_data)
    print("Dados de Despesas (Após inserção):")
    print(updated_expense_data)
