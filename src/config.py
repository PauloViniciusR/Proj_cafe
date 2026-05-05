from pathlib import Path
import os

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = ROOT / "base"
RELATORIOS_DIR = ROOT / "relatorios"
TABELAS_DIR = RELATORIOS_DIR / "tabelas"
GRAFICOS_DIR = RELATORIOS_DIR / "graficos"

BASE_XLSX = BASE_DIR / "base_cafe.xlsx"
BASE_CAFE_CSV = BASE_DIR / "base_cafe.csv"
MAMBO_CSV = BASE_DIR / "mambo.csv"
MARCHE_CSV = BASE_DIR / "marche.csv"

ANALISE_MIX_CSV = TABELAS_DIR / "03_analise_mix.csv"
ANALISE_PRECO_FABRICANTE_CSV = TABELAS_DIR / "06_analise_preco_fabricante.csv"


def entrar_na_raiz() -> Path:
    os.chdir(ROOT)
    return ROOT


def carregar_base_cafe() -> pd.DataFrame:
    if BASE_CAFE_CSV.exists():
        return pd.read_csv(BASE_CAFE_CSV, parse_dates=["Data"])

    base_cafe = pd.read_excel(BASE_XLSX, sheet_name="dados")
    base_cafe = base_cafe.rename(columns={"enviado": "Código"})
    base_cafe["Data"] = pd.to_datetime(base_cafe["Data"], errors="coerce")
    return base_cafe


def carregar_bases_lojas() -> tuple[pd.DataFrame, pd.DataFrame]:
    if MAMBO_CSV.exists() and MARCHE_CSV.exists():
        return pd.read_csv(MAMBO_CSV), pd.read_csv(MARCHE_CSV)

    mambo = pd.read_excel(BASE_XLSX, sheet_name="mambo")
    marche = pd.read_excel(BASE_XLSX, sheet_name="marche")
    return mambo, marche


def carregar_bases_principais() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    mambo, marche = carregar_bases_lojas()
    base_cafe = carregar_base_cafe()
    return mambo, marche, base_cafe


def validar_tabelas_marcas() -> None:
    if not ANALISE_MIX_CSV.exists() or not ANALISE_PRECO_FABRICANTE_CSV.exists():
        raise FileNotFoundError(
            "Tabelas de relatório não encontradas. Execute o notebook principal antes desta análise."
        )
