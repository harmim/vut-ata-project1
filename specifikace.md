Pokud je požadováno přemístění nákladu z jednoho místa do druhého, vozík si
materiál vyzvedne do 1 minuty.

- Není jasné, k čemu se vztahuje časové omezení. Do 1 minuty od čeho?
- "je požadováno" není úplně jednoznačné. Sjednoceno na jednoznačný výraz
  "nastavení požadavku".
- Sjednocení výrazů "náklad" a "materiál".
- Není zde zmínka o nastavení prioritní vlastnosti.
- "else" případ je v následující větě.
- Není jasné, co se myslí "místem".

*Pokud je nastaven požadavek na přemístění materiálu z jedné stanice do druhé,
vozík si materiál vyzvedne do 1 minuty od nastavení tohoto požadavku a zároveň
se tomuto materiálu nenastavuje prioritní vlastnost.*


Pokud se to nestihne, materiálu se nastavuje prioritní vlastnost.

- Nemusí být jasné, na co se odkazuje "to". Pokud se co nestihne?
- Není zde explicitně uvedené, že se nastaví prioritní požadavek pro přemístění
  materiálu.

*Pokud vozík nevyzvedne materiál do 1 minuty od nastavení požadavku na toto
vyzvednutí, materiálu se nastavuje prioritní vlastnost a nastaví se prioritní
požadavek na přemístění tohoto materiálu.*


Každý prioritní materiál musí být vyzvednutý vozíkem do 1 minuty od nastavení
prioritního požadavku.

- Není jednoznačné, co se myslí prioritním materiálem.
- Chybí zde "else" případ. Měla by se vyvolat JISTÁ výjimka. Reálně by
  samozřejmě mělo být definované, jaká přesně výjimka se vyvolá.
- Není jednoznačné, čeho se požadavek týká.

*Každý materiál s nastavenou prioritní vlastností musí být vyzvednutý vozíkem
do 1 minuty od nastavení prioritního požadavku na přemístění tohoto materiálu.
Pokud materiál s nastavenou prioritní vlastností není vyzvednut do 1 minuty od
nastavení prioritního požadavku na přemístění tohoto materiálu, vyvolává se
JISTÁ výjimka.*


Pokud vozík nakládá prioritní materiál, přepíná se do režimu pouze-vykládka.

- Není jednoznačné, co se myslí prioritním materiálem.
- Chybí zde "else" případ.

*Pokud vozík nakládá materiál s nastavenou prioritní vlastností, přepíná se do
režimu pouze-vykládka. Pokud vozík nakládá materiál, který nemá nastavenou
prioritní vlastnost, nepřepíná se do režimu pouze-vykládka.*


V tomto režimu zůstává, dokud nevyloží všechen takový materiál.

- Není jednoznačné, k čemu se vztahuje výraz "v tomto režimu" a kdo v něm
  zůstává.
- Není jednoznačné, co se myslí "takovým materiálem".

*V režimu pouze-vykládka vozík zůstává, dokud nevyloží všechen materiál s
nastavenou prioritní vlastností.*


Normálně vozík během své jízdy může nabírat a vykládat další materiály v jiných
zastávkách.

- Výraz "nabírat" není konsistentní.
- Není jasné, co znamená "normálně" a "jiné zastávky".
- Chybí zde "else" případ.
- Výraz "zastávka" není úplně jasný.

*Pokud je vozík v režimu pouze-vykládka, nemůže vyzvedávat žádné materiály a
může pouze vykládat materiály s nastavenou prioritní vlastností v jejich
cílových stanicích. Pokud vozík není v režimu pouze-vykládka, během své jízdy
může vyzvedávat další materiály v libovolných stanicích a může také materiály
vykládat v libovolných cílových stanicích naložených materiálů.*


Na jednom místě může vozík akceptovat nebo vyložit jeden i více materiálů.

- Není jasné, co se myslí "místem".
- Výraz "akceptovat" není konsistentní.

*V jedné stanici může vozík vyzvedávat nebo vykládat jeden i více materiálů.*


Pořadí vyzvednutí materiálu nesouvisí s pořadím vytváření požadavku.

- Výraz "vytvoření požadavku" není konsistentní.
- Není jednoznačné, čeho se požadavek týká.

*Pořadí vyzvednutí materiálu nesouvisí s pořadím nastavení požadavku na
přemístění daného materiálu.*


Vozík neakceptuje materiál, pokud jsou všechny jeho sloty obsazené nebo by jeho
převzetím byla překročena maximální nosnost.

- Výrazy "akceptovat" a "převzetí" nejsou konsistentní.
- Není možná úplně jasné, k čemu se vztahuje "maximální nosnost".
- Zbytečná negace.

*Vozík může vyzvednout materiál pouze v případě, že má volný alespoň jeden slot
a vyzvednutím tohoto materiálu by nebyla překročena maximální nosnost daného
vozíku.*