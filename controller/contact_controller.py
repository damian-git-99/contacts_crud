from model.contact_model import ContactModel
from view.contact_dialog import ContactDialog
import re

class ContactController:
    def __init__(self, view):
        self.view = view
        self.model = ContactModel()
        
        # Connect view signals with controller methods
        self.view.btn_new.clicked.connect(self.create_contact)
        self.view.btn_edit.clicked.connect(self.edit_contact)
        self.view.btn_delete.clicked.connect(self.delete_contact)
        self.view.btn_export.clicked.connect(self.export_contacts)
        self.view.btn_import.clicked.connect(self.import_contacts)
        
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
    
    def export_contacts(self):
        """Exports contacts to a text file"""
        contacts = self.model.get_all_contacts()
        
        # Check if there are contacts to export
        if not contacts:
            self.view.show_error("There are no contacts to export.")
            return
        
        # Get file path from dialog
        file_path = self.view.export_contacts_dialog()
        if not file_path:
            return  # User cancelled the dialog
        
        try:
            with open(file_path, 'w') as file:
                for contact in contacts:
                    file.write(f"{contact.name}, {contact.phone}\n")
            
            self.view.show_info(f"Contacts successfully exported to {file_path}")
        except Exception as e:
            self.view.show_error(f"Error exporting contacts: {str(e)}")
    
    def import_contacts(self):
        """Imports contacts from a text file"""
        # Get file path from dialog
        file_path = self.view.import_contacts_dialog()
        if not file_path:
            return  # User cancelled the dialog
        
        try:
            imported_count = 0
            invalid_lines = []
            
            with open(file_path, 'r') as file:
                for line_number, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    
                    # Parse line with format "name, phone"
                    match = re.match(r'^(.+?),\s*(\d+)$', line)
                    if match:
                        name = match.group(1).strip()
                        phone = match.group(2).strip()
                        
                        if name and phone:
                            self.model.add_contact(name, phone)
                            imported_count += 1
                        else:
                            invalid_lines.append(f"Line {line_number}: Missing name or phone")
                    else:
                        invalid_lines.append(f"Line {line_number}: Invalid format")
            
            # Refresh the contacts list
            self.refresh_contacts()
            
            # Show results
            if imported_count > 0:
                message = f"Successfully imported {imported_count} contact(s)"
                if invalid_lines:
                    message += f"\n\nWarning: {len(invalid_lines)} line(s) could not be imported:"
                    # Show at most 5 invalid lines to avoid a huge message box
                    for i, error in enumerate(invalid_lines[:5]):
                        message += f"\n- {error}"
                    if len(invalid_lines) > 5:
                        message += f"\n- ... and {len(invalid_lines) - 5} more"
                
                self.view.show_info(message)
            else:
                if invalid_lines:
                    self.view.show_error(f"No contacts were imported. {len(invalid_lines)} line(s) had invalid format.")
                else:
                    self.view.show_error("No contacts were found in the file.")
                    
        except Exception as e:
            self.view.show_error(f"Error importing contacts: {str(e)}")
    
    def refresh_contacts(self):
        """Updates the contact list in the view"""
        contacts = self.model.get_all_contacts()
        self.view.show_contacts(contacts) 