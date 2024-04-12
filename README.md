#  Otimização Computacional De Demandas Contratadas Para Clientes Do Grupo A4

## IDEALIZAÇÃO DO PROJETO

O projeto teve início a partir da solicitação de um cliente que buscava concretizar uma ideia específica. Para isso, ele precisava de um programador que pudesse transformar essa ideia em realidade. O contato entre o cliente e o programador foi estabelecido por meio da plataforma 99Freelas. O cliente já havia desenvolvido toda a parte teórica do projeto e precisava apenas de alguém para otimizar e traduzir essa ideia em código. Ele optou por mim devido à minha formação em engenharia e ao meu conhecimento na área relevante para o projeto. Em termos gerais (de forma muito grosseira falando), o projeto tem como objetivo principal reduzir os custos de energia elétrica em escala industrial, através de algo que antes eu mesmo acreditava ser trivial. O engenheiro que me contatou demonstrou ser possível apenas com mínimos ajustes pontuais referentes à demanda contratada economizar muito.

## Modo de usar
Primeiramente é necessário colocar os arquivos .csv que são os dados de entrada com os nomes "dados.csv" e "tarifa.csv" no direotrio raixo do projeto, após isto basta ir ate o arquivo .py

# Tecnologias utilizadas

- Python
- JuPyteR
  
# Como executar o projeto

## Back end
Pré-requisitos: python 3.12.1 e JuPyteR(Opcional)

## Obs:

É importante notar que este repositório é privado, o que significa que é necessário ter as permissões adequadas para realizar certas etapas. Portanto, as instruções descritas aqui exigem a concessão de permissões pelo autor do projeto.

```bash
# clonar repositório
git clone https://github.com/Miguel-Olimpio/Otimiza-oComputacionalDeDemandasContratadasParaClientesDoGrupoA4.git

# instalar dependências
pip install -r requirements.txt

# executar o projeto basta rodar 
python main.py
```
Ou

