import re

class ImportExportModel:
    def __init__(self, contact_model):
        """Initialize the import/export model with a reference to the contact model"""
        self.contact_model = contact_model
    
    def export_contacts_to_file(self, file_path):
        """Exports contacts to a text file and returns success status and error message"""
        contacts = self.contact_model.get_all_contacts()
        
        # Check if there are contacts to export
        if not contacts:
            return False, "There are no contacts to export."
        
        try:
            with open(file_path, 'w') as file:
                for contact in contacts:
                    file.write(f"{contact.name}, {contact.phone}\n")
            
            return True, f"Contacts successfully exported to {file_path}"
        except Exception as e:
            return False, f"Error exporting contacts: {str(e)}"
    
    def import_contacts_from_file(self, file_path):
        """Imports contacts from a text file and returns results"""
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
                            self.contact_model.add_contact(name, phone)
                            imported_count += 1
                        else:
                            invalid_lines.append(f"Line {line_number}: Missing name or phone")
                    else:
                        invalid_lines.append(f"Line {line_number}: Invalid format")
            
            # Prepare result message
            if imported_count > 0:
                message = f"Successfully imported {imported_count} contact(s)"
                if invalid_lines:
                    message += f"\n\nWarning: {len(invalid_lines)} line(s) could not be imported:"
                    # Show at most 5 invalid lines to avoid a huge message box
                    for i, error in enumerate(invalid_lines[:5]):
                        message += f"\n- {error}"
                    if len(invalid_lines) > 5:
                        message += f"\n- ... and {len(invalid_lines) - 5} more"
                
                return True, message
            else:
                if invalid_lines:
                    return False, f"No contacts were imported. {len(invalid_lines)} line(s) had invalid format."
                else:
                    return False, "No contacts were found in the file."
                    
        except Exception as e:
            return False, f"Error importing contacts: {str(e)}" 