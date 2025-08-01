import csv
import os

def get_csv_headers(file_path):
    """
    Lê apenas a primeira linha (cabeçalho) de um arquivo CSV e retorna os nomes das colunas.

    Args:
        file_path (str): O caminho para o arquivo CSV.

    Returns:
        list: Uma lista com os nomes das colunas do cabeçalho. Retorna lista vazia se houver erro.
    """
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return []

    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as csvfile:
            # Usamos o leitor padrão para pegar apenas a primeira linha
            reader = csv.reader(csvfile, delimiter=';')
            headers = next(reader)
            return [header.strip() for header in headers]
    except (FileNotFoundError, StopIteration) as e:
        print(f"Não foi possível ler o cabeçalho do arquivo: {e}")
        return []

def import_from_csv(file_path, column_mapping):
    """
    Importa despesas de um arquivo CSV usando um mapeamento de colunas customizado.

    Args:
        file_path (str): O caminho para o arquivo CSV.
        column_mapping (dict): Dicionário que mapeia os campos da aplicação para os nomes das colunas no CSV.
                               Ex: {'data': 'Data da Compra', 'descricao': 'Estabelecimento', 'valor': 'Preço'}

    Returns:
        list: Uma lista de dicionários de despesas.
    """
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return []

    expenses = []
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')

            # Valida se as colunas mapeadas existem no cabeçalho do arquivo
            header = reader.fieldnames
            if not header:
                print("Erro: O arquivo CSV está vazio ou o cabeçalho não pôde ser lido.")
                return []

            for field, mapped_col in column_mapping.items():
                if mapped_col not in header:
                    print(f"Erro de mapeamento: A coluna '{mapped_col}' (mapeada para '{field}') não foi encontrada no arquivo CSV.")
                    print(f"Colunas disponíveis: {header}")
                    return []

            for i, row in enumerate(reader, start=2): # Começa da linha 2 (após o cabeçalho)
                try:
                    valor_str = row[column_mapping['valor']]
                    valor = float(valor_str.replace('.', '').replace(',', '.'))

                    expenses.append({
                        'data': row[column_mapping['data']],
                        'descricao': row[column_mapping['descricao']],
                        'valor': valor
                        # Categoria será adicionada depois
                    })
                except ValueError:
                    print(f"Aviso (linha {i}): Não foi possível converter o valor '{valor_str}' para número. Linha ignorada.")
                except KeyError as e:
                    print(f"Aviso (linha {i}): Erro de chave no mapeamento: {e}. Verifique se todas as colunas foram mapeadas corretamente. Linha ignorada.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao processar o arquivo CSV: {e}")
        return []

    return expenses
