import pandas as pd
from pandas.io.formats.style import Styler
from pandas.api.types import is_numeric_dtype


def colunas_numericas(df: pd.DataFrame) -> list[str]:
    return [col for col in df.columns if is_numeric_dtype(df[col])]


def estilizar_tabela_numeros_negrito(
    df: pd.DataFrame,
    casas_decimais: int = 2,
) -> Styler:
    """Retorna um Styler para notebooks com numeros em negrito."""
    numeric_cols = colunas_numericas(df)
    formatadores = {
        col: (
            f"{{:,.{casas_decimais}f}}"
            if not pd.api.types.is_integer_dtype(df[col])
            else "{:,.0f}"
        )
        for col in numeric_cols
    }

    return (
        df.style.format(formatadores)
        .set_properties(subset=numeric_cols, **{"font-weight": "bold"})
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("font-weight", "bold"),
                        ("background-color", "#F4F1EA"),
                        ("color", "#2F4858"),
                    ],
                },
                {
                    "selector": "td",
                    "props": [
                        ("border-color", "#E2DED6"),
                    ],
                },
            ]
        )
    )


def tabela_negrito(df: pd.DataFrame, casas_decimais: int = 2) -> Styler:
    return estilizar_tabela_numeros_negrito(df, casas_decimais=casas_decimais)
