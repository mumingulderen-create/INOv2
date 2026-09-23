"""
PROBLEEMPAGINA'S (zoekintentie: "ik heb NU een probleem")
=========================================================
Mensen googelen hun probleem, niet "elektricien". Deze pagina's beantwoorden
precies die vraag, geven veilige eerste stappen en bieden meteen hulp aan.

Veiligheid: geef bezoekers NOOIT instructies om zelf iets open te schroeven of
aan leidingen te werken. Alleen: kijken, stekkers eruit, schakelaar omhoog/omlaag.

{uur_dag}, {km_tarief} enz. worden automatisch uit config.TARIEVEN ingevuld.
"""

STORINGEN = [
    {
        "slug": "stroomstoring-utrecht",
        "kort": "Geen stroom in huis",
        "title": "Geen stroom in huis? Stroomstoring Utrecht 24/7 | INO",
        "description": "Geen stroom in huis? Check in 1 minuut of het aan je meterkast of het net ligt. Storing in je woning: 24/7 elektricien in Utrecht, vaste prijs vooraf.",
        "h1": "Geen stroom in huis? Zo weet je binnen een minuut waar het zit",
        "intro": "Alles is ineens donker. Voordat je iemand belt: met twee snelle checks weet je of het probleem in je eigen woning zit of in het stroomnet van de straat. Dat scheelt tijd en voorkomt onnodige kosten.",
        "stappen_titel": "Doe deze checks, in deze volgorde",
        "stappen": [
            ["Kijk naar buiten", "Branden de lantaarnpalen en hebben de buren licht? Zit de hele straat zonder stroom, dan is het een netstoring. Bel het gratis Nationaal Storingsnummer 0800-9009. Een elektricien kan daar niets aan doen."],
            ["Open je meterkast", "Staat de hoofdschakelaar omlaag, of één of meer aardlekschakelaars of automaten? Zet dan eerst alles uit wat veel stroom vraagt en zet de schakelaar één keer rustig omhoog."],
            ["Springt hij er direct weer uit?", "Niet blijven proberen en de schakelaar nooit omhoog houden of vastzetten. Er is dan een echte fout, zoals een defect apparaat, vocht of een beschadigde leiding. Bel ons, dan zoeken we de oorzaak veilig op."],
            ["Staat alles omhoog maar geen stroom?", "Dan kan het in de aansluiting vóór je meter zitten (de hoofdzekering). Die is van de netbeheerder en mag je niet zelf vervangen. Bel ons: we checken of het in je installatie zit. Ligt het aan de aansluiting, dan zeggen we je dat eerlijk en schakel je de netbeheerder in."],
        ],
        "gevaar": "Ruik je brandlucht, zie je rook of vonken of voelt de meterkast warm aan? Zet de hoofdschakelaar uit als dat veilig kan, houd afstand en bel bij rook of vuur direct 112. Bel daarna ons voor veilig herstel.",
        "oorzaken_titel": "Veelvoorkomende oorzaken van stroomuitval in huis",
        "oorzaken": [
            ["Een defect apparaat", "Waterkoker, wasmachine, oven of koelkast met een interne fout laten de aardlekschakelaar afslaan."],
            ["Vocht", "Een buitenstopcontact, tuinverlichting of badkamer waar water bij komt."],
            ["Overbelasting", "Te veel zware apparaten tegelijk op één groep."],
            ["Beschadigde leiding", "Na boren of timmeren in de muur, of door ouderdom van de bedrading."],
        ],
        "faq": [
            ["Wie moet ik bellen als de hele straat geen stroom heeft?", "Bel het gratis Nationaal Storingsnummer 0800-9009. Zij geven de melding door aan de netbeheerder, in Utrecht is dat Stedin. Een elektricien kan storingen in het openbare net niet oplossen."],
            ["Wat kost het als jullie komen voor een stroomstoring?", "Overdag (08:00–18:00) betaal je € {uur_dag} voor het eerste uur, inclusief btw en diagnose. In de avond (18:00–22:00) € {uur_avond}. 's Nachts (22:00–08:00) en op complete zaterdagen, zondagen en feestdagen € {uur_nacht}. Binnen de gemeente Utrecht zijn er geen voorrijkosten."],
            ["Mag ik zelf een zekering vervangen?", "Een automaat of aardlekschakelaar weer omhoog zetten mag je zelf. Iets openschroeven of vervangen niet: laat dat aan een elektricien over. De hoofdzekering vóór de meter is van de netbeheerder en mag alleen door hen worden vervangen."],
            ["Hoe snel zijn jullie er?", "In de gemeente Utrecht meestal binnen {aanrijtijd_utrecht} minuten, in de randgemeenten binnen {aanrijtijd_regio} minuten. Bel, dan hoor je direct een tijd."],
        ],
        "gerelateerd": ["aardlekschakelaar-springt-eruit", "kortsluiting-utrecht"],
    },
    {
        "slug": "aardlekschakelaar-springt-eruit",
        "kort": "Aardlekschakelaar springt eruit",
        "title": "Aardlekschakelaar springt eruit? Oorzaak & hulp | INO",
        "description": "Blijft je aardlekschakelaar eruit springen? Zo vind je het apparaat dat de storing veroorzaakt. Lukt het niet: 24/7 elektricien in Utrecht, vaste prijs.",
        "h1": "Aardlekschakelaar springt steeds eruit: zo vind je de oorzaak",
        "intro": "Een aardlekschakelaar schakelt af zodra er stroom 'weglekt', bijvoorbeeld via een defect apparaat of vocht. Dat is precies zijn taak: hij beschermt je tegen een elektrische schok. De kunst is om te vinden waar het lek zit. Vaak lukt dat zelf in een paar minuten.",
        "stappen_titel": "Zo spoor je het apparaat op",
        "stappen": [
            ["Haal alle stekkers eruit", "Op de groepen achter die aardlekschakelaar (vaak de keuken, badkamer of wasruimte). Zet ook vaste apparaten zoals een close-in boiler of kookplaat uit als dat kan."],
            ["Zet de aardlek één keer omhoog", "Blijft hij nu omhoog? Dan zit de fout in een apparaat. Springt hij er zonder apparaten tóch uit, ga dan naar stap 4."],
            ["Steek de stekkers één voor één terug", "Wacht steeds even. Springt de aardlek eruit bij een bepaald apparaat, dan heb je de boosdoener gevonden. Gebruik dat apparaat niet meer tot het is nagekeken of vervangen."],
            ["Springt hij eruit zonder apparaten?", "Dan zit de fout in de installatie zelf: vocht in een (buiten)stopcontact of lasdoos, een beschadigde leiding of een versleten aardlekschakelaar. Blijf niet opnieuw inschakelen en bel ons. We meten per groep door waar het lek zit."],
        ],
        "gevaar": "Houd een aardlekschakelaar nooit met de hand omhoog en zet hem nooit vast met tape. Dan werkt je beveiliging niet meer en loop je risico op een schok of brand.",
        "oorzaken_titel": "De meest voorkomende boosdoeners",
        "oorzaken": [
            ["Waterkoker, oven of vaatwasser", "Verwarmingselementen gaan na jaren lekken. Klassieke oorzaak."],
            ["Wasmachine en droger", "Vooral als de aardlek uitvalt tijdens het wassen of centrifugeren."],
            ["Buitenstopcontact of tuinverlichting", "Vocht na regen. Valt de aardlek vooral uit bij nat weer? Dan is dit vaak de oorzaak."],
            ["Een oude aardlekschakelaar", "Ook een aardlekschakelaar slijt. Oude exemplaren schakelen soms onterecht af."],
        ],
        "faq": [
            ["Is het gevaarlijk als mijn aardlekschakelaar vaak uitvalt?", "De aardlek doet zijn werk: hij beschermt je. Maar het betekent wel dat er ergens stroom weglekt. Blijf niet opnieuw inschakelen als hij direct terugvalt, en laat de oorzaak vinden."],
            ["Waarom valt de aardlek uit als het regent?", "Bijna altijd door vocht in een buitenstopcontact, buitenlamp, tuinverlichting of een kabel naar de schuur. Dat lossen we op met waterdichte verbindingen en de juiste IP-klasse."],
            ["Wat kost het om een aardlekstoring te laten oplossen?", "We werken met een vast uurtarief: overdag € {uur_dag} voor het eerste uur, inclusief btw en diagnose, zonder voorrijkosten in Utrecht. In de meeste gevallen is de oorzaak binnen dat uur gevonden. Is er een onderdeel nodig, dan hoor je eerst de prijs."],
            ["Hoe vaak moet ik de testknop gebruiken?", "Druk een paar keer per jaar op de testknop (T) van elke aardlekschakelaar. Hij moet dan direct uitschakelen. Gebeurt dat niet, laat hem dan vervangen."],
        ],
        "gerelateerd": ["stroomstoring-utrecht", "kortsluiting-utrecht"],
    },
    {
        "slug": "kortsluiting-utrecht",
        "kort": "Kortsluiting / groep valt uit",
        "title": "Kortsluiting of groep valt uit? Elektricien Utrecht | INO",
        "description": "Valt een groep steeds uit of hoorde je een knal? Zo herken je overbelasting of kortsluiting. 24/7 elektricien in Utrecht, vaste prijs vooraf.",
        "h1": "Kortsluiting of valt een groep steeds uit? Zo herken je het verschil",
        "intro": "Een groep die uitvalt kan twee dingen betekenen: overbelasting (te veel apparaten tegelijk) of kortsluiting (een echte fout in een apparaat of leiding). Het verschil herken je aan wanneer en hoe hij uitvalt.",
        "stappen_titel": "Wat je nu het beste kunt doen",
        "stappen": [
            ["Valt hij uit na een tijdje, als veel aan staat?", "Dat is meestal overbelasting. Zet een paar zware apparaten uit (waterkoker, magnetron, kachel, airfryer) en zet de automaat weer omhoog. Gebeurt het vaak? Dan heb je een extra groep nodig."],
            ["Valt hij direct uit bij het inschakelen?", "Dat wijst op kortsluiting. Haal alle stekkers op die groep eruit en zet de automaat één keer omhoog."],
            ["Blijft hij omhoog zonder apparaten?", "Steek de apparaten één voor één terug. Het apparaat waarbij de groep uitvalt is defect: niet meer gebruiken."],
            ["Valt hij ook zonder apparaten uit?", "Dan zit de kortsluiting in de leiding, een stopcontact of een schakelaar. Laat de groep uit staan en bel ons. Blijven inschakelen kan schade en brandgevaar veroorzaken."],
        ],
        "gevaar": "Zie je een zwarte of gesmolten plek bij een stopcontact, ruik je brandlucht of hoorde je een knal? Laat die groep uit, gebruik het stopcontact niet meer en bel ons. Bij rook of vuur: 112.",
        "oorzaken_titel": "Typische oorzaken",
        "oorzaken": [
            ["Defect snoer of stekker", "Beschadigd, geknikt of oud snoer. Vaak zichtbaar aan verkleuring."],
            ["Losse verbinding in een stopcontact", "Een verbinding die warm wordt en uiteindelijk kortsluit."],
            ["Boren door een leiding", "Na het ophangen van een plank of schilderij: een klassieker."],
            ["Te veel op één groep", "Veel keukenapparaten of een elektrische kachel op dezelfde groep."],
        ],
        "faq": [
            ["Wat is het verschil tussen een aardlekschakelaar en een automaat?", "Een automaat (installatieautomaat) beschermt tegen overbelasting en kortsluiting. Een aardlekschakelaar beschermt tegen weglekkende stroom, zoals bij een schok. In moderne kasten zitten ze vaak gecombineerd in één aardlekautomaat."],
            ["Kan ik een extra groep laten aanleggen tegen overbelasting?", "Ja. Een extra groep bijplaatsen kan vanaf € {extra_groep}, afhankelijk van je groepenkast. Stuur een foto van je meterkast, dan krijg je een vaste prijs."],
            ["Komen jullie ook 's nachts bij kortsluiting?", "Ja, we zijn 24/7 bereikbaar. 's Nachts, op zondag en feestdagen geldt € {uur_nacht} voor het eerste uur, inclusief btw en diagnose."],
        ],
        "gerelateerd": ["aardlekschakelaar-springt-eruit", "stopcontact-werkt-niet"],
    },
    {
        "slug": "stopcontact-werkt-niet",
        "kort": "Stopcontact werkt niet of wordt warm",
        "title": "Stopcontact werkt niet of wordt warm? | INO Utrecht",
        "description": "Stopcontact doet het niet, wordt warm, verkleurt of vonkt? Check deze punten en weet wanneer het gevaarlijk is. Elektricien in Utrecht, vaste prijs vooraf.",
        "h1": "Stopcontact werkt niet, wordt warm of vonkt? Dit moet je weten",
        "intro": "Een stopcontact dat niet werkt is vaak simpel te verklaren. Een stopcontact dat warm wordt, knettert, vonkt of verkleurt is een ander verhaal: dat is een waarschuwing die je serieus moet nemen.",
        "stappen_titel": "Stopcontact doet het niet? Check eerst dit",
        "stappen": [
            ["Test het apparaat ergens anders", "Werkt het apparaat in een ander stopcontact wel? Dan zit het probleem in dit stopcontact of de groep ervan."],
            ["Kijk in de meterkast", "Staat er een automaat of aardlekschakelaar omlaag? Zet hem één keer omhoog. Springt hij er weer uit, lees dan onze pagina over aardlek of kortsluiting."],
            ["Is het een geschakeld stopcontact?", "Sommige stopcontacten gaan aan en uit met een lichtschakelaar. Probeer de schakelaars in de kamer."],
            ["Nog steeds niets?", "Dan is er vaak een verbinding losgeraakt in het stopcontact of een lasdoos. Niet zelf openmaken: bel ons, we zoeken het snel en veilig op."],
        ],
        "gevaar": "Wordt een stopcontact of stekker warm, ruik je een brandlucht, hoor je geknetter of zie je verkleuring of vonken? Stop direct met gebruiken, zet de groep uit in de meterkast en laat het nakijken. Losse verbindingen zijn een bekende oorzaak van woningbranden.",
        "oorzaken_titel": "Wat we meestal aantreffen",
        "oorzaken": [
            ["Losgeraakte draad", "Door jarenlang in- en uitsteken of een verbinding die nooit goed vastzat."],
            ["Versleten stopcontact", "Oude stopcontacten met slappe contacten waar stekkers los in zitten."],
            ["Overbelasting via stekkerdozen", "Meerdere zware apparaten op één stopcontact via een verdeelblok."],
            ["Geen randaarde", "Oude stopcontacten zonder aarde, niet geschikt voor apparaten met een geaarde stekker."],
        ],
        "faq": [
            ["Wat kost het vervangen van een stopcontact?", "Het vervangen van een bestaand stopcontact valt meestal ruim binnen het eerste uur (€ {uur_dag} overdag, incl. btw en materiaal op aanvraag). Verleggen naar een nieuwe plek kost vanaf € {stopcontact_verleggen} per punt."],
            ["Is een warm stopcontact gevaarlijk?", "Ja. Een stopcontact hoort niet warm te worden. Warmte betekent meestal een slechte verbinding of overbelasting, en dat kan brand veroorzaken. Stop met gebruiken en laat het nakijken."],
            ["Kunnen jullie oude stopcontacten vervangen door stopcontacten met randaarde?", "Vaak wel, als er een aardedraad aanwezig is of kan worden aangelegd. We bekijken het ter plaatse en geven vooraf een vaste prijs."],
        ],
        "gerelateerd": ["kortsluiting-utrecht", "stroomstoring-utrecht"],
    },
]
