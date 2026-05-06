# Relatorio Executivo - Analise de Precificacao de Cafes

## Contexto

Este projeto avalia precos de produtos de cafe em supermercados com o objetivo de apoiar decisoes de precificacao, comparacao competitiva e leitura de posicionamento de mercado.

A analise considera que produtos de cafe possuem embalagens muito diferentes, como capsulas, porcoes pequenas, pacotes de 250g, 500g e 1kg. Por isso, comparar apenas o preco de prateleira pode levar a conclusoes distorcidas.

## Perguntas respondidas

- Qual loja tem maior preco medio e mediano?
- O menor preco por item tambem representa menor preco por quantidade?
- Como o preco muda quando normalizado para 500g?
- Quais faixas de peso mais distorcem a comparacao?
- Como o mix de fabricantes influencia o posicionamento das lojas?

## Principais resultados

St Marche apresentou o maior preco medio e mediano no preco bruto, indicando um mix com maior participacao de itens premium ou produtos de maior valor agregado.

Mambo ficou em posicao intermediaria no preco bruto, com comportamento semelhante ao St Marche quando os precos sao normalizados por 500g.

Pao de Acucar apresentou o menor preco mediano por item, mas passou a ter o maior preco mediano proporcional quando os produtos foram normalizados para 500g. Isso indica que parte dos produtos pode parecer competitiva no preco de prateleira, mas nao necessariamente no preco por quantidade.

## Insight central

A principal conclusao e que a decisao de preco muda conforme a metrica usada.

No preco bruto por item, Pao de Acucar parece mais competitivo. No preco proporcional por 500g, a leitura se inverte. Ja para pacotes tradicionais entre 251g e 500g, Pao de Acucar volta a aparecer como mais competitivo.

Isso mostra que uma analise de precificacao precisa separar pelo menos tres visoes:

- preco por item;
- preco por quantidade padronizada;
- preco por faixa de embalagem.

## Recomendacoes de negocio

Usar preco mediano em vez de apenas preco medio para reduzir o impacto de produtos muito caros ou muito baratos.

Comparar produtos por faixa de peso antes de tomar decisoes de reajuste, principalmente separando capsulas e porcoes individuais dos pacotes tradicionais.

Monitorar o preco por 500g como indicador padronizado para comparar lojas e fabricantes.

Analisar o mix de fabricantes junto com o preco, pois uma loja pode parecer mais cara simplesmente por trabalhar com maior concentracao de marcas premium.

Usar o dashboard como ferramenta de acompanhamento recorrente para identificar mudancas de posicionamento, produtos fora do padrao e oportunidades de ajuste.

## Limitacoes

A base analisada representa um recorte de produtos disponiveis, nao uma serie historica longa. Por esse motivo, o projeto nao deve ser vendido como modelo completo de precificacao dinamica.

O uso correto e como uma entrega de BI e analise de dados para apoiar decisoes de preco. Uma etapa futura poderia incluir historico de precos, volume de vendas, margem, estoque e dados de concorrencia para evoluir para modelos preditivos.

## Proximos passos sugeridos

Adicionar historico semanal ou mensal de precos.

Incluir margem, custo e volume vendido para avaliar rentabilidade, nao apenas preco.

Criar alertas de produtos com preco acima ou abaixo do padrao da categoria.

Evoluir para um modelo estatistico simples de preco esperado por fabricante, loja, peso e tipo de embalagem.
