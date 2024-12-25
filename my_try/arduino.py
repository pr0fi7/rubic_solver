import serial
import time
from solver import CubeSolver

SERIAL_PORT = "COM3"
BAUD_RATE = 9600

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
    if response != "OK":
        print(f"Arduino error: {response}")
        return False
    return True

def main():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    time.sleep(2)

    solver = CubeSolver()
    solver.initialize_cube()
    solver.solve()


    steps = solver.optimize_steps(solver.steps[20:])
    
    len_steps = f'{len(steps)}\n'
    ser.write(len_steps.encode('utf-8'))
    print(f"Sent command: {len_steps}")
    for step in steps:
        face, direction = step
        motor = motor_map[face]
        if not send_motor_command(ser, motor, direction, 50 * 16):
            print("Command failed!")
            break

    ser.close()

if __name__ == "__main__":
    main()
