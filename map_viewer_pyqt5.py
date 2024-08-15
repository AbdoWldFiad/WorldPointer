from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
import sys

class MapViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Map Viewer")
        
        # Load the image
        pixmap = QPixmap('map.jpg')
        
        # Create a QLabel to display the image
        label = QLabel()
        label.setPixmap(pixmap)
        
        # Set up the main layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        
        container = QWidget()
        container.setLayout(layout)
        
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MapViewer()
    viewer.show()
    sys.exit(app.exec_())
