## Ziel des Projektes:

Ein Anwendung zu erstellen welche erkennen kann in welches Material gebohren wurde
Es soll eine benutzeröberfläche geben die Anzeigt welches der Materialen vorhergesagt und
zusätzlich einen Graphen anzeigt der die Daten visualisiert.
Der Bohrvorgang soll automatisch erkannt werden und nach beenden des Vorgangs automatisch die Vorhesage angezeigt werden.
Der Benutzer muss so nach dem Starten des Programms nichts Manuell eingeben.

-   Daten:
    3 Zeitreihen Daten von `audio`, `voltage`, `current`, welche zur vorhersage benutzt werden

-   Anforderungen:
    Der Benutzer braucht eine einfache Beutzeroberfläche welche schnell reagiert
    und zuversichtliche Ergebnisse liefert.
    **Was muss das Programm somit erfüllen:**
    .1 Schnelle fast Echzeitge Reaktion des Modells (< 1 Sekunde)
    .2 Eine Accuracy von mehr als 70%
    .3 Benutzerfreundliche GUI

## Analysefrage:

Mithilfe eines Maschine Learning Modells vorhersagen zu können, in welches Material,
aus einer Auswahl an zuvor festgelegten Materialenmenge, gebohrt wurde.

## MVP

-   Erkennen von zwei verschiedene Materialien.
-   Verwendung eines ML-Klassifikators zur Bestimmung
    -   Genauigkeit auf den Testdaten > 50%
    -   Besser als der Durchschnitt
-   Integration in MLDOG Framework
    -   Reagiert automatisch auf einen neuen
        Bohrvorgang
    -   Gibt das vorhergesagten Materials auf der GUI als Text aus.
-   Reaktionszeit des Systems unter 5 Sekunde

##### Was muss erledigt sein um einen MVP fertigzustellen:

-   Daten aufnehmen
-   Daten anaylsieren
-   Datenvorverarbeitung
-   Feature Extraction / Selection
-   Modellauswahl
-   Modelltraining
-   Modellevaluierung
-   Parameter Tuning
-   GUI grundstruktur bauen
-   Anbindung vom Modell an das GUI

## Team Organisation

Immer Freitags ein Meeting um den Aktuellen Stand zu besprechen.
Issues für neue Aufgabenpaketen erstellen.
Bei bearbeitung eines Issues immer sich selbst zuweißen damit jeder weiß wer gerade was bearbeitet.
Beim schließen von Issues immer eine Beschreibung angeben was genau getan wurde.
Kommunnikation inherhalb der Woche per Textnachrichten.
Wichtige programmänderungen vor dem Mergen von min. 1 Person überblicken lassen.

Milestone

Datenanylse
Modell
Gui
KOmmunkation
MVP
