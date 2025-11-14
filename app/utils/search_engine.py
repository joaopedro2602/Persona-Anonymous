import json
import os
from difflib import SequenceMatcher

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "..",
    "data",
    "persona_characters.json"
)

def load_database():
    """Carrega a base original."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def similarity(a, b):
    """Retorna similaridade entre duas strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def search_characters(query: str, threshold: float = 0.65):
    """
    Pesquisa personagens por nome, persona ou confidente.
    NÃO RETORNA OS REGISTROS — apenas a contagem.
    Não exibe contagem se for menor que 10.
    """

    db = load_database()
    matches = 0

    # Contagem simples sem retorno dos dados
    for char in db:
        fields = [
            char.get("name", ""),
            char.get("persona", ""),
            char.get("confidant", "")
        ]

        for field in fields:
            if field and similarity(query, field) >= threshold:
                matches += 1
                break

    # Regra: ocultar contagem se < 10
    if matches < 10:
        count_display = "hidden (below privacy threshold)"
    else:
        count_display = matches

    return {
        "query": query,
        "count": count_display
    }
