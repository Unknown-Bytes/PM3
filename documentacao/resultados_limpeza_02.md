# Resultados da Limpeza de Dados - Netflix (Fase 2)

Concluí a limpeza e o pré-processamento da base `netflix_raw.csv`. O dataset agora está padronizado, livre de duplicatas e com as inconsistências lógicas resolvidas. Aqui está o resumo do que foi feito:

## 1. Tratamento de Nulos e Padronização
* **Placeholders eliminados:** Todos os "falsos nulos" (`"???"`, `"Not Given"`, `"NULL"`, `"N/A"`, `"Unknown"`) foram substituídos por valores nulos reais (`NaN`), permitindo cálculos estatísticos precisos.
* **Limpeza Textual:** Apliquei a remoção de espaços extras (strip) em todas as colunas.
* **Casing Uniforme:** As categorias de `type` foram padronizadas estritamente para `Movie` e `TV Show`, corrigindo variações de maiúsculas/minúsculas.

## 2. Reestruturação de Dados (Colunas Deslocadas)
* **Recuperação de Ratings:** Identifiquei e corrigi registros onde a classificação indicativa estava na coluna de "Tipo".
* **Inferência de Tipo:** Para esses registros deslocados, o tipo correto foi recuperado através da análise da unidade de duração (Seasons vs Minutes). Isso evitou a perda de dados valiosos sobre programas de TV.

## 3. Padronização de Unidades
* **Duração Uniforme:** Todas as colunas de duração foram normalizadas para os formatos:
    * `X min` (para filmes)
    * `X Season` ou `X Seasons` (para séries)
* Isso removeu variações como "minutes", "m", e números puros sem unidade.

## 4. Eliminação de Duplicados
* **Unicidade Garantida:** Removi **30 registros duplicados** (incluindo IDs repetidos e registros semanticamente iguais).
* **Estatística Final:** A base foi reduzida de 8.820 para **8.790 registros únicos**.

## 5. Correções Lógicas e de Integridade
* **Fim da "Viagem no Tempo":** Os 34 registros que indicavam adição na plataforma antes do lançamento oficial foram corrigidos. A data de adição foi ajustada para o ano de lançamento, mantendo a coerência cronológica.
* **Correção de Títulos:** Removi sufixos de corrupção de dados, como o `#ERROR!` que aparecia em títulos como "Five Feet Apart".

## 6. Próximos Passos
O dataset resultante, salvo em `dados_intermediarios/netflix_clean.csv`, possui agora alta integridade e está pronto para a **Fase 3: Análise Exploratória de Dados (EDA)** e criação de dashboards.
