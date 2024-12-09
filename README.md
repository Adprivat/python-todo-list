# Python ToDo-Liste

Eine moderne ToDo-Listen-Anwendung mit grafischer Benutzeroberfläche, entwickelt mit Python und tkinter.

## Features

- Aufgaben hinzufügen mit Titel und Priorität
- Prioritäten verwalten (Hoch, Mittel, Niedrig)
- Status-Management (Offen, In Bearbeitung, Erledigt)
- Automatische Sortierung:
  - Hochpriorisierte Aufgaben erscheinen oben
  - Erledigte Aufgaben werden ans Ende verschoben
- Kontextmenü (Rechtsklick) für schnelle Aktionen
- Persistente Speicherung in SQLite-Datenbank

## Installation

1. Klonen Sie das Repository:
```bash
git clone https://github.com/Adprivat/python-todo-list.git
cd python-todo-list
```

2. Stellen Sie sicher, dass Python 3.x installiert ist
3. Keine zusätzlichen Pakete erforderlich (tkinter ist in der Standardbibliothek enthalten)

## Verwendung

Starten Sie die Anwendung mit:
```bash
python main.py
```

### Funktionen

- **Neue Aufgabe**: Geben Sie einen Titel ein und wählen Sie eine Priorität
- **Status ändern**: Über Button oder Rechtsklick → Status ändern
- **Priorität ändern**: Über Button oder Rechtsklick → Priorität ändern
- **Aufgabe löschen**: Über Button oder Rechtsklick → Löschen

## Projektstruktur

- `main.py`: Hauptanwendungsdatei mit GUI und Datenbanklogik
- `todo.db`: SQLite-Datenbank (wird automatisch erstellt)
- `.gitignore`: Konfiguration für Git-Versionierung
- `README.md`: Projektdokumentation

## Lizenz

MIT License 