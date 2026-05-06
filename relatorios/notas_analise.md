# Notas da Análise Completa

## Resumo executivo

O mercado analisado apresenta forte dispersão de preços. O preço típico do café fica próximo de R$30, mas a média é puxada para cima por produtos premium e por itens pequenos, como cápsulas, sachês, cafés solúveis e porções individuais.

Na comparação direta por loja, St Marche tem o maior preço médio e mediano. Mambo aparece em posição intermediária, enquanto Pão de Açúcar tem o menor preço mediano bruto. Quando todo o mix é normalizado para 500g, Pão de Açúcar passa a apresentar o maior preço mediano proporcional, mas essa leitura deve ser interpretada como efeito de mix. A comparação justa precisa separar tipo de produto e faixa de peso.

A base foi reprocessada para corrigir casos como `10 Unidades 8g Cada`, que antes podiam ser lidos como apenas 8g totais. Agora esses itens são tratados como 80g totais. Quando o título de cápsula contém apenas pesos muito pequenos, como 5g, 8g ou 11g, sem indicar claramente peso total ou "cada", o projeto evita calcular preço por 500g para não criar outliers artificiais.

## Preço por loja

St Marche apresenta o maior preço médio, R$36.01, e a maior mediana, R$31.99, sinalizando maior participação de produtos premium no mix.

Mambo fica em patamar intermediário, com preço médio de R$34.10 e mediana de R$29.90. Pão de Açúcar tem o menor preço mediano bruto, R$27.96, o que sugere maior competitividade no preço de prateleira por item.

A diferença entre média e mediana nas lojas indica presença de produtos caros elevando a média, especialmente em St Marche e Mambo.

## Preço normalizado por 500g

A normalização por 500g serve para comparar produtos de tamanhos diferentes em uma mesma base, mas só é uma comparação justa quando os produtos são comparáveis. Cápsulas, solúveis, sachês, grãos e cafés tradicionais têm propostas e embalagens diferentes.

Exemplo simples: um produto de 50g por R$20 custa menos na prateleira do que um pacote de 500g por R$35. Mas, proporcionalmente, 500g desse produto pequeno custariam R$200. Por isso, a normalização ajuda a separar "preço baixo por embalagem" de "preço baixo por quantidade".

No mix completo, Pão de Açúcar apresenta o maior preço mediano por 500g, R$114.95. Mambo fica em R$99.90 e St Marche em R$98.79.

Essa métrica não deve ser lida sozinha como "loja mais cara". Ela mostra que o sortimento do Pão de Açúcar tem maior peso de produtos pequenos ou proporcionalmente caros. Para decisão de preço, o indicador deve ser filtrado por tipo de produto.

Entre cafés tradicionais, a mediana por 500g é R$54.98 no Mambo, R$48.99 no Pão de Açúcar e R$67.80 no St Marche. Nesse recorte, Pão de Açúcar é o mais competitivo.

## Faixa de peso

A análise por faixa de peso confirma que itens pequenos distorcem a comparação geral. A faixa `ate_100g`, composta principalmente por cápsulas e porções individuais, apresenta os maiores valores proporcionais por 500g.

Para comparar cafés tradicionais, a faixa `251g_500g` é a mais adequada. Nessa faixa e considerando apenas produtos tradicionais, Pão de Açúcar tem a menor mediana, R$29.29, enquanto Mambo fica em R$39.94 e St Marche em R$41.50.

Portanto, a leitura correta depende da pergunta de negócio: para preço por item, Pão de Açúcar é mais competitivo; para preço proporcional considerando todo o mix, ele aparece mais caro por efeito de sortimento; para pacotes tradicionais, continua sendo o mais competitivo.

## Tipo de produto

A nova coluna `tipo_produto` separa a base em `capsula`, `tradicional`, `soluvel`, `graos`, `sache_drip` e `outros`. Essa segmentação reduz o risco de comparar produtos que não competem diretamente entre si.

As cápsulas têm preço por 500g muito superior aos cafés tradicionais: Mambo tem mediana de R$239.80, Pão de Açúcar R$240.29 e St Marche R$251.13. Para cápsulas, o preço por unidade também é relevante: Mambo tem mediana de R$2.55, Pão de Açúcar R$2.70 e St Marche R$2.95.

Nos cafés tradicionais, o preço por 500g é mais adequado para comparação direta entre lojas. Nesse recorte, Pão de Açúcar apresenta a menor mediana proporcional.

## Fabricantes

A análise por fabricante indica concentração em faixas intermediárias de preço, com marcas de entrada e marcas premium convivendo no mesmo mercado.

Os nomes equivalentes de fabricantes foram consolidados antes da análise. Exemplos: Lor, L'Or e L'OR foram tratados como L'OR; ORFEU como Orfeu; Três, Três Corações e variantes foram tratados como 3 Corações.

Entre os fabricantes com pelo menos 5 produtos, Italle aparece com baixa variação de preço: média de R$15.88, mediana de R$13.99 e amplitude de R$5.00. Isso sugere posicionamento mais consistente em uma faixa acessível.

## Gráficos gerados

Os gráficos finais estão em `relatorios/graficos` e cobrem:

- preço médio e mediano por loja;
- distribuição de preços por loja;
- mix de fabricantes;
- mix dos principais fabricantes por loja;
- preço normalizado por 500g;
- preço por 500g por faixa de peso;
- preço mediano por fabricante;
- preço por 500g por tipo de produto.
