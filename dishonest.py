from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
import sys 
import twophase.solver  as sv
import serial.tools.list_ports

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Two Phase Solver')
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(2500, 800)
        self.color_sequence = ['red', 'white', 'green', 'orange', 'yellow', 'blue']
        self.button_num = 9
        self.buttons = {}
        self.button_sides = {"U":'red', "L":'yellow', "F":'green', "R":'white', "B":'blue', "D":'orange'}
        self.cube = [9*key for color in self.color_sequence for key, value in self.button_sides.items() if value == color]
        self.solve_button = QPushButton('Solve', self)
        self.solve_button.setGeometry(50, 600, 50, 50)
        self.solve_button.clicked.connect(lambda _, b=self.solve_button: self.get_cube_string())

        self.create_side()  

    @staticmethod
    def initialize_serial(solution):
        ports = serial.tools.list_ports.comports()
        serialInst = serial.Serial()

        ports_list = []

        for port in ports:
            ports_list.append(str(port))

        val = input(f"Choose a port from the following list: {ports_list}\n")

        port_val = ports_list[int(val+1)]

        serialInst.baudrate = 9600
        serialInst.port = port_val
        serialInst.open()
        while True:
            serialInst.write(solution.encode('utf-8'))

    def change_state(self, button):
        current_style = button.styleSheet()
        current_color = current_style.split(':')[1].strip()
        current_index = self.color_sequence.index(current_color)
        next_index = (current_index + 1) % len(self.color_sequence)
        next_color = self.color_sequence[next_index]
        new_style = f"background-color: {next_color}"
        button.setStyleSheet(new_style)
        button_state = [key for key, value in self.button_sides.items() if value == next_color][0]
        button_position = button.text()
        for index_side, side in enumerate(self.cube):
            if button_position[0] == side[4]:
                index = int(button_position[-1])
                self.cube[index_side] = f'{side[:index-1]}{button_state}{side[index:]}'
        print(self.cube)

    def create_side(self):
        current_index = 0

        for button_side, color in self.button_sides.items():
            if current_index == 0:
                x_margin = 200
                y_margin = 0
            elif current_index > 0 and current_index < 5:
                x_margin = 200 * (current_index - 1)
                y_margin = 200
            else:
                x_margin = 200 
                y_margin = 400

            current_index += 1
            for i in range(1, self.button_num + 1):
                button = QPushButton(f'{button_side}{i}', self)
                button.setGeometry(50 * (i - 1) % 150 + x_margin, 50 * ((i - 1) // 3) + y_margin, 50, 50)
                button.setStyleSheet(f'background-color: {color}')
                button.clicked.connect(lambda _, b=button: self.change_state(b))  # Connect to change_state with the specific button
                self.buttons[f'U{i}'] = button

    def get_cube_string(self):
        cube_string = ''
        for side in self.cube:
            cube_string += side
        solution_list = sv.solve(cube_string).split('(')[0].strip().split()
        print(solution_list)
        final_solution = []
        rotations_dict = {
            1: 90,
            2: 180,
            3: 270
        }
        for step in solution_list:
            step = step.strip()
            if int(step[-1]) in rotations_dict:
                final_solution.append(f'{step[:-1]}{rotations_dict[int(step[-1])]}')

        self.initialize_serial(' '.join(final_solution))  

        print(final_solution)
    

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
