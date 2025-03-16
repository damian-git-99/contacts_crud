# Contacts Application

A simple application to manage contacts, developed with PyQt5 following the MVC pattern.

## Features

- Create, edit and delete contacts
- View contacts in a table
- Export contacts to a text file (name, phone format)
- Import contacts from a text file (name, phone format)
- Real-time contact search by name or phone number
- Persistent storage using SQLite database
- Exit confirmation dialog

## Architecture

The application follows the Model-View-Controller (MVC) pattern:

- **Model**:
  - ContactModel: Handles data storage and retrieval using SQLite
  - ImportExportModel: Manages the logic for importing and exporting contacts
- **View**: Manages the user interface with PyQt5
- **Controller**:
  - ContactController: Manages all contact operations (create, edit, delete, import, export)

## Requirements

- Python 3.6+
- PyQt5
- SQLite (included in Python standard library)

## Installation

```
pip install -r requirements.txt
```

## Execution

```
python main.py
```

## Testing

To run the unit tests:

```
python -m pytest -v -s
```

This will run all tests with verbose output and showing print statements.

## Database

The application stores contacts in a SQLite database file (`contacts.db`) in the application directory. This ensures that your contacts are preserved between application sessions.

## License

This application is licensed under the GNU General Public License v3.0 (GPL-3.0). This is compatible with PyQt5's GPL license.