![gif15](https://github.com/Miguel-Olimpio/Otimiza-oComputacionalDeDemandasContratadasParaClientesDoGrupoA4/assets/107503116/3a1fe4a8-8775-436c-a1cd-48952669260b)

#Objetivos e resultados

No Brasil, a distribuicao e fornecimento de energia eletrica sao regulamentados pela Agencia Nacional de Energia Eletrica(ANEL), Existem varios grupos e subgrupos
de consumidores de energia eletrica, que sao definidos com base na tensao de conexao a rede eletrica e no consumo de energia eletrica.
Este projeto é voltado ao grupo A.
Grupo A: clientes com tensao de conexao superior a 2,3 kV, atendidos em alta tensao.
Cada subgrupo tem regras especıficas para o calculo da tarifa de energia eletrica e para a contratacao de demanda eletrica. O objetivo dessas subdivisoes e garantir 
que cada consumidor pague uma tarifa justa e adequada ao seu perfil de consumo de energia eletrica.
Parte do faturamento de energia eletrica para os consumidores do grupo A, e feito com base em sua demanda eletrica, ou seja, na quantidade de energia que e utilizada em
um determinado perıodo de tempo. A demanda eletrica pode variar ao longo do dia, de acordo com o consumo dos equipamentos el´etricos. Para calcular a demanda, e necessario
analisar a curva de carga, que representa a variacao da demanda ao longo do tempo.
Para garantir o fornecimento de energia eletrica de forma adequada, os consumidores devem contratar uma demanda eletrica, chamada de demanda contratada. Essa demanda
contratada e estabelecida em contrato com a distribuidora de energia eletrica e deve ser suficiente para atender o consumo dos equipamentos eletricos do cliente.

Agora introduzidos ao tema, podemos entender melhor o que esta sendo feito aqui, pois o foco é encontrar o valor ideal para a demanda contratada, considerando dois principais fatores:
- Se a unidade consumidora contratar um valor baixo e a demanda medida for 5% maior que a demanda contratada, haverá uma multa por ultrapassagem, resultando em alto custo.
- Por outro lado, se a unidade consumidora contratar um valor alto para a demanda, pode parecer bem dimensionada, mas pode estar pagando por montantes excedentes que não são registrados.

Devido ao fato do conteúdo completo ser extremamente tecnico tentarei resumir ao máximo o que esta sendo feito, pois esta ocorrendo um tratamento de dados para encontrar
qual seria a demanda Contratada correta.
O engenheiro forneceu 2 arquivos csv com os dados do periodo de Março de 2022 ate fevereiro de 2023, com base nestes dados de entrada deve ser feito uma otimização para
encontrar qual deveria ser a demanda contratada ótima, para se pagar o menor preço, considerando assim diversos fatores, como demanda ultrapassada que o preço torna-se
superior ao da demanda contratada, e cada uma dessas variáveis dependem de diversas outras que se explicadas profundamente aqui, este arquivo readme.md se tornaria um
trabalho acadêmico extremamente longo. No entanto os resultados finais podem ser visualizados no gráfico a seguir:

Grafico 1 - Representa a demanda contratada no periodo dos dados fornecidos:

![gif9](https://github.com/Miguel-Olimpio/Otimiza-oComputacionalDeDemandasContratadasParaClientesDoGrupoA4/assets/107503116/35168163-4b18-4d47-9fc5-79fd12b4f3c8)

Grafico 2 - Representa o gasto devida a mesma:

![gif13](https://github.com/Miguel-Olimpio/Otimiza-oComputacionalDeDemandasContratadasParaClientesDoGrupoA4/assets/107503116/768eef54-b5e9-49d4-8c92-fb5c4281d86f)

Grafico 3 - Representa a Demanda calculada como ótima:

![gif11](https://github.com/Miguel-Olimpio/Otimiza-oComputacionalDeDemandasContratadasParaClientesDoGrupoA4/assets/107503116/dcc78f78-794f-4653-a19e-54cce593f10b)

Grafico 4 - Representa o gasto que da demanda calculada como otima:

![gif14](https://github.com/Miguel-Olimpio/Otimiza-oComputacionalDeDemandasContratadasParaClientesDoGrupoA4/assets/107503116/c0ba1691-1788-4ecb-beee-df7930693498)

Observe que o gráfico 2 o gasto medio total é aproximadamente R$11.135,00 e o gráfico 4 o preço médio mensal é de R$7.610,00, mesmo que a demanda ótima tenham
custo de ultrapassagem, a economia no mesmo periodo seria de aproximadamente R$42.295,15.

Observem também as tabelas geradas:
Tabela 1 - Gastos sem otimização

![tabelaAtual](https://github.com/Miguel-Olimpio/Otimiza-oComputacionalDeDemandasContratadasParaClientesDoGrupoA4/assets/107503116/abaf6ba4-0a78-4a7e-817e-029222a710b8)

Tabela 2 - Gastos com otimização

![tabelaOtimizada](https://github.com/Miguel-Olimpio/Otimiza-oComputacionalDeDemandasContratadasParaClientesDoGrupoA4/assets/107503116/fb9cc4e9-3a86-423c-b877-19ea46ff2691)

Embora a explicação tenha sido de uma forma extremamente resumida, abaixo estará exibido como o código de fato chegou a este resultado:

![gifFinal5](https://github.com/Miguel-Olimpio/Otimiza-oComputacionalDeDemandasContratadasParaClientesDoGrupoA4/assets/107503116/bb5c8571-614c-48ee-8b93-1912a0559b55)

Lembrando que cada um destes dados e graficos apresentados no gif acima necessitava ser interativo para que analises pudessem ser feitas junto ao cliente e o código otimizado com o tratamento de dados correto, para que o valor fosse alcansado.

# Autor

Miguel Olimpio de Paula Netto

https://www.linkedin.com/in/miguel-olimpio-ba3220200/
