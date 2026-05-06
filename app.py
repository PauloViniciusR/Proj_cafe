from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parent
BASE_PATH = ROOT / "base" / "base_cafe_normalizada_peso.csv"


st.set_page_config(
    page_title="Analise de Precificacao de Cafes",
    layout="wide",
)


@st.cache_data
def carregar_dados() -> pd.DataFrame:
    if not BASE_PATH.exists():
        st.error(
            "Base local nao encontrada. Coloque o arquivo "
            "`base/base_cafe_normalizada_peso.csv` para executar o dashboard."
        )
        st.stop()

    df = pd.read_csv(BASE_PATH)
    for coluna in ["preco", "preco_500g", "preco_100g", "peso_gramas"]:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    return df


def formatar_moeda(valor: float) -> str:
    if pd.isna(valor):
        return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def selecionar_multiplos(rotulo: str, opcoes: list[str]) -> list[str]:
    return st.sidebar.multiselect(rotulo, options=opcoes, default=opcoes)


df = carregar_dados()

st.title("Analise de Precificacao de Cafes")
st.caption(
    "Dashboard de BI para comparar preco bruto, preco normalizado por peso, "
    "faixas de embalagem e mix de fabricantes entre supermercados."
)

lojas = selecionar_multiplos("Lojas", sorted(df["loja"].dropna().unique()))
faixas = selecionar_multiplos("Faixas de peso", sorted(df["faixa_peso"].dropna().unique()))

fabricantes_opcoes = sorted(df["Fabricante"].dropna().unique())
fabricantes = st.sidebar.multiselect(
    "Fabricantes",
    options=fabricantes_opcoes,
    default=[],
    help="Deixe vazio para considerar todos os fabricantes.",
)

dados = df[df["loja"].isin(lojas) & df["faixa_peso"].isin(faixas)].copy()
if fabricantes:
    dados = dados[dados["Fabricante"].isin(fabricantes)].copy()

if dados.empty:
    st.warning("Nenhum produto encontrado com os filtros selecionados.")
    st.stop()

produtos = len(dados)
lojas_ativas = dados["loja"].nunique()
preco_mediano = dados["preco"].median()
preco_500g_mediano = dados["preco_500g"].median()
cobertura_peso = dados["peso_gramas"].notna().mean() * 100

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Produtos", f"{produtos:,}".replace(",", "."))
col2.metric("Lojas", lojas_ativas)
col3.metric("Preco mediano", formatar_moeda(preco_mediano))
col4.metric("Mediana por 500g", formatar_moeda(preco_500g_mediano))
col5.metric("Cobertura de peso", f"{cobertura_peso:.1f}%".replace(".", ","))

tab_geral, tab_lojas, tab_fabricantes, tab_dados = st.tabs(
    ["Visao geral", "Lojas e peso", "Fabricantes", "Dados"]
)

resumo_loja = (
    dados.groupby("loja", as_index=False)
    .agg(
        preco_medio=("preco", "mean"),
        preco_mediano=("preco", "median"),
        preco_500g_mediano=("preco_500g", "median"),
        produtos=("Titulo", "count"),
    )
    .sort_values("preco_mediano", ascending=False)
)

with tab_geral:
    c1, c2 = st.columns(2)

    fig_preco = px.bar(
        resumo_loja,
        x="loja",
        y=["preco_medio", "preco_mediano"],
        barmode="group",
        title="Preco medio e mediano por loja",
        labels={"value": "Preco (R$)", "loja": "Loja", "variable": "Metrica"},
    )
    c1.plotly_chart(fig_preco, width="stretch")

    fig_box = px.box(
        dados,
        x="loja",
        y="preco",
        color="loja",
        title="Distribuicao de precos por loja",
        labels={"preco": "Preco (R$)", "loja": "Loja"},
    )
    fig_box.update_layout(showlegend=False)
    c2.plotly_chart(fig_box, width="stretch")

with tab_lojas:
    c1, c2 = st.columns(2)

    resumo_peso = (
        dados.dropna(subset=["preco_500g"])
        .groupby(["loja", "faixa_peso"], as_index=False)
        .agg(preco_500g_mediano=("preco_500g", "median"), produtos=("Titulo", "count"))
    )

    fig_500g = px.bar(
        resumo_loja.sort_values("preco_500g_mediano", ascending=False),
        x="loja",
        y="preco_500g_mediano",
        title="Preco mediano normalizado por 500g",
        labels={"preco_500g_mediano": "Preco por 500g (R$)", "loja": "Loja"},
    )
    c1.plotly_chart(fig_500g, width="stretch")

    fig_faixa = px.bar(
        resumo_peso,
        x="faixa_peso",
        y="preco_500g_mediano",
        color="loja",
        barmode="group",
        title="Preco por 500g por faixa de peso",
        labels={
            "faixa_peso": "Faixa de peso",
            "preco_500g_mediano": "Preco por 500g (R$)",
            "loja": "Loja",
        },
    )
    c2.plotly_chart(fig_faixa, width="stretch")

with tab_fabricantes:
    resumo_fabricante = (
        dados.groupby("Fabricante", as_index=False)
        .agg(
            produtos=("Titulo", "count"),
            preco_mediano=("preco", "median"),
            preco_500g_mediano=("preco_500g", "median"),
        )
        .sort_values("produtos", ascending=False)
    )

    c1, c2 = st.columns(2)
    top_mix = resumo_fabricante.head(15).sort_values("produtos")
    fig_mix = px.bar(
        top_mix,
        x="produtos",
        y="Fabricante",
        orientation="h",
        title="Top fabricantes por quantidade de produtos",
        labels={"produtos": "Produtos", "Fabricante": "Fabricante"},
    )
    c1.plotly_chart(fig_mix, width="stretch")

    top_preco = (
        resumo_fabricante[resumo_fabricante["produtos"] >= 5]
        .sort_values("preco_mediano", ascending=False)
        .head(15)
        .sort_values("preco_mediano")
    )
    fig_fabricante = px.bar(
        top_preco,
        x="preco_mediano",
        y="Fabricante",
        orientation="h",
        title="Fabricantes com maior preco mediano",
        labels={"preco_mediano": "Preco mediano (R$)", "Fabricante": "Fabricante"},
    )
    c2.plotly_chart(fig_fabricante, width="stretch")

with tab_dados:
    colunas = [
        "Titulo",
        "Fabricante",
        "loja",
        "preco",
        "peso_gramas",
        "faixa_peso",
        "preco_100g",
        "preco_500g",
        "preco_unidade",
    ]
    st.dataframe(dados[colunas].sort_values("preco", ascending=False), width="stretch")

    st.download_button(
        "Baixar dados filtrados",
        data=dados[colunas].to_csv(index=False).encode("utf-8"),
        file_name="dados_precificacao_cafe_filtrados.csv",
        mime="text/csv",
    )
