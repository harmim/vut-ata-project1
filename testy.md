# Dokumentace testů pro řízení vozíku v robotické továrně


## Graf příčin a důsledků

Graf byl vytvořen pomocí nástroje http://ceg.testos.org. Výsledná konfigurace
pro tento nástroj byla exportována do souboru `ceg.json`. Pro rychlou
demonstraci byl také vytvořen snímek obrazovky z tohoto nástroje (soubor
`ceg.png`). Konfigurace  příčin, důsledků, pravidel a omezení je taktéž
definovaná v souboru `ceg.txt`. Ve vytvořené rozhodovací tabulce je vidět, že
jsou pokryty všechny příčiny i důsledky.

### Rozhodovací tabulka

| Name   | Description                                                                                               | [1]     | [2]     | [3]     | [4]     | [5]     |
| ------ | --------------------------------------------------------------------------------------------------------- | ------- | ------- | ------- | ------- | ------- |
|    `1` | nastavení klasického požadavku                                                                            |       0 |       1 |       1 |       1 |       1 |
|    `2` | časová fáze `< 1 minuta` od nastavení klasického požadavku                                                |       0 |       1 |       1 |       1 |       1 |
|    `3` | vyzvednutí materiálu ve fázi `2`                                                                          |       0 |       1 |       0 |       0 |       0 |
|    `4` | časová fáze `>= 1 minuta` od nastavení klasického požadavku                                               |       0 |       0 |       1 |       1 |       1 |
|    `5` | nastavení prioritního požadavku                                                                           |       0 |       0 |       1 |       1 |       1 |
|    `6` | časová fáze `< 1 minuta` od nastavení prioritního požadavku                                               |       0 |       0 |       1 |       1 |       1 |
|    `7` | vyzvednutí materiálu ve fázi `6`                                                                          |       0 |       0 |       1 |       0 |       0 |
|    `8` | časová fáze `>= 1 minuta` od nastavení prioritního požadavku                                              |       0 |       0 |       0 |       1 |       1 |
|    `9` | vozík je nastaven v režimu `pouze_vykládka`                                                               |       0 |       0 |       1 |       0 |       0 |
|   `10` | vozík má naložený materiál s prioritní vlastností                                                         |       0 |       0 |       1 |       0 |       0 |
|   `11` | vozík má volný alespoň 1 slot                                                                             |       1 |       1 |       1 |       0 |       1 |
|   `12` | vyzvednutím daného materiálu nebude překročena maximální nosnost vozíku                                   |       1 |       1 |       1 |       1 |       0 |
|   `50` | nastavení prioritní vlastnosti materiálu                                                                  | `false` | `false` | `true`  | `true`  | `true`  |
|   `51` | zpracování klasického požadavku a naložení materiálu bez prioritní vlastnosti                             | `false` | `true`  | `false` | `false` | `false` |
|   `52` | nastavení prioritního požadavku                                                                           | `false` | `false` | `true`  | `true`  | `true`  |
|   `53` | zpracování prioritního požadavku a naložení materiálu s prioritní vlastností                              | `false` | `false` | `true`  | `false` | `false` |
|   `54` | vyvolání `JISTÉ výjimky`                                                                                  | `false` | `false` | `false` | `true`  | `true`  |
|   `55` | přepnutí do režimu `pouze_vykládka`                                                                       | `false` | `false` | `true`  | `false` | `false` |
|   `56` | vozík nemůže vyzvedávat žádné materiály a může pouze vykládat materiály s nastavenou prioritní vlastností | `false` | `false` | `true`  | `false` | `false` |
|   `57` | zůstání v režimu `pouze_vykládka`                                                                         | `false` | `false` | `true`  | `false` | `false` |


## Identifikace vstupních parametrů

| ID parametru     | Popis                                               |
| ---------------- | --------------------------------------------------- |
| `req_count`      | celkový počet naplánovaných požadavků               |
| `req_when`       | naplánovaný čas jednoho požadavku                   |
| `req_sum_weight` | suma vah všech požadavků                            |
| `req_weight`     | váha jednoho požadavku                              |
| `req_track`      | trasa jednoho požadavku (zdrojová a cílová stanice) |
| `cart_slots`     | počet slotů vozíku                                  |
| `cart_cap`       | maximální nosnost vozíku                            |
