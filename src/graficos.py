from pathlib import Path
import os


ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib-cache"))

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


BASE = ROOT / "base"
TABELAS = ROOT / "relatorios" / "tabelas"
OUT = ROOT / "relatorios" / "graficos"


def salvar(fig, nome):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / nome, dpi=160, bbox_inches="tight")
    plt.close(fig)


def configurar_estilo():
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.labelsize"] = 11
    plt.rcParams["axes.titlesize"] = 14


def formatar_valor(valor, casas=2):
    if pd.isna(valor):
        return ""
    if casas == 0:
        return f"{valor:.0f}"
    return f"{valor:.{casas}f}"


def rotular_barras_verticais(ax, casas=2):
    for container in ax.containers:
        labels = [formatar_valor(barra.get_height(), casas) for barra in container]
        ax.bar_label(
            container,
            labels=labels,
            label_type="edge",
            padding=-15,
            fontsize=9,
            color="white",
        )
    ax.margins(y=0.12)


def rotular_barras_horizontais(ax, casas=2):
    for container in ax.containers:
        labels = [formatar_valor(barra.get_width(), casas) for barra in container]
        ax.bar_label(
            container,
            labels=labels,
            label_type="edge",
            padding=-30,
            fontsize=9,
            color="white",
        )
    ax.margins(x=0.15)


def grafico_preco_por_loja():
    df = pd.read_csv(TABELAS / "01_analise_preco_loja.csv")
    df = df.sort_values("median", ascending=False)

    fig, ax = plt.subplots()
    x = range(len(df))
    largura = 0.36

    ax.bar([i - largura / 2 for i in x], df["mean"], width=largura, label="Media")
    ax.bar([i + largura / 2 for i in x], df["median"], width=largura, label="Mediana")
    ax.set_xticks(list(x))
    ax.set_xticklabels(df["Loja"])
    ax.set_title("Preco medio e mediano por loja")
    ax.set_ylabel("Preco (R$)")
    ax.legend()
    rotular_barras_verticais(ax)

    salvar(fig, "01_preco_por_loja.png")


def grafico_distribuicao_precos():
    df = pd.read_csv(BASE / "base_cafe_normalizada_peso.csv")
    df = df[df["preco"].notna()].copy()

    fig, ax = plt.subplots()
    sns.boxplot(data=df, x="loja", y="preco", ax=ax)
    ax.set_title("Distribuicao de precos por loja")
    ax.set_xlabel("Loja")
    ax.set_ylabel("Preco (R$)")

    salvar(fig, "02_distribuicao_precos_loja.png")


def grafico_mix_fabricantes():
    df = pd.read_csv(TABELAS / "03_analise_mix.csv")
    top = df.sort_values("Total", ascending=False).head(12)
    top = top.sort_values("Total", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(top["Fabricante"], top["Total"])
    ax.set_title("Top fabricantes por quantidade de produtos")
    ax.set_xlabel("Quantidade de produtos")
    ax.set_ylabel("Fabricante")
    rotular_barras_horizontais(ax, casas=0)

    salvar(fig, "03_top_fabricantes_mix.png")


def grafico_mix_por_loja():
    df = pd.read_csv(TABELAS / "03_analise_mix.csv")
    top = df.sort_values("Total", ascending=False).head(10)
    top = top.set_index("Fabricante")[["Mambo", "St.Marche", "Paodeacucar"]]

    fig, ax = plt.subplots(figsize=(11, 7))
    top.plot(kind="bar", ax=ax)
    ax.set_title("Mix dos principais fabricantes por loja")
    ax.set_xlabel("Fabricante")
    ax.set_ylabel("Quantidade de produtos")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(title="Loja")
    rotular_barras_verticais(ax, casas=0)

    salvar(fig, "3.1_mix_fabricantes_por_loja.png")


def grafico_preco_normalizado_loja():
    df = pd.read_csv(TABELAS / "05_analise_preco_normalizado_peso_loja.csv")
    df = df.sort_values("preco_500g_mediano", ascending=False)

    fig, ax = plt.subplots()
    sns.barplot(data=df, x="loja", y="preco_500g_mediano", ax=ax)
    ax.set_title("Preco mediano normalizado por 500g")
    ax.set_xlabel("Loja")
    ax.set_ylabel("Preco mediano por 500g (R$)")
    rotular_barras_verticais(ax)

    salvar(fig, "04_preco_500g_por_loja.png")


def grafico_faixa_peso_loja():
    df = pd.read_csv(TABELAS / "04_analise_faixa_peso_loja.csv")
    df = df[df["faixa_peso"] != "sem_peso"].copy()
    ordem = ["ate_100g", "101g_250g", "251g_500g", "501g_1kg"]
    df["faixa_peso"] = pd.Categorical(df["faixa_peso"], categories=ordem, ordered=True)
    df = df.sort_values("faixa_peso")

    fig, ax = plt.subplots(figsize=(11, 7))
    sns.barplot(
        data=df,
        x="faixa_peso",
        y="preco_500g_mediano",
        hue="loja",
        ax=ax,
    )
    ax.set_title("Preco por 500g por faixa de peso e loja")
    ax.set_xlabel("Faixa de peso")
    ax.set_ylabel("Preco mediano por 500g (R$)")
    ax.legend(title="Loja")
    rotular_barras_verticais(ax)

    salvar(fig, "05_preco_500g_faixa_peso_loja.png")


def grafico_preco_fabricante():
    df = pd.read_csv(TABELAS / "06_analise_preco_fabricante.csv")
    df = df[df["count"] >= 5].copy()
    top = df.sort_values("median", ascending=False).head(15)
    top = top.sort_values("median", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(top["Fabricante"], top["median"])
    ax.set_title("Fabricantes com maior preco mediano")
    ax.set_xlabel("Preco mediano (R$)")
    ax.set_ylabel("Fabricante")
    rotular_barras_horizontais(ax)

    salvar(fig, "06_preco_mediano_fabricante.png")


def main():
    configurar_estilo()
    grafico_preco_por_loja()
    grafico_distribuicao_precos()
    grafico_mix_fabricantes()
    grafico_mix_por_loja()
    grafico_preco_normalizado_loja()
    grafico_faixa_peso_loja()
    grafico_preco_fabricante()
    print(f"Graficos salvos em: {OUT}")


if __name__ == "__main__":
    main()
