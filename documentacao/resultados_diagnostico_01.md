# Resultados do Diagnóstico de Dados - Netflix

Fiz uma primeira análise na base `netflix_raw.csv` e encontrei vários problemas que vão dar trabalho para limpar. Aqui está o que eu achei:

## 1. Problemas de Preenchimento
* **Muita coisa faltando (NaN):** As colunas de diretor, país e rating estão cheias de buracos.
* **Falsos nulos:** Em vez de deixarem vazio, usaram textos como `"Not Given"`, `"???"`, `"NULL"` e `"N/A"`. Vou ter que trocar tudo isso por nulo de verdade para conseguir trabalhar.

## 2. Bagunça nas Colunas
* **Dados fora de lugar:** Na coluna `type` (que deveria ser só Movie ou TV Show), encontrei classificações de idade como `TV-MA` e `R`. Parece que as colunas "pularam" em algumas linhas.
* **Unidades diferentes:** Na duração, tem hora que escrevem `min` e hora que escrevem `minutes`. Preciso padronizar.

## 3. Erros de Digitação e Formatação
* **Input mal formado:** Tem um filme que aparece como `"9-Feb"`. Deve ter sido alguma conversão errada ou erro de input que mudou o nome original para uma data.
* **Espaços sobrando:** Achei títulos iguais, mas um tem um espaço no final e o outro não. O Python acha que são coisas diferentes.

## 4. Inconsistências Lógicas e Duplicados
* **Viagem no tempo:** Tem 34 filmes que dizem ter sido adicionados na Netflix antes mesmo de serem lançados no cinema/TV. 
* **IDs repetidos:** Encontrei 30 IDs (`show_id`) que aparecem mais de uma vez.

## 5. Próximos Passos
Agora que eu já sei onde está a sujeira, vou começar a fase de limpeza (Data Cleaning) para deixar a base pronta para análise.
