# Team 10

Mike Benz
Artem Vlasiuk
Alexander Severin
Jan Grießer

## Name des Projekts

Projekt Drill Detect

## Projektbeschreibung

Das Projekt soll durch Messdaten einer vorherigen Bohrung erkennen durch welches Material gebohrt wurde.
Nach einem Bohrvorgang werden die aufgezeichneten Messdaten an die Anwendung übergeben, die aus Spannung, Stromverbrauch und einer Geräuschaufnahme besstehen. Die Anwendung soll danach anhand der gegebenen Daten, mit hilfe einer Sklearn Pipeline, ermitteln können durch welches Material gebohrt wurde und anschließend das Ergebnis auf einer geeigneten Oberfläche anzeigen.

## Projektstatus

Die Kernziele des Projekts sind erreicht: die Machine Learning Pipeline ist in GUI integriert und erreicht den geplannten Accuracy-Schwellwert von mehr als 80% und Bearbeitungszeit von weniger als eine Sekunde. 
Während des Klassifikationsvorgangs wird dem Benutzer eine **beeindruckende** Animation präsentiert, die den Prozess _elegant_ visualisiert.

(Durchschnitt)

Genauigkeit: **84%**

Bearbeitungszeit: **< 1 Sekunde**

## Installation und Abhängigkeiten

Zur anwendung benutzen wir Visual Studio Codes mit Python und Jupyter Notebooks. Abhängigkeiten zu den Imports sind hier in der [environment.yml](environment.yml) gespeichert.
Die Umgebung kann mit folgenden Befehl einfach selbst heruntergeladen werden um die Anwendung zu nutzen:

```
conda env create -f environment.yml
```

Wichtig hierbei ist es mit der Konsole in das richtige Verzeichnis zu wechseln und sicher zu gehen, dass es keine Umgebung mit gleichem Namen gibt. Das Verzeichnis in dass hier navigiert werden sollte, ist das "team-10" Verzeichnis.

danach steht der Kernel "drill" in den Python environments zur verfügung.

## Nutzung

1. Konsole bei ...\team-10>
2. (conda env create -f environment.yml) Installation von früher

3. conda activate drill
4. Konsole bei ...\team-10>
5. python src\DrillOG.py

6. Data Source auswählen
7. Drill Detect Application auswählen 

## Roadmap

- Genauigkeit durch Fine Tuning von Hyperparametern und Feature Selection verbessern
- Die Anwendung flexibler gestalten mit mehr Anpassungsfähigkeit für unterschiedliche Datenquellen
- Weitere Materialien integrieren
- Auf eigenes GUI-Framework umsteigen