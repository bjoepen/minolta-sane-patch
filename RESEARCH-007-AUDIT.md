# BeBlog Digitizer – Research 007 – Audit

**Status:** Build und statischer Audit bestanden; Hardwaretest nicht durchgeführt

**Referenz:** `research-004-gamma-4096` / `30b0d8a69c0263c6f2a3bba63b31a3e3e1d9c931`

**Experimentcommit:** `f52f9aaa5d513f8484e17ab5ac0cd30c97bd2c6b`

**Auditdokument:** dem Branch nach dem Codebuild als reine Dokumentation hinzugefügt

## 1. Rekonstruktion des Arbeitsstands

- **CONFIRMED:** Ausgangsrepository `/Users/bernd/Minolta-Research-005-PASS/patch-source` befand sich auf `research-004-gamma-4096`, sauber und exakt auf Referenzcommit `30b0d8a`.
- **CONFIRMED:** Research-007-Branch `research-007-gamma-tail` wurde davon abgezweigt. Der Codecommit `f52f9aa` enthält Patch, Analysewerkzeug, Baselineauswertung, Tests und CI-Anpassung.
- **CONFIRMED:** GitHub Draft-PR [#2](https://github.com/bjoepen/minolta-sane-patch/pull/2) ist `research-007-gamma-tail` → `research-004-gamma-4096`; Mergezustand wurde als `CLEAN` gemeldet. Er ist nicht gegen `main` gerichtet.
- **CONFIRMED:** Der bereits bestehende Draft-PR [#1](https://github.com/bjoepen/minolta-sane-patch/pull/1) von Research 004 zielt auf `main`. Research 007 hat diesen PR und `main` nicht verändert.
- **CONFIRMED:** Der manuell gestartete CI-Lauf [38120420971](https://github.com/bjoepen/minolta-sane-patch/actions/runs/38120420971) prüfte exakt den Codecommit `f52f9aaa5d513f8484e17ab5ac0cd30c97bd2c6b` und endete mit `success`.
- **CONFIRMED:** Das CI-Artefakt `minolta-avision-macos-arm64-r7-1-tail-repeat-experimental` (Artifact ID `11695381483`, 94,564 Byte) ist nicht abgelaufen. Es enthält `libsane-avision.1.so`, alle drei Patches, Linkagebericht, Manifest und Prüfsummen.
- **CONFIRMED:** Vorhandene nicht versionierte Dateien `tests/__pycache__/` und `tools/__pycache__/` wurden vorgefunden und nicht verändert oder gelöscht.

## 2. Änderungen und Eingrenzung

Der Branch enthält gegenüber dem Referenzbranch ausschließlich Research-007-Inhalte:

- separater Patch `minolta-gamma-tail-repeat-experimental.patch`;
- RGB8-RAW/TIFF-Analysewerkzeug ohne externe Python-Abhängigkeiten;
- Unit-Tests und deterministischer Payload-Modellprüfer;
- vollständige Histogramm- und Kennwertauswertung der vorhandenen vier Research-005-RAW/TIFF-Paare;
- CI-Prüfung, ARM64-Build und klar markiertes CI-Artefakt.

**CONFIRMED:** `minolta-gamma-4096-experimental.patch` wurde bytegenau nicht geändert. Der Research-005-Build und die dortigen Scans/RAW/TIFF-Dateien blieben unangetastet. Kein Commit wurde nach `main` erstellt, kein Merge ausgeführt und keine Scannerverbindung geöffnet.

### Patchprüfung

Der R7-1-Patch ersetzt die allgemeine Endwertfüllung nur für USB `0638:026a`, ASIC C2, bei `i == 512` und `gamma_table_raw_size == 4096`. Dann werden die schon berechneten Bytes `0…511` siebenmal wiederholt, um die 4096 Byte zu füllen. Für alle anderen Geräte und Zustände bleibt die bisherige Füllschleife bestehen.

- **PASS:** Reihenfolge `minolta-film-holder-busy-v2.patch` → `minolta-gamma-4096-experimental.patch` → R7-1-Patch wurde gegen den SANE-1.4.0-Quellarchiv geprüft.
- **PASS:** `git apply --check` und tatsächliche Anwendung des R7-1-Patches waren erfolgreich.
- **PASS:** Zugriff in der Experimentierschleife bleibt auf bereits initialisierte 512 Byte begrenzt; Schreibbereich ist `512…4095`.
- **PASS:** 4096-Byte-Transferlänge und CDB-Längenfeld bleiben durch die Änderung unverändert im Gamma-4096-Patch.
- **PASS:** Die lokale Payload-Modellprüfung ergab dieselbe SHA-256 für Referenz und Experiment im Präfix `0…511`: `8d35978b98877da24dc6904f1a27aaf031f9103991d3ed868ae7dc938a6a00fd`.
- **PASS:** Der bestehende Gamma-4096-Patch behielt SHA-256 `9216c1868ef40ac5cdaec515c032bc87cdb15acdd6f97172ffa3a539ed3818c5`.

## 3. Analysewerkzeug und Ausgangsdaten

`tools/analyze_rgb.py` liest interleaved RGB8 RAW (mit passender SANE-Parameterdatei) und unkomprimiertes contiguous RGB8 TIFF. JSON-Ausgabe enthält Dateigröße, SHA-256, Dimensionen, Bittiefe, Histogramm je Kanal, Minimum, Maximum, Mittelwert, Median, Perzentile 0,1/1/99/99,9 sowie Anzahl und Anteil der Werte 0 und 255. Perzentile verwenden lineare Interpolation zwischen nullbasierten Rängen. RAW-Zeilenpadding fließt nicht als Pixel in das Histogramm ein.

Die vorhandenen vier Research-005-RAW/TIFF-Paare stimmen bei Abmessungen und Kanalhistogrammen überein. Sie sind RGB8, 564 × 850. Die R-Kanäle zeigen bereits in der Referenz starke Sättigung: 397.030 bis 444.438 Pixel mit Wert 255; Blau erreicht bei keinem Frame 255. Das ist eine gemessene Baseline unkonvertierter Negative, kein Beweis für die Gamma-Tail-Ursache.

Die Analysedateien liegen unter `analysis/research-005/`. Der Testplan und die späteren Hardwareabläufe stehen in [`RESEARCH-007-TESTANLEITUNG.md`](RESEARCH-007-TESTANLEITUNG.md).

## 4. CI-Build und Artefakt

- Run: [38120420971](https://github.com/bjoepen/minolta-sane-patch/actions/runs/38120420971)
- Status: **SUCCESS**, Laufzeit 3 min 5 s
- Runner: `macos-15`; Schritt `uname -m == arm64` bestanden
- Erfolgreiche Schritte: Werkzeugtests, ARM64-Prüfung, Abhängigkeiten, SANE-1.4.0-Download, Patchprüfung/-anwendung, Configure/Build, Binärsammlung, Linkagebericht und Artifact-Upload
- Gebauter Codecommit: `f52f9aaa5d513f8484e17ab5ac0cd30c97bd2c6b`
- Artefakt: [Download über GitHub Actions](https://github.com/bjoepen/minolta-sane-patch/actions/runs/38120420971)
- Binary: `libsane-avision.1.so`, Mach-O 64-bit bundle, ARM64
- SHA-256: `8e4617d97988855ef2ea90b8d254f52d261c3d5a23e5bb70b377ec6a5aad26e0`

Der Linkagebericht weist System `libxml2`, `libSystem`, Homebrew `libusb-1.0.0.dylib` und Apple CoreFoundation/IOKit aus. Der CI-Runner verwendete macOS 15. Das Artefakt ist nicht als kompatibel mit Homebrew SANE 1.4.0_2 auf macOS Tahoe validiert. Es wurde in `/Users/bernd/Minolta-Research-007-CI/` heruntergeladen und nur inspiziert, nicht installiert oder geladen.

## 5. Risiken und Grenzen

- **CONFIRMED:** Der CI-Build beweist Kompilierbarkeit und Patchanwendbarkeit, nicht, dass der Scanner die neue Tail-Tabelle akzeptiert oder bildwirksam auswertet.
- **UNKNOWN:** Es ist nicht bekannt, ob die Firmware alle 4096 Gammabytes als LUT nutzt oder nur einen Teil davon benötigt.
- **HYPOTHESIS:** Wiederholung der 512-Byte-Tabelle über den Tail könnte sich auf die Bildwerte auswirken, falls die Firmware alle 4096 Einträge abfragt.
- **WARN:** Die CI-Binärdatei bindet an die Homebrew-LibUSB-Pfadstruktur des GitHub-Runnerimages. Lokale Austauschbarkeit ist nicht belegt.
- **WARN:** CI-Run ist `workflow_dispatch` auf `f52f9aa`; GitHub stellt ihn daher nicht als PR-Statuscheck dar. Die GitHub-API meldete für PR #2 `statusCheckRollup: []`.
- **WARN:** Der Workflow enthält zwei identische Kommentarzeilen zur Quellarchiv-/Git-Arbeitsbaum-Situation. Das ist kosmetisch und hatte keinen Einfluss auf erfolgreichen Patchcheck oder Build.

## 6. Urteil

**Audit: PASS für isolierte, spätere Hardwaretestvorbereitung.** Der R7-1-Code verändert ausschließlich den Tail-Payload für den Minolta-FS-V1/C2-Fall und bewahrt Länge, Prefix, Kanäle und bisherigen Referenzpatch. Analysewerkzeug und Research-005-Baseline sind verfügbar. CI-Artefakt ist vorhanden und eindeutig als experimentell markiert.

**Hardwarefreigabe: NICHT ERTEILT.** Es wurden keine Scannerexperimente oder Installationen auf dem Mac vorgenommen. Vor einem realen R7-0/R7-1-Vergleich bleibt die separate Freigabe des Benutzers erforderlich. Bis dahin Draft-PR offen lassen und nicht mergen.
