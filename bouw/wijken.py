"""
WIJK- EN PLAATSPAGINA'S
=======================
Elke wijk hieronder wordt automatisch een eigen pagina: /elektricien-<slug>

BELANGRIJK voor Google: schrijf per wijk ECHT eigen tekst (woningen, straten,
typische klussen die je daar doet). Pagina's die alleen de plaatsnaam wisselen
ziet Google als "doorway pages" en die worden juist lager gezet.
Tip: vervang of vul aan met je eigen ervaringen ("vorige maand in de ... een
groepenkast vervangen"). Echte ervaring is precies wat Google wil zien.

Nieuwe wijk toevoegen: kopieer een blok, pas alles aan, draai `python3 build.py`.

Velden:
  slug          -> URL: /elektricien-<slug>
  naam          -> zoals mensen het typen
  type          -> "wijk" (in gemeente Utrecht) of "plaats" (buiten Utrecht)
  gemeente      -> voor structured data
  buurten       -> subwijken / bekende buurten (worden getoond + in de tekst gebruikt)
  aanrijtijd    -> indicatie bij spoed ("" = niet tonen)
  intro         -> 1e alinea onder de H1
  woningen      -> alinea over het woningtype en wat dat betekent voor de elektra
  klussen       -> lijst: [titel, uitleg]  (typische klussen in deze wijk)
  lokaal        -> praktische lokale info (parkeren, bereikbaarheid, netstoring)
  faq           -> lijst: [vraag, antwoord] (komt ook als FAQ in structured data)
"""

