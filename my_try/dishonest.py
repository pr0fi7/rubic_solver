import serial
import time
from solver import CubeSolver
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
import sys
import random
from PyQt5.QtCore import QTimer

# Arduino Serial Communication
SERIAL_PORT = "COM3"
BAUD_RATE = 115200

motor_map = {
    'F': 'FRONT',
    'R': 'RIGHT',
    'L': 'LEFT',
    'B': 'BACK',
    'U': 'TOP',
    'D': 'BOTTOM',
}

def send_motor_command(ser, motor, direction, steps):
    command = f"{motor},{direction},{steps}\n"
    ser.write(command.encode('utf-8'))
    print(f"Sent command: {command.strip()}")

    response = ser.readline().decode('utf-8').strip()
    print(f"Arduino response: {response}")
    print(f"Expected response: Received {command.strip()}")

    if response == f"Received: {command.strip()}":
        return True
    else:
        print("Failed to receive acknowledgment from Arduino")
        return False


def send_steps_to_arduino(steps):
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)  # Allow Arduino to initialize

        # Send the number of steps
        len_steps = f"{len(steps)}\n"
        ser.write(len_steps.encode('utf-8'))
        print(f"Sent total steps: {len_steps}")

        # Wait for acknowledgment
        response = ser.readline().decode('utf-8').strip()
        if response != f'Received: {len_steps.strip()}':
            print(f"Failed to synchronize: {response}")
            return

        # Send each command
        for step in steps:
            face, direction = step
            motor = motor_map[face]
            if not send_motor_command(ser, motor, direction, 50 * 16):
                print("Command failed!")
                break
            time.sleep(0.1)  # Add a small delay between commands

        while not is_finished(ser):
            pass        
        ser.close()
        return True
    except Exception as e:
        print(f"Error communicating with Arduino: {e}")

def is_finished(ser):
    response = ser.readline().decode('utf-8').strip()
    if response == 'Finished':
        return True
    return False

# PyQt5 WORKER

