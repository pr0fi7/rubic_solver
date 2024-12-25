import copy

def update_white_sides_after(func):
    def wrapper(self, *args, **kwargs):
        # print("Updating white sides")
        result = func(self, *args, **kwargs)
        self.white_sides = self.find_white_sides()  # Recalculate white_sides
        return result
    return wrapper


#finish steps thingy

def rotate_face(cube, face, direction, steps=None):
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
            cube['U'][2], cube['U'][5], cube['U'][8] = initial_cube['B'][8], initial_cube['B'][5], initial_cube['B'][2]
            cube['B'][2], cube['B'][5], cube['B'][8] = initial_cube['D'][2], initial_cube['D'][5], initial_cube['D'][8]
            cube['D'][2], cube['D'][5], cube['D'][8] = initial_cube['F'][8], initial_cube['F'][5], initial_cube['F'][2]
        elif direction == 'CW':
            cube['F'][2], cube['F'][5], cube['F'][8] = initial_cube['D'][8], initial_cube['D'][5], initial_cube['D'][2]
            cube['U'][2], cube['U'][5], cube['U'][8] = initial_cube['F'][2], initial_cube['F'][5], initial_cube['F'][8]
            cube['B'][2], cube['B'][5], cube['B'][8] = initial_cube['U'][8], initial_cube['U'][5], initial_cube['U'][2]
            cube['D'][2], cube['D'][5], cube['D'][8] = initial_cube['B'][2], initial_cube['B'][5], initial_cube['B'][8]

    elif face == 'L':
        if direction == 'CnW':
            cube['F'][0], cube['F'][3], cube['F'][6] = initial_cube['D'][6], initial_cube['D'][3], initial_cube['D'][0]
            cube['U'][0], cube['U'][3], cube['U'][6] = initial_cube['F'][0], initial_cube['F'][3], initial_cube['F'][6]
            cube['B'][0], cube['B'][3], cube['B'][6] = initial_cube['U'][6], initial_cube['U'][3], initial_cube['U'][0]
            cube['D'][0], cube['D'][3], cube['D'][6] = initial_cube['B'][0], initial_cube['B'][3], initial_cube['B'][6]
        elif direction == 'CW':
            cube['F'][0], cube['F'][3], cube['F'][6] = initial_cube['U'][0], initial_cube['U'][3], initial_cube['U'][6]
            cube['U'][0], cube['U'][3], cube['U'][6] = initial_cube['B'][6], initial_cube['B'][3], initial_cube['B'][0]
            cube['B'][0], cube['B'][3], cube['B'][6] = initial_cube['D'][0], initial_cube['D'][3], initial_cube['D'][6]
            cube['D'][0], cube['D'][3], cube['D'][6] = initial_cube['F'][6], initial_cube['F'][3], initial_cube['F'][0]

    elif face == 'U':
        if direction == 'CnW':
            cube['F'][0], cube['F'][1], cube['F'][2] = initial_cube['L'][0], initial_cube['L'][1], initial_cube['L'][2]
            cube['R'][0], cube['R'][1], cube['R'][2] = initial_cube['F'][0], initial_cube['F'][1], initial_cube['F'][2]
            cube['B'][0], cube['B'][1], cube['B'][2] = initial_cube['R'][2], initial_cube['R'][1], initial_cube['R'][0]
            cube['L'][0], cube['L'][1], cube['L'][2] = initial_cube['B'][2], initial_cube['B'][1], initial_cube['B'][0]
        elif direction == 'CW':
            cube['F'][0], cube['F'][1], cube['F'][2] = initial_cube['R'][0], initial_cube['R'][1], initial_cube['R'][2]
            cube['R'][0], cube['R'][1], cube['R'][2] = initial_cube['B'][2], initial_cube['B'][1], initial_cube['B'][0]
            cube['B'][0], cube['B'][1], cube['B'][2] = initial_cube['L'][2], initial_cube['L'][1], initial_cube['L'][0]
            cube['L'][0], cube['L'][1], cube['L'][2] = initial_cube['F'][0], initial_cube['F'][1], initial_cube['F'][2]

    elif face == 'D':
        if direction == 'CnW':
            cube['F'][6], cube['F'][7], cube['F'][8] = initial_cube['L'][6], initial_cube['L'][7], initial_cube['L'][8]
            cube['R'][6], cube['R'][7], cube['R'][8] = initial_cube['F'][6], initial_cube['F'][7], initial_cube['F'][8]
            cube['B'][6], cube['B'][7], cube['B'][8] = initial_cube['R'][8], initial_cube['R'][7], initial_cube['R'][6]
            cube['L'][6], cube['L'][7], cube['L'][8] = initial_cube['B'][8], initial_cube['B'][7], initial_cube['B'][6]
        elif direction == 'CW':
            cube['F'][6], cube['F'][7], cube['F'][8] = initial_cube['R'][6], initial_cube['R'][7], initial_cube['R'][8]
            cube['R'][6], cube['R'][7], cube['R'][8] = initial_cube['B'][8], initial_cube['B'][7], initial_cube['B'][6]
            cube['B'][6], cube['B'][7], cube['B'][8] = initial_cube['L'][8], initial_cube['L'][7], initial_cube['L'][6]
            cube['L'][6], cube['L'][7], cube['L'][8] = initial_cube['F'][6], initial_cube['F'][7], initial_cube['F'][8]

    elif face == 'F':
        if direction == 'CnW':
            cube['U'][6], cube['U'][7], cube['U'][8] = initial_cube['R'][0], initial_cube['R'][3], initial_cube['R'][6]
            cube['L'][2], cube['L'][5], cube['L'][8] = initial_cube['U'][8], initial_cube['U'][7], initial_cube['U'][6]
            cube['D'][6], cube['D'][7], cube['D'][8] = initial_cube['L'][2], initial_cube['L'][5], initial_cube['L'][8]
            cube['R'][0], cube['R'][3], cube['R'][6] = initial_cube['D'][8], initial_cube['D'][7], initial_cube['D'][6]
        elif direction == 'CW':
            cube['U'][6], cube['U'][7], cube['U'][8] = initial_cube['L'][8], initial_cube['L'][5], initial_cube['L'][2]
            cube['L'][2], cube['L'][5], cube['L'][8] = initial_cube['D'][6], initial_cube['D'][7], initial_cube['D'][8]
            cube['D'][6], cube['D'][7], cube['D'][8] = initial_cube['R'][6], initial_cube['R'][3], initial_cube['R'][0]
            cube['R'][0], cube['R'][3], cube['R'][6] = initial_cube['U'][6], initial_cube['U'][7], initial_cube['U'][8]

    elif face == 'B':
        if direction == 'CnW':
            cube['U'][0], cube['U'][1], cube['U'][2] = initial_cube['R'][2], initial_cube['R'][5], initial_cube['R'][8]
            cube['L'][0], cube['L'][3], cube['L'][6] = initial_cube['U'][2], initial_cube['U'][1], initial_cube['U'][0]
            cube['D'][0], cube['D'][1], cube['D'][2] = initial_cube['L'][0], initial_cube['L'][3], initial_cube['L'][6]
            cube['R'][2], cube['R'][5], cube['R'][8] = initial_cube['D'][2], initial_cube['D'][1], initial_cube['D'][0]
        elif direction == 'CW':
            cube['U'][0], cube['U'][1], cube['U'][2] = initial_cube['L'][6], initial_cube['L'][3], initial_cube['L'][0]
            cube['L'][0], cube['L'][3], cube['L'][6] = initial_cube['D'][0], initial_cube['D'][1], initial_cube['D'][2]
            cube['D'][0], cube['D'][1], cube['D'][2] = initial_cube['R'][8], initial_cube['R'][5], initial_cube['R'][2]
            cube['R'][2], cube['R'][5], cube['R'][8] = initial_cube['U'][0], initial_cube['U'][1], initial_cube['U'][2]

    else:
        raise ValueError(f"Invalid face '{face}'. Use one of 'U', 'D', 'F', 'B', 'L', 'R'.")
    
    steps.append((face, direction))

    return cube