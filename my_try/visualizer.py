from PyQt5.QtWidgets import QMainWindow, QPushButton

class CubeVisualizer(QMainWindow):
    def __init__(self, cube,title):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(600,600)

        self.cube = cube
        self.colors_dict = {"Y": "yellow", "O": "orange", "B": "blue", "R": "red", "G": "green", "W": "white"}

        self.buttons = {}

        self.draw_cube()
        self.exit()

    def draw_cube(self):
        # Define a simple net layout for the cube faces:
        #      U
        #    L F R B
        #      D

        face_positions = {
            'U': (150,  0),
            'L': (0,   150),
            'F': (150, 150),
            'R': (300, 150),
            'B': (450, 150),
            'D': (150, 300),
        }

        button_size = 40

        for face, squares in self.cube.items():
            base_x, base_y = face_positions[face]
            for i, color_code in enumerate(squares):
                row = i // 3
                col = i % 3
                x = base_x + col*button_size
                y = base_y + row*button_size
                btn = QPushButton(self)
                btn.setGeometry(x, y, button_size, button_size)
                btn.setStyleSheet(f"background-color: {self.colors_dict[color_code]}")
                self.buttons[(face, i)] = btn

    def exit(self):
        btn = QPushButton('Exit', self)
        btn.setStyleSheet("background-color: black; color: white")

        btn.setGeometry(250, 550, 100, 50)
        btn.clicked.connect(lambda _, b=self: b.close())


    def update_cube_display(self):
        for (face, i), btn in self.buttons.items():
            color_code = self.cube[face][i]
            btn.setStyleSheet(f"background-color: {self.colors_dict[color_code]}")
