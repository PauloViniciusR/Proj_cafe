# Análise de Precificação de Cafés em Supermercados

Projeto de Analista de Dados/BI voltado à comparação de preços, sortimento e posicionamento de produtos de café em supermercados. A proposta é transformar dados de prateleira em indicadores de apoio à decisão comercial, com foco em precificação, mix de fabricantes e comparação justa entre embalagens de tamanhos diferentes.

## Problema de negócio

Comparar preços de produtos de café apenas pelo valor de prateleira pode gerar conclusões incorretas. Um item de 50g pode parecer barato quando comparado a um pacote de 500g, mas ser muito mais caro quando o preço é convertido para uma mesma quantidade.

Este projeto responde perguntas como:

- Qual loja apresenta maior ou menor preço mediano?
- O menor preço por embalagem também representa menor preço por quantidade?
- Como o mix de fabricantes muda entre supermercados?
- Quais fabricantes aparecem em faixas mais premium ou mais acessíveis?
- Como embalagens pequenas, cápsulas e porções individuais distorcem a leitura de preço?

## Objetivo

Construir uma análise de apoio à precificação para cafés vendidos em supermercados, usando Python para preparar os dados, gerar indicadores, criar visualizações e consolidar insights de negócio.

O projeto foi posicionado como um case de **Analista de Dados/BI**, com foco em:

- preparação e padronização de dados;
- criação de indicadores de preço;
- análise exploratória;
- visualizações para tomada de decisão;
- comunicação executiva dos resultados.

## Dados

A base contém produtos de café coletados em lojas como Mambo, St Marche e Pão de Açúcar. Os dados brutos ficam na pasta `base/`, mas essa pasta está preparada para não versionar arquivos `.csv` e `.xlsx` no GitHub.

Isso evita publicar dados brutos quando eles não puderem ser compartilhados. Para permitir a publicação do dashboard, o projeto mantém uma base processada e reduzida em `data/processed/base_cafe_normalizada_peso.csv`, contendo apenas os campos necessários para os indicadores e gráficos.

Os resultados derivados do projeto ficam em:

- `data/processed/`: base processada usada pelo dashboard publicado;
- `relatorios/tabelas/`: tabelas consolidadas da análise;
- `relatorios/graficos/`: gráficos exportados;
- `relatorios/notas_analise.md`: notas detalhadas da análise;
- `relatorios/relatorio_executivo.md`: leitura de negócio para apresentação.

## Metodologia

1. **Coleta e consolidação**
   - reunião dos produtos por loja;
   - padronização de nomes de lojas e fabricantes;
   - tratamento de preços e disponibilidade.

2. **Tratamento e enriquecimento**
   - extração do peso em gramas;
   - classificação por faixa de peso;
   - cálculo de preço por 100g, 500g e unidade;
   - consolidação de fabricantes equivalentes.

3. **Análise**
   - preço médio, mediano, mínimo e máximo por loja;
   - distribuição de preços e outliers;
   - comparação do preço bruto contra preço normalizado por 500g;
   - análise de mix de fabricantes;
   - análise de preço por fabricante.

4. **Visualização**
   - gráficos estáticos exportados em PNG;
   - dashboard em Streamlit para exploração interativa.

## Principais insights

- St Marche possui o maior preço médio e mediano no preço bruto, sugerindo maior presença de produtos premium.
- Pão de Açúcar tem o menor preço mediano por item, mas passa a ter o maior preço mediano quando o preço é normalizado por 500g.
- Itens pequenos, como cápsulas e porções individuais, elevam muito o preço proporcional por quantidade.
- Para comparar cafés tradicionais, a faixa de 251g a 500g é mais adequada do que comparar todo o mix junto.
- O mix de fabricantes influencia diretamente a leitura de posicionamento de preço de cada loja.


## Estrutura

```text
.
├── app.py                         # Dashboard interativo em Streamlit
├── base/                          # Dados brutos locais, não versionados
├── data/
│   └── processed/                 # Base processada para o dashboard
├── notebooks/                     # Análises exploratórias
├── relatorios/
│   ├── graficos/                  # Gráficos exportados
│   ├── tabelas/                   # Indicadores consolidados
│   ├── notas_analise.md           # Notas detalhadas da análise
│   └── relatorio_executivo.md     # Resumo
├── src/
│   ├── config.py                  # Caminhos e funções de carga
│   ├── graficos.py                # Geração dos gráficos
│   └── utils.py                   # Funções auxiliares
├── environment.yml
└── README.md
```

## Limitações

- A análise é majoritariamente descritiva, pois a base não possui histórico longo suficiente para modelagem temporal robusta.
- O projeto não afirma implementar precificação dinâmica completa; ele entrega uma base analítica para apoiar decisões de preço.
- Comparações entre lojas dependem do sortimento disponível em cada uma, então a interpretação deve considerar diferenças de mix, embalagem e fabricante.
