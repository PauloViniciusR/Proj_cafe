# Análise Descritiva de Preços de Café em Supermercados

Este projeto realiza uma análise descritiva de preços de produtos de café em diferentes supermercados, utilizando dados coletados de lojas como Mambo, St Marche e Pão de Açúcar.

O objetivo principal é comparar preços, sortimento e posicionamento das lojas a partir de métricas como preço médio, mediana, distribuição de preços, mix de fabricantes e preço normalizado por peso.

## Principais Análises

- Comparação de preço médio e mediano por loja
- Distribuição de preços e identificação de outliers
- Análise do mix de fabricantes por supermercado
- Ranking de fabricantes por quantidade de produtos
- Análise de preço por fabricante
- Normalização de preços por peso
- Comparação de preço por 100g, 500g e unidade/cápsula
- Análise por faixas de peso
- Geração de gráficos para apresentação dos resultados

## Destaques

A normalização por peso foi uma etapa importante do projeto, pois permite comparar produtos de tamanhos diferentes, como cápsulas, sachês, pacotes de 250g, 500g e cafés de 1kg.

Com isso, a análise evita conclusões distorcidas baseadas apenas no preço bruto do produto.

## Tecnologias

- Python
- Pandas
- Matplotlib
- Seaborn

## Estrutura

- `base/`: bases utilizadas no projeto
- `results/`: tabelas finais, notas analíticas e gráficos
- `scripts/`: scripts para geração dos gráficos

## Observação

Este projeto tem foco em análise descritiva. A base não foi utilizada para previsão temporal, pois o histórico disponível é curto.
