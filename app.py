from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parent
BASE_PUBLICA_PATH = ROOT / "data" / "processed" / "base_cafe_normalizada_peso.csv"
BASE_LOCAL_PATH = ROOT / "base" / "base_cafe_normalizada_peso.csv"
BASE_CANDIDATES = [BASE_PUBLICA_PATH, BASE_LOCAL_PATH]
REPOSITORY_URL = "https://github.com/PauloViniciusR/Proj_"

LOJA_LABELS = {
    "Mambo": "Mambo",
    "Paodeacucar": "Pão de Açúcar",
    "St Marche": "St Marche",
}

TIPO_PRODUTO_LABELS = {
    "capsula": "Cápsula",
    "graos": "Grãos",
    "outros": "Outros",
    "sache_drip": "Sachê",
    "soluvel": "Solúvel",
    "tradicional": "Tradicional",
}

FAIXA_PESO_LABELS = {
    "ate_100g": "Até 100g",
    "101g_250g": "101g a 250g",
    "251g_500g": "251g a 500g",
    "501g_1kg": "501g a 1kg",
    "acima_1kg": "Acima de 1kg",
    "sem_peso": "Sem peso",
}


st.set_page_config(
    page_title="Análise de Precificação de Cafés",
    layout="wide",
)


@st.cache_data
def carregar_dados() -> pd.DataFrame:
    base_path = next((path for path in BASE_CANDIDATES if path.exists()), None)
    if base_path is None:
        st.error(
            "Base processada não encontrada. Para publicar o dashboard, inclua o arquivo "
            "`data/processed/base_cafe_normalizada_peso.csv` no repositório. "
            "Para uso local, também é possível usar `base/base_cafe_normalizada_peso.csv`."
        )
        st.stop()

    df = pd.read_csv(base_path)
    for coluna in [
        "preco",
        "preco_500g",
        "preco_100g",
        "peso_gramas",
        "quantidade_unidades",
        "preco_unidade",
    ]:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    df["loja_label"] = df["loja"].map(LOJA_LABELS).fillna(df["loja"])
    df["tipo_produto_label"] = (
        df["tipo_produto"].map(TIPO_PRODUTO_LABELS).fillna(df["tipo_produto"])
    )
    df["faixa_peso_label"] = (
        df["faixa_peso"].map(FAIXA_PESO_LABELS).fillna(df["faixa_peso"])
    )
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


def adicionar_rotulos_barras(fig, formato: str = ".2f"):
    fig.update_traces(
        texttemplate=f"%{{value:{formato}}}",
        textposition="outside",
        textfont_color="#2F4858",
        cliponaxis=False,
    )
    fig.update_layout(uniformtext_minsize=9, uniformtext_mode="hide")
    return fig


df = carregar_dados()

st.title("Análise de Precificação de Cafés")
st.caption(
    "Dashboard de BI para comparar preço bruto, preço normalizado por peso, "
    "faixas de embalagem e mix de fabricantes entre supermercados."
)
st.info(
    "Leitura principal: este projeto compara preços de produtos de café em "
    "supermercados considerando que o sortimento mistura cápsulas, cafés solúveis, "
    "sachês, grãos e pacotes tradicionais. A visão geral mostra o comportamento "
    "do mix completo de cada loja. Para uma comparação justa de preço por "
    "quantidade, use os filtros de tipo de produto e faixa de peso, evitando "
    "comparar formatos diferentes, como cápsulas e pacotes tradicionais, na mesma "
    "métrica."
)

lojas = selecionar_multiplos("Lojas", sorted(df["loja_label"].dropna().unique()))
tipos = selecionar_multiplos(
    "Tipos de produto",
    sorted(df["tipo_produto_label"].dropna().unique()),
)
faixas = selecionar_multiplos(
    "Faixas de peso",
    sorted(df["faixa_peso_label"].dropna().unique()),
)

fabricantes_opcoes = sorted(df["Fabricante"].dropna().unique())
fabricantes = st.sidebar.multiselect(
    "Fabricantes normalizados",
    options=fabricantes_opcoes,
    default=[],
    help="Deixe vazio para considerar todos os fabricantes.",
)

dados = df[
    df["loja_label"].isin(lojas)
    & df["tipo_produto_label"].isin(tipos)
    & df["faixa_peso_label"].isin(faixas)
].copy()
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
col5.metric("% com peso identificado", f"{cobertura_peso:.1f}%".replace(".", ","))

st.markdown(
    "**Como ler os KPIs:** a mediana representa melhor o preço típico, pois reduz "
    "o impacto de valores extremos, como produtos muito caros ou muito baratos. "
    "Já a mediana por 500g só deve ser comparada entre produtos equivalentes. "
    "Use o filtro de tipo de produto para separar cápsulas, solúveis, sachês, "
    "grãos e cafés tradicionais."
)

