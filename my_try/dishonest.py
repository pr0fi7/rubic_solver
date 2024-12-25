import serial
import time
from solver import CubeSolver
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
import sys
import random

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


# PyQt5 GUI
class MainWindow(QMainWindow):
    def __init__(self, cube=None):
        super().__init__()
        self.setWindowTitle('Two Phase Solver')
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(1500, 800)
        self.color_sequence = ['red', 'white', 'green', 'orange', 'yellow', 'blue']
        self.button_num = 9
        self.buttons = {}
        self.button_sides = {"U": 'yellow', "L": 'orange', "F": 'blue', "R": 'red', "B": 'green', "D": 'white'}
        self.cube = cube or {}
        self.initialize_cube()
        self.solve_button = QPushButton('Solve', self)
        self.solve_button.setGeometry(50, 600, 100, 50)
        self.solve_button.clicked.connect(self.solve_cube)

        self.create_side()

    def initialize_cube(self):
        self.cube = {face: [None] * 9 for face in ['U', 'L', 'F', 'R', 'B', 'D']}
        face_colors = {'U': 'Y', 'L': 'O', 'F': 'B', 'R': 'R', 'B': 'G', 'D': 'W'}
        for face, color in face_colors.items():
            for index in range(9):
                self.cube[face][index] = color
        print(self.cube)
        
    def scramble( self ):
        sides = ['U', 'L', 'F', 'R', 'B', 'D']
        rotations = ['CW', 'CnW']
        
        for _ in range(20):
            side = random.choice(sides)
            rotation = random.choice(rotations)
            self.cube = self.rotate_face(side, rotation)
        return self.cube
        

    def change_state(self, button):
        color_mapper = {'green': 'G', 'red': 'R', 'blue': 'B', 'white': 'W', 'yellow': 'Y', 'orange': 'O'}
        current_style = button.styleSheet()
        current_color = current_style.split(':')[1].strip()
        current_index = self.color_sequence.index(current_color)
        next_index = (current_index + 1) % len(self.color_sequence)

        button_position = button.text()
        my_index = int(button_position[1]) - 1

        next_color = self.color_sequence[next_index] if not my_index == 4 else current_color
        new_style = f"background-color: {next_color}"
        button.setStyleSheet(new_style)
        my_color = color_mapper[next_color]
        my_face = button_position[0]

        for face, _ in self.cube.items():
            if face == my_face:
                self.cube[face][my_index] = my_color

        print(self.cube)

    def create_side(self):
        current_index = 0

        for button_side, color in self.button_sides.items():
            if current_index == 0:
                x_margin = 200
                y_margin = 0
            elif 0 < current_index < 5:
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
                self.buttons[f'{button_side}{i}'] = button

    def solve_cube(self):
        # Solve the cube
        initial_cube = {face: [None] * 9 for face in ['U', 'L', 'F', 'R', 'B', 'D']}
        face_colors = {'U': 'Y', 'L': 'O', 'F': 'B', 'R': 'R', 'B': 'G', 'D': 'W'}
        for face, color in face_colors.items():
            for index in range(9):
                initial_cube[face][index] = color

        scrambled_cube = CubeSolver(initial_cube)
        scrambled_cube.scramble()

        scramble_steps = scrambled_cube.optimize_steps(scrambled_cube.steps)

        if send_steps_to_arduino(scramble_steps):
            print('Scramble sent successfully')
            cube_to_solve = scrambled_cube.cube

            my_cube = cube_to_solve #self.cube        
            solver = CubeSolver(my_cube)
            # solver.scramble()
            print('sovercube')
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
