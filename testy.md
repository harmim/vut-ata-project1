# Dokumentace testů pro řízení vozíku v robotické továrně


## Graf příčin a důsledků

Graf byl vytvořen pomocí nástroje [Ceg](http://ceg.testos.org). Výsledná
konfigurace pro nástroj Ceg byla exportována do souboru `ceg.json`. Pro rychlou
demonstraci byl také vytvořen snímek obrazovky z nástroje Ceg (soubor
`ceg.png`). Konfigurace  příčin, důsledků, pravidel a omezení je taktéž
definovaná v souboru `ceg.txt`. Ve vytvořené rozhodovací tabulce je vidět, že
jsou pokryty všechny příčiny i důsledky.

### Rozhodovací tabulka

| Name   | Description                                                                                               |     `1` |     `2` |     `3` |     `4` |     `5` |
| :----: | --------------------------------------------------------------------------------------------------------- | :-----: | :-----: | :-----: | :-----: | :-----: |
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

Existují i jiné vstupní parametry. Parametry níže jsou však pro kombinační
testování daného systému asi nejzajímavější.

| ID parametru     | Popis                                               |
| :--------------: | --------------------------------------------------- |
| `req_count`      | celkový počet naplánovaných požadavků               |
| `req_when`       | naplánovaný čas jednoho požadavku                   |
| `req_sum_weight` | suma vah všech požadavků                            |
| `req_weight`     | váha jednoho požadavku                              |
| `req_track`      | trasa jednoho požadavku (zdrojová a cílová stanice) |
| `cart_slots`     | počet slotů vozíku                                  |
| `cart_cap`       | maximální nosnost vozíku                            |


## Charakteristiky vstupních parametrů

| `C_req_count` | počet naplánovaných požadavků |
| :-----------: | :---------------------------: |
|             1 | `C_req_count = 1`             |
|             2 | `C_req_count > 1`             |

| `C_req_when` | čas naplánování požadavku (u alespoň jednoho požadavku) |
| :----------: | :-----------------------------------------------------: |
|            1 | `C_req_when = 0`                                        |
|            2 | `C_req_when > 0`                                        |

| `C_req_same_time` | naplánování více požadavků na stejný čas |
| :---------------: | :--------------------------------------: |
|                 1 | `true`                                   |
|                 2 | `false`                                  |

| `C_req_same_track` | naplánování více požadavků se stejnou trasou |
| :----------------: | :------------------------------------------: |
|                  1 | `true`                                       |
|                  2 | `false`                                      |

| `C_req_sum_weight_gt_cart_cap` | suma vah všech požadavků je větší než maximální nosnost vozíku |
| :----------------------------: | :------------------------------------------------------------: |
|                              1 | `true`                                                         |
|                              2 | `false`                                                        |

| `C_req_weight_gt_cart_cap` | váha jednoho požadavku je větší než maximální nosnost vozíku (u alespoň jednoho požadavku) |
| :------------------------: | :----------------------------------------------------------------------------------------: |
|                          1 | `true`                                                                                     |
|                          2 | `false`                                                                                    |

| `C_req_track_edges` | minimální počet hran mezi zdrojovou a cílovou stanicí (u alespoň jednoho požadavku) |
| :-----------------: | :---------------------------------------------------------------------------------: |
|                   1 | `C_req_track_edges = 0`                                                             |
|                   2 | `C_req_track_edges = 1`                                                             |
|                   3 | `C_req_track_edges > 1`                                                             |

| `C_cart_slots` | počet slotů vozíku |
| :------------: | -----------------: |
|              1 |                  1 |
|              2 |                  2 |
|              3 |               3, 4 |

| `C_cart_cap` | maximální nosnost vozíku |
| :----------: | -----------------------: |
|            1 |                       50 |
|            2 |                      150 |
|            3 |                      500 |

### Omezení kombinace bloků různých charakteristik

- `C_req_count.1 -> !C_req_same_time.1`
- `C_req_count.1 -> !C_req_same_track.1`
- `C_req_same_time.1 -> C_req_count.2`
- `C_req_same_track.1 -> C_req_count.2`
- `C_req_sum_weight_gt_cart_cap.2 -> !C_req_weight_gt_cart_cap.1`
- `C_req_weight_gt_cart_cap.1 -> !C_req_sum_weight_gt_cart_cap.2`
- `C_cart_cap.1 -> !C_cart_slots.1`
- `C_cart_cap.3 -> !C_cart_slots.3`

### Kombinace dvojic charakteristik

Kombinace byly vytvořeny pomocí nástroje [Combine](https://combine.testos.org).
Výsledná konfigurace pro nástroj Combine byla exportována do souboru
`combine.json`. Pro rychlou demonstraci byl také vytvořen snímek obrazovky z
nástroje Combine (soubor `combine.png`). **Bylo zjištěno, že nástroj Combine
nefunguje úplně správně, protože generuje redundantní testovací případy a
případy, které nesplňují omezující podmínky. Redundantní případy jsou na snímku
obrazovky označeny červeně. Případy, které nesplňují omezující podmínky, jsou
opraveny a označeny oranžově.** Tabulka níže odpovídá opravené tabulce
vygenerované nástrojem Combine. Jednotlivé hodnoty odpovídají indexům bloků
daných charakteristik.

| Test Case ID   | `C_req_track_edges` | `C_cart_slots` | `C_cart_cap` | `C_req_count` | `C_req_when` | `C_req_same_time` | `C_req_same_track` | `C_req_sum_weight_gt_cart_cap` | `C_req_weight_gt_cart_cap` |
| :------------: | :-----------------: | :------------: | :----------: | :-----------: | :----------: | :---------------: | :----------------: | :----------------------------: | :------------------------: |
|            `1` |                   1 |              1 |            2 |             1 |            1 |                 2 |                  2 |                              1 |                          1 |
|            `2` |                   1 |              2 |            1 |             2 |            2 |                 1 |                  1 |                              2 |                          2 |
|            `3` |                   1 |              3 |            1 |             1 |            1 |                 2 |                  2 |                              2 |                          2 |
|            `4` |                   2 |              1 |            3 |             2 |            1 |                 1 |                  1 |                              1 |                          1 |
|            `5` |                   2 |              2 |            2 |             1 |            2 |                 2 |                  2 |                              1 |                          2 |
|            `6` |                   2 |              3 |            1 |             2 |            2 |                 1 |                  2 |                              1 |                          1 |
|            `7` |                   3 |              1 |            2 |             2 |            2 |                 1 |                  1 |                              2 |                          2 |
|            `8` |                   3 |              2 |            3 |             1 |            1 |                 2 |                  2 |                              1 |                          1 |
|            `9` |                   3 |              3 |            1 |             1 |            1 |                 2 |                  2 |                              1 |                          1 |
|           `10` |                   1 |              3 |            2 |             1 |            1 |                 2 |                  2 |                              1 |                          1 |
|           `11` |                   1 |              1 |            3 |             1 |            2 |                 2 |                  2 |                              2 |                          2 |
|           `12` |                   1 |              3 |            1 |             2 |            1 |                 2 |                  1 |                              1 |                          1 |
|           `13` |                   2 |              1 |            2 |             1 |            1 |                 2 |                  2 |                              2 |                          2 |


## Pokrytí automatizovanými testy

Automatizované testy se nachází v souboru `cartctl/cartctl_test.py` ve třídě
`TestCartRequests`. Některé z testů odhalily chyby v implementaci, které byly
opraveny v souboru `cartctl/cartctl_fixed.py`, tj. v této verzi implementace
všechy testy prochází. Pro provedené změny vizte
`diff -u cartctl/cartctl.py cartctl/cartctl_fixed.py`.

Tabulka níže ukazuje, který test (tj. která metoda v testovací třídě) pokrývá
který testovací případ z rozhodovací tabulky.

| Metoda                       | Testovací případ |
| :--------------------------: | :--------------: |
| `test_no_request`            |              `1` |
| `test_process_basic_request` |              `2` |
| `test_process_prio_request`  |              `3` |
| `test_no_free_slots`         |              `4` |
| `test_no_capacity`           |              `5` |

Tabulka níže ukazuje, který test (tj. která metoda v testovací třídě) pokrývá
který testovací případ z tabulky kombinací dvojic charakteristik.

| Metoda                       | Testovací případ |
| :--------------------------: | :--------------: |
| `test_combine_1`             |              `1` |
| `test_combine_2`             |              `2` |
| `test_combine_3`             |              `3` |
| `test_combine_4`             |              `4` |
| `test_combine_5`             |              `5` |
| `test_combine_6`             |              `6` |
| `test_combine_7`             |              `7` |
| `test_combine_8`             |              `8` |
| `test_combine_9`             |              `9` |
| `test_combine_10`            |             `10` |
| `test_combine_11`            |             `11` |
| `test_combine_12`            |             `12` |
| `test_combine_13`            |             `13` |
