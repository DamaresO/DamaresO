# Módulo responsável por gerenciar as despesas (adicionar, listar, etc.).

class ExpenseManager:
    """
    Gerencia as operações relacionadas a despesas, como adicionar,
    listar e calcular totais.
    """
    def __init__(self):
        """Inicializa o gerenciador com uma lista vazia de despesas."""
        self._expenses = []

    def add_expense(self, expense_data):
        """
        Adiciona uma única despesa à lista.
        Espera-se que `expense_data` já contenha a chave 'categoria'.

        Args:
            expense_data (dict): Um dicionário com os dados da despesa,
                                 incluindo 'data', 'descricao', 'valor' e 'categoria'.
        """
        self._expenses.append(expense_data)
        # O feedback ao usuário será dado no main.py, onde a interação ocorre.

    def add_expenses(self, expenses_list):
        """
        Adiciona uma lista de despesas. A categorização deve ser feita antes.

        Args:
            expenses_list (list): Uma lista de dicionários de despesas.
        """
        if not expenses_list:
            return

        self._expenses.extend(expenses_list)
        print(f"Total de {len(expenses_list)} despesas importadas e categorizadas com sucesso.")

    def get_expenses(self):
        """Retorna a lista de todas as despesas registradas."""
        return self._expenses

    def get_total_expenses(self):
        """Calcula e retorna o valor total de todas as despesas."""
        return sum(expense['valor'] for expense in self._expenses)

    def get_expenses_by_category(self):
        """
        Agrupa as despesas por categoria e retorna um dicionário com os totais.

        Returns:
            dict: Um dicionário onde as chaves são as categorias e os valores são os totais.
        """
        totals_by_category = {}
        for expense in self._expenses:
            # Usa 'Sem Categoria' se a categoria não estiver definida
            category = expense.get('categoria', 'Sem Categoria')
            totals_by_category[category] = totals_by_category.get(category, 0) + expense['valor']

        return totals_by_category
