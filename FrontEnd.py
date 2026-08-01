from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
import Globals as gb
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QFontDatabase
class ColorTextWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mediapipe Tacking Informer")
        self.setGeometry(100, 100, 800, 200)

        self.setStyleSheet("background-color: black;")
        # Create labels with different colors
        self.left_hand_text_head = QLabel("")
        self.left_hand_text_head.move(50, 20)

        self.right_hand_text_head = QLabel("")
        self.right_hand_text_head.move(450, 20)

        self.left_hand_text = QLabel("")
        self.left_hand_text.move(50, 70)

        self.right_hand_text = QLabel("")
        self.right_hand_text.move(450, 70)
        font_id = QFontDatabase.addApplicationFont("Assets/Fonts/pixelFont.ttf")
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(family, 24)
        font.setStyleStrategy(QFont.NoAntialias)        
        font.setBold(True)
        for label in [self.left_hand_text_head, self.right_hand_text_head]:
            label.setFont(font)

        font = QFont(family, 22)
        font.setBold(False)
        for label in [self.left_hand_text, self.right_hand_text]:
            label.setFont(font)
            label.setStyleSheet("color: yellow;")

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        left_layout.addWidget(self.left_hand_text_head)
        left_layout.addWidget(self.left_hand_text)

        right_layout.addWidget(self.right_hand_text_head)
        right_layout.addWidget(self.right_hand_text)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def Update(self,left,right):
        if gb.leftMissing:
            self.left_hand_text_head.setText("Left Hand Missing!")
            self.left_hand_text_head.setStyleSheet("color: red;")            
            self.left_hand_text.hide()

        else:
            self.left_hand_text_head.setText("Left Hand Ok!")
            self.left_hand_text_head.setStyleSheet("color: green;")
            self.left_hand_text.setText(left)
            self.left_hand_text.show()

        if gb.rightMissing:
            self.right_hand_text_head.setText("Right Hand Missing!")
            self.right_hand_text_head.setStyleSheet("color: red;")
            self.right_hand_text.hide()
        else:
            self.right_hand_text_head.setText("Right Hand Ok!")
            self.right_hand_text_head.setStyleSheet("color: green;")            
            self.right_hand_text.setText(right)
            self.right_hand_text.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()