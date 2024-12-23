import serial
from solver import CubeSolver
import time

# Serial port configuration (Update as per your Arduino port)
SERIAL_PORT = "COM3"  # Adjust for your system
BAUD_RATE = 9600

# Mapping between cube faces and motor pins
motor_map = {
    'F': 'FRONT',
    'R': 'RIGHT',
    'L': 'LEFT',
    'B': 'BACK',
    'U': 'TOP',
    'D': 'BOTTOM',
}

# Function to send a motor command to Arduino
def send_motor_command(ser, motor, direction, steps):
    """
    motor: Motor name (e.g., 'FRONT', 'RIGHT')
    direction: 'CW' or 'CnW'
    steps: Number of steps to rotate
    """
    command = f"{motor},{direction},{steps}\n"
    ser.write(command.encode('utf-8'))
    print(f"Sent command: {command.strip()}")

def main():
    # Open serial connection to Arduino
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for Arduino to initialize

    # Initialize the solver
    solver = CubeSolver(None)
    solver.initialize_cube()
    solver.scramble()
    solver.solve()

    # Optimize steps and send them to Arduino
    verified_steps = solver.steps[20:]
    optimized_steps = solver.optimize_steps(verified_steps)

    print(f"Optimized Steps: {optimized_steps}")

    for step in optimized_steps:
        face, direction = step
        motor = motor_map[face]  # Map face to motor
        steps = 200 * 16  # Example: 200 steps/rev × microstepping (adjust as needed)
        send_motor_command(ser, motor, direction, steps)
        time.sleep(0.1)  # Delay between commands for motor to finish

    # Close the serial connection
    ser.close()

if __name__ == "__main__":
    main()
