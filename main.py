import copy
import random


def initialize_cube():
    cube = {face: [None] * 9 for face in ['U', 'L', 'F', 'R', 'B', 'D']}
    face_colors = {'U': 'Y', 'L': 'O', 'F': 'B', 'R': 'R', 'B': 'G', 'D': 'W'}
    for face, color in face_colors.items():
        for index in range(9):
            cube[face][index] = color
    return cube

# Rotate face with deep copy for adjacent changes
def rotate_face(face, cube, direction):
    initial_cube = copy.deepcopy(cube)  # Make a deep copy of the cube to retain original state

    # Define rotation matrices for CW and CnW rotations
    rotation_matrix_CW = [6, 3, 0, 7, 4, 1, 8, 5, 2]
    rotation_matrix_CnW = [2, 5, 8, 1, 4, 7, 0, 3, 6]

    # Select the appropriate rotation matrix based on direction
    if direction == 'CnW':
        rotation_matrix = rotation_matrix_CnW
    elif direction == 'CW':
        rotation_matrix = rotation_matrix_CW
    else:
        raise ValueError("Invalid rotation direction. Use 'CW' or 'CnW'.")

    # Rotate the face
    cube[face] = [cube[face][index] for index in rotation_matrix]

    # Handle adjacent face updates based on the face being rotated
    if face == 'R':
        if direction == 'CnW':
            cube['F'][2], cube['F'][5], cube['F'][8] = initial_cube['U'][2], initial_cube['U'][5], initial_cube['U'][8]
            cube['U'][2], cube['U'][5], cube['U'][8] = initial_cube['B'][6], initial_cube['B'][3], initial_cube['B'][0]
            cube['B'][0], cube['B'][3], cube['B'][6] = initial_cube['D'][2], initial_cube['D'][5], initial_cube['D'][8]
            cube['D'][2], cube['D'][5], cube['D'][8] = initial_cube['F'][2], initial_cube['F'][5], initial_cube['F'][8]
        elif direction == 'CW':
            cube['U'][2], cube['U'][5], cube['U'][8] = initial_cube['F'][2], initial_cube['F'][5], initial_cube['F'][8]
            cube['F'][2], cube['F'][5], cube['F'][8] = initial_cube['D'][2], initial_cube['D'][5], initial_cube['D'][8]
            cube['D'][2], cube['D'][5], cube['D'][8] = initial_cube['B'][6], initial_cube['B'][3], initial_cube['B'][0]
            cube['B'][0], cube['B'][3], cube['B'][6] = initial_cube['U'][8], initial_cube['U'][5], initial_cube['U'][2]

    elif face == 'L':
        if direction == 'CnW':
            cube['F'][0], cube['F'][3], cube['F'][6] = initial_cube['D'][0], initial_cube['D'][3], initial_cube['D'][6]
            cube['D'][0], cube['D'][3], cube['D'][6] = initial_cube['B'][8], initial_cube['B'][5], initial_cube['B'][2]
            cube['B'][2], cube['B'][5], cube['B'][8] = initial_cube['U'][0], initial_cube['U'][3], initial_cube['U'][6]
            cube['U'][0], cube['U'][3], cube['U'][6] = initial_cube['F'][0], initial_cube['F'][3], initial_cube['F'][6]
        elif direction == 'CW':
            cube['F'][0], cube['F'][3], cube['F'][6] = initial_cube['U'][0], initial_cube['U'][3], initial_cube['U'][6]
            cube['U'][0], cube['U'][3], cube['U'][6] = initial_cube['B'][8], initial_cube['B'][5], initial_cube['B'][2]
            cube['B'][2], cube['B'][5], cube['B'][8] = initial_cube['D'][0], initial_cube['D'][3], initial_cube['D'][6]
            cube['D'][0], cube['D'][3], cube['D'][6] = initial_cube['F'][0], initial_cube['F'][3], initial_cube['F'][6]

    elif face == 'U':
        if direction == 'CnW':
            cube['F'][0], cube['F'][1], cube['F'][2] = initial_cube['R'][0], initial_cube['R'][1], initial_cube['R'][2]
            cube['R'][0], cube['R'][1], cube['R'][2] = initial_cube['B'][0], initial_cube['B'][1], initial_cube['B'][2]
            cube['B'][0], cube['B'][1], cube['B'][2] = initial_cube['L'][0], initial_cube['L'][1], initial_cube['L'][2]
            cube['L'][0], cube['L'][1], cube['L'][2] = initial_cube['F'][0], initial_cube['F'][1], initial_cube['F'][2]
        elif direction == 'CW':
            cube['F'][0], cube['F'][1], cube['F'][2] = initial_cube['L'][0], initial_cube['L'][1], initial_cube['L'][2]
            cube['L'][0], cube['L'][1], cube['L'][2] = initial_cube['B'][0], initial_cube['B'][1], initial_cube['B'][2]
            cube['B'][0], cube['B'][1], cube['B'][2] = initial_cube['R'][0], initial_cube['R'][1], initial_cube['R'][2]
            cube['R'][0], cube['R'][1], cube['R'][2] = initial_cube['F'][0], initial_cube['F'][1], initial_cube['F'][2]

    elif face == 'D':
        if direction == 'CnW':
            cube['F'][6], cube['F'][7], cube['F'][8] = initial_cube['L'][6], initial_cube['L'][7], initial_cube['L'][8]
            cube['L'][6], cube['L'][7], cube['L'][8] = initial_cube['B'][6], initial_cube['B'][7], initial_cube['B'][8]
            cube['B'][6], cube['B'][7], cube['B'][8] = initial_cube['R'][6], initial_cube['R'][7], initial_cube['R'][8]
            cube['R'][6], cube['R'][7], cube['R'][8] = initial_cube['F'][6], initial_cube['F'][7], initial_cube['F'][8]
        elif direction == 'CW':
            cube['F'][6], cube['F'][7], cube['F'][8] = initial_cube['R'][6], initial_cube['R'][7], initial_cube['R'][8]
            cube['R'][6], cube['R'][7], cube['R'][8] = initial_cube['B'][6], initial_cube['B'][7], initial_cube['B'][8]
            cube['B'][6], cube['B'][7], cube['B'][8] = initial_cube['L'][6], initial_cube['L'][7], initial_cube['L'][8]
            cube['L'][6], cube['L'][7], cube['L'][8] = initial_cube['F'][6], initial_cube['F'][7], initial_cube['F'][8]

    elif face == 'F':
        if direction == 'CnW':
            cube['U'][6], cube['U'][7], cube['U'][8] = initial_cube['L'][8], initial_cube['L'][5], initial_cube['L'][2]
            cube['L'][2], cube['L'][5], cube['L'][8] = initial_cube['D'][2], initial_cube['D'][1], initial_cube['D'][0]
            cube['D'][0], cube['D'][1], cube['D'][2] = initial_cube['R'][6], initial_cube['R'][3], initial_cube['R'][0]
            cube['R'][0], cube['R'][3], cube['R'][6] = initial_cube['U'][6], initial_cube['U'][7], initial_cube['U'][8]
        elif direction == 'CW':
            cube['U'][6], cube['U'][7], cube['U'][8] = initial_cube['R'][0], initial_cube['R'][3], initial_cube['R'][6]
            cube['R'][0], cube['R'][3], cube['R'][6] = initial_cube['D'][2], initial_cube['D'][1], initial_cube['D'][0]
            cube['D'][0], cube['D'][1], cube['D'][2] = initial_cube['L'][8], initial_cube['L'][5], initial_cube['L'][2]
            cube['L'][2], cube['L'][5], cube['L'][8] = initial_cube['U'][6], initial_cube['U'][7], initial_cube['U'][8]

    elif face == 'B':
        if direction == 'CnW':
            cube['U'][0], cube['U'][1], cube['U'][2] = initial_cube['R'][2], initial_cube['R'][5], initial_cube['R'][8]
            cube['R'][2], cube['R'][5], cube['R'][8] = initial_cube['D'][8], initial_cube['D'][7], initial_cube['D'][6]
            cube['D'][6], cube['D'][7], cube['D'][8] = initial_cube['L'][0], initial_cube['L'][3], initial_cube['L'][6]
            cube['L'][0], cube['L'][3], cube['L'][6] = initial_cube['U'][0], initial_cube['U'][1], initial_cube['U'][2]
        elif direction == 'CW':
            cube['U'][0], cube['U'][1], cube['U'][2] = initial_cube['L'][6], initial_cube['L'][3], initial_cube['L'][0]
            cube['L'][0], cube['L'][3], cube['L'][6] = initial_cube['D'][6], initial_cube['D'][7], initial_cube['D'][8]
            cube['D'][6], cube['D'][7], cube['D'][8] = initial_cube['R'][8], initial_cube['R'][5], initial_cube['R'][2]
            cube['R'][2], cube['R'][5], cube['R'][8] = initial_cube['U'][0], initial_cube['U'][1], initial_cube['U'][2]

    else:
        raise ValueError(f"Invalid face '{face}'. Use one of 'U', 'D', 'F', 'B', 'L', 'R'.")

    return cube

