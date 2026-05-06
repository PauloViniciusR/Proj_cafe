from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parent
BASE_PATH = ROOT / "base" / "base_cafe_normalizada_peso.csv"


st.set_page_config(
    page_title="Análise de Precificação de Cafés",
    layout="wide",
)


@st.cache_data
def carregar_dados() -> pd.DataFrame:
    if not BASE_PATH.exists():
        st.error(
            "Base local não encontrada. Coloque o arquivo "
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


def loja_extremo(df: pd.DataFrame, coluna: str, maior: bool = True) -> str:
    if df.empty or df[coluna].isna().all():
        return "sem dados"
    linha = df.sort_values(coluna, ascending=not maior).iloc[0]
    return str(linha["loja"])


df = carregar_dados()

st.title("Análise de Precificação de Cafés")
st.caption(
    "Dashboard de BI para comparar preço bruto, preço normalizado por peso, "
    "faixas de embalagem e mix de fabricantes entre supermercados."
)
st.info(
    "Leitura principal: este projeto avalia preços de produtos de café em "
    "supermercados com o objetivo de apoiar decisões de precificação, comparação "
    "competitiva e leitura de posicionamento de mercado. A análise considera que "
    "produtos de café possuem embalagens muito diferentes, como cápsulas, porções "
    "pequenas, pacotes de 250g, 500g e 1kg. Por isso, comparar apenas o preço de "
    "prateleira pode levar a conclusões distorcidas."
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
col3.metric("Preço mediano", formatar_moeda(preco_mediano))
col4.metric("Mediana por 500g", formatar_moeda(preco_500g_mediano))
col5.metric("Cobertura de peso", f"{cobertura_peso:.1f}%".replace(".", ","))

st.markdown(
    "**Como ler os KPIs:** a mediana representa melhor o preço típico, pois reduz "
    "o impacto de valores extremos, como produtos muito caros ou muito baratos. "
    "Já a mediana por 500g padroniza produtos com diferentes pesos, permitindo "
    "uma comparação mais justa da competitividade entre eles."
)

tab_geral, tab_lojas, tab_fabricantes, tab_dados = st.tabs(
    ["Visão geral", "Lojas e peso", "Fabricantes", "Dados"]
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
    loja_maior_preco = loja_extremo(resumo_loja, "preco_mediano", maior=True)
    loja_menor_preco = loja_extremo(resumo_loja, "preco_mediano", maior=False)

    st.markdown(
        f"**Leitura de negócio:** no preço bruto, `{loja_maior_preco}` aparece com "
        f"maior preço mediano e `{loja_menor_preco}` com menor preço mediano. "
        "A comparação deve ser vista junto da distribuição, porque produtos premium "
        "e outliers podem puxar a média para cima."
    )

    c1, c2 = st.columns(2)

    fig_preco = px.bar(
        resumo_loja,
        x="loja",
        y=["preco_medio", "preco_mediano"],
        barmode="group",
        title="Preço médio e mediano por loja",
        labels={"value": "Preço (R$)", "loja": "Loja", "variable": "Métrica"},
    )
    c1.plotly_chart(fig_preco, width="stretch")

    fig_box = px.box(
        dados,
        x="loja",
        y="preco",
        color="loja",
        title="Distribuição de preços por loja",
        labels={"preco": "Preço (R$)", "loja": "Loja"},
    )
    fig_box.update_layout(showlegend=False)
    c2.plotly_chart(fig_box, width="stretch")

with tab_lojas:
    loja_maior_500g = loja_extremo(resumo_loja, "preco_500g_mediano", maior=True)
    loja_menor_500g = loja_extremo(resumo_loja, "preco_500g_mediano", maior=False)

    st.markdown(
        f"**Interpretação:** quando o preço é normalizado para 500g, "
        f"`{loja_maior_500g}` apresenta o maior valor mediano por quantidade, "
        f"enquanto `{loja_menor_500g}` tem o menor. Essa análise revela qual loja "
        "é realmente mais cara ou mais barata considerando a mesma quantidade de "
        "produto, e não apenas o preço final da embalagem."
    )

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
        title="Preço mediano normalizado por 500g",
        labels={"preco_500g_mediano": "Preço por 500g (R$)", "loja": "Loja"},
    )
    c1.plotly_chart(fig_500g, width="stretch")

    fig_faixa = px.bar(
        resumo_peso,
        x="faixa_peso",
        y="preco_500g_mediano",
        color="loja",
        barmode="group",
        title="Preço por 500g por faixa de peso",
        labels={
            "faixa_peso": "Faixa de peso",
            "preco_500g_mediano": "Preço por 500g (R$)",
            "loja": "Loja",
        },
    )
    c2.plotly_chart(fig_faixa, width="stretch")
    st.info(
        "Ponto de atenção: faixas pequenas, como cápsulas e porções individuais, "
        "normalmente ficam mais caras quando convertidas para 500g. Para comparar "
        "cafés tradicionais, a faixa de 251g a 500g tende a ser mais adequada."
    )

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

    fabricante_mais_presente = resumo_fabricante.iloc[0]["Fabricante"]
    st.markdown(
        f"**Leitura de mix:** `{fabricante_mais_presente}` é o fabricante com maior "
        "presença dentro dos filtros atuais. O mix ajuda a explicar diferenças de "
        "preço entre lojas, pois uma loja com mais marcas premium pode parecer "
        "mais cara mesmo sem estar precificando acima do mercado."
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
        title="Fabricantes com maior preço mediano",
        labels={"preco_mediano": "Preço mediano (R$)", "Fabricante": "Fabricante"},
    )
    c2.plotly_chart(fig_fabricante, width="stretch")

with tab_dados:
    st.markdown(
        "**Detalhamento:** esta tabela mostra os produtos que formam os indicadores "
        "do painel. Ela serve para investigar casos específicos, validar outliers "
        "e exportar uma base filtrada para análises complementares."
    )

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
