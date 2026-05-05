# Notas da Analise

## Analise de distribuicao de preco

O preco tipico do cafe esta proximo de R$30.

A maior parte do mercado esta entre R$25 e R$38.

Existem produtos premium que elevam a media.

O mercado apresenta alta variacao de precos.

O mercado de cafe possui alta dispersao de precos, indicando forte segmentacao entre produtos economicos, intermediarios e premium.

## Analise de preco por loja

A analise de precos de cafe entre os supermercados indica diferencas claras de posicionamento. O St Marche apresenta o maior preco medio, aproximadamente R$36, e mediana de R$31, sugerindo presenca significativa de produtos premium.

O Mambo apresenta precos intermediarios, enquanto o Pao de Acucar demonstra maior competitividade de preco no mercado analisado.

A diferenca entre media e mediana nas lojas indica a existencia de produtos de alto valor que elevam o preco medio, especialmente no St Marche.

### Outliers

https://marche.com.br/collections/mercearia/products/cappuccino-lor-baunilha-8-unidades-162-4g?store_id=66677604431

Temos a presenca de outliers na distribuicao de precos. O menor corresponde a um produto em formato de dose individual, enquanto o maior preco refere-se a um cafe premium em graos. Esses extremos ampliam a dispersao dos dados.

https://marche.com.br/collections/mercearia/products/cafe-espresso-graos-cafe-do-ponto-1kg?store_id=66677604431

### Para melhorar o dataset

Normalizacao por peso implementada nos arquivos:

- `base_cafe_normalizada_peso.csv`: base consolidada com peso extraido do titulo, unidade original, faixa de peso, preco por 100g, preco por 500g e preco por unidade.
- `05_analise_preco_normalizado_peso_loja.csv`: resumo por loja com cobertura de peso e medianas normalizadas.
- `04_analise_faixa_peso_loja.csv`: comparacao de preco por loja e faixa de peso.

A extracao identifica produtos em g e kg, converte kg para gramas e separa produtos sem peso explicito. Quando existe quantidade de capsulas/unidades no titulo, tambem calcula preco por unidade.

### Analise de preco normalizado por peso e loja

Essa tabela resume o preco dos produtos por loja depois da normalizacao de peso. Ela ajuda a comparar supermercados mesmo quando os produtos possuem tamanhos diferentes, como 52g, 250g, 500g ou 1kg.

Colunas:

- `loja`: supermercado analisado.
- `produtos`: quantidade total de produtos considerados na loja.
- `produtos_com_peso`: quantidade de produtos em que foi possivel extrair peso do titulo.
- `cobertura_peso_pct`: percentual de produtos com peso identificado.
- `preco_mediano`: mediana do preco original dos produtos, sem ajuste por peso.
- `preco_500g_mediano`: mediana do preco convertido para uma base comum de 500g.
- `preco_100g_mediano`: mediana do preco convertido para uma base comum de 100g.
- `preco_unidade_mediano`: mediana do preco por unidade ou capsula, quando a quantidade aparece no titulo.

Leitura da tabela:

O `preco_mediano` mostra o preco tipico de compra por produto. Ja o `preco_500g_mediano` e o `preco_100g_mediano` permitem comparar melhor produtos de tamanhos diferentes. O `preco_unidade_mediano` e mais util para capsulas, sachês e caixas com varias unidades.

Pelos resultados, Mambo e St Marche ficaram muito proximos no preco mediano por 500g, enquanto o Pao de Acucar ficou acima nessa metrica. Isso indica que, apesar de o Pao de Acucar ter menor preco mediano bruto, os produtos comparaveis por peso podem ter preco relativo maior.

### Analise por faixa de peso e loja

Essa tabela separa os produtos em faixas de peso para comparar produtos mais parecidos entre si. Isso evita misturar uma capsula de 52g com um pacote de 500g ou um cafe em graos de 1kg na mesma leitura.

Colunas:

- `loja`: supermercado analisado.
- `faixa_peso`: grupo de peso extraido do titulo.
- `produtos`: quantidade de produtos naquela loja e naquela faixa.
- `preco_mediano`: mediana do preco original dentro da faixa.
- `preco_500g_mediano`: mediana do preco convertido para 500g dentro da faixa.

Faixas usadas:

- `ate_100g`: produtos pequenos, geralmente capsulas, sachês e porcoes individuais.
- `101g_250g`: produtos intermediarios, como pacotes de 250g e alguns soluveis.
- `251g_500g`: pacotes tradicionais, principalmente cafes de 500g.
- `501g_1kg`: produtos maiores, como pacotes de 1kg.
- `sem_peso`: produtos em que o peso nao foi identificado no titulo.

Leitura da tabela:

A faixa `ate_100g` tende a apresentar preco por 500g muito mais alto, porque concentra capsulas e produtos pequenos. Ja a faixa `251g_500g` e melhor para comparar cafes tradicionais de pacote, pois reduz a distorcao causada por capsulas e itens premium pequenos.

Importante: o `preco_500g_mediano` nao significa que o produto custa esse valor na prateleira. Ele mostra quanto o produto custaria proporcionalmente se tivesse 500g.

Exemplo:

- Uma caixa de capsulas com 50g custa R$25.
- Como 500g equivale a 10 vezes 50g, o preco proporcional por 500g fica R$250.
- Isso nao quer dizer que a caixa custa R$250; ela continua custando R$25.
- O calculo apenas mostra que, por quantidade de cafe, capsulas e produtos pequenos sao mais caros que pacotes tradicionais.

Por isso, no grafico de preco por 500g por faixa de peso, a faixa `ate_100g` aparece mais alta. Ela concentra produtos pequenos, que ficam caros quando comparados em uma base proporcional de 500g.

Essa separacao deixa a analise mais justa: em vez de comparar todos os cafes juntos, compara produtos por tamanho aproximado.

## Graficos da analise

Os graficos estao organizados na pasta `relatorios/graficos`.

Arquivos gerados:

- `01_preco_por_loja.png`: compara media e mediana de preco por loja.
- `02_distribuicao_precos_loja.png`: mostra a dispersao de precos por loja e evidencia outliers.
- `03_top_fabricantes_mix.png`: mostra os fabricantes com maior quantidade total de produtos.
- `3.1_mix_fabricantes_por_loja.png`: compara o mix dos principais fabricantes entre as lojas.
- `04_preco_500g_por_loja.png`: compara o preco mediano normalizado para 500g por loja.
- `05_preco_500g_faixa_peso_loja.png`: compara o preco por 500g dentro de cada faixa de peso e loja, desconsiderando `sem_peso` porque essa categoria nao permite normalizacao por gramas.
- `06_preco_mediano_fabricante.png`: destaca fabricantes com maior preco mediano, considerando fabricantes com pelo menos 5 produtos.

## Analise de preco por fabricante

A analise de precos por fabricante indica que o mercado de cafe possui concentracao de produtos em faixas de preco intermediarias.

Os nomes equivalentes de fabricantes foram normalizados antes da agregacao. Exemplos: Lor, L'Or e L'OR foram consolidados como L'OR; ORFEU foi consolidado como Orfeu; Tres, Três e Tres Coracoes foram consolidados como 3 Corações.

A marca Italle mostra um preco medio de R$15.88 com mediana de R$13.99, indicando que a maior parte dos produtos esta concentrada em faixas de preco relativamente acessiveis.

A amplitude de preco e de R$5, demonstrando baixa variacao dentro do portfolio da marca. Isso sugere uma estrategia de precificacao consistente, posicionando a marca em um segmento de preco mais competitivo e acessivel no mercado.