WIJKEN = [
    {
        "slug": "overvecht",
        "naam": "Overvecht",
        "type": "wijk",
        "gemeente": "Utrecht",
        "buurten": ["Overvecht-Noord", "Overvecht-Zuid", "Overvecht-Centrum", "Vechtzoom", "Taagdreef e.o.", "Zambesidreef e.o."],
        "aanrijtijd": "20–40 min",
        "intro": (
            "Stroom uitgevallen, een aardlekschakelaar die blijft uitspringen of toe aan een nieuwe groepenkast "
            "in Overvecht? INO is een elektricien uit Utrecht die dagelijks in Overvecht-Noord en -Zuid werkt. "
            "Je belt direct met de monteur, krijgt vooraf een vaste prijs en betaalt binnen de gemeente Utrecht "
            "geen voorrijkosten."
        ),
        "woningen": (
            "Overvecht is grotendeels in de jaren '60 en '70 gebouwd: veel portiek- en galerijflats langs de "
            "dreven, aangevuld met eengezinswoningen en nieuwere bouw na de renovaties van de afgelopen jaren. "
            "In woningen die nooit vernieuwd zijn zien we vaak een groepenkast met weinig groepen, niet alle "
            "groepen achter een aardlekschakelaar en in slaapkamers soms nog stopcontacten zonder randaarde. "
            "Omdat steeds meer bewoners overstappen op elektrisch koken, is een extra kookgroep of Perilex-aansluiting "
            "hier een van onze meest gevraagde klussen."
        ),
        "klussen": [
            ["Groepenkast vervangen in een flat", "Oude kast met smeltzekeringen of te weinig aardlekschakelaars? We plaatsen een nieuwe, NEN 1010-conforme kast, meestal binnen één werkdag."],
            ["Kookgroep voor inductie", "Overstappen van gas naar inductie? We trekken een aparte kookgroep met Perilex-aansluiting vanaf de meterkast."],
            ["Aardlek slaat steeds af", "Vaak een apparaat of vocht in een buitenstopcontact of badkamer. We meten het per groep door en lossen de oorzaak op."],
            ["Stopcontacten met randaarde", "Oude stopcontacten zonder aarde vervangen of extra stopcontacten bijplaatsen, netjes weggewerkt."],
        ],
        "lokaal": (
            "Parkeren is in Overvecht meestal geen probleem, dus we staan snel voor de deur. Zit niet alleen jij "
            "maar de hele flat of straat zonder stroom? Dan ligt de storing waarschijnlijk bij de netbeheerder: bel "
            "dan eerst het gratis Nationaal Storingsnummer 0800-9009."
        ),
        "faq": [
            ["Rekenen jullie voorrijkosten in Overvecht?", "Nee. Overvecht valt binnen de gemeente Utrecht, dus je betaalt geen voorrijkosten. Je betaalt alleen het vaste tarief dat we vooraf afspreken."],
            ["Mag ik in mijn huurwoning de groepenkast laten vervangen?", "Bij een huurwoning is de groepenkast meestal van de verhuurder of woningcorporatie. Overleg eerst met je verhuurder; wij kunnen een offerte en foto's aanleveren zodat zij snel kunnen beslissen."],
            ["Hoe snel zijn jullie bij spoed in Overvecht?", "Bij een acute storing zijn we meestal binnen 20 tot 40 minuten ter plaatse, afhankelijk van het verkeer. Bel direct, dan hoor je meteen hoe laat we er kunnen zijn."],
        ],
    },
    {
        "slug": "kanaleneiland",
        "naam": "Kanaleneiland",
        "type": "wijk",
        "gemeente": "Utrecht",
        "buurten": ["Kanaleneiland-Noord", "Kanaleneiland-Zuid", "Kanaleneiland-Centrum"],
        "aanrijtijd": "20–35 min",
        "intro": (
            "Een elektricien nodig in Kanaleneiland? INO helpt bewoners tussen het Merwedekanaal en het "
            "Amsterdam-Rijnkanaal met storingen, nieuwe groepen en complete groepenkasten. Vaste prijs vooraf, "
            "geen voorrijkosten binnen Utrecht en bij spoed 24/7 bereikbaar."
        ),
        "woningen": (
            "Kanaleneiland is een typische wederopbouwwijk uit eind jaren '50 en begin jaren '60, met veel "
            "portiekflats en lange bouwblokken. De originele elektrische installatie is daar vaak aangelegd voor "
            "een paar lampen en een wasmachine, niet voor de apparaten die we nu gebruiken. Dat merk je aan "
            "groepen die uitvallen zodra de waterkoker, magnetron en airfryer tegelijk aan staan. Een extra groep "
            "of een nieuwe groepenkast lost dat structureel op."
        ),
        "klussen": [
            ["Groep valt uit bij koken", "Keukenapparaten op één groep overbelasten de installatie. We verdelen ze over extra groepen zodat het niet meer uitvalt."],
            ["Groepenkast vernieuwen", "Oude kasten met porseleinen zekeringen vervangen we door een moderne kast met aardlekautomaten."],
            ["Wasmachine en droger apart", "Een eigen groep voor wasmachine en droger voorkomt dat de aardlek afslaat tijdens het wassen."],
            ["Storing zoeken", "Valt de stroom af en toe weg zonder duidelijke reden? We meten isolatieweerstand en verbindingen door tot we de oorzaak hebben."],
        ],
        "lokaal": (
            "Kanaleneiland ligt vlak bij de ring en de Jaarbeurs, waardoor we er bij spoed meestal snel zijn. In "
            "portiekflats zit de meterkast soms in het trappenhuis of in de gang; stuur gerust een foto via "
            "WhatsApp, dan kunnen we vooraf al veel inschatten."
        ),
        "faq": [
            ["Wat kost een extra groep in Kanaleneiland?", "Een extra groep bijplaatsen kan vanaf € {extra_groep}, afhankelijk van je huidige kast en de ruimte. Stuur een foto van je meterkast, dan krijg je direct een vaste prijs."],
            ["Waarom valt mijn stroom uit als ik kook?", "Meestal staan te veel zware apparaten op één groep. Dat is geen defect maar overbelasting. De oplossing is een extra groep of een aparte kookgroep."],
            ["Zijn er voorrijkosten in Kanaleneiland?", "Nee, Kanaleneiland valt binnen de gemeente Utrecht. Je betaalt geen voorrijkosten."],
        ],
    },
    {
        "slug": "transwijk",
        "naam": "Transwijk",
        "type": "wijk",
        "gemeente": "Utrecht",
        "buurten": ["Transwijk-Noord", "Transwijk-Zuid", "Park Transwijk", "Dichterswijk (grenzend)"],
        "aanrijtijd": "20–35 min",
        "intro": (
            "INO is je elektricien in Transwijk, van de flats rond Park Transwijk tot de eengezinswoningen richting "
            "het Merwedekanaal. Of het nu gaat om een storing, een nieuwe groepenkast of extra stopcontacten: je "
            "krijgt vooraf een vaste prijs en betaalt binnen Utrecht geen voorrijkosten."
        ),
        "woningen": (
            "Transwijk is net als het naastgelegen Kanaleneiland na de oorlog gebouwd, met een mix van flats en "
            "rijtjeshuizen. Veel woningen zijn inmiddels verbouwd: een open keuken, een uitbouw of een zolderkamer. "
            "Precies daar gaat het vaak mis, omdat de installatie niet is meegegroeid. We zien regelmatig verlengde "
            "leidingen, te veel stopcontacten op één groep en een groepenkast die vol zit. In de oudere, vooroorlogse "
            "huizen van de aangrenzende Dichterswijk komen we daarnaast nog weleens oude bedrading tegen."
        ),
        "klussen": [
            ["Elektra voor een verbouwing", "Nieuwe keuken of uitbouw? We leggen de groepen, stopcontacten en verlichting aan volgens NEN 1010."],
            ["Groepenkast uitbreiden", "Kast vol? We breiden uit of vervangen hem door een kast met ruimte voor laadpaal of warmtepomp later."],
            ["Stopcontacten verleggen", "Stofarm frezen en stopcontacten verplaatsen, zodat je interieur klopt."],
            ["Oude bedrading controleren", "Twijfel over de staat van je leidingen? We meten de installatie door en adviseren wat echt nodig is."],
        ],
        "lokaal": (
            "Heb je een storing en twijfel je of het aan je eigen woning ligt? Kijk of de buren en de "
            "straatverlichting nog stroom hebben. Zo ja, dan zit het in je eigen installatie en kunnen wij helpen. "
            "Zo nee, bel dan het Nationaal Storingsnummer 0800-9009."
        ),
        "faq": [
            ["Kunnen jullie de elektra voor mijn nieuwe keuken aanleggen?", "Ja. We maken vooraf een plan voor groepen, kookgroep en stopcontacten, en werken met een vaste prijs. Stuur je keukentekening mee, dan rekenen we het direct door."],
            ["Werken jullie ook in de Dichterswijk en Rivierenwijk?", "Ja, we werken in heel Utrecht-Zuidwest en Zuid. Overal geldt dezelfde vaste prijs zonder voorrijkosten."],
            ["Hoe lang duurt het vervangen van een groepenkast?", "Meestal een halve tot hele werkdag. Je zit in die tijd kort zonder stroom; we spreken vooraf af wanneer dat het beste uitkomt."],
        ],
    },
    {
        "slug": "leidsche-rijn",
        "naam": "Leidsche Rijn",
        "type": "wijk",
        "gemeente": "Utrecht",
        "buurten": ["Parkwijk", "Terwijde", "Langerak", "Het Zand", "Leidsche Rijn Centrum", "Vleuterweide"],
        "aanrijtijd": "25–45 min",
        "intro": (
            "Laadpaal installeren, groepenkast uitbreiden of een storing in je nieuwbouwwoning in Leidsche Rijn? "
            "INO werkt in Parkwijk, Terwijde, Langerak, Het Zand en de rest van Leidsche Rijn. Vaste prijs vooraf, "
            "geen voorrijkosten binnen de gemeente Utrecht."
        ),
        "woningen": (
            "Leidsche Rijn is vanaf eind jaren '90 gebouwd, dus de installaties zijn relatief nieuw en veilig. De "
            "vragen hier gaan dan ook minder over veroudering en meer over uitbreiden: een laadpaal op de oprit, "
            "een warmtepomp, zonnepanelen, een elektrisch verwarmde uitbouw of een tuinhuis met stroom. Een "
            "groepenkast die bij oplevering precies groot genoeg was, zit dan snel vol. Vaak is uitbreiden met een "
            "extra aardlekautomaat genoeg; soms is een 3-fase aansluiting slimmer."
        ),
        "klussen": [
            ["Laadpaal installeren", "Wallbox aan de gevel of op de oprit, met een eigen groep en waar nodig slimme load balancing."],
            ["Groepenkast uitbreiden", "Extra groepen voor warmtepomp, inductie of uitbouw, zonder de hele kast te vervangen als dat niet nodig is."],
            ["Krachtstroom (400V)", "Voor warmtepomp, sauna of zware werkplaats leggen we een 3-fase groep aan."],
            ["Tuinverlichting en buitenstopcontact", "Grondkabel, waterdichte verbindingen en een buitenstopcontact op een aparte groep."],
        ],
        "lokaal": (
            "In Leidsche Rijn zijn we er bij spoed meestal binnen 25 tot 45 minuten, afhankelijk van het verkeer op "
            "de A2 en de Leidsche Rijn-tunnel. Voor laadpalen komen we graag eerst kijken, of je stuurt foto's van je "
            "meterkast en de plek van de laadpaal."
        ),
        "faq": [
            ["Kan mijn groepenkast een laadpaal aan?", "Vaak wel, maar het hangt af van je aansluiting (1-fase of 3-fase) en de ruimte in de kast. Stuur een foto van je meterkast en typeplaatje, dan zeggen we het je direct."],
            ["Moet ik voor een laadpaal een 3-fase aansluiting hebben?", "Nee, laden kan ook op 1-fase, alleen langzamer. Heb je al 3-fase, dan laadt je auto sneller. We adviseren je eerlijk wat bij je auto en gebruik past."],
            ["Werken jullie ook in Vleuten en De Meern?", "Ja. Vleuten, De Meern en Vleuterweide horen bij de gemeente Utrecht, dus ook daar zonder voorrijkosten."],
        ],
    },
    {
        "slug": "maarssen",
        "naam": "Maarssen",
        "type": "plaats",
        "gemeente": "Stichtse Vecht",
        "buurten": ["Maarssen-Dorp", "Maarssenbroek", "Bloemstede", "Fazantenkamp", "Zogweteringen", "Bisonspoor"],
        "aanrijtijd": "30–50 min",
        "intro": (
            "Een elektricien in Maarssen nodig? INO komt vanuit Utrecht naar Maarssen-Dorp en Maarssenbroek voor "
            "storingen, groepenkasten, Perilex-aansluitingen en laadpalen. Je spreekt direct de monteur en weet "
            "vooraf wat het kost."
        ),
        "woningen": (
            "Maarssen heeft twee gezichten. In Maarssen-Dorp langs de Vecht staan oude, soms monumentale panden "
            "waar de bedrading in de loop der jaren stukje bij beetje is aangepast. Daar is zorgvuldig werken en "
            "netjes wegwerken belangrijk. Maarssenbroek is vooral in de jaren '70 en '80 gebouwd; daar zijn de "
            "installaties vaak nog origineel, met een groepenkast die aan vervanging toe is of te klein is voor "
            "inductie, een warmtepomp of een laadpaal."
        ),
        "klussen": [
            ["Groepenkast vervangen", "Originele kast uit de jaren '70/'80? We vervangen hem door een moderne kast met aardlekautomaten."],
            ["Perilex en inductie", "Aparte kookgroep met Perilex-aansluiting voor je nieuwe inductiekookplaat."],
            ["Werken in oudere panden", "Zorgvuldig aanpassen van bestaande bedrading, met oog voor het karakter van het pand."],
            ["Laadpaal op eigen terrein", "Installatie van een laadpaal met eigen groep en veilige aansluiting."],
        ],
        "lokaal": (
            "Maarssen valt buiten de gemeente Utrecht. We rekenen daarom een vast kilometertarief van € {km_tarief} "
            "per km, en dat bedrag hoor je altijd vooraf. Via de A2 zijn we er vanuit Utrecht snel."
        ),
        "faq": [
            ["Wat kost voorrijden naar Maarssen?", "Voor Maarssen rekenen we € {km_tarief} per km. Je hoort het exacte bedrag altijd vooraf, samen met de prijs van de klus."],
            ["Werken jullie ook in oudere panden in Maarssen-Dorp?", "Ja. We werken zorgvuldig, overleggen waar leidingen komen en werken alles netjes weg. Bij monumenten stemmen we vooraf af wat wel en niet mag."],
            ["Komen jullie ook bij spoed naar Maarssen?", "Ja, ook buiten kantooruren. Bel direct, dan hoor je meteen wanneer we er kunnen zijn."],
        ],
    },
    {
        "slug": "nieuwegein",
        "naam": "Nieuwegein",
        "type": "plaats",
        "gemeente": "Nieuwegein",
        "buurten": ["Batau", "Doorslag", "Fokkesteeg", "Galecop", "Jutphaas-Wijkersloot", "Zuilenstein", "Merwestein", "Vreeswijk", "Blokhoeve"],
        "aanrijtijd": "30–50 min",
        "intro": (
            "INO is elektricien voor Nieuwegein: van Batau en Galecop tot Zuilenstein en het oude Vreeswijk. We "
            "helpen bij stroomstoringen, vervangen groepenkasten en leggen kookgroepen en laadpalen aan. Altijd met "
            "een vaste prijs vooraf."
        ),
        "woningen": (
            "Nieuwegein is als groeikern grotendeels in de jaren '70 en '80 gebouwd. Veel van die woningen hebben "
            "nog de originele groepenkast, soms met smeltzekeringen en vaak met maar één of twee "
            "aardlekschakelaars voor het hele huis. Valt er één groep uit, dan zit je in een groot deel van het huis "
            "in het donker. Een moderne kast met aardlekautomaten per groep is veiliger en voorkomt dat. In het "
            "historische Vreeswijk en in nieuwbouw als Blokhoeve liggen de vragen weer anders, van oude bedrading "
            "tot laadpalen."
        ),
        "klussen": [
            ["Kast met smeltzekeringen vervangen", "Schroefzekeringen en één oude aardlek? We plaatsen een veilige, moderne groepenkast."],
            ["Aardlekautomaten per groep", "Zo valt bij een storing alleen die ene groep uit en niet je halve huis."],
            ["Kookgroep en Perilex", "Klaar voor inductie met een aparte kookgroep vanaf de meterkast."],
            ["Laadpaal en krachtstroom", "Laadpaal of warmtepomp? We bekijken of je huidige aansluiting volstaat."],
        ],
        "lokaal": (
            "Nieuwegein valt buiten de gemeente Utrecht; we rekenen € {km_tarief} per km en melden dat vooraf. Via de "
            "A12 en A2 zijn we er bij spoed snel. Hele wijk zonder stroom? Bel dan eerst 0800-9009 (netbeheerder)."
        ),
        "faq": [
            ["Mijn huis uit de jaren '70 heeft nog schroefzekeringen. Is dat gevaarlijk?", "Niet direct gevaarlijk zolang alles werkt, maar het voldoet niet meer aan de huidige normen en biedt minder bescherming tegen elektrocutie en brand. Vervangen is een verstandige investering, zeker als je meer elektrisch gaat gebruiken."],
            ["Wat kost een nieuwe groepenkast in Nieuwegein?", "Een 1-fase kast begint bij € {groepenkast_1f} all-in, een 3-fase kast bij € {groepenkast_3f}. Daar komt de kilometervergoeding bij, die je vooraf hoort."],
            ["Werken jullie ook in Vreeswijk?", "Ja, in heel Nieuwegein, inclusief Vreeswijk en de nieuwbouw in Blokhoeve."],
        ],
    },
    {
        "slug": "vianen",
        "naam": "Vianen",
        "type": "plaats",
        "gemeente": "Vijfheerenlanden",
        "buurten": ["Binnenstad (Voorstraat)", "Vianen-Noord", "Hoef en Haag", "Hagestein", "Everdingen"],
        "aanrijtijd": "",
        "intro": (
            "Een elektricien in Vianen, net over de Lekbrug? INO komt vanuit Utrecht naar de historische binnenstad "
            "van Vianen, de woonwijken en nieuwbouw als Hoef en Haag. Voor storingen, groepenkasten, kookgroepen en "
            "laadpalen, altijd met een vaste prijs vooraf."
        ),
        "woningen": (
            "In de oude vestingstad rond de Voorstraat staan panden die soms honderden jaren oud zijn. De "
            "elektrische installatie is daar vaak in fases aangepast, met verschillende soorten leidingen door "
            "elkaar. Doormeten en zorgvuldig vernieuwen is daar het belangrijkste werk. In de naoorlogse wijken "
            "vervangen we vooral verouderde groepenkasten, en in de nieuwbouw van Hoef en Haag draait het meestal "
            "om uitbreiden: laadpaal, zonnepanelen of een extra groep."
        ),
        "klussen": [
            ["Installatie doormeten", "Twijfel over oude bedrading? We meten isolatie en aarding door en geven een eerlijk advies."],
            ["Groepenkast vervangen", "Een verouderde kast vervangen door een moderne, veilige kast met aardlekautomaten."],
            ["Laadpaal in nieuwbouw", "Laadpaal installeren met eigen groep, ook als je al zonnepanelen hebt."],
            ["Storingen verhelpen", "Aardlek die afslaat of een groep die uitvalt: we zoeken de oorzaak en lossen het op."],
        ],
        "lokaal": (
            "Vianen valt buiten de gemeente Utrecht. We rekenen € {km_tarief} per km en melden dat altijd vooraf. "
            "Bel bij spoed direct, dan hoor je meteen wanneer we er kunnen zijn."
        ),
        "faq": [
            ["Komen jullie ook naar Vianen?", "Ja. Vianen ligt direct ten zuiden van Utrecht, over de Lek. We rekenen € {km_tarief} per km voorrijden en je hoort dat bedrag vooraf."],
            ["Kunnen jullie werken in een oud pand in de binnenstad?", "Ja. We werken zorgvuldig en overleggen vooraf waar leidingen lopen. Bij een monument stemmen we af wat wel en niet mag."],
            ["Werken jullie ook in Hagestein en Everdingen?", "Ja, ook in de kernen rond Vianen. Vraag gerust je adres na."],
        ],
    },
    {
        "slug": "breukelen",
        "naam": "Breukelen",
        "type": "plaats",
        "gemeente": "Stichtse Vecht",
        "buurten": ["Breukelen-Centrum", "Breukelen-Noord", "Breukelen-Zuid", "Nieuwer Ter Aa", "Kockengen"],
        "aanrijtijd": "",
        "intro": (
            "INO is ook je elektricien in Breukelen. Van de oude dorpskern en de panden langs de Vecht tot de "
            "woonwijken rond het station: we helpen bij storingen, groepenkasten, kookgroepen, laadpalen en "
            "buitenverlichting. Vooraf een vaste prijs, geen verrassingen achteraf."
        ),
        "woningen": (
            "Breukelen combineert een historische kern met naoorlogse en nieuwere woonwijken. In de oudere panden "
            "kom je vaak installaties tegen die in de loop der jaren zijn uitgebreid zonder dat de groepenkast "
            "meegroeide. Buiten het centrum, met grotere tuinen en vrijstaande woningen, zijn tuinverlichting, "
            "stroom naar het tuinhuis en een laadpaal op eigen terrein veelgevraagde klussen."
        ),
        "klussen": [
            ["Stroom naar tuinhuis of schuur", "Grondkabel, eigen groep en een waterdichte aansluiting, veilig aangelegd."],
            ["Tuinverlichting", "Sfeervolle buitenverlichting met IP-klasse verlichting en nette kabelgoten."],
            ["Groepenkast uitbreiden of vervangen", "Meer groepen of een complete nieuwe kast als de oude te klein of verouderd is."],
            ["Laadpaal op eigen terrein", "Laadpaal met eigen groep en, waar nodig, load balancing."],
        ],
        "lokaal": (
            "Breukelen valt buiten de gemeente Utrecht. We rekenen € {km_tarief} per km en melden dat vooraf. Via de "
            "A2 zijn we er vanuit Utrecht snel."
        ),
        "faq": [
            ["Wat kost stroom naar mijn tuinhuis?", "Dat hangt af van de afstand en de ondergrond. Stuur foto's van je meterkast en de route naar het tuinhuis, dan krijg je een vaste prijs vooraf."],
            ["Komen jullie ook naar Kockengen en Nieuwer Ter Aa?", "Ja. Vraag gerust je adres na; we rekenen € {km_tarief} per km en melden dat vooraf."],
            ["Kan ik ook in het weekend een afspraak maken?", "Voor storingen zijn we 24/7 bereikbaar. Geplande klussen in het weekend kunnen in overleg; daarvoor gelden de avond- en weekendtarieven."],
        ],
    },
]

