from src.csv_importer import import_from_csv, get_csv_headers
from src.expense_manager import ExpenseManager
from src.category_suggester import suggest_category, CATEGORIES
import os

def print_menu():
    """Imprime o menu de opções para o usuário."""
    print("\n--- Controle Financeiro Pessoal ---")
    print("1. Importar despesas de arquivo CSV")
    print("2. Adicionar despesa manualmente")
    print("3. Listar todas as despesas")
    print("4. Ver total de gastos")
    print("5. Ver gastos por categoria")
    print("6. Sair")
    print("-----------------------------------")

def _get_category_for_expense(description):
    """
    Apresenta uma sugestão de categoria e permite ao usuário confirmar ou escolher outra.
    """
    suggested_category = suggest_category(description)

    print(f"\n> Para a despesa: '{description}'")

    # Lista as categorias para o usuário escolher
    print("  Sugestão de categoria: {}".format(suggested_category))
    print("  Escolha uma das categorias abaixo:")
    for i, category_name in enumerate(CATEGORIES, 1):
        print(f"    {i}: {category_name}")

    while True:
        try:
            prompt = f"  Digite o número da categoria (Enter para aceitar '{suggested_category}'): "
            choice_str = input(prompt)

            if not choice_str:
                return suggested_category

            choice_num = int(choice_str)
            if 1 <= choice_num <= len(CATEGORIES):
                return CATEGORIES[choice_num - 1]
            else:
                print("  -> Número inválido. Tente novamente.")
        except ValueError:
            print("  -> Entrada inválida. Por favor, digite um número ou pressione Enter.")

def list_expenses(manager):
    """Exibe a lista de despesas de forma organizada."""
    expenses = manager.get_expenses()
    if not expenses:
        print("\nNenhuma despesa registrada ainda.")
        return

    print("\n--- Lista de Despesas ---")
    try:
        sorted_expenses = sorted(expenses, key=lambda x: tuple(x['data'].split('/')[::-1]))
    except (ValueError, IndexError):
        sorted_expenses = expenses

    for expense in sorted_expenses:
        categoria_str = f" | Categoria: {expense.get('categoria', 'N/A')}"
        print(f"Data: {expense['data']:<12} | Descrição: {expense['descricao']:<30} | Valor: R$ {expense['valor']:.2f}{categoria_str}")
    print("-------------------------")

def add_manual_expense(manager):
    """Coleta os dados de uma nova despesa do usuário e a adiciona."""
    print("\n--- Adicionar Despesa Manual ---")
    try:
        data = input("Data da despesa (DD/MM/AAAA): ")
        descricao = input("Descrição da despesa: ")
        valor_str = input("Valor (ex: 50,25): ").replace(',', '.')
        valor = float(valor_str)

        if len(data.split('/')) != 3:
            print("\nFormato de data inválido. Use DD/MM/AAAA.")
            return

        categoria = _get_category_for_expense(descricao)
        expense_data = {'data': data, 'descricao': descricao, 'valor': valor, 'categoria': categoria}
        manager.add_expense(expense_data)
        print(f"\nDespesa '{descricao}' adicionada na categoria '{categoria}'.")

    except ValueError:
        print("\nErro: Valor inválido. O valor deve ser um número.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")

def import_csv_file(manager):
    """Gerencia a importação de despesas de um arquivo CSV, com mapeamento e categorização."""
    print("\n--- Importar Extrato CSV ---")
    # ... (código de seleção de arquivo e mapeamento de colunas) ...
    # (O código anterior para mapeamento é mantido aqui)
    filename = input("Digite o nome do arquivo na pasta 'data/' (ex: extrato.csv): ")
    file_path = os.path.join('data', filename)
    headers = get_csv_headers(file_path)
    if not headers:
        print("Não foi possível ler o cabeçalho. Verifique o arquivo.")
        return
    for i, h in enumerate(headers, 1): print(f"{i}: {h}")
    try:
        data_col = headers[int(input("NÚMERO da coluna da DATA: ")) - 1]
        desc_col = headers[int(input("NÚMERO da coluna da DESCRIÇÃO: ")) - 1]
        valor_col = headers[int(input("NÚMERO da coluna do VALOR: ")) - 1]
        column_mapping = {'data': data_col, 'descricao': desc_col, 'valor': valor_col}

        imported_expenses = import_from_csv(file_path, column_mapping)
        if not imported_expenses:
            print("\nNenhuma despesa importada. Verifique o arquivo e o mapeamento.")
            return

        print("\n--- Categorização de Despesas Importadas ---")
        categorized_expenses = []
        for expense in imported_expenses:
            category = _get_category_for_expense(expense['descricao'])
            expense['categoria'] = category
            categorized_expenses.append(expense)

        manager.add_expenses(categorized_expenses)

    except (ValueError, IndexError):
        print("\nErro de entrada. Por favor, digite apenas os números das colunas.")

def show_total(manager):
    """Exibe o total de gastos acumulados."""
    total = manager.get_total_expenses()
    print(f"\n--- Total de Gastos ---")
    print(f"O valor total de suas despesas é: R$ {total:.2f}")
    print(f"-------------------------")

def show_expenses_by_category(manager):
    """Exibe um relatório de gastos agrupados por categoria."""
    print("\n--- Gastos por Categoria ---")
    totals = manager.get_expenses_by_category()
    if not totals:
        print("Nenhuma despesa categorizada para exibir.")
        return

    for category, total in sorted(totals.items()):
        print(f"{category:<20} | R$ {total:>10.2f}")
    print("----------------------------")

def main():
    """Função principal que executa o loop da aplicação e gerencia o menu."""
    manager = ExpenseManager()
    while True:
        print_menu()
        choice = input("Escolha uma opção: ")
        if choice == '1': import_csv_file(manager)
        elif choice == '2': add_manual_expense(manager)
        elif choice == '3': list_expenses(manager)
        elif choice == '4': show_total(manager)
        elif choice == '5': show_expenses_by_category(manager)
        elif choice == '6':
            print("\nSaindo do programa. Até mais!")
            break
        else:
            print("\nOpção inválida. Por favor, escolha um número de 1 a 6.")

if __name__ == "__main__":
    main()
