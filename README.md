# Contacts Application

A simple application to manage contacts, developed with PyQt5 following the MVC pattern.

## Features

- Create, edit and delete contacts
- View contacts in a table
- Export contacts to a text file (name, phone format)
- Import contacts from a text file (name, phone format)
- Persistent storage using SQLite database

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

## Database

The application stores contacts in a SQLite database file (`contacts.db`) in the application directory. This ensures that your contacts are preserved between application sessions.
