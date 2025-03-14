class Contact:
    def __init__(self, name="", phone="", contact_id=None):
        self.name = name
        self.phone = phone
        self.contact_id = contact_id

class ContactModel:
    def __init__(self):
        self.contacts = []
        self.next_id = 1
        
    def add_contact(self, name, phone):
        """Adds a new contact and returns its ID"""
        contact = Contact(name, phone, self.next_id)
        self.contacts.append(contact)
        self.next_id += 1
        return contact.contact_id
        
    def update_contact(self, contact_id, name, phone):
        """Updates an existing contact"""
        for contact in self.contacts:
            if contact.contact_id == contact_id:
                contact.name = name
                contact.phone = phone
                return True
        return False
        
    def delete_contact(self, contact_id):
        """Deletes a contact by its ID"""
        for i, contact in enumerate(self.contacts):
            if contact.contact_id == contact_id:
                del self.contacts[i]
                return True
        return False
        
    def get_contact(self, contact_id):
        """Gets a contact by its ID"""
        for contact in self.contacts:
            if contact.contact_id == contact_id:
                return contact
        return None
        
    def get_all_contacts(self):
        """Returns all contacts"""
        return self.contacts 