import sys
from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow
from controller.contact_controller import ContactController

def main():
    """Main function to start the application"""
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Set global style
    app.setStyle("Fusion")
    
    # Create main window
    main_window = MainWindow()
    
    # Create contact controller and connect it with the view
    contact_controller = ContactController(main_window)
    
    # Show main window
    main_window.show()
    
    # Run event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 