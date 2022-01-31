# RailNL

Deze case gaat over het bepalen van de lijnvoering van intercitytreinen in Nederland. Met lijnvoering wordt de trajecten waarover de treinen gedurende de dag heen en weer rijden bedoelt. Een traject bestaat uit minstens twee stations die verbonden zijn door minstens één connectie. In de afbeelding hieronder zijn de stations weergegeven als rode stippen en de mogelijke connecties tussen stations als zwarte stippellijnen.

*plaatje*

Er zijn een aantal restricties bij deze case: in Holland mogen er maximaal 7 trajecten worden gemaakt en mag de tijd in één traject maximaal 120 minuten zijn. Voor Nationaal is het maximum 20 trajecten en maximaal 180 minuten per traject.

RailNL heeft een doelfunctie opgesteld om de kwaliteit van de lijnvoering te bepalen. Het doel is dat de kwaliteit van de lijnvoering zo hoog mogelijk is en dat deze doelfunctie dus wordt gemaximaliseerd.

*plaatje*Doelfunctie: K = p*10000 - (T*100 + Min)

Hierin is p de fractie van de gebruikte connecties (aantal gebruikte connecties / totaal aantal connecties) , T het aantal trajecten en Min het aantal minuten in alle trajecten samen. Je kunt zeggen dat het belangrijk is om alle verbindingen te gebruiken, omdat dan het groene gedeelte van de functie een hoge waarde geeft, je kunt ook zeggen dat het juist belangrijk is om zo weinig mogelijk trajecten te hebben of een zo kort mogelijk totale tijd, zodat het blauwe gedeelte van de functie laag wordt. Er zijn veel mogelijke connecties en daarmee ook veel verschillende trajecten die gemaakt kunnen worden, waardoor de state space erg groot is.

# Algoritmen

## Random
Random is een algoritme wat redelijk random een oplossing genereerd door eerst random een startstation te kiezen en daarna random een vervolgstation te kiezen. Dit algoritme is niet helemaal random, omdat het alleen geldige oplossingen genereerd en omdat er in dezelfde route een station en connectie niet meer dan één keer mogen voorkomen.

NewRandom werkt over het algemeen hetzelfde als Random en is dus ook niet helemaal random. Bij NewRandom is er toegevoegd dat het startstation wordt gekozen op basis van minst aantal connecties.

## AdaptedGreedy
AdaptedGreedy is een variatie op Greedy. Hier is voor gekozen, omdat op deze manier de stations met de minst aantal verbindingen als eerste kunnen worden toegevoegd aan een route. We hebben verschillende soorten variaties van het Greedy algoritme geprobeerd. AdaptedGreedy start bij de stations met de minste connecties, waarna alle stations in de route geen optie meer zijn voor de volgende startstations van een route. Als er geen stations meer over zijn om mee te starten wordt er gekeken naar de nog niet gepasseerde connecties en wordt random een van die twee stations als startstation van de route gekozen. Wanneer er connecties gemaakt worden binnen een traject wordt er gekeken naar het aantal mogelijkeheden in vervolgconnecties en hoe vaak een connectie al is gepasseerd en wordt de connectie met de minste mogelijkheden en minst gepasseerde connectie als volgende verbinding van het traject gekozen. Een traject is af wanneer de tijd bijna gelijk is aan de gegeven maximale tijd. Dit gaat door tot het maximale aantal trajecten is bereikt of wanneer alle connecties gepasseerd zijn.

Voordat we tot AdaptedGreedy zijn gekomen zijn daar veel stappen en andere varianten van dit algoritme aan vooraf gegaan. De overeenkomst tussen deze algoritmes is dat zij allemaal het startstation op dezelfde manier bepalen. Het verschil in deze algoritmes is dat zij allemaal op een net even andere manier een vervolgconnectie kiezen. Zo wordt bij Greedy de connectie gekozen met het minst aantal vervolgconnecties, omdat deze connectie moeilijk is om aan een route toe te voegen. Bij ReverseGreedy is dit precies omgedraaid: de connectie met het meest aantal vervolgconnecties wordt gekozen, omdat dit zorgt voor veel mogelijkheden voor de vervolgroute. Bij het RandomGreedy algoritme wordt er random een connectie gekozen. Uiteindelijk heeft AdaptedGreedy tot de beste resultaten geleid en hebben we voor dit algoritme gekozen.

## HillClimber
Er is voor een HillClimber algoritme gekozen, omdat dit een iteratief algoritme is en dus significant anders dan ons eerste algoritme. Aan de HillClimber wordt een geldige oplossing meegegeven. Dit kan een oplossing zijn geproduceerd door het Random algoritme, of AdaptedGreedy algoritme. Als er geen geldige oplossing wordt meegegeven, krijgt de gebruiker een foutmelding.

Als eerste stap wordt er een random route gekozen en bij deze route wordt er gekeken of de score verbeterd als het laatste station wordt verwijderd. Als de score verbeterd, dan wordt dit station met bijbehorende connectie verwijderd in deze route. Als de score niet verbeterd, wordt 
de route teruggezet naar hoe deze eerst was en kan deze route niet meer opnieuw worden gekozen. Er wordt steeds random een nieuwe route gekozen, totdat er geen routes meer over zijn. Een route die een verbetering geeft bij het verwijderen van het laatste station, zal dus altijd nog een keer gekozen worden.

In de tweede stap wordt er steeds random een route gekozen en wordt er gekeken of het verwijderen van die route een betere score geeft, als dit zo is dan wordt de route verwijderd, als dit niet zo is dan blijft de route gewoon staan. Als een route gekozen is, kan deze niet opnieuw gekozen worden. Dit blijft doorgaan totdat alle routes afgegaan zijn.

Als derde wordt er gekeken of twee verschillende routes samengevoegd kunnen worden. Als dit mogelijk is, dan wordt dit gedaan als hierdoor de score verbeterd en als de maximale route tijd niet wordt overschreven.

Als laatste stap wordt er gekeken of de nog ongebruikte connecties (als die er zijn), aan het einde van een route kunnen worden toegevoegd. Alle ongebruikte connecties worden afgegaan en per ongebruikte connectie worden alle routes afgegaan om te kijken of deze connectie aan een route kan worden toegevoegd. Als het mogelijk is om de connectie aan de route toe te voegen dan wordt dit gedaan als de score daardoor verbeterd, de maximale route tijd niet wordt overschreven en het station nog niet eerder in de route is voorgekomen.

# Resultaten

Regel code waarmee je dit resultaat kan krijgen

*plaatje waarin de verdeling van de algoritmen te zien zijn*

tekst met uitleg, vergelijkingen maken


Regel code waarmee je dit resultaat kan krijgen

*plaatje waarin de verdeling van de algoritmen te zien zijn nadat hier de hillclimber op is uitgevoerd*

tekst met uitleg, vergelijkingen maken


Regel code waarmee je dit resultaat kan krijgen

*plaatje waarin per algoritme twee staafdiagrammen te zien zijn met hoogste score en gemiddelde score na ... runs*

tekst met uitleg, vergelijkingen maken
