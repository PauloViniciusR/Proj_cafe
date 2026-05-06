# Analise de Precificacao de Cafes em Supermercados

Projeto de Analista de Dados/BI voltado a comparacao de precos, sortimento e posicionamento de produtos de cafe em supermercados. A proposta e transformar dados de prateleira em indicadores de apoio a decisao comercial, com foco em precificacao, mix de fabricantes e comparacao justa entre embalagens de tamanhos diferentes.

## Problema de negocio

Comparar precos de produtos de cafe apenas pelo valor de prateleira pode gerar conclusoes incorretas. Um item de 50g pode parecer barato quando comparado a um pacote de 500g, mas ser muito mais caro quando o preco e convertido para uma mesma quantidade.

Este projeto responde perguntas como:

- Qual loja apresenta maior ou menor preco mediano?
- O menor preco por embalagem tambem representa menor preco por quantidade?
- Como o mix de fabricantes muda entre supermercados?
- Quais fabricantes aparecem em faixas mais premium ou mais acessiveis?
- Como embalagens pequenas, capsulas e porcoes individuais distorcem a leitura de preco?

## Objetivo

Construir uma analise de apoio a precificacao para cafes vendidos em supermercados, usando Python para preparar os dados, gerar indicadores, criar visualizacoes e consolidar insights de negocio.

O projeto foi posicionado como um case de **Analista de Dados/BI**, com foco em:

- preparacao e padronizacao de dados;
- criacao de indicadores de preco;
- analise exploratoria;
- visualizacoes para tomada de decisao;
- comunicacao executiva dos resultados.

## Dados

A base contem produtos de cafe coletados em lojas como Mambo, St Marche e Pao de Acucar. Os dados brutos ficam na pasta `base/`, mas essa pasta esta preparada para nao versionar arquivos `.csv` e `.xlsx` no GitHub.

Isso evita publicar dados brutos quando eles nao puderem ser compartilhados. Os resultados derivados do projeto ficam em:

- `relatorios/tabelas/`: tabelas consolidadas da analise;
- `relatorios/graficos/`: graficos exportados;
- `relatorios/relatorio_executivo.md`: leitura de negocio para apresentacao.

## Metodologia

1. **Coleta e consolidacao**
   - reuniao dos produtos por loja;
   - padronizacao de nomes de lojas e fabricantes;
   - tratamento de precos e disponibilidade.

2. **Tratamento e enriquecimento**
   - extracao do peso em gramas;
   - classificacao por faixa de peso;
   - calculo de preco por 100g, 500g e unidade;
   - consolidacao de fabricantes equivalentes.

3. **Analise**
   - preco medio, mediano, minimo e maximo por loja;
   - distribuicao de precos e outliers;
   - comparacao do preco bruto contra preco normalizado por 500g;
   - analise de mix de fabricantes;
   - analise de preco por fabricante.

4. **Visualizacao**
   - graficos estaticos exportados em PNG;
   - dashboard opcional em Streamlit para exploracao interativa.

## Principais insights

- St Marche possui o maior preco medio e mediano no preco bruto, sugerindo maior presenca de produtos premium.
- Pao de Acucar tem o menor preco mediano por item, mas passa a ter o maior preco mediano quando o preco e normalizado por 500g.
- Itens pequenos, como capsulas e porcoes individuais, elevam muito o preco proporcional por quantidade.
- Para comparar cafes tradicionais, a faixa de 251g a 500g e mais adequada do que comparar todo o mix junto.
- O mix de fabricantes influencia diretamente a leitura de posicionamento de preco de cada loja.

## Dashboard em Streamlit

Streamlit e uma biblioteca Python que transforma analises em uma pagina interativa no navegador. Neste projeto, ele serve para apresentar KPIs, filtros e graficos de precificacao sem precisar criar um sistema web completo.

Para executar:

```bash
streamlit run app.py
```

Se o ambiente ainda nao tiver as bibliotecas do dashboard:

```bash
pip install -r requirements.txt
```

## Estrutura

```text
.
├── app.py                         # Dashboard interativo em Streamlit
├── base/                          # Dados brutos locais, nao versionados
├── notebooks/                     # Analises exploratorias
├── relatorios/
│   ├── graficos/                  # Graficos exportados
│   ├── tabelas/                   # Indicadores consolidados
│   ├── notas_analise.md           # Notas detalhadas da analise
│   └── relatorio_executivo.md     # Resumo para negocio/gestao
├── src/
│   ├── config.py                  # Caminhos e funcoes de carga
│   ├── graficos.py                # Geracao dos graficos
│   └── utils.py                   # Funcoes auxiliares
├── environment.yml
└── README.md
```

## Limitacoes

- A analise e majoritariamente descritiva, pois a base nao possui historico longo suficiente para modelagem temporal robusta.
- O projeto nao afirma implementar precificacao dinamica completa; ele entrega uma base analitica para apoiar decisoes de preco.
- Comparacoes entre lojas dependem do sortimento disponivel em cada uma, entao a interpretacao deve considerar diferencas de mix, embalagem e fabricante.

## Como apresentar este projeto

Descricao curta para curriculo ou mensagem ao gestor:

> Desenvolvi um projeto de BI para analise de precificacao de cafes em supermercados, com tratamento de dados em Python, normalizacao de precos por peso, criacao de indicadores, comparacao entre lojas, analise de mix de fabricantes e dashboard interativo para apoio a tomada de decisao.

Descricao mais completa:

> O projeto analisa precos de cafes em diferentes supermercados e demonstra como o preco bruto pode distorcer conclusoes quando produtos possuem pesos diferentes. Foram criados indicadores de preco medio, mediano, preco por 100g, preco por 500g, cobertura de peso, faixa de embalagem e mix de fabricantes. A entrega inclui tabelas consolidadas, graficos, relatorio executivo e dashboard em Streamlit, simulando uma solucao de BI para suporte a decisoes de precificacao.
