# -*- coding: utf-8 -*-

"""
Este módulo contém a lógica para sugerir categorias de despesas
com base em palavras-chave encontradas na descrição.
"""
import unicodedata

# Dicionário de palavras-chave para sugestão de categoria.
# As chaves DEVEM estar em minúsculas e sem acentos.
KEYWORD_MAP = {
    # Alimentação
    'ifood': 'Alimentação',
    'rappi': 'Alimentação',
    'supermercado': 'Alimentação',
    'restaurante': 'Alimentação',
    'padaria': 'Alimentação',
    'lanche': 'Alimentação',
    'mercado': 'Alimentação',

    # Transporte
    'uber': 'Transporte',
    '99app': 'Transporte',
    'posto': 'Transporte',
    'gasolina': 'Transporte',
    'combustivel': 'Transporte',
    'estacionamento': 'Transporte',
    'pedagio': 'Transporte',
    'passagem aerea': 'Transporte',

    # Moradia
    'aluguel': 'Moradia',
    'condominio': 'Moradia',
    'conta de luz': 'Moradia',
    'cpfl': 'Moradia',
    'enel': 'Moradia',
    'internet': 'Moradia',
    'vivo': 'Moradia',
    'claro': 'Moradia',
    'tim': 'Moradia',
    'agua': 'Moradia',
    'sabesp': 'Moradia',
    'iptu': 'Moradia',

    # Lazer
    'netflix': 'Lazer',
    'spotify': 'Lazer',
    'amazon prime': 'Lazer',
    'disney+': 'Lazer',
    'cinema': 'Lazer',
    'show': 'Lazer',
    'bar': 'Lazer',
    'ingresso': 'Lazer',

    # Saúde
    'farmacia': 'Saúde',
    'drogaria': 'Saúde',
    'medico': 'Saúde',
    'consulta': 'Saúde', # Adicionado para resolver o problema do teste
    'dentista': 'Saúde',
    'plano de saude': 'Saúde',
    'unimed': 'Saúde',

    # Educação
    'faculdade': 'Educação',
    'curso': 'Educação',
    'livro': 'Educação',
    'udemy': 'Educação',

    # Compras
    'magazine luiza': 'Compras',
    'amazon': 'Compras',
    'mercado livre': 'Compras',
    'shopee': 'Compras'
}

# Lista oficial de categorias para garantir consistência
CATEGORIES = sorted(list(set(KEYWORD_MAP.values())) + ['Outros'])

def _normalize_string(s):
    """Remove acentos de uma string e a converte para minúsculas."""
    s = str(s)
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    ).lower()

def suggest_category(description):
    """
    Sugere uma categoria para uma despesa com base em palavras-chave na descrição.
    A comparação é feita sem levar em conta acentos ou maiúsculas/minúsculas.

    Args:
        description (str): A descrição da despesa.

    Returns:
        str: A categoria sugerida.
    """
    if not isinstance(description, str):
        return 'Outros'

    normalized_desc = _normalize_string(description)
    for keyword, category in KEYWORD_MAP.items():
        if keyword in normalized_desc:
            return category

    return 'Outros'
