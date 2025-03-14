from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QLabel, QFileDialog)
from PyQt5.QtCore import Qt
from view.contact_dialog import ContactDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Main window configuration
        self.setWindowTitle("Contacts Application")
        self.setGeometry(100, 100, 800, 500)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel (buttons)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Left panel title
        left_title = QLabel("Actions")
        left_title.setAlignment(Qt.AlignCenter)
        left_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 20px;")
        left_layout.addWidget(left_title)
        
        # Buttons
        self.btn_new = QPushButton("New Contact")
        self.btn_edit = QPushButton("Edit Contact")
        self.btn_delete = QPushButton("Delete Contact")
        self.btn_export = QPushButton("Export to TXT")
        
        # Button style
        button_style = """
            QPushButton {
                padding: 10px;
                font-size: 14px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """
        self.btn_new.setStyleSheet(button_style)
        self.btn_edit.setStyleSheet(button_style)
        self.btn_delete.setStyleSheet(button_style.replace("#4CAF50", "#f44336").replace("#45a049", "#d32f2f"))
        
        # Export button with blue style
        self.btn_export.setStyleSheet(button_style.replace("#4CAF50", "#2196F3").replace("#45a049", "#0b7dda"))
        
        # Add buttons to layout
        left_layout.addWidget(self.btn_new)
        left_layout.addWidget(self.btn_edit)
        left_layout.addWidget(self.btn_delete)
        left_layout.addSpacing(20)  # Add some space before the export button
        left_layout.addWidget(self.btn_export)
        left_layout.addStretch()
        
        # Right panel (table)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Right panel title
        right_title = QLabel("Contacts List")
        right_title.setAlignment(Qt.AlignCenter)
        right_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 20px;")
        right_layout.addWidget(right_title)
        
        # Contacts table
        self.table = QTableWidget(0, 3)  # 0 rows initially, 3 columns (ID, Name, Phone)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Phone"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Table style
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dddddd;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #f2f2f2;
                padding: 5px;
                border: 1px solid #dddddd;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #e0f7fa;
            }
        """)
        
        right_layout.addWidget(self.table)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 3)
        
        # Initially, disable edit and delete buttons
        self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)
        
        # Connect table selection with button enabling
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
    
    def on_selection_changed(self):
        """Enable or disable buttons based on table selection"""
        has_selection = len(self.table.selectedItems()) > 0
        self.btn_edit.setEnabled(has_selection)
        self.btn_delete.setEnabled(has_selection)
    
    def get_selected_contact_id(self):
        """Get the ID of the selected contact"""
        if len(self.table.selectedItems()) > 0:
            row = self.table.selectedItems()[0].row()
            id_item = self.table.item(row, 0)
            return int(id_item.text())
        return None
    
    def show_contacts(self, contacts):
        """Show contacts in the table"""
        self.table.setRowCount(0)
        for contact in contacts:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(contact.contact_id)))
            self.table.setItem(row, 1, QTableWidgetItem(contact.name))
            self.table.setItem(row, 2, QTableWidgetItem(contact.phone))
    
    def show_error(self, message):
        """Show an error message"""
        QMessageBox.critical(self, "Error", message)
    
    def show_info(self, message):
        """Show an informative message"""
        QMessageBox.information(self, "Information", message)
    
    def confirm_delete(self):
        """Request confirmation to delete a contact"""
        reply = QMessageBox.question(
            self, 
            "Confirm deletion",
            "Are you sure you want to delete this contact?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes
    
    def export_contacts_dialog(self):
        """Open a dialog to export contacts to a text file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Contacts",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            return file_path
        return None 