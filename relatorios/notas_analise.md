# Notas da Analise

## Resumo executivo

O mercado analisado apresenta forte dispersao de precos. O preco tipico do cafe fica proximo de R$30, mas a media e puxada para cima por produtos premium e por itens pequenos, como capsulas e porcoes individuais.

Na comparacao direta por loja, St Marche tem o maior preco medio e mediano. Mambo aparece em posicao intermediaria, enquanto Pao de Acucar tem o menor preco mediano bruto. Quando o preco e normalizado para 500g, a leitura muda: Pao de Acucar passa a apresentar o maior preco mediano proporcional.

## Preco por loja

St Marche apresenta o maior preco medio, R$36.01, e a maior mediana, R$31.99, sinalizando maior participacao de produtos premium no mix.

Mambo fica em patamar intermediario, com preco medio de R$34.10 e mediana de R$29.90. Pao de Acucar tem o menor preco mediano bruto, R$27.96, o que sugere maior competitividade no preco de prateleira por item.

A diferenca entre media e mediana nas lojas indica presenca de produtos caros elevando a media, especialmente em St Marche e Mambo.

## Preco normalizado por 500g

A normalizacao por 500g serve para comparar produtos de tamanhos diferentes em uma mesma base. Sem esse ajuste, uma embalagem pequena pode parecer barata apenas porque custa menos no total, mesmo sendo mais cara quando olhamos o preco por quantidade de cafe.

Exemplo simples: um produto de 50g por R$20 custa menos na prateleira do que um pacote de 500g por R$35. Mas, proporcionalmente, 500g desse produto pequeno custariam R$200. Por isso, a normalizacao ajuda a separar "preco baixo por embalagem" de "preco baixo por quantidade".

Nessa metrica, Pao de Acucar apresenta o maior preco mediano por 500g, R$112.38. Mambo e St Marche ficam muito proximos, com R$99.90 e R$99.86, respectivamente.

Isso mostra que o menor preco bruto do Pao de Acucar nao significa necessariamente menor preco relativo por quantidade de cafe. A loja pode ter produtos com embalagens menores ou itens que parecem baratos na prateleira, mas ficam mais caros quando convertidos para uma base comum de 500g.

## Faixa de peso

A analise por faixa de peso confirma que itens pequenos distorcem a comparacao geral. A faixa `ate_100g`, composta principalmente por capsulas e porcoes individuais, apresenta os maiores valores proporcionais por 500g.

Para comparar cafes tradicionais, a faixa `251g_500g` e a mais adequada. Nessa faixa, Pao de Acucar tem a menor mediana, R$34.99, enquanto St Marche fica em R$41.50 e Mambo em R$43.49.

Portanto, a leitura correta depende da pergunta de negocio: para preco por item, Pao de Acucar e mais competitivo; para preco proporcional considerando todo o mix, ele aparece mais caro; para pacotes tradicionais, volta a ser o mais competitivo.

## Fabricantes

A analise por fabricante indica concentracao em faixas intermediarias de preco, com marcas de entrada e marcas premium convivendo no mesmo mercado.

Os nomes equivalentes de fabricantes foram consolidados antes da analise. Exemplos: Lor, L'Or e L'OR foram tratados como L'OR; ORFEU como Orfeu; Tres, Tres Coracoes e variantes foram tratados como 3 Coracoes.

Entre os fabricantes com pelo menos 5 produtos, Italle aparece com baixa variacao de preco: media de R$15.88, mediana de R$13.99 e amplitude de R$5.00. Isso sugere posicionamento mais consistente em uma faixa acessivel.

## Graficos gerados

Os graficos finais estao em `relatorios/graficos` e cobrem:

- preco medio e mediano por loja;
- distribuicao de precos por loja;
- mix de fabricantes;
- mix dos principais fabricantes por loja;
- preco normalizado por 500g;
- preco por 500g por faixa de peso;
- preco mediano por fabricante.