tab_geral, tab_lojas, tab_fabricantes, tab_dados = st.tabs(
    ["Visão geral", "Lojas e peso", "Fabricantes", "Dados"]
)

resumo_loja = (
    dados.groupby("loja_label", as_index=False)
    .agg(
        preco_medio=("preco", "mean"),
        preco_mediano=("preco", "median"),
        preco_500g_mediano=("preco_500g", "median"),
        produtos=("Titulo", "count"),
    )
    .rename(columns={"loja_label": "loja"})
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
    adicionar_rotulos_barras(fig_preco)
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
        f"**Interpretação:** com os filtros atuais, `{loja_maior_500g}` tem a maior "
        f"mediana por 500g e `{loja_menor_500g}` a menor. Essa comparação mostra "
        "diferença de preço proporcional, mas só é justa quando os produtos têm o "
        "mesmo formato. Para cápsulas e sachês, acompanhe também o preço por unidade."
    )

    c1, c2 = st.columns(2)

    resumo_peso = (
        dados.dropna(subset=["preco_500g"])
        .groupby(["loja_label", "faixa_peso_label"], as_index=False)
        .agg(preco_500g_mediano=("preco_500g", "median"), produtos=("Titulo", "count"))
        .rename(columns={"loja_label": "loja", "faixa_peso_label": "faixa_peso"})
    )

    fig_500g = px.bar(
        resumo_loja.sort_values("preco_500g_mediano", ascending=False),
        x="loja",
        y="preco_500g_mediano",
        title="Preço mediano normalizado por 500g",
        labels={"preco_500g_mediano": "Preço por 500g (R$)", "loja": "Loja"},
    )
    adicionar_rotulos_barras(fig_500g)
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
    adicionar_rotulos_barras(fig_faixa)
    c2.plotly_chart(fig_faixa, width="stretch")

    resumo_tipo = (
        dados.dropna(subset=["preco_500g"])
        .groupby(["loja_label", "tipo_produto_label"], as_index=False)
        .agg(
            preco_500g_mediano=("preco_500g", "median"),
            preco_unidade_mediano=("preco_unidade", "median"),
            produtos=("Titulo", "count"),
        )
        .rename(columns={"loja_label": "loja", "tipo_produto_label": "tipo_produto"})
    )

    fig_tipo = px.bar(
        resumo_tipo,
        x="tipo_produto",
        y="preco_500g_mediano",
        color="loja",
        barmode="group",
        title="Preço por 500g por tipo de produto",
        labels={
            "tipo_produto": "Tipo de produto",
            "preco_500g_mediano": "Preço por 500g (R$)",
            "loja": "Loja",
        },
        hover_data={
            "produtos": True,
            "preco_unidade_mediano": ":.2f",
            "preco_500g_mediano": ":.2f",
        },
    )
    adicionar_rotulos_barras(fig_tipo)
    st.plotly_chart(fig_tipo, width="stretch")

    st.info(
        "Ponto de atenção: faixas pequenas, como cápsulas e porções individuais, "
        "normalmente ficam mais caras quando convertidas para 500g. Para comparar "
        "cafés tradicionais, visualize `Tradicional` e a faixa de 251g a 500g. "
        "`Outros` reúne produtos cujo título não deixa claro se são cápsula, "
        "solúvel, sachê, grãos ou café tradicional."
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
        f"**Leitura de mix:** `{fabricante_mais_presente}` é o fabricante com mais "
        "produtos dentro dos filtros atuais. O gráfico de mix mostra quais marcas "
        "têm maior presença no recorte selecionado. O gráfico de preço mediano "
        "compara o preço típico das marcas com pelo menos 5 produtos, evitando "
        "distorções causadas por fabricantes com poucos itens."
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
    adicionar_rotulos_barras(fig_mix, formato=".0f")
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
    adicionar_rotulos_barras(fig_fabricante)
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
        "loja_label",
        "tipo_produto_label",
        "preco",
        "quantidade_unidades",
        "peso_gramas",
        "faixa_peso_label",
        "preco_100g",
        "preco_500g",
        "preco_unidade",
    ]
    dados_tabela = dados[colunas].rename(
        columns={
            "loja_label": "Loja",
            "tipo_produto_label": "Tipo de produto",
            "faixa_peso_label": "Faixa de peso",
        }
    )
    st.dataframe(dados_tabela.sort_values("preco", ascending=False), width="stretch")

    st.download_button(
        "Baixar dados filtrados",
        data=dados_tabela.to_csv(index=False).encode("utf-8"),
        file_name="dados_precificacao_cafe_filtrados.csv",
        mime="text/csv",
    )

st.divider()
st.caption(
    "Para uma análise mais detalhada, acesse o "
    f"[repositório do projeto]({REPOSITORY_URL})."
)