def tik_tak_move(cube):
    rotate_face('R', cube, 'CW')
    rotate_face('U', cube, 'CnW')
    rotate_face('R', cube, 'CnW')
    rotate_face('U', cube, 'CW')
    return cube

def get_white_square(cube):

    white_positions_U = {
        1: 'B', 
        3: 'L',  
        5: 'R',  
        7: 'F' 
    }
    white_positions_U_condition = {
        1: 1,
        3: 5,
        5: 3,
        7: 7
    }

    white_positions_L = {
        3: 'B',  # Position 3 corresponds to the Up (U) face
        5: 'F',  # Position 5 corresponds to the Down (D) face
    }

    white_positions_L_condition = {
        3: 1,
        5: 7
    }
     
    white_positions_R = {
        3: 'F',  # Position 3 corresponds to the Up (U) face
        5: 'B',  # Position 5 corresponds to the Down (D) face
    }

    white_positions_R_condition = {
        3: 7,
        5: 1
    }

    white_positions_F = {
        3: 'L',  # Position 3 corresponds to the Up (U) face
        5: 'R',  # Position 5 corresponds to the Down (D) face
    }
    white_positions_F_condition = {
        3: 5,
        5: 3
    }

    white_positions_B = {
        3: 'R',  # Position 3 corresponds to the Up (U) face
        5: 'L',  # Position 5 corresponds to the Down (D) face
    }

    white_positions_B_condition = {
        3: 3,
        5: 5
    }


    for position, face in white_positions_U.items():
        if cube['U'][position] == 'W':
            for position_cond, corresponding in white_positions_U_condition.items():
                if position == position_cond:
                    while cube['D'][corresponding] == 'W':
                        rotate_face('D' , cube, 'CW')

            rotate_face(face, cube, 'CW')
            rotate_face(face, cube, 'CW')

    for position, face in white_positions_R.items():
        if cube['R'][position] == 'W':
            for positinon_cond, corresponding in white_positions_R_condition.items():
                if position == positinon_cond:
                    while cube['D'][corresponding] == 'W':
                        rotate_face('D' , cube, 'CW')
            rotate_face(face, cube, 'CW')

    for position, face in white_positions_L.items():
        if cube['L'][position] == 'W':
            for positinon_cond, corresponding in white_positions_L_condition.items():
                if position == positinon_cond:
                    while cube['D'][corresponding] == 'W':
                        rotate_face('D' , cube, 'CW')
            rotate_face(face, cube, 'CW')
    
    for position, face in white_positions_B.items():
        if cube['B'][position] == 'W':
            for positinon_cond, corresponding in white_positions_B_condition.items():
                if position == positinon_cond:
                    while cube['D'][corresponding] == 'W':
                        rotate_face('D' , cube, 'CW')
            rotate_face(face, cube, 'CW')    

    for position, face in white_positions_F.items():
        if cube['F'][position] == 'W':
            for positinon_cond, corresponding in white_positions_F_condition.items():
                if position == positinon_cond:
                    while cube['D'][corresponding] == 'W':
                        rotate_face('D' , cube, 'CW')
            rotate_face(face, cube, 'CW')

    return cube

def scramble(cube, moves=20):
    moves_list = ['U', 'D', 'F', 'B', 'L', 'R']
    for _ in range(moves):
        move = random.choice(moves_list)
        clockwise = random.choice([True, False])
        rotate_face(move, cube, 'CW' if clockwise else 'CnW')
    return cube

# Display the cube for visualization
def display_cube(cube):
    for face in ['U', 'L', 'F', 'R', 'B', 'D']:
        print(f"{face}: {cube[face][0:3]}\n   {cube[face][3:6]}\n   {cube[face][6:9]}\n")

# Initialize cube and rotate the 'R' face
cube = initialize_cube()
cube = scramble(cube)

while not all(cube['D'][pos] == 'W' for pos in [1, 3, 5, 7]):
    cube = get_white_square(cube)

    cube = get_white_square(cube)
    # Optional: Display intermediate states for debugging
    print("After get_white_square rotation:")
    display_cube(cube)

# Final cube state
print("Final Cube State:")
display_cube(cube)


