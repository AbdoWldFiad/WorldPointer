from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsEllipseItem, QPushButton, QColorDialog, QDockWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QColor, QPainter, QIcon
from PyQt5.QtCore import QRectF, Qt
import sys

class MapViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Map Viewer")
        self.setGeometry(100, 100, 1200, 800)  # Set initial window size

        # Initialize the color
        self.marker_color = QColor('red')

        # Load the image
        self.pixmap = QPixmap('map.jpg')

        # Create a QGraphicsScene and add the map image
        self.scene = QGraphicsScene()
        self.pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.pixmap_item)

        # Set up the QGraphicsView to display the scene
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)

        # Set up the central widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Create a sliding sidebar (dock widget) for color picker
        self.dock_widget = QDockWidget("Controls", self)
        self.dock_widget.setFloating(False)
        self.dock_widget.setVisible(False)  # Initially hidden
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

        # Create a sidebar widget
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout()
        self.color_button = QPushButton('Choose Marker Color')
        self.color_button.clicked.connect(self.choose_color)
        sidebar_layout.addWidget(self.color_button)

        # Add future buttons here if needed
        self.future_button = QPushButton('Future Button')
        sidebar_layout.addWidget(self.future_button)
        
        sidebar_widget.setLayout(sidebar_layout)
        self.dock_widget.setWidget(sidebar_widget)

        # Create a top-right widget for the toggle button
        top_right_widget = QWidget()
        top_right_layout = QHBoxLayout()
        top_right_layout.setContentsMargins(0, 0, 0, 0)  # No margins
        top_right_layout.setSpacing(0)  # No spacing
        self.toggle_button = QPushButton(QIcon(QPixmap('hamburger_icon.png')), '', self)
        self.toggle_button.setFixedSize(30, 30)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        top_right_layout.addWidget(self.toggle_button)
        top_right_widget.setLayout(top_right_layout)
        
        # Add top-right widget to the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(top_right_widget)
        main_layout.addWidget(self.view)
        central_widget.setLayout(main_layout)

        # Connect zoom functionality
        self.view.wheelEvent = self.zoom

        # Connect right-click event
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.add_marker)

        # Connect dragging (panning) functionality
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scale_factor = 1.0

    def choose_color(self):
        # Open the color picker dialog and set the selected color
        color = QColorDialog.getColor()
        if color.isValid():
            self.marker_color = color

    def toggle_sidebar(self):
        if self.dock_widget.isVisible():
            self.dock_widget.setVisible(False)
        else:
            self.dock_widget.setVisible(True)

    def zoom(self, event):
        # Zoom factor
        factor = 1.2
        if event.angleDelta().y() < 0:
            factor = 1 / factor

        # Calculate the new scale factor
        self.scale_factor *= factor

        # Get the window size
        window_size = self.view.size()
        image_size = self.pixmap.size()

        # Calculate the maximum zoom-out factor
        max_zoom_out_factor = min(window_size.width() / image_size.width(), window_size.height() / image_size.height())
        if self.scale_factor < max_zoom_out_factor:
            self.scale_factor = max_zoom_out_factor

        # Apply zoom transformation
        self.view.resetTransform()
        self.view.scale(self.scale_factor, self.scale_factor)

    def add_marker(self, position):
        # Convert the position to scene coordinates
        scene_pos = self.view.mapToScene(position)
        
        # Create a marker with the chosen color
        marker = QGraphicsEllipseItem(QRectF(scene_pos.x() - 5, scene_pos.y() - 5, 10, 10))
        marker.setBrush(self.marker_color)
        self.scene.addItem(marker)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MapViewer()
    viewer.show()
    sys.exit(app.exec_())
