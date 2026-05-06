# Relatório Executivo - Análise de Precificação de Cafés

## Contexto

Este projeto avalia preços de produtos de café em supermercados com o objetivo de apoiar decisões de precificação, comparação competitiva e leitura de posicionamento de mercado.

A análise considera que produtos de café possuem embalagens muito diferentes, como cápsulas, porções pequenas, pacotes de 250g, 500g e 1kg. Por isso, comparar apenas o preço de prateleira pode levar a conclusões distorcidas.

## Perguntas respondidas

- Qual loja tem maior preço médio e mediano?
- O menor preço por item também representa menor preço por quantidade?
- Como o preço muda quando normalizado para 500g?
- Quais faixas de peso mais distorcem a comparação?
- Como o mix de fabricantes influencia o posicionamento das lojas?

## Principais resultados

St Marche apresentou o maior preço médio e mediano no preço bruto, indicando um mix com maior participação de itens premium ou produtos de maior valor agregado.

Mambo ficou em posição intermediária no preço bruto, com comportamento semelhante ao St Marche quando os preços são normalizados por 500g.

Pão de Açúcar apresentou o menor preço mediano por item, mas passou a ter o maior preço mediano proporcional quando os produtos foram normalizados para 500g. Isso indica que parte dos produtos pode parecer competitiva no preço de prateleira, mas não necessariamente no preço por quantidade.

## Insight central

A principal conclusão é que a decisão de preço muda conforme a métrica usada.

No preço bruto por item, Pão de Açúcar parece mais competitivo. No preço proporcional por 500g, a leitura se inverte. Já para pacotes tradicionais entre 251g e 500g, Pão de Açúcar volta a aparecer como mais competitivo.

Isso mostra que uma análise de precificação precisa separar pelo menos três visões:

- preço por item;
- preço por quantidade padronizada;
- preço por faixa de embalagem.

## Recomendações de negócio

Usar preço mediano em vez de apenas preço médio para reduzir o impacto de produtos muito caros ou muito baratos.

Comparar produtos por faixa de peso antes de tomar decisões de reajuste, principalmente separando cápsulas e porções individuais dos pacotes tradicionais.

Monitorar o preço por 500g como indicador padronizado para comparar lojas e fabricantes.

Analisar o mix de fabricantes junto com o preço, pois uma loja pode parecer mais cara simplesmente por trabalhar com maior concentração de marcas premium.

Usar o dashboard como ferramenta de acompanhamento recorrente para identificar mudanças de posicionamento, produtos fora do padrão e oportunidades de ajuste.

## Limitações

A base analisada representa um recorte de produtos disponíveis, não uma série histórica longa. Por esse motivo, o projeto não deve ser vendido como modelo completo de precificação dinâmica.

O uso correto é como uma entrega de BI e análise de dados para apoiar decisões de preço. Uma etapa futura poderia incluir histórico de preços, volume de vendas, margem, estoque e dados de concorrência para evoluir para modelos preditivos.

## Próximos passos sugeridos

Adicionar histórico semanal ou mensal de preços.

Incluir margem, custo e volume vendido para avaliar rentabilidade, não apenas preço.

Criar alertas de produtos com preço acima ou abaixo do padrão da categoria.

Evoluir para um modelo estatístico simples de preço esperado por fabricante, loja, peso e tipo de embalagem.
