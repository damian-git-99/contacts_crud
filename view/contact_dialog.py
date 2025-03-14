from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt

class ContactDialog(QDialog):
    def __init__(self, parent=None, contact=None):
        super().__init__(parent)
        
        # Dialog configuration
        self.setWindowTitle("New Contact" if contact is None else "Edit Contact")
        self.setFixedSize(400, 200)
        self.setModal(True)
        
        # Contact data (if editing)
        self.contact = contact
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Input fields
        form_layout = QVBoxLayout()
        
        # Name field
        name_layout = QVBoxLayout()
        name_label = QLabel("Name:")
        name_label.setStyleSheet("font-weight: bold;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter contact name")
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        
        if contact:
            self.name_input.setText(contact.name)
            
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        form_layout.addLayout(name_layout)
        
        # Space between fields
        form_layout.addSpacing(10)
        
        # Phone field
        phone_layout = QVBoxLayout()
        phone_label = QLabel("Phone:")
        phone_label.setStyleSheet("font-weight: bold;")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number")
        self.phone_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        
        if contact:
            self.phone_input.setText(contact.phone)
            
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_input)
        form_layout.addLayout(phone_layout)
        
        layout.addLayout(form_layout)
        
        # Space before buttons
        layout.addSpacing(20)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        # Cancel button
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #f2f2f2;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
        """)
        
        # Save button
        self.btn_save = QPushButton("Save")
        self.btn_save.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        buttons_layout.addWidget(self.btn_cancel)
        buttons_layout.addWidget(self.btn_save)
        
        layout.addLayout(buttons_layout)
        
        # Connect signals
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.accept_if_valid)
    
    def accept_if_valid(self):
        """Validate data before accepting the dialog"""
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        
        # Validate name
        if not name:
            QMessageBox.warning(self, "Validation", "Name cannot be empty.")
            self.name_input.setFocus()
            return
        
        # Validate phone
        if not phone:
            QMessageBox.warning(self, "Validation", "Phone cannot be empty.")
            self.phone_input.setFocus()
            return
        
        # Validate phone format (numbers only)
        if not phone.isdigit():
            QMessageBox.warning(self, "Validation", "Phone must contain only numbers.")
            self.phone_input.setFocus()
            return
        
        # All valid, accept
        self.accept()
    
    def get_data(self):
        """Return the entered data"""
        return {
            'name': self.name_input.text().strip(),
            'phone': self.phone_input.text().strip()
        } 