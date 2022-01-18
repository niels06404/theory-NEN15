# Baseline

## Niet helemaal random...
Het algoritme is niet helemaal random, omdat:
- In dezelfde route kan dezelfde connectie niet meer dan één keer gemaakt worden.
  Voorbeeld: Een route van Alkmaar - Hoorn - Alkmaar is hierdoor niet mogelijk.
- In dezelfde route kan hetzelfde station niet nog een keer voorkomen.
  Voorbeeld: Een route van Amsterdam Centraal - Amsterdam Amstel - Amsterdam Zuid - Amsterdam Sloterdijk - Amsterdam Centraal is hierdoor niet mogelijk.
- De routes mogen niet langer zijn dat een bepaalde tijd, hierdoor kunnen routes niet oneindig lang worden.
- Het aantal routes is ook begrensd
- Het algoritme neemt alleen geldige oplossingen mee (alleen connecties die bestaan). Hierdoor worden ongeldige oplossingen uitgesloten.

## Voorbeeld resultaat
Route 1: Hoorn, Zaandam, Castricum, Alkmaar, Den Helder, Time: 83.0 <br />
Route 2: Schiedam Centrum, Rotterdam Centraal, Dordrecht, Time: 22.0 <br />
Route 3: Zaandam, Castricum, Alkmaar, Den Helder, Time: 57.0 <br />
Route 4: Gouda, Den Haag Centraal, Delft, Schiedam Centrum, Rotterdam Centraal, Dordrecht, Time: 60.0 <br />
Route 5: Delft, Schiedam Centrum, Rotterdam Centraal, Rotterdam Alexander, Gouda, Den Haag Centraal, Leiden Centraal, Heemstede-Aerdenhout, Haarlem, Beverwijk, Zaandam, Time: 120.0 <br />
Route 6: Amsterdam Amstel, Amsterdam Zuid, Schiphol Airport, Leiden Centraal, Alphen a/d Rijn, Gouda, Rotterdam Alexander, Rotterdam Centraal, Schiedam Centrum, Delft, Den Haag Centraal, Time: 107.0 <br />
Route 7: Rotterdam Centraal, Schiedam Centrum, Delft, Den Haag Centraal, Leiden Centraal, Alphen a/d Rijn, Gouda, Rotterdam Alexander, Time: 80.0

Unvisited connections: [('Haarlem', 'Amsterdam Sloterdijk'), ('Amsterdam Zuid', 'Amsterdam Sloterdijk'), ('Amsterdam Centraal', 'Amsterdam Sloterdijk'), ('Amsterdam Amstel', 'Amsterdam Centraal'), ('Hoorn', 'Alkmaar'), ('Beverwijk', 'Castricum'), ('Zaandam', 'Amsterdam Sloterdijk')] , Length: 7 <br />
p = 0.75 <br />
T = 7 <br />
Min = 529.0 <br />
Score: 6271.0

### Gemiddelde resultaat

### Uitleg
De score wordt berekend op basis van de volgende formule: K = p * 10000 - (T * 100 + Min). In deze formule is K de kwaliteit van de gegenereerde routes, p de fractie van de gebruikte connecties, T het aantal trajecten en Min de totale tijd van alle trajecten (in minuten).

Dit zijn de resultaten van een lijnvoering voor Holland. Er zijn enkele connecties niet gebruikt, dit is omdat er random routes worden gegenereerd, hierdoor is p dus niet gelijk aan 1.

Uitleggen of het goed of niet goed is, idee krijgen over waar je heen wilt, wat je nog wilt implementeren, 