# Overige wijken/plaatsen zonder eigen pagina (verschijnen op /wijken met link naar offerte).
# Wil je er een eigen pagina voor? Verplaats hem naar WIJKEN hierboven en schrijf eigen tekst.
OVERIGE_UTRECHT = [
    ["Binnenstad", "Domplein · Neude · Oudegracht"],
    ["Oost", "Wilhelminapark · Rubenslaan · Abstede"],
    ["Noordoost", "Tuindorp · Voordorp · Watervogelbuurt"],
    ["Noordwest", "Zuilen · Ondiep · Pijlsweerd"],
    ["West", "Lombok · Oog in Al"],
    ["Zuid", "Hoograven · Tolsteeg · Bokkenbuurt"],
    ["Vleuten-De Meern", "Vleuten · De Meern · Haarzicht"],
]
OVERIGE_REGIO = [
    ["Houten", "Houten-Zuid · Castellum · Het Rond"],
    ["Zeist", "Zeist-West · Kerckebosch · Vollenhove"],
    ["De Bilt", "De Bilt · Bilthoven"],
    ["IJsselstein", "IJsselveld · Zenderpark"],
    ["Woerden", "Woerden-Centrum · Molenvliet"],
    ["Amersfoort", "Kruiskamp · Vathorst · Schothorst"],
    ["Veenendaal", "Veenendaal-Oost · De Compagnie"],
]
