from pathlib import Path

import pandas as pd

from features import enriquecer_base_precos


ROOT = Path(__file__).resolve().parents[1]
BASE_PROCESSADA = ROOT / "data" / "processed" / "base_cafe_normalizada_peso.csv"
TABELAS_DIR = ROOT / "relatorios" / "tabelas"


def arredondar_colunas(df: pd.DataFrame, casas: int = 2) -> pd.DataFrame:
    dados = df.copy()
    for coluna in dados.select_dtypes(include="number").columns:
        dados[coluna] = dados[coluna].round(casas)
    return dados


def carregar_base_entrada() -> pd.DataFrame:
    if not BASE_PROCESSADA.exists():
        raise FileNotFoundError(f"Base processada nao encontrada: {BASE_PROCESSADA}")

    colunas_base = ["Titulo", "Fabricante", "preco", "loja"]
    df = pd.read_csv(BASE_PROCESSADA)
    faltantes = [coluna for coluna in colunas_base if coluna not in df.columns]
    if faltantes:
        raise ValueError(f"Colunas obrigatorias ausentes: {faltantes}")
    return df[colunas_base].copy()


def gerar_tabela_preco_loja(df: pd.DataFrame) -> pd.DataFrame:
    tabela = (
        df.groupby("loja")["preco"]
        .agg(["mean", "median", "min", "max", "count"])
        .round(2)
        .reset_index()
        .rename(columns={"loja": "Loja"})
        .sort_values("median", ascending=False)
    )
    return tabela


def gerar_tabela_distribuicao_preco(df: pd.DataFrame) -> pd.DataFrame:
    tabela = df["preco"].describe().round(2).reset_index()
    tabela.columns = ["Describe", "Preco"]
    return tabela


def gerar_tabela_mix(df: pd.DataFrame) -> pd.DataFrame:
    tabela = pd.crosstab(df["Fabricante"], df["loja"])
    for loja in ["Mambo", "St Marche", "Paodeacucar"]:
        if loja not in tabela.columns:
            tabela[loja] = 0

    tabela["Total"] = tabela.sum(axis=1)
    tabela = (
        tabela.reset_index()
        .rename(columns={"St Marche": "St.Marche"})
        .sort_values("Total", ascending=False)
    )
    return tabela[["Fabricante", "Mambo", "St.Marche", "Paodeacucar", "Total"]]


def gerar_tabela_faixa_peso_loja(df: pd.DataFrame) -> pd.DataFrame:
    tabela = (
        df.groupby(["loja", "faixa_peso"], as_index=False)
        .agg(
            produtos=("Titulo", "count"),
            preco_mediano=("preco", "median"),
            preco_500g_mediano=("preco_500g", "median"),
        )
        .round(2)
    )
    return tabela


def gerar_tabela_preco_normalizado_loja(df: pd.DataFrame) -> pd.DataFrame:
    tabela = (
        df.groupby("loja", as_index=False)
        .agg(
            produtos=("Titulo", "count"),
            produtos_com_peso=("peso_gramas", lambda serie: int(serie.notna().sum())),
            preco_mediano=("preco", "median"),
            preco_500g_mediano=("preco_500g", "median"),
            preco_100g_mediano=("preco_100g", "median"),
            preco_unidade_mediano=("preco_unidade", "median"),
        )
    )
    tabela["cobertura_peso_pct"] = (
        tabela["produtos_com_peso"] / tabela["produtos"] * 100
    ).round(2)
    colunas = [
        "loja",
        "produtos",
        "produtos_com_peso",
        "cobertura_peso_pct",
        "preco_mediano",
        "preco_500g_mediano",
        "preco_100g_mediano",
        "preco_unidade_mediano",
    ]
    return tabela[colunas].round(2)


def gerar_tabela_tipo_produto_loja(df: pd.DataFrame) -> pd.DataFrame:
    tabela = (
        df.groupby(["loja", "tipo_produto"], as_index=False)
        .agg(
            produtos=("Titulo", "count"),
            produtos_com_peso=("peso_gramas", lambda serie: int(serie.notna().sum())),
            preco_mediano=("preco", "median"),
            preco_500g_mediano=("preco_500g", "median"),
            preco_unidade_mediano=("preco_unidade", "median"),
        )
        .round(2)
    )
    return tabela


def gerar_tabela_preco_fabricante(df: pd.DataFrame) -> pd.DataFrame:
    tabela = (
        df.groupby("Fabricante")["preco"]
        .agg(["mean", "median", "min", "max", "count"])
        .round(2)
        .reset_index()
    )
    tabela["range"] = (tabela["max"] - tabela["min"]).round(2)
    return tabela.sort_values(["median", "count"], ascending=[True, False])


def salvar_tabelas(df: pd.DataFrame) -> None:
    TABELAS_DIR.mkdir(parents=True, exist_ok=True)
    tabelas = {
        "01_analise_preco_loja.csv": gerar_tabela_preco_loja(df),
        "02_analise_distribuicao_preco.csv": gerar_tabela_distribuicao_preco(df),
        "03_analise_mix.csv": gerar_tabela_mix(df),
        "04_analise_faixa_peso_loja.csv": gerar_tabela_faixa_peso_loja(df),
        "05_analise_preco_normalizado_peso_loja.csv": gerar_tabela_preco_normalizado_loja(df),
        "06_analise_preco_fabricante.csv": gerar_tabela_preco_fabricante(df),
        "07_analise_tipo_produto_loja.csv": gerar_tabela_tipo_produto_loja(df),
    }
    for nome, tabela in tabelas.items():
        tabela.to_csv(TABELAS_DIR / nome, index=False)


def main() -> None:
    df = carregar_base_entrada()
    df = enriquecer_base_precos(df)
    df = arredondar_colunas(df, casas=4)

    BASE_PROCESSADA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BASE_PROCESSADA, index=False)
    salvar_tabelas(df)
    print(f"Base e tabelas regeneradas a partir de {len(df)} produtos.")


if __name__ == "__main__":
    main()
