import copy
import random
from utils import update_white_sides_after
class CubeSolver( ):
    def __init__( self, cube= None ):
        self.cube = cube
        # self.initialize_cube()
        self.white_sides = self.find_white_sides()
        self.steps = []

    @update_white_sides_after
    def rotate_face(self, face, direction):
        initial_cube = copy.deepcopy(self.cube)  # Make a deep copy of the cube to retain original state

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
        self.cube[face] = [self.cube[face][index] for index in rotation_matrix]

        # Handle adjacent face updates based on the face being rotated
        if face == 'R':
            if direction == 'CnW':
                self.cube['F'][2], self.cube['F'][5], self.cube['F'][8] = initial_cube['U'][2], initial_cube['U'][5], initial_cube['U'][8]
                self.cube['U'][2], self.cube['U'][5], self.cube['U'][8] = initial_cube['B'][8], initial_cube['B'][5], initial_cube['B'][2]
                self.cube['B'][2], self.cube['B'][5], self.cube['B'][8] = initial_cube['D'][2], initial_cube['D'][5], initial_cube['D'][8]
                self.cube['D'][2], self.cube['D'][5], self.cube['D'][8] = initial_cube['F'][8], initial_cube['F'][5], initial_cube['F'][2]
            elif direction == 'CW':
                self.cube['F'][2], self.cube['F'][5], self.cube['F'][8] = initial_cube['D'][8], initial_cube['D'][5], initial_cube['D'][2]
                self.cube['U'][2], self.cube['U'][5], self.cube['U'][8] = initial_cube['F'][2], initial_cube['F'][5], initial_cube['F'][8]
                self.cube['B'][2], self.cube['B'][5], self.cube['B'][8] = initial_cube['U'][8], initial_cube['U'][5], initial_cube['U'][2]
                self.cube['D'][2], self.cube['D'][5], self.cube['D'][8] = initial_cube['B'][2], initial_cube['B'][5], initial_cube['B'][8]

        elif face == 'L':
            if direction == 'CnW':
                self.cube['F'][0], self.cube['F'][3], self.cube['F'][6] = initial_cube['D'][6], initial_cube['D'][3], initial_cube['D'][0]
                self.cube['U'][0], self.cube['U'][3], self.cube['U'][6] = initial_cube['F'][0], initial_cube['F'][3], initial_cube['F'][6]
                self.cube['B'][0], self.cube['B'][3], self.cube['B'][6] = initial_cube['U'][6], initial_cube['U'][3], initial_cube['U'][0]
                self.cube['D'][0], self.cube['D'][3], self.cube['D'][6] = initial_cube['B'][0], initial_cube['B'][3], initial_cube['B'][6]
            elif direction == 'CW':
                self.cube['F'][0], self.cube['F'][3], self.cube['F'][6] = initial_cube['U'][0], initial_cube['U'][3], initial_cube['U'][6]
                self.cube['U'][0], self.cube['U'][3], self.cube['U'][6] = initial_cube['B'][6], initial_cube['B'][3], initial_cube['B'][0]
                self.cube['B'][0], self.cube['B'][3], self.cube['B'][6] = initial_cube['D'][0], initial_cube['D'][3], initial_cube['D'][6]
                self.cube['D'][0], self.cube['D'][3], self.cube['D'][6] = initial_cube['F'][6], initial_cube['F'][3], initial_cube['F'][0]

        elif face == 'U':
            if direction == 'CnW':
                self.cube['F'][0], self.cube['F'][1], self.cube['F'][2] = initial_cube['L'][0], initial_cube['L'][1], initial_cube['L'][2]
                self.cube['R'][0], self.cube['R'][1], self.cube['R'][2] = initial_cube['F'][0], initial_cube['F'][1], initial_cube['F'][2]
                self.cube['B'][0], self.cube['B'][1], self.cube['B'][2] = initial_cube['R'][2], initial_cube['R'][1], initial_cube['R'][0]
                self.cube['L'][0], self.cube['L'][1], self.cube['L'][2] = initial_cube['B'][2], initial_cube['B'][1], initial_cube['B'][0]
            elif direction == 'CW':
                self.cube['F'][0], self.cube['F'][1], self.cube['F'][2] = initial_cube['R'][0], initial_cube['R'][1], initial_cube['R'][2]
                self.cube['R'][0], self.cube['R'][1], self.cube['R'][2] = initial_cube['B'][2], initial_cube['B'][1], initial_cube['B'][0]
                self.cube['B'][0], self.cube['B'][1], self.cube['B'][2] = initial_cube['L'][2], initial_cube['L'][1], initial_cube['L'][0]
                self.cube['L'][0], self.cube['L'][1], self.cube['L'][2] = initial_cube['F'][0], initial_cube['F'][1], initial_cube['F'][2]

        elif face == 'D':
            if direction == 'CnW':
                self.cube['F'][6], self.cube['F'][7], self.cube['F'][8] = initial_cube['L'][6], initial_cube['L'][7], initial_cube['L'][8]
                self.cube['R'][6], self.cube['R'][7], self.cube['R'][8] = initial_cube['F'][6], initial_cube['F'][7], initial_cube['F'][8]
                self.cube['B'][6], self.cube['B'][7], self.cube['B'][8] = initial_cube['R'][8], initial_cube['R'][7], initial_cube['R'][6]
                self.cube['L'][6], self.cube['L'][7], self.cube['L'][8] = initial_cube['B'][8], initial_cube['B'][7], initial_cube['B'][6]
            elif direction == 'CW':
                self.cube['F'][6], self.cube['F'][7], self.cube['F'][8] = initial_cube['R'][6], initial_cube['R'][7], initial_cube['R'][8]
                self.cube['R'][6], self.cube['R'][7], self.cube['R'][8] = initial_cube['B'][8], initial_cube['B'][7], initial_cube['B'][6]
                self.cube['B'][6], self.cube['B'][7], self.cube['B'][8] = initial_cube['L'][8], initial_cube['L'][7], initial_cube['L'][6]
                self.cube['L'][6], self.cube['L'][7], self.cube['L'][8] = initial_cube['F'][6], initial_cube['F'][7], initial_cube['F'][8]

        elif face == 'F':
            if direction == 'CnW':
                self.cube['U'][6], self.cube['U'][7], self.cube['U'][8] = initial_cube['R'][0], initial_cube['R'][3], initial_cube['R'][6]
                self.cube['L'][2], self.cube['L'][5], self.cube['L'][8] = initial_cube['U'][8], initial_cube['U'][7], initial_cube['U'][6]
                self.cube['D'][6], self.cube['D'][7], self.cube['D'][8] = initial_cube['L'][2], initial_cube['L'][5], initial_cube['L'][8]
                self.cube['R'][0], self.cube['R'][3], self.cube['R'][6] = initial_cube['D'][8], initial_cube['D'][7], initial_cube['D'][6]
            elif direction == 'CW':
                self.cube['U'][6], self.cube['U'][7], self.cube['U'][8] = initial_cube['L'][8], initial_cube['L'][5], initial_cube['L'][2]
                self.cube['L'][2], self.cube['L'][5], self.cube['L'][8] = initial_cube['D'][6], initial_cube['D'][7], initial_cube['D'][8]
                self.cube['D'][6], self.cube['D'][7], self.cube['D'][8] = initial_cube['R'][6], initial_cube['R'][3], initial_cube['R'][0]
                self.cube['R'][0], self.cube['R'][3], self.cube['R'][6] = initial_cube['U'][6], initial_cube['U'][7], initial_cube['U'][8]

        elif face == 'B':
            if direction == 'CnW':
                self.cube['U'][0], self.cube['U'][1], self.cube['U'][2] = initial_cube['R'][2], initial_cube['R'][5], initial_cube['R'][8]
                self.cube['L'][0], self.cube['L'][3], self.cube['L'][6] = initial_cube['U'][2], initial_cube['U'][1], initial_cube['U'][0]
                self.cube['D'][0], self.cube['D'][1], self.cube['D'][2] = initial_cube['L'][0], initial_cube['L'][3], initial_cube['L'][6]
                self.cube['R'][2], self.cube['R'][5], self.cube['R'][8] = initial_cube['D'][2], initial_cube['D'][1], initial_cube['D'][0]
            elif direction == 'CW':
                self.cube['U'][0], self.cube['U'][1], self.cube['U'][2] = initial_cube['L'][6], initial_cube['L'][3], initial_cube['L'][0]
                self.cube['L'][0], self.cube['L'][3], self.cube['L'][6] = initial_cube['D'][0], initial_cube['D'][1], initial_cube['D'][2]
                self.cube['D'][0], self.cube['D'][1], self.cube['D'][2] = initial_cube['R'][8], initial_cube['R'][5], initial_cube['R'][2]
                self.cube['R'][2], self.cube['R'][5], self.cube['R'][8] = initial_cube['U'][0], initial_cube['U'][1], initial_cube['U'][2]

        else:
            raise ValueError(f"Invalid face '{face}'. Use one of 'U', 'D', 'F', 'B', 'L', 'R'.")
        
        self.steps.append((face, direction))

        return self.cube

    def initialize_cube(self):
        self.cube = {face: [None] * 9 for face in ['U', 'L', 'F', 'R', 'B', 'D']}
        face_colors = {'U': 'Y', 'L': 'O', 'F': 'B', 'R': 'R', 'B': 'G', 'D': 'W'}
        for face, color in face_colors.items():
            for index in range(9):
                self.cube[face][index] = color
        return self.cube

    def scramble( self ):
        sides = ['U', 'L', 'F', 'R', 'B', 'D']
        rotations = ['CW', 'CnW']
        
        for _ in range(20):
            side = random.choice(sides)
            rotation = random.choice(rotations)
            self.cube = self.rotate_face(side, rotation)
        return self.cube
        

    def find_white_sides( self ):
        self.white_sides = {face:[] for face in ['U', 'L', 'F', 'R', 'B', 'D']}
        omit = [0, 2, 4, 6, 8]
        for face, squares in self.cube.items():
            for index, color in enumerate(squares):
                if index not in omit:
                    if color == 'W':
                        self.white_sides[face].append(index)
        print(self.white_sides)
        return self.white_sides

    def white_cross(self):
        self.daisy()
        self._solve_front_side()
        self._solve_right_side()
        self._solve_left_side()
        self._solve_back_side()

    def _solve_front_side(self):
        counter = 0
        print('front:', self.cube['F'][1], self.cube['U'][7])
        while self.cube['F'][1] != 'B' or self.cube['U'][7] != 'W':
            self.cube = self.rotate_face('U', 'CW')
            counter += 1
            
        print('counter_front:', counter)
        self.cube =self.rotate_face('F', 'CW')
        self.cube =self.rotate_face('F', 'CW')
        print('finished front side')
    
    def _solve_right_side(self):
        counter = 0
        while self.cube['R'][1] != 'R' or self.cube['U'][5] != 'W':
            self.cube =self.rotate_face('U', 'CW')
            counter += 1
        print('counter_right:', counter)
        self.cube = self.rotate_face('R', 'CW')
        self.cube = self.rotate_face('R', 'CW')
        print('finished right side')
    
    def _solve_left_side(self):
        counter = 0
        while self.cube['L'][1] != 'O'or self.cube['U'][3] != 'W':
            self.cube = self.rotate_face('U', 'CW')
            counter += 1
        print('counter_left:', counter)
        self.cube =self.rotate_face('L', 'CW')
        self.cube =self.rotate_face('L', 'CW')
        print('finished left side')
    
    def _solve_back_side(self):
        counter = 0
        while self.cube['B'][1] != 'G' or self.cube['U'][1] != 'W':
            self.cube =self.rotate_face('U', 'CW')
            counter += 1
        print('counter_back:', counter)
        self.cube = self.rotate_face('B', 'CW')
        self.cube = self.rotate_face('B', 'CW')
        print('finished back side')
    

    def daisy(self): 
        instructions = {
            'L': {1: ['L', 'CW'], 3: ['B', 'CW'], 5: ['F', 'CW'], 7: ['L', 'CnW']},
            'F': {1: ['F', 'CW'], 3: ['L', 'CnW'], 5: ['R', 'CW'], 7: ['F', 'CnW']},
            'R': {1: ['R', 'CW'], 3: ['F', 'CnW'], 5: ['B', 'CnW'], 7: ['R', 'CnW']},
            'B': {1: ['B', 'CnW'], 3: ['L', 'CW'], 5: ['R', 'CnW'], 7: ['B', 'CW']},
            "D": {1: ['B', 'CW'], 3: ['L', 'CW'], 5: ['R', 'CnW'], 7: ['F', 'CnW']}
        }

        made_a_move = True

        while made_a_move:
            made_a_move = False
            self.find_white_sides()  # Refresh white sides on each iteration

            for face, squares in self.white_sides.items():
                if face != 'U':
                    if squares:
                        for square in squares:
                            instruction = instructions[face][square]
                            if self.check_rotation(face, square):
                                if face == 'D':
                                    print(f"Rotating {instruction[0]} {instruction[1]} (face={face}, sq={square})")
                                    self.rotate_face(instruction[0], instruction[1])
                                    self.rotate_face(instruction[0], instruction[1])
                                    made_a_move = True
                                    break
                                print(f"Rotating {instruction[0]} {instruction[1]} (face={face}, sq={square})")
                                self.rotate_face(instruction[0], instruction[1])
                                made_a_move = True
                                break  # break from squares
                                
                            else:
                                print("No valid rotations, rotating D")
                                self.rotate_face('U', 'CW')
                                made_a_move = True
                                break  # break from squares
                    if made_a_move:
                        break  # break from faces

        print("No more moves can be made (or we've rotated D repeatedly).")

    def check_rotation(self, face, square):
        white_faces = self.white_sides['U']
        print('checked_white_faces', white_faces)

        # If there are no white squares on the D face, we can do any rotation
        if not white_faces:
            return True

        my_bools = []
        for i in white_faces:
            # "Conflict condition" => if it matches, we want to disallow
            conflict = (
                (i == 1 and ((face == 'L' and square == 3) or
                            (face == 'R' and square == 5) or
                            (face == 'D' and square == 1) or
                            (face == 'B' and (square == 1 or square == 7)))) or
                (i == 7 and ((face == 'L' and square == 5) or
                            (face == 'R' and square == 3) or
                            (face == 'D' and square == 7) or
                            (face == 'F' and (square == 1 or square == 7)))) or
                (i == 3 and ((face == 'F' and square == 3) or
                            (face == 'B' and square == 3) or
                            (face == 'D' and square == 3) or
                            (face == 'L' and (square == 1 or square == 7)))) or
                (i == 5 and ((face == 'F' and square == 5) or
                            (face == 'B' and square == 5) or
                            (face == 'D' and square == 5) or
                            (face == 'R' and (square == 1 or square == 7))))
            )

            # If there's a conflict => push False
            # If no conflict => push True
            my_bools.append(not conflict)

        # If ANY is True => we can do the rotation; else no
        # or if ANY is False => we can't do the rotation
        print('my_bools:', my_bools)
        return all(my_bools)
    
    def _white_f_l_corner(self):
        while self.cube['F'][6] != self.cube['F'][4] or self.cube['L'][8] != self.cube['L'][4] or self.cube['D'][6] != self.cube['D'][4]:
            needed_corners = self._find_needed_corners('F', 'left')
            print('needed_corners:', needed_corners)

            for corner in needed_corners:
                if corner[0] == 'F' and (corner[1] == 6 or corner[1] == 0):
                    while self.cube['F'][6] != self.cube['F'][4] or self.cube['L'][8] != self.cube['L'][4] or self.cube['D'][6] != self.cube['D'][4]:
                        self.mover_left(corner[0])
                        continue
                
            filtered_corners = [corner for corner in needed_corners if corner[0] not in ['B']]

            corner = filtered_corners[0]
            print('finlterd', corner)

            if corner[1] in [0,2]:
                self.rotate_face('U', 'CW')
                continue
                
            elif corner[1] == 6:
                if corner[0] == 'L':
                    self.rotate_face('B', 'CW')
                    self.rotate_face('U', 'CnW')
                    self.rotate_face('B', 'CnW')
                    self.rotate_face('U', 'CW')
                self.mover_left(corner[0])
                self.rotate_face('U', 'CW')
                continue
                    
            elif corner[1] == 8:
                if corner[0] == 'R':
                    self.rotate_face('B', 'CnW')
                    self.rotate_face('U', 'CW')
                    self.rotate_face('B', 'CW')
                    self.rotate_face('U', 'CnW')
                self.mover_right(corner[0])
                self.rotate_face('U', 'CW')
                continue

            

    def _white_f_r_corner(self):
        while self.cube['F'][8] != self.cube['F'][4] or self.cube['R'][6] != self.cube['R'][4] or self.cube['D'][8] != self.cube['D'][4]:
            needed_corners = self._find_needed_corners('F', 'right')
            print('needed_corners:', needed_corners)

            for corner in needed_corners:
                if corner[0] == 'F' and (corner[1] == 2 or corner[1] == 8):
                    while self.cube['F'][8] != self.cube['F'][4] or self.cube['R'][6] != self.cube['R'][4] or self.cube['D'][8] != self.cube['D'][4]:
                        self.mover_right(corner[0])
                        continue
                
            filtered_corners = [corner for corner in needed_corners if corner[0] not in ['B']]

            corner = filtered_corners[0]
            print('finlterd', corner)

            if corner[1] in [0,2]:
                self.rotate_face('U', 'CW')
                continue
                
            elif corner[1] == 6:
                if corner[0] == 'L':
                    self.rotate_face('B', 'CW')
                    self.rotate_face('U', 'CnW')
                    self.rotate_face('B', 'CnW')
                    self.rotate_face('U', 'CW')
                self.mover_left(corner[0])
                self.rotate_face('U', 'CW')
                continue
                    
            elif corner[1] == 8:
                if corner[0] == 'R':
                    self.rotate_face('B', 'CnW')
                    self.rotate_face('U', 'CW')
                    self.rotate_face('B', 'CW')
                    self.rotate_face('U', 'CnW')
                self.mover_right(corner[0])
                self.rotate_face('U', 'CW')
                continue

        print('2nd corner')
            
    def _white_b_l_corner(self):
        while self.cube['B'][6] != self.cube['B'][4] or self.cube['L'][6] != self.cube['L'][4] or self.cube['D'][0] != self.cube['D'][4]:
            needed_corners = self._find_needed_corners('B', 'left') #MB change to left

            print('needed_corners:', needed_corners)

            for corner in needed_corners:
                if corner[0] == 'B' and (corner[1] == 0 or corner[1] == 6):
                     while self.cube['B'][6] != self.cube['B'][4] or self.cube['L'][6] != self.cube['L'][4] or self.cube['D'][0] != self.cube['D'][4]:
                        self.mover_right(corner[0]) #MB change to left
                        continue
                
            filtered_corners = [corner for corner in needed_corners if corner[0] not in ['B']]

            corner = filtered_corners[0]
            print('finlterd', corner)

            if corner[1] in [0,2]:
                self.rotate_face('U', 'CW')
                continue
                
            elif corner[1] == 6:
                if corner[0] == 'L':
                    self.rotate_face('B', 'CW')
                    self.rotate_face('U', 'CnW')
                    self.rotate_face('B', 'CnW')
                    self.rotate_face('U', 'CW')
                self.mover_left(corner[0])
                self.rotate_face('U', 'CW')
                continue
                    
            elif corner[1] == 8:
                if corner[0] == 'R':
                    self.rotate_face('B', 'CnW')
                    self.rotate_face('U', 'CW')
                    self.rotate_face('B', 'CW')
                    self.rotate_face('U', 'CnW')
                self.mover_right(corner[0])
                self.rotate_face('U', 'CW')
                continue

        print('3rd corner')

    def _white_b_r_corner(self):
        while self.cube['B'][8] != self.cube['B'][4] or self.cube['R'][8] != self.cube['R'][4] or self.cube['D'][2] != self.cube['D'][4]:
            needed_corners = self._find_needed_corners('B', 'right')

            print('needed_corners:', needed_corners)

            for corner in needed_corners:
                if corner[0] == 'B' and (corner[1] == 2 or corner[1] == 8):
                    while self.cube['B'][8] != self.cube['B'][4] or self.cube['R'][8] != self.cube['R'][4] or self.cube['D'][2] != self.cube['D'][4]:
                        print(f"Applying mover_left to {corner}")
                        self.mover_left(corner[0])  # Perform the move
                    break  # Exit the for loop since the corner was handled

            else:
                # Filter corners not on 'B'
                filtered_corners = [corner for corner in needed_corners if corner[0] not in ['B']]

                if not filtered_corners:
                    print("No valid corners to process. Rotating U face.")
                    self.rotate_face('U', 'CW')
                    continue  # Retry the while loop

                corner = filtered_corners[0]
                print('filtered corner:', corner)

                if corner[1] in [0, 2]:
                    print("Corner in top layer; rotating U.")
                    self.rotate_face('U', 'CW')
                    continue

                elif corner[1] == 6:
                    if corner[0] == 'L':
                        print("Handling corner on L6.")
                        self.rotate_face('B', 'CW')
                        self.rotate_face('U', 'CnW')
                        self.rotate_face('B', 'CnW')
                        self.rotate_face('U', 'CW')
                    print(f"Applying mover_left to {corner}")
                    self.mover_left(corner[0])
                    self.rotate_face('U', 'CW')
                    continue

                elif corner[1] == 8:
                    if corner[0] == 'R':
                        print("Handling corner on R8.")
                        self.rotate_face('B', 'CnW')
                        self.rotate_face('U', 'CW')
                        self.rotate_face('B', 'CW')
                        self.rotate_face('U', 'CnW')
                    print(f"Applying mover_right to {corner}")
                    self.mover_right(corner[0])
                    self.rotate_face('U', 'CW')
                    continue

            print('4th corner solved.')


    def _find_needed_corners(self, target_face, corner):
        left_mapper = {'F': 'L', 'L': 'B', 'B': 'L', 'R': 'F'}
        right_mapper = {'F': 'R', 'R': 'B', 'B': 'R', 'L': 'F'}

        side_mapper = {6:'left', 8:'right', 0:'left', 2:'right'}

        up_or_down_mapper = {6:'D', 8:'D', 0:'U', 2:'U'}

        square_mapper = {6:8, 8:6, 0:2, 2:0}
        back_square_mapper = {0:0,6:6,2:2,8:8}

        updown_square_mapper = {'F': {6:6, 8:8, 0:6, 2:8}, 'L': {6:0, 8:6, 0:0, 2:6}, 'R': {6:8, 8:2, 0:8, 2:2}, 'B': {6:0, 8:2, 0:0, 2:2}}

        target_mapper = left_mapper[target_face] if corner=='left' else right_mapper[target_face]

        target_color_map = set([self.cube[target_face][4], self.cube[target_mapper][4], self.cube["D"][4]])
        print('target_color_map:', target_color_map)

        needed_corners = []

        for face, squares in self.cube.items():
            if face not in ['U', 'D']:
                print('face:', face)
                squares_of_interest = {i:squares[i] for i in [0, 2, 6, 8]}
                print('squares_of_interest:', squares_of_interest)
                for square, _ in squares_of_interest.items():
                    up_or_down = up_or_down_mapper[square]
                    print('up_or_down:', up_or_down)
                    correct_mapper = left_mapper[face] if side_mapper[square]=='left' else right_mapper[face]
                    if correct_mapper == 'B' or face == 'B':
                        adjacent_square = back_square_mapper[square]
                        print('adjacent_square:', adjacent_square)
                    else:
                        adjacent_square = square_mapper[square]
                        print('adjacent_square:', adjacent_square)
                    
                    updown_adjacent_square = updown_square_mapper[face][square]

                    print('correct_mapper:', correct_mapper)
                    if set([self.cube[face][square], self.cube[correct_mapper][adjacent_square], self.cube[up_or_down][updown_adjacent_square]]) == target_color_map:
                        needed_corners.append((face, square))
        return needed_corners
                

    def white_corners(self):
        self._white_f_l_corner()
        self._white_f_r_corner()
        self._white_b_l_corner()
        self._white_b_r_corner()

    def _all_white_corners_solved(self):
        """Check if all white corners are correctly placed."""
        corners = [
            [self.cube['F'][6], self.cube['L'][8], self.cube['D'][6]],
            [self.cube['F'][8], self.cube['R'][6], self.cube['D'][8]],
            [self.cube['B'][6], self.cube['L'][0], self.cube['D'][0]],
            [self.cube['B'][8], self.cube['R'][0], self.cube['D'][2]],
        ]
        targets = [
            [self.cube['F'][4], self.cube['L'][4], self.cube['D'][4]],
            [self.cube['F'][4], self.cube['R'][4], self.cube['D'][4]],
            [self.cube['B'][4], self.cube['L'][4], self.cube['D'][4]],
            [self.cube['B'][4], self.cube['R'][4], self.cube['D'][4]],
        ]
        return all(sorted(corner) == sorted(target) for corner, target in zip(corners, targets))


    def mover_right(self, face):
        mapper = {'F': 'R', 'R': 'B', 'B': 'L', 'L': 'F'}
        self.rotate_face(mapper[face], 'CW')
        self.rotate_face('U', 'CW')
        self.rotate_face(mapper[face], 'CnW')
        self.rotate_face('U', 'CnW')

    def mover_left(self, face):
        mapper = {'F': 'L', 'L': 'B', 'B': 'R', 'R': 'F'}
        self.rotate_face(mapper[face], 'CnW')
        self.rotate_face('U', 'CnW')
        self.rotate_face(mapper[face], 'CW')
        self.rotate_face('U', 'CW')
    
    def new_mover_right(self, face): 
        if face == 'R':
            self.rotate_face('B', 'CnW')
            self.rotate_face('U', 'CW')
            self.rotate_face('B', 'CW')
            self.rotate_face('U', 'CnW')
        # elif face == 'F':
        #     self.rotate_face('R', 'CnW')
        #     self.rotate_face('U', 'CW')
        #     self.rotate_face('R', 'CW')
        #     self.rotate_face('U', 'CnW') 
        else:
            mapper = {'L': 'F', 'B': 'L', 'F': 'R'}
    
            self.rotate_face(mapper[face], 'CW')
            self.rotate_face('U', 'CW')
            self.rotate_face(mapper[face], 'CnW')
            self.rotate_face('U', 'CnW')
            

    def new_mover_left(self, face):
        if face == 'L':
            self.rotate_face('B', 'CW')
            self.rotate_face('U', 'CnW')
            self.rotate_face('B', 'CnW')
            self.rotate_face('U', 'CW')
        # elif face == 'B':
        #     self.rotate_face('R', 'CW')
        #     self.rotate_face('U', 'CnW')
        #     self.rotate_face('R', 'CnW')
        #     self.rotate_face('U', 'CW')
        else:
            mapper = {'F': 'L', 'R': 'F', 'B': 'R'}

            self.rotate_face(mapper[face], 'CnW')
            self.rotate_face('U', 'CnW')
            self.rotate_face(mapper[face], 'CW')
            self.rotate_face('U', 'CW')


    def second_layer(self):
        while True:
            second_layer_squares = self.find_second_layer()
            if len(second_layer_squares) == 0:
                break

            mapper = {1: 'B', 3: 'L', 5: 'R', 7: 'F'}

            face_color_mapper = {'B': 'F', 'O': 'L', 'R': 'R', 'G': 'B'}
            rotation_mapper = {'F-R': 'CnW', 'R-B': 'CnW', 'B-L': 'CnW', 'L-F': 'CnW', 'F-L': 'CW', 'L-B': 'CW', 'B-R': 'CW', 'R-F': 'CW'}

            current_square = second_layer_squares[0]
            current_square_color = self.cube['U'][current_square[1]]
            adjacent_face = self.cube[mapper[current_square[1]]]
            adjacent_square_color = adjacent_face[1]
            print('current_square:', current_square)
            print('adjacent_square:', adjacent_square_color)

            face_to_rotate = face_color_mapper[adjacent_square_color]
            from_where = mapper[current_square[1]] 

            path = f'{from_where}-{face_to_rotate}'
            if path in ['F-B', 'B-F', 'L-R', 'R-L']:
                self._adjust_second_layer('doesnt matter', 2)
            elif path in rotation_mapper.keys():
                rotation = rotation_mapper[path]
                self._adjust_second_layer(rotation, 1)
            
            print('current_square_color:', current_square_color)
            print('face_to_rotate:', face_to_rotate)
            self._move_opposite_way(current_square_color, face_to_rotate)
    

    def _adjust_second_layer(self, rotation, times):
        if times == 2:
            self.rotate_face('U', 'CW')
            self.rotate_face('U', 'CW')
        else:
            self.rotate_face('U', rotation)

    def _move_opposite_way(self, top_color, face):
        neighbors = {'F': ['L','R'], 'L': ['B','F'], 'R': ['F','B'], 'B': ['R','L']}

        left_mapper = {'F': 'L', 'L': 'B', 'B': 'R', 'R': 'F'}
        right_mapper = {'F': 'R', 'R': 'B', 'B': 'L', 'L': 'F'}

        current_neighbors = neighbors[face]
        first_neighbor_color = self.cube[current_neighbors[0]][4]
        second_neighbor_color = self.cube[current_neighbors[1]][4]

        next_mover = None

        if first_neighbor_color == top_color:
            self.rotate_face('U', 'CnW')
            next_mover = 'left' 
        elif second_neighbor_color == top_color:
            self.rotate_face('U', 'CW')
            next_mover = 'right'

        left_mapper = {'F': 'L', 'L': 'B', 'B': 'R', 'R': 'F'}
        right_mapper = {'F': 'R', 'R': 'B', 'B': 'L', 'L': 'F'}

        self.new_mover_right(face) if next_mover == 'right' else self.new_mover_left(face)

        next_neighbor = left_mapper[face] if next_mover == 'left' else right_mapper[face]
        print('next_neighbor:', next_neighbor)
        self.new_mover_right(next_neighbor) if next_mover == 'left' else self.new_mover_left(next_neighbor)

    def find_second_layer(self):
        square_mapper = {1: 'B', 3: 'L', 5: 'R', 7: 'F'}

        left_mapper = {'F': 'L', 'L': 'B', 'B': 'R', 'R': 'F'}
        right_mapper = {'F': 'R', 'R': 'B', 'B': 'L', 'L': 'F'}

        return_squares = []

        for face, squares in self.cube.items():
            if face == 'U':
                squares_of_interest = {i: squares[i] for i in [1, 3, 5, 7]}
                for square, color in squares_of_interest.items():
                    adjacent_square = self.cube[square_mapper[square]][1]
                    if color != 'Y' and adjacent_square != 'Y':
                        
                        return_squares.append((face, square))
        
        arg1, arg2 = self._verify_all_second_layer()
        if len(return_squares) == 0:
            if arg1 == 'left':
                next_face = left_mapper[arg2]
                self.new_mover_left(arg2)
                self.new_mover_right(next_face)
                return self.find_second_layer()
                
            elif arg1 == 'right':
                next_face = right_mapper[arg2]
                self.new_mover_right(arg2)
                self.new_mover_left(next_face)
                return self.find_second_layer()

            else:
                return return_squares

        return return_squares


    def _verify_all_second_layer(self):
        """
        Return:
        ('left', face)  if face has mismatch in square[3] 
        ('right', face) if face has mismatch in square[5]
        (True, None)    if all second-layer edges match their centers
        """
        for face in ['L', 'F', 'R', 'B']:
            # Check left edge
            if self.cube[face][3] != self.cube[face][4]:
                return 'left', face
            # Check right edge
            if self.cube[face][5] != self.cube[face][4]:
                return 'right', face

        # If the loop finishes, all second-layer edges match
        return True, None
    
    def yellow_cross(self):
        """
        Repeatedly checks which top pattern we have and applies
        the F (R U R' U') F' trigger (possibly with extra U-rotations)
        until all four U edges (U[1], U[3], U[5], U[7]) are yellow.
        """
        # Keep going until we have a full yellow cross on top.
        while not self._is_yellow_cross_formed():

            # 1) If it's a DOT, apply the trigger once
            #    -> dot becomes an L-shape
            if self._is_dot():
                self._do_frurufp()

            # 2) If it's an L-SHAPE, orient the L so it's in the "top-left" corners
            #    i.e., we want U[1] and U[3] to be yellow before we do the trigger.
            elif self._is_l_shape():
                # Rotate U until L is in top-left
                # That means (U[1], U[3]) both == 'Y'
                while not (self.cube['U'][1] == 'Y' and self.cube['U'][3] == 'Y'):
                    self.rotate_face('U','CW')
                self._do_frurufp()

            # 3) If it's a LINE, orient the line horizontally
            #    i.e., U[3] and U[5] are 'Y', then do the trigger
            elif self._is_line():
                # Rotate U until line is horizontal (U[3], U[5])
                while not (self.cube['U'][3] == 'Y' and self.cube['U'][5] == 'Y'):
                    self.rotate_face('U','CW')
                self._do_frurufp()

            else:
                # If we get here, we might have some other weird arrangement or partial cross.
                # Safest approach: just do the standard trigger once, then re-check.
                self._do_frurufp()

        print("Yellow cross completed!")

    def _is_yellow_cross_formed(self) -> bool:
        """
        Returns True if the 4 edges of U are yellow (i.e., U[1], U[3], U[5], U[7]).
        """
        return all(self.cube['U'][i] == 'Y' for i in [1, 3, 5, 7])

    def _is_dot(self) -> bool:
        """
        True if only the center (U[4]) is yellow (none of the edges on U).
        """
        return all(self.cube['U'][i] != 'Y' for i in [1, 3, 5, 7])

    def _is_line(self) -> bool:
        """
        True if exactly 2 opposite edges are yellow, e.g. U[3] & U[5] (horizontal)
        or U[1] & U[7] (vertical).
        """
        edges = [i for i in [1, 3, 5, 7] if self.cube['U'][i] == 'Y']
        if len(edges) != 2:
            return False
        # Opposite edges pairs: (1,7) => vertical line, (3,5) => horizontal line
        edges.sort()
        return edges == [1, 7] or edges == [3, 5]

    def _is_l_shape(self) -> bool:
        """
        True if exactly 2 adjacent edges on U are yellow.
        Valid adjacency pairs: (1,3), (3,7), (7,5), (5,1).
        """
        edges = [i for i in [1, 3, 5, 7] if self.cube['U'][i] == 'Y']
        if len(edges) != 2:
            return False

        valid_pairs = [{1, 3}, {3, 7}, {7, 5}, {5, 1}]
        return set(edges) in valid_pairs

    def _do_frurufp(self):
        """
        Performs the standard F (R U R' U') F' algorithm in code.
        This is the key "trigger" used to go from dot->L, L->line, line->cross.
        """
        # F
        self.rotate_face('F','CW')
        # (R U R' U')
        self.rotate_face('R','CW')
        self.rotate_face('U','CW')
        self.rotate_face('R','CnW')
        self.rotate_face('U','CnW')
        # F'
        self.rotate_face('F','CnW')

    def align_squares(self):
        while not self._all_4_aligned() and not self._aligned_2():
            self.rotate_face('U', 'CW')

    def _all_4_aligned(self):
        return all(self.cube[i][1] == self.cube[i][4] for i in ['F', 'L', 'R', 'B'])
    
    def _aligned_2(self):
        return sum(self.cube[i][1] == self.cube[i][4] for i in ['F', 'B', 'L', 'R']) == 2


    def align_all_4(self):
        self.align_squares()
        while not self._all_4_aligned():
            start_face = self._identify_start_face()
            right_mapper = {'F': 'R', 'B': 'L', 'L': 'F'}
            if start_face == 'R':
                self.rotate_face('B', 'CnW')
                self.rotate_face('U', 'CW')
                self.rotate_face('B', 'CW')
                self.rotate_face('U', 'CW')
                self.rotate_face('B', 'CnW')
                self.rotate_face('U', 'CnW')
                self.rotate_face('U', 'CnW')
                self.rotate_face('B', 'CW')
                self.align_squares()
            else:
                self.rotate_face(right_mapper[start_face], 'CW')
                self.rotate_face('U', 'CW')
                self.rotate_face(right_mapper[start_face], 'CnW')
                self.rotate_face('U', 'CW')
                self.rotate_face(right_mapper[start_face], 'CW')
                self.rotate_face('U', 'CnW')
                self.rotate_face('U', 'CnW')
                self.rotate_face(right_mapper[start_face], 'CnW')
                self.align_squares()


    def _identify_start_face(self):
        aligned_squares = []
        for face in ['F', 'L', 'R', 'B']:
            if self.cube[face][1] == self.cube[face][4]:
                aligned_squares.append(face)
        combined_squares = ''.join(aligned_squares)
        mapper = {'FL': 'B', 'FR': 'L', 'BL': 'R', 'BR': 'F', 'LF': 'B', 'RF': 'L', 'LB': 'R', 'RB': 'F'}
        if combined_squares in mapper.keys():
            return mapper[combined_squares]
        else:
            return 'F'
        
    def align_corners(self):
        print('correct corners')
        left_mapper = {'F': 'L', 'L': 'B', 'B': 'R', 'R': 'F'}
        right_mapper = {'F': 'R', 'R': 'B', 'B': 'L', 'L': 'F'}
        while len(self._count_correct_corners()) < 4:
            print('len', len(self._count_correct_corners()))
            
            if len(self._count_correct_corners()) == 0:
                self.rotate_face('U', 'CW')
                self.rotate_face('R', 'CW')
                self.rotate_face('U', 'CnW')
                self.rotate_face('L', 'CnW')
                self.rotate_face('U', 'CW')
                self.rotate_face('R', 'CnW')
                self.rotate_face('U', 'CnW')
                self.rotate_face('L', 'CW')
                continue
                
                    
            adjusted_face = None        
            for face, square in self._count_correct_corners().items():
                print('face:', face)
                print('square:', square)
                adjusted_face = self._adjust_from_right({face:square})
                print('adjusted_face:', adjusted_face)
                if adjusted_face is not None:
                    break

            if adjusted_face is not None:
                if adjusted_face == 'R':
                    self.rotate_face('U', 'CW')
                    self.rotate_face('B', 'CnW')
                    self.rotate_face('U', 'CnW')
                    self.rotate_face('F', 'CnW')
                    self.rotate_face('U', 'CW')
                    self.rotate_face('B', 'CW')
                    self.rotate_face('U', 'CnW')
                    self.rotate_face('F', 'CW')
                    print('right')
                elif adjusted_face == 'L':
                    self.rotate_face('U', 'CW')
                    self.rotate_face('F', 'CW')
                    self.rotate_face('U', 'CnW')
                    self.rotate_face('B', 'CW')
                    self.rotate_face('U', 'CW')
                    self.rotate_face('F', 'CnW')
                    self.rotate_face('U', 'CnW')
                    self.rotate_face('B', 'CnW')
                else:
                    self.rotate_face('U', 'CW')
                    self.rotate_face(right_mapper[adjusted_face], 'CW')
                    self.rotate_face('U', 'CnW')
                    self.rotate_face(left_mapper[adjusted_face], 'CnW')
                    self.rotate_face('U', 'CW')
                    self.rotate_face(right_mapper[adjusted_face], 'CnW')
                    self.rotate_face('U', 'CnW')
                    self.rotate_face(left_mapper[adjusted_face], 'CW')
                    print('else')
            else:   
                continue
        print('we have', len(self._count_correct_corners()))
    def _count_correct_corners(self):
        mapper = {'F':{0:'L', 2:'R'}, 'L':{0:'B', 2:'F'}, 'R':{0:'F', 2:'B'}, 'B':{0:'L', 2:'R'}}
        
        top_mapper = {'F':{0:6, 2:8}, 'L':{0:0, 2:6}, 'R':{0:8, 2:2}, 'B':{0:0, 2:2}}
        correct_corners = {}
        for face, squares in self.cube.items():
            if face not in ['U', 'D']:
                squares_of_interest = {i: squares[i] for i in [0,2]}
                for square, color in squares_of_interest.items():
                    
                    current_face_color = self.cube[face][4]
                    top_face_color = self.cube['U'][4]
                    adjacent_face = mapper[face][square]
                    adjacent_face_color = self.cube[adjacent_face][4]
                    # print('adjacent_face_color:', adjacent_face_color)
                    # print('current_face_color:', current_face_color)
                    # print('top_face_color:', top_face_color)

                    current_square_color = self.cube[face][square]
                    adjacent_face_square = [square for square in [0,2] if mapper[adjacent_face][square] == face][0]

                    adjacent_square_color = self.cube[adjacent_face][adjacent_face_square]
                    top_face_square = top_mapper[face][square]
                    top_square_color = self.cube['U'][top_face_square]
                    # print('adjacent_square_color:', adjacent_square_color)
                    # print('current_square_color:', current_square_color)
                    # print('top_square_color:', top_square_color)

                    if set([current_face_color, adjacent_face_color, top_face_color]) == set([current_square_color, adjacent_square_color, top_square_color]):
                        correct_corners[face] = square
        return correct_corners
    
    def _adjust_from_right(self, face_square=dict):
        side_mapper = {'F': {0: 'L', 2: 'R'}, 'L': {0: 'L', 2: 'R'}, 'R': {0: 'L', 2: 'R'}, 'B': {0: 'R', 2: 'L'}}
        for face, square in face_square.items():
            if side_mapper[face][square] == 'R':
                return face
        return None
    
    def mover_right_upside_down(self):
        self.rotate_face('L', 'CW')
        self.rotate_face('D', 'CnW')
        self.rotate_face("L", 'CnW')
        self.rotate_face('D', 'CW')

    def _cube_solved(self):
        for _, squares in self.cube.items():
            if len(set(squares)) != 1:
                return False
        return True

    def finish_cube(self):
        counter = 0
        while True:
            # Every iteration, read the *updated* colors from self.cube
            current_front_color = self.cube['F'][1]
            adjacent_face_color = self.cube['L'][1]
            top_face_color = 'Y'  # or self.cube['U'][4] if you prefer to read center color

            current_square_color = self.cube['F'][0]
            adjacent_square_color = self.cube['L'][2]
            top_square_color = self.cube['U'][6]

            if self._cube_solved():
                print("Cube solved!")
                break

            # Check if the condition is satisfied
            if (current_front_color == current_square_color 
            and adjacent_face_color == adjacent_square_color
            and top_face_color == top_square_color):
                self.rotate_face('U', 'CW')
                continue

            self.mover_right_upside_down()
            counter += 1
            if counter == 30:
                print("Exiting after 30 tries (avoid infinite loop).")
                break

    def solve(self):
        self.white_cross()
        self.white_corners()
        self.second_layer()
        self.yellow_cross()
        self.align_all_4()
        self.align_corners()
        self.finish_cube()
            
    @staticmethod
    def optimize_steps(steps):
        """
        Repeatedly scans self.steps, removing:
        - pairs of moves that cancel each other out (e.g. (R,CW), (R,CnW)),
        - triple identical moves (3 in a row => 1 opposite),
        - quadruple identical moves (4 in a row => remove entirely).
        Continues until no more changes can be done.
        """
        opposite = {'CW': 'CnW', 'CnW': 'CW'}
        changed = True

        while changed:
            changed = False

            # --- 1) Remove PAIRS THAT CANCEL EACH OTHER OUT ---
            i = 0
            new_steps = []
            while i < len(steps):
                if i < len(steps) - 1:
                    face1, dir1 = steps[i]
                    face2, dir2 = steps[i+1]
                    # If same face and directions are opposite => remove both
                    if face1 == face2 and ((dir1 == 'CW' and dir2 == 'CnW') or
                                        (dir1 == 'CnW' and dir2 == 'CW')):
                        # Skip them (i.e., pop both)
                        i += 2
                        changed = True
                        continue
                # If we didn't remove them, keep the current move
                new_steps.append(steps[i])
                i += 1
            steps = new_steps

            # --- 2) Replace TRIPLE identical moves with 1 opposite move ---
            i = 0
            new_steps = []
            while i < len(steps):
                if i < len(steps) - 2:
                    face1, dir1 = steps[i]
                    face2, dir2 = steps[i+1]
                    face3, dir3 = steps[i+2]
                    if face1 == face2 == face3 and dir1 == dir2 == dir3:
                        # E.g. three times (R, 'CW') => (R, 'CnW') once
                        new_steps.append((face1, opposite[dir1]))
                        i += 3
                        changed = True
                        continue
                # Otherwise keep the current move
                new_steps.append(steps[i])
                i += 1
            steps = new_steps

            # --- 3) Remove QUADRUPLE identical moves entirely ---
            i = 0
            new_steps = []
            while i < len(steps):
                if i < len(steps) - 3:
                    face1, dir1 = steps[i]
                    face2, dir2 = steps[i+1]
                    face3, dir3 = steps[i+2]
                    face4, dir4 = steps[i+3]
                    if (face1 == face2 == face3 == face4 and
                        dir1 == dir2 == dir3 == dir4):
                        # 4 identical moves on the same face => 360° => remove
                        i += 4
                        changed = True
                        continue
                new_steps.append(steps[i])
                i += 1

        return new_steps

            # OPTIONAL: 
            # If you want two identical moves in a row -> treat as a 180° turn,
            # you could add another pass or handle it differently.

        # End of while changed

