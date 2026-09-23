"""
WIJK- EN PLAATSPAGINA'S
=======================
Alle 18 wijken en omliggende gemeenten in de regio Utrecht.
Elke wijk heeft unieke content over woningtypes, lokale buurten, typische klussen en lokale FAQ.

Optioneel veld "praktijk": echte recente klussen in die wijk, bijv.
    "praktijk": [["Groepenkast vervangen in portiekflat, Zambesidreef", "1 werkdag, 3-fase, 10 groepen."]]
Dat maakt de pagina uniek en laat ervaring zien. Alleen echte klussen invullen.
Prijzen altijd als placeholder: {groepenkast_1f}, {km_tarief}, {uur_dag} enz. (zie config.py).
"""

WIJKEN = [
    {
        "slug": "utrecht-binnenstad",
        "naam": "Utrecht Binnenstad & Centrum",
        "type": "wijk",
        "gemeente": "Utrecht",
        "buurten": [
            "Domplein",
            "Neude",
            "Oudegracht",
            "Museumkwartier",
            "Breedstraatbuurt",
            "Lange Nieuwstraat",
            "Nobelstraat"
        ],
        "aanrijtijd": "{aanrijtijd_utrecht} min",
        "intro": "Geen stroom in een monumentaal pand, stoppen doorgeslagen of je meterkast moderniseren in de Utrechtse binnenstad? INO Elektra is gevestigd in Utrecht en kent de unieke installaties rondom de Oudegracht, de Neude en het Museumkwartier door en door. Rechtstreeks contact met een erkend elektricien, heldere prijsafspraken vooraf en binnen de gemeente Utrecht rekenen wij nooit voorrijkosten.",
        "woningen": "In de historische binnenstad van Utrecht tref je veel eeuwenoude panden, grachtenpanden en monumentale herenhuizen aan. De elektra is hier vaak door de decennia heen stapsgewijs uitgebreid. In de praktijk komen we regelmatig nog stoffen bedrading tegen, oude stalen leidingen, ontbrekende aarding in woonvertrekken en overbelaste smeltzekeringen. Wie overstapt op een moderne inductiekookplaat, airconditioning of zwaardere apparatuur, heeft een vakkundige verzwaring en complete modernisering naar aardlekautomaten volgens NEN 1010 nodig.",
        "klussen": [
            [
                "Groepenkast vernieuwen & beveiligen",
                "Vervanging van verouderde stoppenkasten door moderne ABB of Hager groepenkasten met aardlekschakelaars en overspanningsbeveiliging."
            ],
            [
                "Aarding aanleggen & doormeten",
                "Slaan van aardpennen of koppelen van potentiaalvereffening in historische panden waar nog geen veilige randaarde aanwezig is."
            ],
            [
                "Kookgroep / Perilex voor inductie",
                "Veilig aansluiten van moderne inductiekookplaten via een 2-fase of 3-fase kookgroep zonder het monumentale karakter te beschadigen."
            ],
            [
                "Storingsdienst 24/7 bij uitval",
                "Directe opsporing van kortsluiting, aardlekfouten of overbelasting in binnenstadswoningen en horecazaken."
            ]
        ],
        "lokaal": "In de Utrechtse binnenstad zijn parkeergelegenheid en voetgangerszones soms een uitdaging. Wij zijn uitstekend uitgerust om snel ter plaatse te zijn. Bij algemene uitval op het netwerk meld je dit direct bij Stedin via 0800-9009.",
        "faq": [
            [
                "Kan er in een monumentaal grachtenpand zomaar een moderne groepenkast geplaatst worden?",
                "Jazeker. Wij plaatsen compacte, moderne kasten van topmerken die exact binnen de bestaande meterkastruimte passen, met behoud van de historische bouwkundige staat."
            ],
            [
                "Hoe zit het met voorrijkosten in de binnenstad?",
                "Binnen de gehele gemeente Utrecht, inclusief het centrum en Museumkwartier, rekenen wij € {voorrijkosten_utrecht} voorrijkosten."
            ]
        ]
    },
    {
        "slug": "utrecht-oost",
        "naam": "Utrecht Oost",
        "type": "wijk",
        "gemeente": "Utrecht",
        "buurten": [
            "Wilhelminapark",
            "Oudwijk",
            "Schildersbuurt",
            "Abstede",
            "Buiten-Wittevrouwen",
            "Rijnsweerd",
            "Sterrenwijk"
        ],
        "aanrijtijd": "{aanrijtijd_utrecht} min",
        "intro": "Elektricien nodig in Utrecht Oost? Van een karakteristiek herenhuis aan het Wilhelminapark tot een sfeervolle jaren '30 woning in Oudwijk: INO Elektra voert alle elektrotechnische werkzaamheden veilig en vakkundig uit. Bel direct met onze monteur voor spoed, advies of een vaste offerte.",
        "woningen": "Utrecht Oost staat bekend om zijn statige bouw uit het begin van de 20e eeuw en fraaie jaren '30 architectuur. Veel woningen worden grondig verbouwd of verduurzaamd met een hybride warmtepomp, zonnepanelen of een luxe woonkeuken. De bestaande 1-fase aansluiting is dan vaak ontoereikend. Wij verzorgen de complete meterkastomzetting naar 3-fase krachtstroom, het infrezen van extra wandcontactdozen en nette leidingtrajecten.",
        "klussen": [
            [
                "3-Fase groepenkast voorbereiden",
                "Uitbreiding van de meterkast voor inductie, warmtepompen en laadpunten met behoud van de nette afwerking."
            ],
            [
                "Sleuven frezen & stopcontacten verleggen",
                "Stofarm infrezen van nieuwe elektrapunten in hoge plafonds en authentieke stucwanden."
            ],
            [
                "Tuinverlichting & buitenstopcontacten",
                "Aanleg van waterdichte grondkabels en designverlichting voor diepe stadstuinen."
            ],
            [
                "Spoedhulp bij aardlekstoringen",
                "Snel doormeten van vertakkingen en vochtproblemen in oude souterrains en kelders."
            ]
        ],
        "lokaal": "In Oudwijk en Abstede is straatparkeren vaak gereguleerd. Wij rekenen in heel Utrecht Oost geen voorrijkosten en hanteren altijd vaste tarieven vooraf.",
        "faq": [
            [
                "Is een 3-fase verzwaring noodzakelijk voor een kookplaat in Utrecht Oost?",
                "Voor de meeste moderne inductieplaten boven 7,4 kW of een combinatie met een oven en quooker is een 3-fase aansluiting sterk aan te raden om overbelasting te voorkomen."
            ],
            [
                "Kunnen leidingen stofarm gefreesd worden in een bewoonde woning?",
                "Ja, wij werken met professionele sleuvenfrezen voorzien van industriële M-klasse stofafzuiging, zodat je interieur netjes en schoon blijft."
            ]
        ]
    },
    {
        "slug": "leidsche-rijn",
        "naam": "Leidsche Rijn",
        "type": "wijk",
        "gemeente": "Utrecht",
        "buurten": [
            "Parkwijk",
            "Terwijde",
            "Langerak",
            "Het Zand",
            "Leidsche Rijn Centrum",
            "Vleuterweide"
        ],
        "aanrijtijd": "{aanrijtijd_utrecht} min",
        "intro": "Laadpaal installeren, groepenkast uitbreiden of een storing in je nieuwbouwwoning in Leidsche Rijn? INO werkt in Parkwijk, Terwijde, Langerak, Het Zand en de rest van Leidsche Rijn. Vaste prijs vooraf, geen voorrijkosten binnen de gemeente Utrecht.",
        "woningen": "Leidsche Rijn is vanaf eind jaren '90 gebouwd, dus de installaties zijn relatief nieuw en veilig. De vragen hier gaan dan ook minder over veroudering en meer over uitbreiden: een laadpaal op de oprit, een warmtepomp, zonnepanelen, een elektrisch verwarmde uitbouw of een tuinhuis met stroom. Een groepenkast die bij oplevering precies groot genoeg was, zit dan snel vol. Vaak is uitbreiden met een extra aardlekautomaat genoeg; soms is een 3-fase aansluiting slimmer.",
        "klussen": [
            [
                "Laadpaal installeren",
                "Wallbox aan de gevel of op de oprit, met een eigen groep en waar nodig slimme load balancing."
            ],
            [
                "Groepenkast uitbreiden",
                "Extra groepen voor warmtepomp, inductie of uitbouw, zonder de hele kast te vervangen als dat niet nodig is."
            ],
            [
                "Krachtstroom (400V)",
                "Voor warmtepomp, sauna of zware werkplaats leggen we een 3-fase groep aan."
            ],
            [
                "Tuinverlichting en buitenstopcontact",
                "Grondkabel, waterdichte verbindingen en een buitenstopcontact op een aparte groep."
            ]
        ],
        "lokaal": "In Leidsche Rijn zijn we er bij spoed meestal binnen {aanrijtijd_utrecht} minuten, afhankelijk van het verkeer. Voor laadpalen komen we graag eerst kijken, of je stuurt foto's van je meterkast en de plek van de laadpaal.",
        "faq": [
            [
                "Kan mijn groepenkast een laadpaal aan?",
                "Vaak wel, maar het hangt af van je aansluiting (1-fase of 3-fase) en de ruimte in de kast. Stuur een foto van je meterkast en typeplaatje, dan zeggen we het je direct."
            ],
            [
                "Moet ik voor een laadpaal een 3-fase aansluiting hebben?",
                "Nee, laden kan ook op 1-fase, alleen langzamer. Heb je al 3-fase, dan laadt je auto sneller. We adviseren je eerlijk wat bij je auto en gebruik past."
            ],
            [
                "Werken jullie ook in Vleuten en De Meern?",
                "Ja. Vleuten, De Meern en Vleuterweide horen bij de gemeente Utrecht, dus ook daar zonder voorrijkosten."
            ]
        ]
    },
    {
        "slug": "vleuten-de-meern",
        "naam": "Vleuten-De Meern",
        "type": "wijk",
        "gemeente": "Utrecht",
        "buurten": [
            "Vleuten",
            "De Meern",
            "Haarzuilens",
            "Haarzicht",
            "Veldhuizen",
            "Rijnenburg",
            "Máximapark"
        ],
        "aanrijtijd": "{aanrijtijd_utrecht} min",
        "intro": "Betrouwbare elektricien gezocht in Vleuten, De Meern of Haarzuilens? INO Elektra staat klaar voor groepenkastvervanging, laadpalen, krachtstroom en 24/7 storingshulp. Geen voorrijkosten binnen Utrecht, vaste prijzen en gecertificeerd volgens NEN 1010.",
        "woningen": "In Vleuten-De Meern vind je een gevarieerde combinatie van authentieke dorpskernen, ruime eengezinswoningen en moderne nieuwbouw zoals in Haarzicht en Veldhuizen. Veel woningen beschikken over een eigen oprit en ruime tuin. Veelgevraagde klussen zijn dan ook het aanleggen van krachtstroom naar de garage of schuur, het installeren van een laadpaal, en het doortrekken van grondkabels voor tuinverlichting.",
        "klussen": [
            [
                "Krachtstroom 400V aanleggen",
                "Aanleg van 3-fase bekabeling naar garages, werkplaatsen of warmtepompen."
            ],
            [
                "Laadpaal op eigen oprit",
                "Professionele montage van laadpalen inclusief load balancing en graafwerk."
            ],
            [
                "Groepenkast moderniseren",
                "Upgraden van oudere kasten met moderne aardlekautomaten en hoofdschakelaars."
            ],
            [
                "Tuinelektra & buitenverlichting",
                "Aanleg van waterdichte schakelaars, grondspots en spatwaterdichte contactdozen."
            ]
        ],
        "lokaal": "Vleuten en De Meern vallen volledig onder de gemeente Utrecht, waardoor je profiteert van € {voorrijkosten_utrecht} voorrijkosten. Bij acute uitval zijn we vlot ter plaatse via de A2/A12/ring.",
        "faq": [
            [
                "Kan er een kabel naar mijn vrijstaande garage getrokken worden?",
                "Ja, wij leggen grondkabels (YMvK-as) met aardscherm vakkundig aan en plaatsen indien gewenst een onderverdeelkast in de garage."
            ],
            [
                "Hoe snel kunnen jullie zijn bij een storing in Vleuten?",
                "Bij acute spoedmeldingen zijn we doorgaans binnen {aanrijtijd_utrecht} minuten voor de deur."
            ]
        ]
    },
    {
        "slug": "utrecht-west",
        "naam": "Utrecht West & Lombok",
        "type": "wijk",
        "gemeente": "Utrecht",
        "buurten": [
            "Lombok",
            "Nieuw Engeland",
            "Oog in Al",
            "Majellapark",
            "Schepenbuurt",
            "Cartesius"
        ],
        "aanrijtijd": "{aanrijtijd_utrecht} min",
        "intro": "Elektricien in Utrecht West, Lombok of Oog in Al nodig? INO Elektra helpt je snel en vakkundig. Of het nu gaat om het veilig aansluiten van een nieuwe keuken, groepenkast vernieuwen of acute storingsdienst: je spreekt rechtstreeks met de vakman. Geen voorrijkosten binnen Utrecht en altijd een vaste prijs vooraf.",
        "woningen": "Utrecht West kent een karakteristieke mix van gezellige vooroorlogse arbeiderswoningen in Lombok en Nieuw Engeland, en statige jaren '30 villa's en herenhuizen in Oog in Al. Bij verbouwingen stuiten bewoners geregeld op verouderde meterkasten, leidingen met onvoldoende capaciteit of ontbrekende aarding. Wij brengen de installatie volledig op het niveau van de huidige NEN 1010 veiligheidsnormen.",
        "klussen": [
            [
                "Groepenkast moderniseren",
                "Oude smeltveiligheden vervangen door veilige installatieautomaten en aardlekschakelaars."
            ],
            [
                "Perilex kookgroep aanleggen",
                "Van gas naar inductie: veilige bekabeling trekken vanaf de meterkast naar de kookplaat."
            ],
            [
                "Sleuven frezen voor inbouwschakelmateriaal",
                "Strak wegwerken van leidingen in baksteen en gips zonder zichtbare kabelgoten."
            ],
            [
                "Storingsdienst bij kortsluiting",
                "Snel lokaliseren en verhelpen van uitval in oudere circuits."
            ]
        ],
        "lokaal": "In Lombok en Nieuw Engeland is parkeren vaak krap. Wij plannen onze ritten strak in en zorgen dat we materiaal direct bij de hand hebben. Geen voorrijkosten in heel Utrecht West.",
        "faq": [
            [
                "Kan ik mijn oude stoppenkast in Lombok behouden als ik elektrisch ga koken?",
                "Nee, voor een inductiekookplaat is een aparte kookgroep of krachtgroep met een hoofdschakelaar en aardlekschakelaar vereist volgens NEN 1010. Een oude stoppenkast voldoet daar niet aan."
            ],
            [
                "Wat kost het vervangen van een groepenkast in Utrecht West?",
                "Een complete 1-fase groepenkast vervangen inclusief montage, A-merk componenten en btw start bij € {groepenkast_1f}. Voor 3-fase start dit bij € {groepenkast_3f}."
            ]
        ]
    },
    {
        "slug": "zuilen",
        "naam": "Zuilen & Ondiep (Noordwest)",
        "type": "wijk",
        "gemeente": "Utrecht",
        "buurten": [
            "Oud-Zuilen",
            "Zuilen-Noord",
            "Elinkwijk",
            "Ondiep",
            "Pijlsweerd",
            "2e Daalsebuurt",
            "Geuzenwijk"
        ],
        "aanrijtijd": "{aanrijtijd_utrecht} min",
        "intro": "Woon je in Zuilen, Ondiep of Pijlsweerd en zoek je een betrouwbare elektricien? INO Elektra is jouw lokale installateur in Utrecht Noordwest. Voor groepenkasten, Perilex, elektra-uitbreidingen en spoedservice. Altijd een duidelijke prijs vooraf, 100% transparant en geen voorrijkosten.",
        "woningen": "In Zuilen en Ondiep staan veel sfeervolle arbeiders- en spoorwegwoningen uit het begin van de 20e eeuw (zoals in Elinkwijk) naast gerenoveerde portiekwoningen en eigentijdse nieuwbouw langs de Vecht. Veel bewoners renoveren hun woning en schakelen over van aardgas naar inductie. Daarbij is vaak een upgrade van de meterkast nodig, het trekken van nieuwe bedrading en het aarden van natte ruimtes.",
        "klussen": [
            [
                "Groepenkast vervangen",
                "Vervanging van verouderde meterkasten door compacte 1-fase of 3-fase A-merk kasten."
            ],
            [
                "Perilex aansluiting monteren",
                "Aanleg van 2-fase kookgroep voor zorgeloos koken op inductie."
            ],
            [
                "Aarding in de badkamer & keuken",
                "Plaatsen van vereffening en aarding ter voorkoming van schokken of lekstromen."
            ],
            [
                "Storingsdienst bij aardlekuitval",
                "Gerichte foutdiagnose met professionele isolatieweerstandsmeters."
            ]
        ],
        "lokaal": "Zuilen en Ondiep zijn uitstekend bereikbaar vanaf de Amsterdamsestraatweg en de Vleutenseweg. Binnen de gemeente Utrecht betaal je € {voorrijkosten_utrecht} voorrijkosten.",
        "faq": [
            [
                "Mijn aardlekschakelaar springt er steeds uit in Ondiep, wat moet ik doen?",
                "Schakel alle groepen achter die aardlekschakelaar uit, zet de aardlekschakelaar weer omhoog en schakel de groepen één voor één weer in. Blijft hij uitvallen? Bel ons direct voor storingshulp."
            ],
            [
                "Hoe lang duurt het vervangen van een groepenkast?",
                "Een standaard vervanging duurt gemiddeld 2 tot 3,5 uur. Tijdens de werkzaamheden is de stroom tijdelijk uitgeschakeld."
            ]
        ]
    },
    {
        "slug": "overvecht",
        "naam": "Overvecht",
        "type": "wijk",
        "gemeente": "Utrecht",
        "buurten": [
            "Overvecht-Noord",
            "Overvecht-Zuid",
            "Overvecht-Centrum",
            "Vechtzoom",
            "Taagdreef e.o.",
            "Zambesidreef e.o."
        ],
        "aanrijtijd": "{aanrijtijd_utrecht} min",
        "intro": "Stroom uitgevallen, een aardlekschakelaar die blijft uitspringen of toe aan een nieuwe groepenkast in Overvecht? INO is een elektricien uit Utrecht die dagelijks in Overvecht-Noord en -Zuid werkt. Je belt direct met de monteur, krijgt vooraf een vaste prijs en betaalt binnen de gemeente Utrecht geen voorrijkosten.",
        "woningen": "Overvecht is grotendeels in de jaren '60 en '70 gebouwd: veel portiek- en galerijflats langs de dreven, aangevuld met eengezinswoningen en nieuwere bouw na de renovaties van de afgelopen jaren. In woningen die nooit vernieuwd zijn zien we vaak een groepenkast met weinig groepen, niet alle groepen achter een aardlekschakelaar en in slaapkamers soms nog stopcontacten zonder randaarde. Omdat steeds meer bewoners overstappen op elektrisch koken, is een extra kookgroep of Perilex-aansluiting hier een van onze meest gevraagde klussen.",
        "klussen": [
            [
                "Groepenkast vervangen in een flat",
                "Oude kast met smeltzekeringen of te weinig aardlekschakelaars? We plaatsen een nieuwe, NEN 1010-conforme kast, meestal binnen één werkdag."
            ],
            [
                "Kookgroep voor inductie",
                "Overstappen van gas naar inductie? We trekken een aparte kookgroep met Perilex-aansluiting vanaf de meterkast."
            ],
            [
                "Aardlek slaat steeds af",
                "Vaak een apparaat of vocht in een buitenstopcontact of badkamer. We meten het per groep door en lossen de oorzaak op."
            ],
            [
                "Stopcontacten met randaarde",
                "Oude stopcontacten zonder aarde vervangen of extra stopcontacten bijplaatsen, netjes weggewerkt."
            ]
        ],
        "lokaal": "Parkeren is in Overvecht meestal geen probleem, dus we staan snel voor de deur. Zit niet alleen jij maar de hele flat of straat zonder stroom? Dan ligt de storing waarschijnlijk bij de netbeheerder: bel dan eerst het gratis Nationaal Storingsnummer 0800-9009.",
        "faq": [
            [
                "Rekenen jullie voorrijkosten in Overvecht?",
                "Nee. Overvecht valt binnen de gemeente Utrecht, dus je betaalt geen voorrijkosten. Je betaalt alleen het vaste tarief dat we vooraf afspreken."
            ],
            [
                "Mag ik in mijn huurwoning de groepenkast laten vervangen?",
                "Bij een huurwoning is de groepenkast meestal van de verhuurder of woningcorporatie. Overleg eerst met je verhuurder; wij kunnen een offerte en foto's aanleveren zodat zij snel kunnen beslissen."
            ],
            [
                "Hoe snel zijn jullie bij spoed in Overvecht?",
                "Bij een acute storing zijn we meestal binnen {aanrijtijd_utrecht} minuten ter plaatse, afhankelijk van het verkeer. Bel direct, dan hoor je meteen hoe laat we er kunnen zijn."
            ]
        ]
    },
    {
        "slug": "hoograven",
        "naam": "Hoograven, Lunetten & Tolsteeg",
        "type": "wijk",
        "gemeente": "Utrecht",
        "buurten": [
            "Oud-Hoograven",
            "Nieuw-Hoograven",
            "Tolsteeg",
            "Lunetten",
            "Bokkenbuurt",
            "Rotsoord"
        ],
        "aanrijtijd": "{aanrijtijd_utrecht} min",
        "intro": "Elektricien in Hoograven, Lunetten of Tolsteeg gezocht? INO Elektra is gevestigd in Utrecht en staat voor vakmanschap, veiligheid en transparante prijzen. Van het vervangen van je meterkast tot keuken-elektra en storingshulp: wij helpen je snel en zonder voorrijkosten.",
        "woningen": "In Hoograven en Tolsteeg vind je een rijke variatie van jaren '30 en '50 woningen tot de kenmerkende jaren '70 bloemkool-indeling in Lunetten en nieuwe lofts op Rotsoord. Veel keukens en badkamers worden verbouwd, waarbij extra geaarde groepen nodig zijn voor vaatwassers, inductiekookplaten en ovens. Wij zorgen voor een veilige verdeling over de verschillende fasen en aardlekschakelaars.",
        "klussen": [
            [
                "Keukenelektra & kookgroepen",
                "Aparte groepen voor quookers, vaatwassers, ovens en inductieplaten."
            ],
            [
                "Groepenkast vervangen",
                "Installatie van moderne, brandveilige kasten van ABB of Hager."
            ],
            [
                "Aardlekschakelaars toevoegen",
                "Voldoen aan de norm: maximaal 4 groepen per aardlekschakelaar voor optimale veiligheid."
            ],
            [
                "Opsporen van aardlekstoringen",
                "Lekstromen doormeten in vochtige kruipruimtes en buitenbekabeling."
            ]
        ],
        "lokaal": "Dankzij de ligging nabij de Waterlinieweg en de ring Utrecht Zuid zijn wij zeer snel op locatie in Hoograven en Lunetten. Geen voorrijkosten.",
        "faq": [
            [
                "Hoeveel groepen mogen er achter één aardlekschakelaar?",
                "Volgens de NEN 1010 norm mogen er maximaal 4 groepen achter één aardlekschakelaar worden aangesloten, om onnodige uitval door minimale lekstromen te voorkomen."
            ],
            [
                "Kunnen jullie ook helpen bij het verplaatsen van stopcontacten in Lunetten?",
                "Jazeker, wij frezen leidingen netjes in en monteren dubbele of enkele inbouwstopcontacten op elke gewenste hoogte."
            ]
        ]
    },
    {
        "slug": "kanaleneiland",
        "naam": "Kanaleneiland",
        "type": "wijk",
        "gemeente": "Utrecht",
        "buurten": [
            "Kanaleneiland-Noord",
            "Kanaleneiland-Zuid",
            "Kanaleneiland-Centrum"
        ],
        "aanrijtijd": "{aanrijtijd_utrecht} min",
        "intro": "Een elektricien nodig in Kanaleneiland? INO helpt bewoners tussen het Merwedekanaal en het Amsterdam-Rijnkanaal met storingen, nieuwe groepen en complete groepenkasten. Vaste prijs vooraf, geen voorrijkosten binnen Utrecht en bij spoed 24/7 bereikbaar.",
        "woningen": "Kanaleneiland is een typische wederopbouwwijk uit eind jaren '50 en begin jaren '60, met veel portiekflats en lange bouwblokken. De originele elektrische installatie is daar vaak aangelegd voor een paar lampen en een wasmachine, niet voor de apparaten die we nu gebruiken. Dat merk je aan groepen die uitvallen zodra de waterkoker, magnetron en airfryer tegelijk aan staan. Een extra groep of een nieuwe groepenkast lost dat structureel op.",
        "klussen": [
            [
                "Groep valt uit bij koken",
                "Keukenapparaten op één groep overbelasten de installatie. We verdelen ze over extra groepen zodat het niet meer uitvalt."
            ],
            [
                "Groepenkast vernieuwen",
                "Oude kasten met porseleinen zekeringen vervangen we door een moderne kast met aardlekautomaten."
            ],
            [
                "Wasmachine en droger apart",
                "Een eigen groep voor wasmachine en droger voorkomt dat de aardlek afslaat tijdens het wassen."
            ],
            [
                "Storing zoeken",
                "Valt de stroom af en toe weg zonder duidelijke reden? We meten isolatieweerstand en verbindingen door tot we de oorzaak hebben."
            ]
        ],
        "lokaal": "Kanaleneiland ligt vlak bij de ring en de Jaarbeurs, waardoor we er bij spoed meestal snel zijn. In portiekflats zit de meterkast soms in het trappenhuis of in de gang; stuur gerust een foto via WhatsApp, dan kunnen we vooraf al veel inschatten.",
        "faq": [
            [
                "Wat kost een extra groep in Kanaleneiland?",
                "Een extra groep bijplaatsen kan vanaf € {extra_groep}, afhankelijk van je huidige kast en de ruimte. Stuur een foto van je meterkast, dan krijg je direct een vaste prijs."
            ],
            [
                "Waarom valt mijn stroom uit als ik kook?",
                "Meestal staan te veel zware apparaten op één groep. Dat is geen defect maar overbelasting. De oplossing is een extra groep of een aparte kookgroep."
            ],
            [
                "Zijn er voorrijkosten in Kanaleneiland?",
                "Nee, Kanaleneiland valt binnen de gemeente Utrecht. Je betaalt geen voorrijkosten."
            ]
        ]
    },
    {
        "slug": "transwijk",
        "naam": "Transwijk",
        "type": "wijk",
        "gemeente": "Utrecht",
        "buurten": [
            "Transwijk-Noord",
            "Transwijk-Zuid",
            "Park Transwijk",
            "Dichterswijk (grenzend)"
        ],
        "aanrijtijd": "{aanrijtijd_utrecht} min",
        "intro": "INO is je elektricien in Transwijk, van de flats rond Park Transwijk tot de eengezinswoningen richting het Merwedekanaal. Of het nu gaat om een storing, een nieuwe groepenkast of extra stopcontacten: je krijgt vooraf een vaste prijs en betaalt binnen Utrecht geen voorrijkosten.",
        "woningen": "Transwijk is net als het naastgelegen Kanaleneiland na de oorlog gebouwd, met een mix van flats en rijtjeshuizen. Veel woningen zijn inmiddels verbouwd: een open keuken, een uitbouw of een zolderkamer. Precies daar gaat het vaak mis, omdat de installatie niet is meegegroeid. We zien regelmatig verlengde leidingen, te veel stopcontacten op één groep en een groepenkast die vol zit. In de oudere, vooroorlogse huizen van de aangrenzende Dichterswijk komen we daarnaast nog weleens oude bedrading tegen.",
        "klussen": [
            [
                "Elektra voor een verbouwing",
                "Nieuwe keuken of uitbouw? We leggen de groepen, stopcontacten en verlichting aan volgens NEN 1010."
            ],
            [
                "Groepenkast uitbreiden",
                "Kast vol? We breiden uit of vervangen hem door een kast met ruimte voor laadpaal of warmtepomp later."
            ],
            [
                "Stopcontacten verleggen",
                "Stofarm frezen en stopcontacten verplaatsen, zodat je interieur klopt."
            ],
            [
                "Oude bedrading controleren",
                "Twijfel over de staat van je leidingen? We meten de installatie door en adviseren wat echt nodig is."
            ]
        ],
        "lokaal": "Heb je een storing en twijfel je of het aan je eigen woning ligt? Kijk of de buren en de straatverlichting nog stroom hebben. Zo ja, dan zit het in je eigen installatie en kunnen wij helpen. Zo nee, bel dan het Nationaal Storingsnummer 0800-9009.",
        "faq": [
            [
                "Kunnen jullie de elektra voor mijn nieuwe keuken aanleggen?",
                "Ja. We maken vooraf een plan voor groepen, kookgroep en stopcontacten, en werken met een vaste prijs. Stuur je keukentekening mee, dan rekenen we het direct door."
            ],
            [
                "Werken jullie ook in de Dichterswijk en Rivierenwijk?",
                "Ja, we werken in heel Utrecht-Zuidwest en Zuid. Overal geldt dezelfde vaste prijs zonder voorrijkosten."
            ],
            [
                "Hoe lang duurt het vervangen van een groepenkast?",
                "Meestal een halve tot hele werkdag. Je zit in die tijd kort zonder stroom; we spreken vooraf af wanneer dat het beste uitkomt."
            ]
        ]
    },
    {
        "slug": "utrecht-noordoost",
        "naam": "Utrecht Noordoost & Wittevrouwen",
        "type": "wijk",
        "gemeente": "Utrecht",
        "buurten": [
            "Wittevrouwen",
            "Vogelenbuurt",
            "Tuindorp",
            "Tuinwijk",
            "Voordorp",
            "Lauwerecht"
        ],
        "aanrijtijd": "{aanrijtijd_utrecht} min",
        "intro": "Elektricien in Utrecht Noordoost, Wittevrouwen of Tuindorp gezocht? INO Elektra is gespecialiseerd in het vakkundig aanpassen en vernieuwen van elektrotechnische installaties in historische en vooroorlogse woningen. Betrouwbaar, volgens NEN 1010 en zonder voorrijkosten binnen Utrecht.",
        "woningen": "Wittevrouwen en Tuinwijk behoren tot de meest gewilde woonwijken van Utrecht met prachtige gevels uit de late 19e en vroege 20e eeuw. Tuindorp kenmerkt zich door hoogwaardige jaren '30 bouw. De elektrische installaties vragen hier om echt vakmanschap: oude stuc- en lijstwerkplafonds moeten behouden blijven terwijl de capaciteit verdubbeld wordt voor inductiekoken, zonnepanelen en quookers.",
        "klussen": [
            [
                "Groepenkast vergroten & moderniseren",
                "Upgraden naar 8 tot 12 groepen met aardlekautomaten voor optimale betrouwbaarheid."
            ],
            [
                "Perilex inductiekookgroep aanleggen",
                "Subtiele bekabeling naar de keuken zonder hakwerk in monumentale stucdetails."
            ],
            [
                "Aarding herstellen & verbeteren",
                "Doormeten en slaan van aardelektrodes voor maximale veiligheid."
            ],
            [
                "Buitenverlichting en tuinstopcontacten",
                "Sfeervolle verlichting in stadstuinen met veilige spatwaterdichte IP65 aansluitingen."
            ]
        ],
        "lokaal": "In Wittevrouwen en Tuinwijk kan parkeren uitdagend zijn. Wij houden hier rekening mee in onze planning. Geen voorrijkosten in heel Noordoost.",
        "faq": [
            [
                "Kunnen jullie extra groepen toevoegen zonder dat de hele meterkast vervangen moet worden?",
                "Als de huidige kast van een degelijk A-merk is en voldoende vrije moduleruimte heeft, kunnen we losse aardlekautomaten bijplaatsen. Is de kast verouderd, dan is complete vervanging veiliger en vaak voordeliger."
            ],
            [
                "Geven jullie garantie op de werkzaamheden?",
                "Ja, wij bieden standaard 12 maanden volledige installatiegarantie en 2 jaar fabrieksgarantie op alle geleverde A-merk materialen."
            ]
        ]
    },
    {
        "slug": "nieuwegein",
        "naam": "Nieuwegein",
        "type": "plaats",
        "gemeente": "Nieuwegein",
        "buurten": [
            "Batau",
            "Doorslag",
            "Fokkesteeg",
            "Galecop",
            "Jutphaas-Wijkersloot",
            "Zuilenstein",
            "Merwestein",
            "Vreeswijk",
            "Blokhoeve"
        ],
        "aanrijtijd": "{aanrijtijd_regio} min",
        "intro": "INO is elektricien voor Nieuwegein: van Batau en Galecop tot Zuilenstein en het oude Vreeswijk. We helpen bij stroomstoringen, vervangen groepenkasten en leggen kookgroepen en laadpalen aan. Altijd met een vaste prijs vooraf.",
        "woningen": "Nieuwegein is als groeikern grotendeels in de jaren '70 en '80 gebouwd. Veel van die woningen hebben nog de originele groepenkast, soms met smeltzekeringen en vaak met maar één of twee aardlekschakelaars voor het hele huis. Valt er één groep uit, dan zit je in een groot deel van het huis in het donker. Een moderne kast met aardlekautomaten per groep is veiliger en voorkomt dat. In het historische Vreeswijk en in nieuwbouw als Blokhoeve liggen de vragen weer anders, van oude bedrading tot laadpalen.",
        "klussen": [
            [
                "Kast met smeltzekeringen vervangen",
                "Schroefzekeringen en één oude aardlek? We plaatsen een veilige, moderne groepenkast."
            ],
            [
                "Aardlekautomaten per groep",
                "Zo valt bij een storing alleen die ene groep uit en niet je halve huis."
            ],
            [
                "Kookgroep en Perilex",
                "Klaar voor inductie met een aparte kookgroep vanaf de meterkast."
            ],
            [
                "Laadpaal en krachtstroom",
                "Laadpaal of warmtepomp? We bekijken of je huidige aansluiting volstaat."
            ]
        ],
        "lokaal": "Nieuwegein valt buiten de gemeente Utrecht; we rekenen € {km_tarief} per km en melden dat vooraf. Via de A12 en A2 zijn we er bij spoed snel. Hele wijk zonder stroom? Bel dan eerst 0800-9009 (netbeheerder).",
        "faq": [
            [
                "Mijn huis uit de jaren '70 heeft nog schroefzekeringen. Is dat gevaarlijk?",
                "Niet direct gevaarlijk zolang alles werkt, maar het voldoet niet meer aan de huidige normen en biedt minder bescherming tegen elektrocutie en brand. Vervangen is een verstandige investering, zeker als je meer elektrisch gaat gebruiken."
            ],
            [
                "Wat kost een nieuwe groepenkast in Nieuwegein?",
                "Een 1-fase kast begint bij € {groepenkast_1f} all-in, een 3-fase kast bij € {groepenkast_3f}. Daar komt de kilometervergoeding bij, die je vooraf hoort."
            ],
            [
                "Werken jullie ook in Vreeswijk?",
                "Ja, in heel Nieuwegein, inclusief Vreeswijk en de nieuwbouw in Blokhoeve."
            ]
        ]
    },
    {
        "slug": "maarssen",
        "naam": "Maarssen",
        "type": "plaats",
        "gemeente": "Stichtse Vecht",
        "buurten": [
            "Maarssen-Dorp",
            "Maarssenbroek",
            "Bloemstede",
            "Fazantenkamp",
            "Zogweteringen",
            "Bisonspoor"
        ],
        "aanrijtijd": "{aanrijtijd_regio} min",
        "intro": "Een elektricien in Maarssen nodig? INO komt vanuit Utrecht naar Maarssen-Dorp en Maarssenbroek voor storingen, groepenkasten, Perilex-aansluitingen en laadpalen. Je spreekt direct de monteur en weet vooraf wat het kost.",
        "woningen": "Maarssen heeft twee gezichten. In Maarssen-Dorp langs de Vecht staan oude, soms monumentale panden waar de bedrading in de loop der jaren stukje bij beetje is aangepast. Daar is zorgvuldig werken en netjes wegwerken belangrijk. Maarssenbroek is vooral in de jaren '70 en '80 gebouwd; daar zijn de installaties vaak nog origineel, met een groepenkast die aan vervanging toe is of te klein is voor inductie, een warmtepomp of een laadpaal.",
        "klussen": [
            [
                "Groepenkast vervangen",
                "Originele kast uit de jaren '70/'80? We vervangen hem door een moderne kast met aardlekautomaten."
            ],
            [
                "Perilex en inductie",
                "Aparte kookgroep met Perilex-aansluiting voor je nieuwe inductiekookplaat."
            ],
            [
                "Werken in oudere panden",
                "Zorgvuldig aanpassen van bestaande bedrading, met oog voor het karakter van het pand."
            ],
            [
                "Laadpaal op eigen terrein",
                "Installatie van een laadpaal met eigen groep en veilige aansluiting."
            ]
        ],
        "lokaal": "Maarssen valt buiten de gemeente Utrecht. We rekenen daarom een vast kilometertarief van € {km_tarief} per km, en dat bedrag hoor je altijd vooraf. Via de A2 zijn we er vanuit Utrecht snel.",
        "faq": [
            [
                "Wat kost voorrijden naar Maarssen?",
                "Voor Maarssen rekenen we € {km_tarief} per km. Je hoort het exacte bedrag altijd vooraf, samen met de prijs van de klus."
            ],
            [
                "Werken jullie ook in oudere panden in Maarssen-Dorp?",
                "Ja. We werken zorgvuldig, overleggen waar leidingen komen en werken alles netjes weg. Bij monumenten stemmen we vooraf af wat wel en niet mag."
            ],
            [
                "Komen jullie ook bij spoed naar Maarssen?",
                "Ja, ook buiten kantooruren. Bel direct, dan hoor je meteen wanneer we er kunnen zijn."
            ]
        ]
    },
    {
        "slug": "houten",
        "naam": "Houten",
        "type": "plaats",
        "gemeente": "Houten",
        "buurten": [
            "Het Rond",
            "Castellum",
            "Schonauwen",
            "Tiellandt",
            "Wulven",
            "Houten-Zuid",
            "Loerik"
        ],
        "aanrijtijd": "{aanrijtijd_regio} min",
        "intro": "Elektricien in Houten gezocht? INO Elektra verzorgt complete installaties in Houten-Noord en Houten-Zuid. Specialist in groepenkasten, laadpalen met load balancing, krachtstroom en keukenelektra. Vooraf een duidelijke all-in prijs en gecertificeerd vakmanschap volgens NEN 1010.",
        "woningen": "Houten is een moderne gemeente met voornamelijk naoorlogse en recente eengezinswoningen rond de twee spoorwegcentra (Het Rond en Castellum). Het autobezit en gebruik van elektrische voertuigen en zonnepanelen is hier erg hoog. We zien hier veel vraag naar laadpaalinstallaties met dynamic load balancing, krachtstroom voor warmtepompen en het uitbreiden van meterkasten met extra PV-groepen.",
        "klussen": [
            [
                "Laadpaal installeren",
                "Montage van slimme laadpunten op de eigen oprit inclusief kabeltraject en load balancing."
            ],
            [
                "Groepenkast uitbreiden voor PV & warmtepomp",
                "Aparte aardlekautomaten plaatsen voor zonnepanelen en hybride warmtepompen."
            ],
            [
                "3-Fase krachtstroom aanleggen",
                "Professionele meterkastvoorbereiding voor zware apparatuur."
            ],
            [
                "Elektra inbouw & keukenvoorbereiding",
                "Verleggen van stopcontacten en leidingen bij nieuwe keukens."
            ]
        ],
        "lokaal": "Vanaf de A27 en De Rondweg Houten zijn alle wijken snel bereikbaar. Wij rekenen voor Houten slechts € {km_tarief}/km voorrijden.",
        "faq": [
            [
                "Kan mijn bestaande groepenkast in Houten uitgebreid worden voor een warmtepomp?",
                "Vaak wel, mits er voldoende vrije moduleruimte op de DIN-rail is en de hoofdschakelaar zwaar genoeg is. We bekijken dit graag vooraf aan de hand van een foto."
            ],
            [
                "Leveren jullie ook de laadpaal zelf?",
                "Wij kunnen het complete pakket leveren (zoals Alfen of Easee) of uitsluitend de montage en aansluiting verzorgen van een laadpaal die je zelf hebt aangeschaft."
            ]
        ]
    },
    {
        "slug": "zeist",
        "naam": "Zeist",
        "type": "plaats",
        "gemeente": "Zeist",
        "buurten": [
            "Centrum",
            "Zeist-West",
            "Kerckebosch",
            "Vollenhove",
            "Huis ter Heide",
            "Griffensteijn",
            "Coucheron"
        ],
        "aanrijtijd": "{aanrijtijd_regio} min",
        "intro": "Elektricien in Zeist nodig? INO Elektra helpt particulieren en bedrijven in Zeist, Kerckebosch en Zeist-West. Van groepenkasten en krachtstroom tot tuinverlichting en storingsdienst. Erkend vakman, duidelijke tarieven en betrouwbare service volgens NEN 1010.",
        "woningen": "Zeist kenmerkt zich door prachtige bosrijke villawijken, karakteristieke jaren '30 panden en naoorlogse woonwijken. In veel woningen met grote percelen installeren wij uitgebreide buitenverlichting met grondkabels en schemerschakelaars. Daarnaast voeren we regelmatig 3-fase verzwaringen uit voor inductiekoken, sauna's en warmtepompen.",
        "klussen": [
            [
                "Tuinverlichting & grondkabels",
                "Aanleg van waterdichte grondkabelnetwerken, spots en schemerschakelaars."
            ],
            [
                "Krachtstroom & zware aansluitingen",
                "3-fase aanleg voor sauna's, laadpalen en warmtepompen."
            ],
            [
                "Groepenkast vernieuwen",
                "Vervanging van oude stoppenkasten door veilige A-merk installaties."
            ],
            [
                "Storingsdienst 24/7",
                "Snel opsporen van lekstroomstoringen in buitenkabels en binnencircuits."
            ]
        ],
        "lokaal": "Via de Utrechtseweg en de A28 zijn we bij spoed binnen {aanrijtijd_regio} minuten in Zeist. Vaste prijzen vooraf en heldere afspraken.",
        "faq": [
            [
                "Mijn tuinverlichting laat de aardlek eruit springen, kunnen jullie dit oplossen?",
                "Jazeker, vocht in grondmoffen of beschadigde grondkabels zijn een veelvoorkomende oorzaak. Wij sporen de exacte locatie op en maken de verbinding waterdicht."
            ],
            [
                "Wat kost een schouw in Zeist?",
                "Een schouw op locatie kost € {schouw} incl. btw, en dit bedrag brengen we volledig in mindering op de factuur zodra je de klus door ons laat uitvoeren."
            ]
        ]
    },
    {
        "slug": "ijsselstein",
        "naam": "IJsselstein",
        "type": "plaats",
        "gemeente": "IJsselstein",
        "buurten": [
            "Binnenstad",
            "IJsselveld",
            "Achterveld",
            "Zenderpark",
            "Hazeneiland"
        ],
        "aanrijtijd": "{aanrijtijd_regio} min",
        "intro": "Betrouwbare elektricien in IJsselstein nodig? INO Elektra staat voor je klaar in Zenderpark, Achterveld en de historische binnenstad. Groepenkast vervangen, kookgroep aansluiten of met spoed een storing oplossen. Altijd een vaste prijs vooraf, A-merk materialen en 12 maanden garantie.",
        "woningen": "IJsselstein heeft een sfeervol historisch centrum en ruime woonwijken zoals Achterveld en Zenderpark. Veel huishoudens stappen over op elektrisch koken of schaffen een elektrische auto aan. Wij zorgen voor veilige meterkastuitbreidingen, het trekken van Perilex-leidingen en de installatie van laadpalen.",
        "klussen": [
            [
                "Groepenkast vervangen",
                "Montage van complete 1-fase of 3-fase kasten met 5 jaar fabrieksgarantie."
            ],
            [
                "Perilex kookgroep monteren",
                "Netjes weggewerkt leidingwerk naar de kookplaat."
            ],
            [
                "Laadpaal voor thuis",
                "Veilige montage met dynamic load balancing op de oprit."
            ],
            [
                "Storingsdienst 24/7",
                "Snel herstel bij uitval van de spanning."
            ]
        ],
        "lokaal": "Via de A2 en de N210 zijn we bij spoed binnen {aanrijtijd_regio} minuten in IJsselstein. Transparant kilometertarief van € {km_tarief}/km buiten Utrecht.",
        "faq": [
            [
                "Kan ik via WhatsApp een offerte krijgen voor IJsselstein?",
                "Zeker! Stuur een foto van je meterkast via WhatsApp naar 06 28 76 37 75 en je ontvangt snel een vaste all-in prijs."
            ],
            [
                "Zijn jullie ook 's avonds beschikbaar voor spoedklussen?",
                "Ja, onze storingsmonteur is 24/7 oproepbaar voor acute calamiteiten."
            ]
        ]
    },
    {
        "slug": "vianen",
        "naam": "Vianen",
        "type": "plaats",
        "gemeente": "Vijfheerenlanden",
        "buurten": [
            "Binnenstad (Voorstraat)",
            "Vianen-Noord",
            "Hoef en Haag",
            "Hagestein",
            "Everdingen"
        ],
        "aanrijtijd": "{aanrijtijd_regio} min",
        "intro": "Een elektricien in Vianen, net over de Lekbrug? INO komt vanuit Utrecht naar de historische binnenstad van Vianen, de woonwijken en nieuwbouw als Hoef en Haag. Voor storingen, groepenkasten, kookgroepen en laadpalen, altijd met een vaste prijs vooraf.",
        "woningen": "In de oude vestingstad rond de Voorstraat staan panden die soms honderden jaren oud zijn. De elektrische installatie is daar vaak in fases aangepast, met verschillende soorten leidingen door elkaar. Doormeten en zorgvuldig vernieuwen is daar het belangrijkste werk. In de naoorlogse wijken vervangen we vooral verouderde groepenkasten, en in de nieuwbouw van Hoef en Haag draait het meestal om uitbreiden: laadpaal, zonnepanelen of een extra groep.",
        "klussen": [
            [
                "Installatie doormeten",
                "Twijfel over oude bedrading? We meten isolatie en aarding door en geven een eerlijk advies."
            ],
            [
                "Groepenkast vervangen",
                "Een verouderde kast vervangen door een moderne, veilige kast met aardlekautomaten."
            ],
            [
                "Laadpaal in nieuwbouw",
                "Laadpaal installeren met eigen groep, ook als je al zonnepanelen hebt."
            ],
            [
                "Storingen verhelpen",
                "Aardlek die afslaat of een groep die uitvalt: we zoeken de oorzaak en lossen het op."
            ]
        ],
        "lokaal": "Vianen valt buiten de gemeente Utrecht. We rekenen € {km_tarief} per km en melden dat altijd vooraf. Bel bij spoed direct, dan hoor je meteen wanneer we er kunnen zijn.",
        "faq": [
            [
                "Komen jullie ook naar Vianen?",
                "Ja. Vianen ligt direct ten zuiden van Utrecht, over de Lek. We rekenen € {km_tarief} per km voorrijden en je hoort dat bedrag vooraf."
            ],
            [
                "Kunnen jullie werken in een oud pand in de binnenstad?",
                "Ja. We werken zorgvuldig en overleggen vooraf waar leidingen lopen. Bij een monument stemmen we af wat wel en niet mag."
            ],
            [
                "Werken jullie ook in Hagestein en Everdingen?",
                "Ja, ook in de kernen rond Vianen. Vraag gerust je adres na."
            ]
        ]
    },
    {
        "slug": "breukelen",
        "naam": "Breukelen",
        "type": "plaats",
        "gemeente": "Stichtse Vecht",
        "buurten": [
            "Breukelen-Centrum",
            "Breukelen-Noord",
            "Breukelen-Zuid",
            "Nieuwer Ter Aa",
            "Kockengen"
        ],
        "aanrijtijd": "{aanrijtijd_regio} min",
        "intro": "INO is ook je elektricien in Breukelen. Van de oude dorpskern en de panden langs de Vecht tot de woonwijken rond het station: we helpen bij storingen, groepenkasten, kookgroepen, laadpalen en buitenverlichting. Vooraf een vaste prijs, geen verrassingen achteraf.",
        "woningen": "Breukelen combineert een historische kern met naoorlogse en nieuwere woonwijken. In de oudere panden kom je vaak installaties tegen die in de loop der jaren zijn uitgebreid zonder dat de groepenkast meegroeide. Buiten het centrum, met grotere tuinen en vrijstaande woningen, zijn tuinverlichting, stroom naar het tuinhuis en een laadpaal op eigen terrein veelgevraagde klussen.",
        "klussen": [
            [
                "Stroom naar tuinhuis of schuur",
                "Grondkabel, eigen groep en een waterdichte aansluiting, veilig aangelegd."
            ],
            [
                "Tuinverlichting",
                "Sfeervolle buitenverlichting met IP-klasse verlichting en nette kabelgoten."
            ],
            [
                "Groepenkast uitbreiden of vervangen",
                "Meer groepen of een complete nieuwe kast als de oude te klein of verouderd is."
            ],
            [
                "Laadpaal op eigen terrein",
                "Laadpaal met eigen groep en, waar nodig, load balancing."
            ]
        ],
        "lokaal": "Breukelen valt buiten de gemeente Utrecht. We rekenen € {km_tarief} per km en melden dat vooraf. Via de A2 zijn we er vanuit Utrecht snel.",
        "faq": [
            [
                "Wat kost stroom naar mijn tuinhuis?",
                "Dat hangt af van de afstand en de ondergrond. Stuur foto's van je meterkast en de route naar het tuinhuis, dan krijg je een vaste prijs vooraf."
            ],
            [
                "Komen jullie ook naar Kockengen en Nieuwer Ter Aa?",
                "Ja. Vraag gerust je adres na; we rekenen € {km_tarief} per km en melden dat vooraf."
            ],
            [
                "Kan ik ook in het weekend een afspraak maken?",
                "Voor storingen zijn we 24/7 bereikbaar. Geplande klussen in het weekend kunnen in overleg; daarvoor gelden de avond- en weekendtarieven."
            ]
        ]
    }
]


