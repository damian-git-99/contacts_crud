import sqlite3


class Contact:
    def __init__(self, name="", phone="", contact_id=None):
        self.name = name
        self.phone = phone
        self.contact_id = contact_id


class ContactModel:
    def __init__(self, db_path="contacts.db"):
        """Initialize the contact model with SQLite database"""
        self.db_path = db_path
        self._create_table()

    def _get_connection(self):
        """Get a connection to the SQLite database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        return conn

    def _create_table(self):
        """Create the contacts table if it doesn't exist"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Create contacts table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        """
        )

        conn.commit()
        conn.close()

    def add_contact(self, name, phone):
        """Adds a new contact and returns its ID"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone)
        )

        # Get the ID of the inserted contact
        contact_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return contact_id

    def update_contact(self, contact_id, name, phone):
        """Updates an existing contact"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE contacts SET name = ?, phone = ? WHERE id = ?",
            (name, phone, contact_id),
        )

        # Check if any row was affected
        success = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return success

    def delete_contact(self, contact_id):
        """Deletes a contact by its ID"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))

        # Check if any row was affected
        success = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return success

    def get_contact(self, contact_id):
        """Gets a contact by its ID"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, phone FROM contacts WHERE id = ?", (contact_id,)
        )
        row = cursor.fetchone()

        conn.close()

        if row:
            return Contact(row["name"], row["phone"], row["id"])
        return None

    def get_all_contacts(self):
        """Returns all contacts"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, phone FROM contacts ORDER BY name")
        rows = cursor.fetchall()

        conn.close()

        # Convert rows to Contact objects
        contacts = []
        for row in rows:
            contacts.append(Contact(row["name"], row["phone"], row["id"]))

        return contacts

    def filter_contacts(self, search_text):
        """Returns contacts that match the search text in name or phone"""
        conn = self._get_connection()
        cursor = conn.cursor()

        query = """
            SELECT id, name, phone 
            FROM contacts 
            WHERE LOWER(name) LIKE ? OR LOWER(phone) LIKE ?
            ORDER BY name
        """
        search_pattern = f"%{search_text}%"
        cursor.execute(query, (search_pattern, search_pattern))
        rows = cursor.fetchall()

        conn.close()

        # Convert rows to Contact objects
        contacts = []
        for row in rows:
            contacts.append(Contact(row["name"], row["phone"], row["id"]))

        return contacts
