# Relatório - Análise de Precificação de Cafés

## Contexto

Este projeto avalia preços de produtos de café em supermercados com o objetivo de apoiar decisões de precificação, comparação competitiva e leitura de posicionamento de mercado.

A análise considera que produtos de café possuem embalagens e formatos muito diferentes, como cápsulas, cafés solúveis, sachês, grãos, pacotes de 250g, 500g e 1kg. Por isso, comparar apenas o preço de prateleira ou misturar todos os formatos em um único preço por 500g pode levar a conclusões distorcidas.

## Perguntas respondidas

- Qual loja tem maior preço médio e mediano?
- O menor preço por item também representa menor preço por quantidade?
- Como o preço muda quando normalizado para 500g?
- Quais faixas de peso mais distorcem a comparação?
- Como a leitura muda quando separamos cápsulas, solúveis e cafés tradicionais?
- Como o mix de fabricantes influencia o posicionamento das lojas?

## Principais resultados

St Marche apresentou o maior preço médio e mediano no preço bruto, indicando um mix com maior participação de itens premium ou produtos de maior valor agregado.

Mambo ficou em posição intermediária no preço bruto, com comportamento semelhante ao St Marche quando o mix completo é normalizado por 500g.

Pão de Açúcar apresentou o menor preço mediano por item, mas passou a ter o maior preço mediano proporcional quando todo o mix foi normalizado para 500g. Essa leitura não deve ser usada isoladamente como conclusão de loja mais cara: ela reflete forte influência de cápsulas e itens pequenos.

Após segmentar por tipo de produto, a análise fica mais consistente. Em cafés tradicionais, Pão de Açúcar apresenta menor mediana por 500g do que Mambo e St Marche. Em cápsulas, a comparação deve considerar também preço por unidade.

## Insight central

A principal conclusão é que a decisão de preço muda conforme a métrica e o recorte usados.

No preço bruto por item, Pão de Açúcar parece mais competitivo. No preço proporcional por 500g considerando todo o mix, a leitura se inverte por efeito de sortimento. Já para cafés tradicionais entre 251g e 500g, Pão de Açúcar volta a aparecer como mais competitivo.

Isso mostra que uma análise de precificação precisa separar pelo menos quatro visões:

- preço por item;
- preço por quantidade padronizada;
- preço por faixa de embalagem.
- preço por tipo de produto.

## Recomendações de negócio

Usar preço mediano em vez de apenas preço médio para reduzir o impacto de produtos muito caros ou muito baratos.

Comparar produtos por tipo e faixa de peso antes de tomar decisões de reajuste, principalmente separando cápsulas, solúveis, sachês e pacotes tradicionais.

Monitorar o preço por 500g como indicador padronizado apenas dentro de recortes comparáveis. Para cápsulas, acompanhar também preço por unidade.

Analisar o mix de fabricantes junto com o preço, pois uma loja pode parecer mais cara simplesmente por trabalhar com maior concentração de marcas premium.

Usar o dashboard como ferramenta de acompanhamento recorrente para identificar mudanças de posicionamento, produtos fora do padrão e oportunidades de ajuste.

## Limitações

A base analisada representa um recorte de produtos disponíveis, não uma série histórica longa. Por esse motivo, o projeto não é um modelo completo de precificação dinâmica. Alguns títulos truncados não informam peso total de forma confiável; nesses casos, o preço por 500g foi deixado em branco para evitar distorções.