OVERIGE_UTRECHT = [
    ["Binnenstad", "Domplein · Neude · Oudegracht · Museumkwartier"],
    ["Oost", "Wilhelminapark · Oudwijk · Schildersbuurt · Abstede"],
    ["Leidsche Rijn", "Terwijde · Het Zand · Parkwijk · Rijnvliet"],
    ["Vleuten-De Meern", "Vleuten · De Meern · Haarzicht · Veldhuizen"],
    ["West", "Lombok · Nieuw Engeland · Oog in Al · Majella"],
    ["Noordwest", "Zuilen · Ondiep · Pijlsweerd · Elinkwijk"],
    ["Overvecht", "Overvecht-Noord · Overvecht-Zuid · Zambesidreef"],
    ["Zuid", "Hoograven · Tolsteeg · Lunetten · Bokkenbuurt"],
    ["Zuidwest", "Kanaleneiland · Transwijk · Dichterswijk · Rivierenwijk"],
    ["Noordoost", "Wittevrouwen · Vogelenbuurt · Tuindorp · Tuinwijk"],
]

OVERIGE_REGIO = [
    ["Nieuwegein", "Jutphaas · Vreeswijk · Batau · Galecop"],
    ["Maarssen", "Maarssen-Dorp · Maarssenbroek · Boomstede"],
    ["Houten", "Het Rond · Castellum · Schonauwen"],
    ["Zeist", "Centrum · Zeist-West · Kerckebosch"],
    ["IJsselstein", "Binnenstad · IJsselveld · Zenderpark"],
    ["Vianen", "Centrum · De Hagen · Monnikenhof"],
    ["Breukelen", "Centrum · Broeckland · Nijenrode"],
    ["De Bilt", "De Bilt · Bilthoven"],
    ["Woerden", "Centrum · Molenvliet"],
]
