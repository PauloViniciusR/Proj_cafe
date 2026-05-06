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

MAPA_FABRICANTES = {
    "3 coracoes": "3 Corações",
    "3 corações": "3 Corações",
    "tres": "3 Corações",
    "tres coracoes": "3 Corações",
    "três": "3 Corações",
    "três corações": "3 Corações",
    "l'or": "L'OR",
    "lor": "L'OR",
    "orfeu": "Orfeu",
    "santa monica": "Santa Mônica",
    "santa mônica": "Santa Mônica",
    "bravo": "Bravo Café",
    "bravo cafe": "Bravo Café",
    "bravo café": "Bravo Café",
    "qualita": "Qualitá",
    "qualitá": "Qualitá",
    "qualita exclusive": "Qualitá",
    "qualitá exclusive": "Qualitá",
    "prima qualita": "Prima Qualitá",
    "prima qualitá": "Prima Qualitá",
    "cafe do ponto": "Café do Ponto",
    "café do ponto": "Café do Ponto",
    "café do ponto": "Café do Ponto",
    "do ponto": "Café do Ponto",
    "cafe floresta": "Floresta",
    "floresta": "Floresta",
    "cafe iguacu": "Iguaçu",
    "café iguaçu": "Iguaçu",
    "iguacu": "Iguaçu",
    "iguaçu": "Iguaçu",
    "nescafe": "Nescafé",
    "nescafé": "Nescafé",
    "nescafe gold": "Nescafé",
    "nescafé gold": "Nescafé",
    "nescafe dolce gusto": "Nescafé",
    "nescafé dolce gusto": "Nescafé",
    "dolce gusto": "Nescafé",
    "gold": "Nescafé",
    "cafe uniao pouch 250g": "União",
    "brasileiro": "Café Brasileiro",
    "astro cafe": "Astro Café",
    "cia organica": "Cia Orgânica",
}

FABRICANTES_TITULO = [
    ("3 Corações", r"\b(3\s*coracoes|3\s*corecoes|3\s*corações|tres|três)\b"),
    ("Pilão", r"\bpila[oã]\b"),
    ("Melitta", r"\bmelitta\b"),
    ("Nescafé", r"\b(nescafe|nescafé|dolce\s*gusto)\b"),
    ("L'OR", r"\b(l\\?'?or|lor)\b"),
    ("Qualitá", r"\bqualita\b"),
    ("Baggio", r"\bbaggio\b"),
    ("Bravo Café", r"\bbravo\b"),
    ("Illy", r"\billy\b"),
    ("Juan Valdez", r"\bjuan\s+valdez\b"),
    ("Starbucks", r"\bstarbucks\b"),
    ("Orfeu", r"\borfeu\b"),
    ("Latitude 13", r"\blatitude\s*13\b"),
    ("Cafellow", r"\bcafellow\b"),
    ("Café do Ponto", r"\bdo\s*ponto\b"),
    ("Floresta", r"\bfloresta\b"),
    ("Iguaçu", r"\biguacu\b"),
    ("União", r"\buniao\b"),
    ("Tereza do Quilombo", r"\btereza\s+do\s+quilombo\b"),
    ("Dandara do Quilombo", r"\bdandara\s+do\s+quilombo\b"),
    ("Anastácia do Quilombo", r"\banastacia\s+do\s+quilombo\b"),
    ("Kopenhagen", r"\bkopenhagen\b"),
]


def normalizar_texto(texto: object) -> str:
    if pd.isna(texto):
        return ""
    texto = str(texto).lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(char for char in texto if not unicodedata.combining(char))
    return texto


def chave_texto(texto: object) -> str:
    return " ".join(normalizar_texto(texto).split())


def normalizar_fabricante(fabricante: object, titulo: object) -> str:
    fabricante_chave = chave_texto(fabricante)
    titulo_chave = chave_texto(titulo)

    if fabricante_chave in MAPA_FABRICANTES:
        return MAPA_FABRICANTES[fabricante_chave]

    if fabricante_chave in {
        "",
        "nan",
        "none",
        "pa",
        "nao identificado",
        "st marche",
        "st. marche",
        "mambo",
        "paodeacucar",
        "pao de acucar",
    }:
        for fabricante_padrao, padrao in FABRICANTES_TITULO:
            if re.search(padrao, titulo_chave):
                return fabricante_padrao
        return "Não identificado"

    return str(fabricante).strip()


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
    dados["fabricante_original"] = dados["Fabricante"]
    dados["Fabricante"] = dados.apply(
        lambda linha: normalizar_fabricante(linha["Fabricante"], linha["Titulo"]),
        axis=1,
    )
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
