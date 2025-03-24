import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QFont, QPixmap, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt

class DropLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setText("Drop Image Here")
        self.setFont(QFont("Arial", 25))
        self.setStyleSheet("border: 2px dashed #aaa; padding: 20px;")
        self.setAcceptDrops(True)
        self.parent_window = parent

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("border: 2px dashed #3498db; padding: 20px;")
    
    def dragLeaveEvent(self, event):
        self.setStyleSheet("border: 2px dashed #aaa; padding: 20px;")
    
    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = urls[0].toLocalFile()
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    self.parent_window.load_image(file_path)
                    event.acceptProposedAction()
        
        self.setStyleSheet("border: 2px dashed #aaa; padding: 20px; background-color: #f0f0f0;")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fotoshob")
        self.setGeometry(500, 300, 700, 600)
        
        # Create the drop zone
        self.drop_label = DropLabel(self)
        self.drop_label.setGeometry(25, 25, 650, 500)
        
        # Create open button
        self.button_open = QPushButton("Open", self)
        self.button_open.setGeometry(595, 558, 100, 35)
        self.button_open.setStyleSheet("font-size: 20px;")
        self.button_open.clicked.connect(self.open_file_dialog)

        # Create the continue button
        self.button_Proceed = QPushButton("Proceed", self)
        self.button_Proceed.setGeometry(5, 558, 100, 35)
        self.button_Proceed.setStyleSheet("font-size: 20px;")
        self.button_Proceed.clicked.connect(self.open_EditWindow)
        self.button_Proceed.hide()
        # Current loaded image path
        self.current_image_path = None

        self.EditWindow = EditWindow(self)
    def open_EditWindow(self):
       if self.current_image_path:
        self.EditWindow.load_image_from_main(self.current_image_path)
        self.hide()
        self.EditWindow.show()
    
    def applicationSupportsSecureRestorableState(self):
        return True
    
    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open Image File", 
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)",
            options=options
        )
        
        if file_path:
            self.load_image(file_path)
            self.button_Proceed.show()
    
    def load_image(self, file_path):
        self.current_image_path = file_path
        
        # Load and display the image
        pixmap = QPixmap(file_path)
        
        # Scale the pixmap to fit the label while maintaining aspect ratio
        pixmap = pixmap.scaled(
            self.drop_label.width(), 
            self.drop_label.height(),
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        
        self.drop_label.setPixmap(pixmap)
        self.button_Proceed.show()
        # Add editing features here later
        print(f"Loaded image: {file_path}")



class EditWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("U can only crop")
        self.setGeometry(500, 300, 700, 600)
        
         # Create a label to display the image
        self.image_preview = QLabel(self)
        self.image_preview.setGeometry(25, 25, 650, 500)
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setStyleSheet("border: 1px solid #aaa; background-color: #f0f0f0;")
        
        # Create back button
        self.back_button = QPushButton("Back", self)
        self.back_button.setGeometry(5, 558, 100, 35)
        self.back_button.setStyleSheet("font-size: 20px;")
        self.back_button.clicked.connect(self.go_back)

    def go_back(self):
        self.hide()
        if self.parent:
            self.parent.show()

        # load the img
    def load_image_from_main(self, image_path):
        if image_path:
            # Load and display the image
            pixmap = QPixmap(image_path)
            
            # Scale the pixmap to fit the label while maintaining aspect ratio
            pixmap = pixmap.scaled(
                self.image_preview.width(), 
                self.image_preview.height(),
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            
            self.image_preview.setPixmap(pixmap)
            self.current_image_path = image_path
        # crop

        # Add overlay

        # Brightness

        # filters

        # histogram


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window = EditWindow

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()