# PyQt5 GUI
class MainWindow(QMainWindow):
    def __init__(self, cube=None):
        super().__init__()
        self.setWindowTitle('Two Phase Solver')
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(980, 700)
        self.current_color = 'white'
        self.colors = ['yellow', 'orange', 'blue', 'red', 'green', 'white']
        self.button_num = 9
        self.buttons = {}
        self.colors_mapper = {'Y': 'yellow', 'O': 'orange', 'B': 'blue', 'R': 'red', 'G': 'green', 'W': 'white'}
        self.button_sides = {"U": 'yellow', "L": 'orange', "F": 'blue', "R": 'red', "B": 'green', "D": 'white'}
        self.cube = cube or {}
        self.initialize_cube()
        self.solve_button = QPushButton('Solve', self)
        self.scramble_button = QPushButton('Scramble', self)
        self.reset = QPushButton('Reset', self)
        self.reset.setGeometry(850, 600, 100, 50)
        self.reset.setStyleSheet('background-color: white; color: black')
        self.solve_button.setGeometry(50, 600, 300, 50)
        self.scramble_button.setGeometry(450, 600, 300, 50)
        for buttons in [self.solve_button, self.scramble_button]:
            buttons.setStyleSheet('background-color: black; color: white')

        self.solve_button.clicked.connect(lambda: self.solve_cube() if self.possibility_check() else self.raise_problem())
        self.scramble_button.clicked.connect(lambda: self.scramble())
        self.reset.clicked.connect(lambda: self.reset_state())

        self.create_side()
        self.right_bar()

    def reset_state(self):
        self.initialize_cube()
        self.update_colors()

    def initialize_cube(self):
        self.cube = {face: [None] * 9 for face in ['U', 'L', 'F', 'R', 'B', 'D']}
        face_colors = {'U': 'Y', 'L': 'O', 'F': 'B', 'R': 'R', 'B': 'G', 'D': 'W'}
        for face, color in face_colors.items():
            for index in range(9):
                self.cube[face][index] = color
        print(self.cube)
        
    def raise_problem(self):
        self.banner = QPushButton('Impossible to solve cube', self)
        self.banner.setGeometry(80, 120, 800, 300)
        self.banner.setStyleSheet('background-color: red; color: white; font-size: 50px')
        self.banner.show()  # Ensure the button is visible
        QTimer.singleShot(2000, self.banner.close)

    def right_bar(self):
        for color in self.colors:
            button = QPushButton('', self)
            button.setGeometry(850, 55 * self.colors.index(color) + 115, 50, 50)
            button.setStyleSheet(f'background-color: {color}')
            button.text = color
            button.clicked.connect(lambda _, color=color: self.set_current_color(color))

    def set_current_color(self, color):
        self.current_color = color
        
    def scramble( self ):
        sides = ['U', 'L', 'F', 'R', 'B', 'D']
        rotations = ['CW', 'CnW']

        cubesolver = CubeSolver(self.cube)
        
        for _ in range(20):
            side = random.choice(sides)
            rotation = random.choice(rotations)
            self.cube = cubesolver.rotate_face(side, rotation)
        self.update_colors()
        return self.cube

    def change_color(self, buttons, current_color):
        button_position = buttons.text()
        my_index = int(button_position[1]) - 1
        my_face = button_position[0]

        buttons.setStyleSheet(f"background-color: {current_color}")        

        for face, _ in self.cube.items():
            if face == my_face:
                self.cube[face][my_index] = current_color[0].upper()
        print(self.cube)
    
    def update_colors(self):
        for button_pos, button in self.buttons.items():
            button.setStyleSheet(f"background-color: {self.colors_mapper[self.cube[button_pos[0]][int(button_pos[1]) - 1]]}")

    def create_side(self, initial_x=40):
        current_index = 0

        for button_side, color in self.button_sides.items():
            if current_index == 0:
                x_margin = initial_x + 200
                y_margin = 0
            elif 0 < current_index < 5:
                x_margin = initial_x + 200 * (current_index - 1)
                y_margin = 200
            else:
                x_margin = initial_x + 200
                y_margin = 400

            current_index += 1
            for i in range(1, self.button_num + 1):
                button = QPushButton(f'{button_side}{i}', self)
                button.setGeometry(50 * (i - 1) % 150 + x_margin, 50 * ((i - 1) // 3) + y_margin, 50, 50)
                button.setStyleSheet(f'background-color: {color}')
                button.clicked.connect(lambda _, b=button: self.change_color(b, self.current_color))  
                self.buttons[f'{button_side}{i}'] = button

    def possibility_check(self):
        color_count = {}

        # Count occurrences of each color in the cube
        for stickers in self.cube.values():
            for sticker in stickers:
                color_count[sticker] = color_count.get(sticker, 0) + 1
                # If any color exceeds 9, return False immediately
                if color_count[sticker] > 9:
                    print(f"Color {sticker} appears more than 9 times!")
                    return False

        print("Possibility check passed")
        return True

            
    def solve_cube(self):
        # Solve the cube
        # initial_cube = {face: [None] * 9 for face in ['U', 'L', 'F', 'R', 'B', 'D']}
        # face_colors = {'U': 'Y', 'L': 'O', 'F': 'B', 'R': 'R', 'B': 'G', 'D': 'W'}
        # for face, color in face_colors.items():
        #     for index in range(9):
        #         initial_cube[face][index] = color

        # scrambled_cube = CubeSolver(initial_cube)
        # scrambled_cube.scramble()

        # scramble_steps = scrambled_cube.optimize_steps(scrambled_cube.steps)

        # if send_steps_to_arduino(scramble_steps):
        #     print('Scramble sent successfully')
        #     cube_to_solve = scrambled_cube.cube

        #     my_cube = cube_to_solve #self.cube        
        solver = CubeSolver(self.cube)
        # solver.scramble()
        print('solvercube')
        print(solver.cube)

        # solver.cube = self.cube
        solver.solve()
        steps = solver.optimize_steps(solver.steps)

        send_steps_to_arduino(steps)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
