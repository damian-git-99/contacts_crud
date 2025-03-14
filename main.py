import sys
from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow
from controller.contact_controller import ContactController

def main():
    """Función principal para iniciar la aplicación"""
    # Crear la aplicación Qt
    app = QApplication(sys.argv)
    
    # Establecer estilo global
    app.setStyle("Fusion")
    
    # Crear la ventana principal
    main_window = MainWindow()
    
    # Crear el controlador y conectarlo con la vista
    controller = ContactController(main_window)
    
    # Mostrar la ventana principal
    main_window.show()
    
    # Ejecutar el bucle de eventos
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 