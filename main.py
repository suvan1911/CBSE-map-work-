import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.MAPITEMS= {'Salal': (214, 117), 'Bhakra Nangal': (246, 158), 'Tehri': (292, 206), 'Rana Pratap Sagar': (223, 338), 'Sardar Sarovar': (164, 438), 'Hirakud': (417, 444), 'Nagarjuna Sagar': (302, 576), 'Tungabhadra': (235, 588), 'Namrup': (701, 263), 'Singrauli': (382, 364), 'Ramagundam': (313, 506), 'Narora': (296, 256), 'Kakrapara': (161, 441), 'Tarapur': (156, 485), 'Kalpakkam': (328, 667), 'Noida': (272, 241), 'Gandhinagar': (134, 380), 'Mumbai': (160, 501), 'Pune': (175, 510), 'Hyderabad': (291, 550), 'Bengaluru': (261, 671), 'Chennai': (333, 663), 'Thiruvananthapuram': (248, 779), 'Kandla': (80, 389), 'Marmagao': (180, 603), 'New Mangalore': (206, 668), 'Kochi': (238, 750), 'Tuticorin': (274, 776), 'Vishakhapatnam': (413, 534), 'Paradip': (490, 463), 'Haldia': (520, 421), 'Amritsar(Raja Sansi - Sri Gurum Dass jee)': (218, 153), 'Delhi(Indira Gandhi)': (259, 242), 'Mumbai(Chhatrapati Shivaji)': (159, 495), 'Chennai(Meenam Bakkam)': (329, 666), 'Kolkata(Netaji Subhash Chandra Bose)': (529, 401), 'Hyderabad(Rajiv Gandhi)': (295, 549)}
        for place, pos in self.MAPITEMS.items():
            self.MAPITEMS[place] = (pos[0]-40,pos[1]-5)

        # Create the graphics view and scene
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        # Set the view's background color
        self.view.setBackgroundBrush(QColor(240, 240, 240))

        # Load the image from a file and add it to the scene
        pixmap = QPixmap("map.jpg")
        self.scene.addPixmap(pixmap)

        # Connect the mouse press event to a slot
        self.view.mousePressEvent = self.on_mouse_press

        # Create a label for the heading
        self.heading_label = QLabel(self)
        font = QFont()
        font.setPointSize(24)
        self.heading_label.setFont(font)
        self.heading_label.setAlignment(Qt.AlignCenter)

        # Create the submit button and disable it
        self.submit_button = QPushButton("Submit")
        self.submit_button.setEnabled(False)
        self.submit_button.clicked.connect(self.on_submit_button_clicked)

        # Create the layout and add the widgets
        layout = QVBoxLayout()
        layout.addWidget(self.heading_label)
        layout.addWidget(self.view)
        layout.addWidget(self.submit_button)

        # Create a container widget and set the layout
        container = QWidget()
        container.setLayout(layout)

        # Set the container widget as the main widget
        self.setCentralWidget(container)

        # Set the window size to match the image size
        self.resize(pixmap.width()+100, pixmap.height()+100)
        # Set the current circle item to None
        self.selected_circle = None
        self.newQ()

    def on_mouse_press(self, event):

        # Get the position of the mouse click
        pos = event.pos()
        scene_pos = self.view.mapToScene(pos)
        # Check if the mouse click was inside the image bounds
        image_bounds = self.scene.sceneRect()
        if not image_bounds.contains(scene_pos):
            return

        # Convert the position to a scene coordinate
        # Create a red brush and pen to draw the point
        brush = QBrush(QColor(255, 0, 0))
        pen = QPen(brush, 3)

        # Create a larger circle to represent the point
        new_circle = self.scene.addEllipse(scene_pos.x() - 5, scene_pos.y() - 5, 10, 10, pen, brush)

        # Remove the previously selected circle
        if self.selected_circle is not None:
            self.scene.removeItem(self.selected_circle)

        # Set the newly created circle as the selected circle
        self.selected_circle = new_circle

        # Enable the submit button
        self.submit_button.setEnabled(True)

    def on_submit_button_clicked(self):
        if self.selected_circle is not None:
            self.submit_button.setDisabled(True)
            self.scene.removeItem(self.selected_circle)
            brush = QBrush(QColor(0, 255, 0))
            pen = QPen(brush, 3)

            # Create a  circle to represent the point
            correct = self.scene.addEllipse( self.position[0],  self.position[1], 10, 10, pen, brush)

            # Get the position of the selected circle
            pos = self.selected_circle.rect().center()

            # Convert the position to a view coordinate
            view_pos = self.view.mapFromScene(pos)
            viewx,viewy = view_pos.x(), view_pos.y()

            loop = QEventLoop()
            QTimer.singleShot(2000, loop.quit)
            loop.exec_()

            self.scene.removeItem(correct)
            self.newQ()


    def newQ(self):
        self.submit_button.setEnabled(True)
        self.place, self.position = random.choice(list(self.MAPITEMS.items()))
        self.heading_label.setText(f"Mark {self.place}")

        self.MAPITEMS.pop(self.place)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
