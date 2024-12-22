import copy
import random
from decorators import update_white_sides_after
class CubeSolver( ):
    def __init__( self, cube ):
        self.cube = cube
        self.initialize_cube()
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

    def solve( self ):
        pass

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
        while self.cube['F'][1] != 'B' and self.cube['U'][7] != 'W':
            self.cube = self.rotate_face('U', 'CW')
        self.cube =self.rotate_face('F', 'CW')
        self.cube =self.rotate_face('F', 'CW')
        print('finished front side')
    
    def _solve_right_side(self):
        while self.cube['R'][1] != 'R' and self.cube['U'][5] != 'W':
            self.cube =self.rotate_face('U', 'CW')
        self.cube =self.rotate_face('R', 'CW')
        self.cube =self.rotate_face('R', 'CW')
        print('finished right side')
    
    def _solve_left_side(self):
        while self.cube['L'][1] != 'O' and self.cube['U'][3] != 'W':
            self.cube = self.rotate_face('U', 'CW')
        self.cube =self.rotate_face('L', 'CW')
        self.cube =self.rotate_face('L', 'CW')
        print('finished left side')
    
    def _solve_back_side(self):
        while self.cube['B'][1] != 'G' and self.cube['U'][1] != 'W':
            self.cube =self.rotate_face('U', 'CW')
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
    
    def optimize_steps(self):
        for i in range(len(self.steps)-1):
            try:
                if self.steps[i][0] == self.steps[i+1][0] == self.steps[i+3][0] and self.steps[i][1] == self.steps[i+1][1] == self.steps[i+3][1]:
                        self.steps.pop(i)
                        self.steps.pop(i)
                        self.steps.pop(i)
                        mapper = {'CW': 'CnW', 'CnW': 'CW'}
                        self.steps.append((self.steps[i][0], mapper[self.steps[i][1]]))
                        break
            except IndexError:
                break

    def _white_f_l_corner(self):
        print(f'the corner is in {self._find_needed_corners("F", "left")}')
        # if set([self.cube['F'][6], self.cube['L'][8], self.cube['D'][6]]) != set([self.cube['F'][4], self.cube['D'][4], self.cube['L'][4]]):
        #     pass
        # else:
        #     while self.cube['F'][6] != self.cube['F'][4] and self.cube['L'][8] != self.cube['L'][4] and self.cube['D'][6] != self.cube['D'][4]:
        #         self.mover_left()

        #     while set([self.cube['F'][0], self.cube['U'][6], self.cube['L'][2]]) != set([self.cube['F'][4], self.cube['D'][4], self.cube['L'][4]]):
        #         self.rotate_face('U', 'CW')
        #     while self.cube['F'][6] != self.cube['F'][4] and self.cube['L'][8] != self.cube['L'][4] and self.cube['D'][6] != self.cube['D'][4]:
        #         self.mover_left()
        #     print('1st corner')

    def _white_f_r_corner(self):
            if set([self.cube['F'][2], self.cube['U'][8], self.cube['R'][0]]) != set([self.cube['F'][4], self.cube['D'][4], self.cube['R'][4]]):
                self.mover_right()
                while set([self.cube['F'][0], self.cube['U'][6], self.cube['L'][2]]) != set([self.cube['F'][4], self.cube['D'][4], self.cube['L'][4]]):
                    self.rotate_face('U', 'CW')
                while self.cube['F'][8] != self.cube['F'][4] and self.cube['R'][6] != self.cube['R'][4] and self.cube['D'][8] != self.cube['D'][4]:
                    self.mover_right()
                print('2nd corner')
    
    def _white_b_l_corner(self):
        pass
    def _white_b_r_corner(self):
        pass

    def _find_needed_corners(self, target_face, corner):
        left_mapper = {'F': 'L', 'L': 'B', 'B': 'R', 'R': 'F'}
        right_mapper = {'F': 'R', 'R': 'B', 'B': 'L', 'L': 'F'}

        side_mapper = {6:'left', 8:'right', 0:'left', 2:'right'}

        up_or_down_mapper = {6:'D', 8:'D', 0:'U', 2:'U'}

        square_mapper = {6:8, 8:6, 0:2, 2:0}



        target_mapper = left_mapper[target_face] if corner=='left' else right_mapper[target_face]

        target_color_map = set([self.cube[target_face][4], self.cube[target_mapper][4], self.cube["D"][4]])
        print('target_color_map:', target_color_map)

        for face, squares in self.cube.items():
            if squares in [0,2,6,8]:
                for square in squares:
                    up_or_down = up_or_down_mapper[square]
                    correct_mapper = left_mapper[face] if side_mapper[square]=='left' else right_mapper[face]
                    if set([self.cube[face][square], self.cube[correct_mapper][square_mapper[square_mapper]], self.cube[up_or_down][square_mapper[square]]]) == target_color_map:
                        return face, square
                

            

    def white_corners(self):
        # while not self._all_white_corners_solved():
        #     if [self.cube['F'][0], self.cube['U'][6], self.cube['L'][2]] == [self.cube['F'][4], self.cube['D'][4], self.cube['L'][4]]:
        #         print('1st corner')
        #         while self.cube['F'][6] != self.cube['F'][4] and self.cube['L'][8] != self.cube['L'][4] and self.cube['D'][6] != self.cube['D'][4]:
        #             self.mover_left()

        #     elif [self.cube['F'][2], self.cube['U'][8], self.cube['R'][0]] == [self.cube['F'][4], self.cube['D'][4], self.cube['R'][4]]:
        #         print('2nd corner')
        #         while self.cube['F'][8] != self.cube['F'][4] and self.cube['R'][6] != self.cube['R'][4] and self.cube['D'][8] != self.cube['D'][4]:
        #             self.mover_right()

        #     elif [self.cube['B'][0], self.cube['U'][0], self.cube['L'][6]] == [self.cube['B'][4], self.cube['D'][4], self.cube['L'][4]]:
        #         print('3rd corner')
        #         while self.cube['B'][6] != self.cube['B'][4] and self.cube['L'][0] != self.cube['L'][4] and self.cube['D'][0] != self.cube['D'][4]:
        #             self.mover_left()

        #     elif [self.cube['B'][2], self.cube['U'][2], self.cube['R'][8]] == [self.cube['B'][4], self.cube['D'][4], self.cube['R'][4]]:
        #         print('4th corner')
        #         while self.cube['B'][8] != self.cube['B'][4] and self.cube['R'][0] != self.cube['R'][4] and self.cube['D'][2] != self.cube['D'][4]:
        #             self.mover_right()

        #     self.rotate_face('U', 'CW')
        self._white_f_l_corner()
        # self._white_f_r_corner()
        # self._white_b_l_corner()
        # self._white_b_r_corner()

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


    def mover_right(self):
        self.rotate_face('R', 'CW')
        self.rotate_face('U', 'CW')
        self.rotate_face('R', 'CnW')
        self.rotate_face('U', 'CnW')

    def mover_left(self):
        self.rotate_face('L', 'CnW')
        self.rotate_face('U', 'CnW')
        self.rotate_face('L', 'CW')
        self.rotate_face('U', 'CW') 




# myCube = Cube( None )
# myCube.initialize_cube( )
# print( myCube.cube )
# myCube.cube = Cube.rotate_face('U', myCube.cube, 'CW')
# print( myCube.cube )