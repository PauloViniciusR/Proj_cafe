import re
import unicodedata

import numpy as np
import pandas as pd


FAIXAS_PESO = [
    (0, 100, "ate_100g"),
    (100, 250, "101g_250g"),
    (250, 500, "251g_500g"),
    (500, 1000, "501g_1kg"),
]


def normalizar_texto(texto: object) -> str:
    if pd.isna(texto):
        return ""
    texto = str(texto).lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(char for char in texto if not unicodedata.combining(char))
    return texto


def numero_pt_br(valor: str) -> float:
    return float(valor.replace(".", "").replace(",", "."))


def classificar_tipo_produto(titulo: object) -> str:
    texto = normalizar_texto(titulo)
    if re.search(r"\b(capsula|capsulas|nespresso|dolce\s*gusto|delta\s*q)\b", texto):
        return "capsula"
    if re.search(r"\b(soluvel|liofilizado|instantaneo|cappuccino|cappucino)\b", texto):
        return "soluvel"
    if re.search(r"\b(drip|sache|sachet|filtro individual|envelope)\b", texto):
        return "sache_drip"
    if re.search(r"\b(graos|grao)\b", texto):
        return "graos"
    if re.search(r"\b(torrado|moido|moida|vacuo|pouch|pacote)\b", texto):
        return "tradicional"
    return "outros"


def extrair_quantidade_unidades(titulo: object) -> float:
    texto = normalizar_texto(titulo)
    padroes = [
        r"(\d{1,3})\s*(?:unidades|unidade|unid\.?|capsulas|capsula|caps\.?)\b",
        r"\b(?:com|cx|caixa)\s*(\d{1,3})\s*(?:unidades|unidade|unid\.?|capsulas|capsula|caps\.?)\b",
    ]
    for padrao in padroes:
        match = re.search(padrao, texto)
        if match:
            return float(match.group(1))
    return np.nan


def _extrair_peso_cada(texto: str) -> float:
    match = re.search(
        r"(\d+(?:[,.]\d+)?)\s*(kg|g)\s*(?:cada|unitario|por\s*(?:capsula|unidade))\b",
        texto,
    )
    if not match:
        return np.nan

    valor = numero_pt_br(match.group(1))
    unidade = match.group(2)
    return valor * 1000 if unidade == "kg" else valor


def _extrair_pesos_gramas(texto: str) -> list[float]:
    pesos = []
    for valor, unidade in re.findall(r"(\d+(?:[,.]\d+)?)\s*(kg|g)\b", texto):
        peso = numero_pt_br(valor)
        pesos.append(peso * 1000 if unidade == "kg" else peso)
    return pesos


def extrair_peso_gramas(titulo: object) -> float:
    texto = normalizar_texto(titulo)
    tipo_produto = classificar_tipo_produto(titulo)
    quantidade = extrair_quantidade_unidades(titulo)

    peso_cada = _extrair_peso_cada(texto)
    if not pd.isna(peso_cada):
        if not pd.isna(quantidade):
            return float(peso_cada * quantidade)
        return np.nan

    pesos = _extrair_pesos_gramas(texto)
    if not pesos:
        return np.nan

    # Em capsulas, pesos como "8g" e "11g" sem "cada" costumam representar
    # peso unitario truncado no titulo. Nao usamos isso para normalizar por 500g.
    if tipo_produto == "capsula" and max(pesos) <= 15:
        return np.nan

    return float(max(pesos))


def classificar_faixa_peso(peso_gramas: object) -> str:
    if pd.isna(peso_gramas):
        return "sem_peso"

    peso = float(peso_gramas)
    for limite_inferior, limite_superior, faixa in FAIXAS_PESO:
        if limite_inferior < peso <= limite_superior:
            return faixa
    if peso > 1000:
        return "acima_1kg"
    return "sem_peso"


def enriquecer_base_precos(df: pd.DataFrame) -> pd.DataFrame:
    dados = df.copy()
    dados["preco"] = pd.to_numeric(dados["preco"], errors="coerce")
    dados["tipo_produto"] = dados["Titulo"].apply(classificar_tipo_produto)
    dados["quantidade_unidades"] = dados["Titulo"].apply(extrair_quantidade_unidades)
    dados["peso_gramas"] = dados["Titulo"].apply(extrair_peso_gramas)
    dados["faixa_peso"] = dados["peso_gramas"].apply(classificar_faixa_peso)

    dados["preco_100g"] = np.where(
        dados["peso_gramas"].gt(0),
        dados["preco"] / dados["peso_gramas"] * 100,
        np.nan,
    )
    dados["preco_500g"] = np.where(
        dados["peso_gramas"].gt(0),
        dados["preco"] / dados["peso_gramas"] * 500,
        np.nan,
    )
    dados["preco_unidade"] = np.where(
        dados["quantidade_unidades"].gt(0),
        dados["preco"] / dados["quantidade_unidades"],
        np.nan,
    )

    return dados
