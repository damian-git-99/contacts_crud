from model.contact_model import ContactModel
from view.contact_dialog import ContactDialog

class ContactController:
    def __init__(self, view):
        self.view = view
        self.model = ContactModel()
        
        # Connect view signals with controller methods
        self.view.btn_new.clicked.connect(self.create_contact)
        self.view.btn_edit.clicked.connect(self.edit_contact)
        self.view.btn_delete.clicked.connect(self.delete_contact)
        
        # Load initial contacts (if any)
        self.refresh_contacts()
    
    def create_contact(self):
        """Creates a new contact"""
        dialog = ContactDialog(self.view)
        if dialog.exec_():
            data = dialog.get_data()
            contact_id = self.model.add_contact(data['name'], data['phone'])
            self.refresh_contacts()
            self.view.show_info(f"Contact '{data['name']}' created successfully.")
    
    def edit_contact(self):
        """Edits an existing contact"""
        contact_id = self.view.get_selected_contact_id()
        if contact_id is None:
            self.view.show_error("You must select a contact to edit.")
            return
        
        contact = self.model.get_contact(contact_id)
        if contact is None:
            self.view.show_error("The selected contact no longer exists.")
            self.refresh_contacts()
            return
        
        dialog = ContactDialog(self.view, contact)
        if dialog.exec_():
            data = dialog.get_data()
            success = self.model.update_contact(contact_id, data['name'], data['phone'])
            if success:
                self.refresh_contacts()
                self.view.show_info(f"Contact '{data['name']}' updated successfully.")
            else:
                self.view.show_error("Could not update the contact.")
    
    def delete_contact(self):
        """Deletes an existing contact"""
        contact_id = self.view.get_selected_contact_id()
        if contact_id is None:
            self.view.show_error("You must select a contact to delete.")
            return
        
        contact = self.model.get_contact(contact_id)
        if contact is None:
            self.view.show_error("The selected contact no longer exists.")
            self.refresh_contacts()
            return
        
        if self.view.confirm_delete():
            success = self.model.delete_contact(contact_id)
            if success:
                self.refresh_contacts()
                self.view.show_info(f"Contact '{contact.name}' deleted successfully.")
            else:
                self.view.show_error("Could not delete the contact.")
    
    def refresh_contacts(self):
        """Updates the contact list in the view"""
        contacts = self.model.get_all_contacts()
        self.view.show_contacts(contacts) 