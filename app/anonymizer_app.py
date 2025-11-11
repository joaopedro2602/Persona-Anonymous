# app/anonymizer_app.py
import json
import hashlib
import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder

def load_input(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def weighted_hash(name: str, weight: float = 0.5):
    """Gera hash com ruído ponderado."""
    salt = os.getenv("ANON_SALT", "default_salt")
    base = hashlib.sha256((name + salt).encode()).hexdigest()
    rnd = np.random.default_rng(seed=int(base[:8], 16))
    weighted_noise = weight * rnd.random() + (1 - weight) * rnd.normal()
    return hashlib.sha1(str(weighted_noise).encode()).hexdigest()[:8]

def anonymize_data(data: list):
    """Aplica anonimização básica em cada registro."""
    df = pd.DataFrame(data)
    df["anon_name"] = df["name"].apply(lambda n: f"Character_{weighted_hash(n)}")
    df["anon_persona"] = df["persona"].apply(
        lambda p: f"Persona_{weighted_hash(str(p), 0.7)}" if p else None
    )
    df["anon_confidant"] = df["confidant"].apply(
        lambda c: f"Conf_{weighted_hash(str(c), 0.9)}" if c else None
    )
    anonymized = df[["anon_name", "anon_persona", "anon_confidant"]].to_dict(orient="records")
    return anonymized

def save_output(data, output_path="data/persona_characters_anonymized.json"):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def run_anonymization(input_path="data/persona_characters.json"):
    data = load_input(input_path)
    anonymized = anonymize_data(data)
    save_output(anonymized)
    return anonymized
