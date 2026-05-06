# Notas da Análise COmpleta

## Resumo executivo

O mercado analisado apresenta forte dispersão de preços. O preço típico do café fica próximo de R$30, mas a média é puxada para cima por produtos premium e por itens pequenos, como cápsulas e porções individuais.

Na comparação direta por loja, St Marche tem o maior preço médio e mediano. Mambo aparece em posição intermediária, enquanto Pão de Açúcar tem o menor preço mediano bruto. Quando o preço é normalizado para 500g, a leitura muda: Pão de Açúcar passa a apresentar o maior preço mediano proporcional.

## Preço por loja

St Marche apresenta o maior preço médio, R$36.01, e a maior mediana, R$31.99, sinalizando maior participação de produtos premium no mix.

Mambo fica em patamar intermediário, com preço médio de R$34.10 e mediana de R$29.90. Pão de Açúcar tem o menor preço mediano bruto, R$27.96, o que sugere maior competitividade no preço de prateleira por item.

A diferença entre média e mediana nas lojas indica presença de produtos caros elevando a média, especialmente em St Marche e Mambo.

## Preço normalizado por 500g

A normalização por 500g serve para comparar produtos de tamanhos diferentes em uma mesma base. Sem esse ajuste, uma embalagem pequena pode parecer barata apenas porque custa menos no total, mesmo sendo mais cara quando olhamos o preço por quantidade de café.

Exemplo simples: um produto de 50g por R$20 custa menos na prateleira do que um pacote de 500g por R$35. Mas, proporcionalmente, 500g desse produto pequeno custariam R$200. Por isso, a normalização ajuda a separar "preço baixo por embalagem" de "preço baixo por quantidade".

Nessa métrica, Pão de Açúcar apresenta o maior preço mediano por 500g, R$112.38. Mambo e St Marche ficam muito próximos, com R$99.90 e R$99.86, respectivamente.

Isso mostra que o menor preço bruto do Pão de Açúcar não significa necessariamente menor preço relativo por quantidade de café. A loja pode ter produtos com embalagens menores ou itens que parecem baratos na prateleira, mas ficam mais caros quando convertidos para uma base comum de 500g.

## Faixa de peso

A análise por faixa de peso confirma que itens pequenos distorcem a comparação geral. A faixa `ate_100g`, composta principalmente por cápsulas e porções individuais, apresenta os maiores valores proporcionais por 500g.

Para comparar cafés tradicionais, a faixa `251g_500g` é a mais adequada. Nessa faixa, Pão de Açúcar tem a menor mediana, R$34.99, enquanto St Marche fica em R$41.50 e Mambo em R$43.49.

Portanto, a leitura correta depende da pergunta de negócio: para preço por item, Pão de Açúcar é mais competitivo; para preço proporcional considerando todo o mix, ele aparece mais caro; para pacotes tradicionais, volta a ser o mais competitivo.

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
- preço mediano por fabricante.
