# BeBlog Digitizer – Research 007 – Testanleitung

## Ziel und Grenze

R7-1 vergleicht die bestehende 4096-Byte-Referenz mit einem Payload, dessen Bytes 512–4095 sieben weitere Kopien der unveränderten Bytes 0–511 enthalten. Es soll nur geprüft werden, ob der Tail die RAW-Tonwerte beeinflusst.

Diese Anleitung bereitet den Hardwarevergleich vor. Sie führt keinen Scannerzugriff aus und installiert das CI-Artefakt nicht. Der Hardwaretest beginnt erst nach separater ausdrücklicher Freigabe.

## Unveränderte Bedingungen

Für beide Varianten muss dasselbe Negativ und dieselbe Position verwendet werden. Konstant halten:

- USB-Gerät und Verbindung, Filmhalter und Einzelbild;
- Color, 600 dpi, 8 Bit;
- Exposure 100, Brightness 0, Contrast 0;
- Gamma 2,22 und dieselben initialen RGB-Kurven;
- drei getrennte RGB-Gamma-Uploads zu je 4096 Byte;
- dieselbe SANE-Sitzungs-/Prozessfolge wie Research 005;
- mindestens 30 Sekunden Abstand zwischen beendeten Scanprozessen;
- dieselbe Scanfläche, Backendkonfiguration, SANE-Version und Debugstufe.

Keine Negativinversion oder Farbkorrektur vor der RAW-Auswertung anwenden. Keine weiteren Gamma-, Exposure-, Kalibrierungs-, Auflösungs- oder Sitzungsänderungen in denselben Vergleich aufnehmen.

## R7-0 – Referenz

1. Zuerst den unveränderten Research-005-Backendstand verwenden.
2. Dasselbe Negativ mit exakt denselben Parametern scannen.
3. Nach EOF mindestens 30 Sekunden warten.
4. Ziel sind drei erfolgreiche Wiederholungen. Nach einem Fehler nicht automatisch erneut starten; Logs sichern und Ursache beurteilen.
5. Pro Wiederholung RAW, Parameterdatei, TIFF und vollständiges Backend-/Clientlog mit eindeutiger Kennung sichern.

## R7-1 – Wiederholtes Gamma-Tail

1. Erst nach erfolgreichem R7-0 und separater Freigabe auf das experimentelle R7-1-Backend umschalten.
2. Vor Start Hash, `EXPERIMENT.txt`, Patchversion und Gerätekennung prüfen. Erwartete Konfiguration: Busy-Patch + Gamma-4096-Patch + R7-1-Tail-Patch.
3. Dasselbe Negativ und dieselben Parameter verwenden.
4. Scan genau einmal starten. Bei USB-Fehler, `sane_start()`-Fehler, Hänger oder unerwarteter Mechanikbewegung abbrechen; keinen Retry ausführen. Logs und Status erhalten und den Referenzstand wiederherstellen, bevor weitere Tests erwogen werden.
5. Nach EOF mindestens 30 Sekunden warten. Ziel sind drei erfolgreiche Wiederholungen, jeweils mit neuem Dateipräfix.

Der CI-Build allein legitimiert keinen Austausch der Homebrew-Bibliothek. Vor dem Hardwaretermin muss ein kontrolliertes, rücksetzbares Backend-Lademodell festgelegt werden. Das heruntergeladene Artefakt ist nicht installiert und im Audit nicht als kompatibler Drop-in-Ersatz für Tahoe/Homebrew SANE bestätigt.

## Analyse und Vergleich

Für jede RAW-Datei die dazugehörige `.params.txt` auswerten:

```sh
python3 tools/analyze_rgb.py r7-0-run1.raw \
  --params r7-0-run1.params.txt \
  --output r7-0-run1.stats.json

python3 tools/analyze_rgb.py r7-1-run1.raw \
  --params r7-1-run1.params.txt \
  --output r7-1-run1.stats.json
```

Optional das zugehörige TIFF unabhängig gegenprüfen:

```sh
python3 tools/analyze_rgb.py r7-0-run1.tiff --output r7-0-run1-tiff.stats.json
python3 tools/analyze_rgb.py r7-1-run1.tiff --output r7-1-run1-tiff.stats.json
```

Vor dem Bildvergleich prüfen, dass Dimensionen, Bittiefe, Pixelzahl und RAW-Bytezahl übereinstimmen und die Backendlogs je Variante drei erfolgreiche 4096-Byte-Gammaübertragungen zeigen. Anschließend je Kanal Histogramme und Minimum, Maximum, Mittelwert, Median, Perzentile 0,1/1/99/99,9 sowie 0-/255-Anteile vergleichen. Alle Prozentile werden nach derselben linearen Ranginterpolation berechnet.

## Entscheidungskriterien

- Reproduzierbare Histogrammunterschiede bei erfolgreichen, geometrisch identischen Scans: Tail ist bildwirksam.
- Keine messbaren Unterschiede: Tail könnte wirkungslos sein; daraus folgt kein Beweis, dass die Firmware alle Tailbytes ignoriert.
- USB-Fehler, Scanblockade oder fehlerhafte Bilddaten: R7-1 abbrechen, Referenz wiederherstellen, keine automatischen Wiederholungen.
- Keine Übernahme nach `main` oder in den stabilen Backendstand ohne Folgeaudit und ausdrückliche Freigabe.

## Rücksetzung

Vor einem später genehmigten Test müssen Originalbackend und Prüfsumme verfügbar sein und ein dokumentierter Rückweg bereitliegen. Bei Fehler oder Testende den experimentellen Backendpfad verlassen und den zuvor gesicherten Research-005-Referenzstand wieder aktivieren; anschließend dessen Prüfsumme verifizieren. Die konkreten Austauschschritte hängen vom erst noch festzulegenden isolierten Loader-/Backendpfad ab und werden deshalb hier nicht als Installationsbefehle für das laufende Homebrew-System angegeben.
