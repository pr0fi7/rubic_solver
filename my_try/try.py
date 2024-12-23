from visualizer import CubeVisualizer
from solver import CubeSolver
from PyQt5.QtWidgets import QApplication
import sys
import copy

if __name__ == '__main__':
    app = QApplication(sys.argv)
    c = CubeSolver(None)
    c.initialize_cube()
    # c.cube['F'] = ['B', 'Y', 'Y', 'R', 'B', 'Y', 'B', 'B', 'B']
    # c.cube['R'] = ['R', 'O', 'B', 'O', 'R', 'G', 'R', 'R', 'R']
    # c.cube['B'] = ['O', 'R', 'Y', 'B', 'G', 'Y', 'G', 'G', 'G']
    # c.cube['L'] = ['Y', 'B', 'Y', 'Y', 'O', 'G', 'O', 'O', 'O']
    # c.cube['U'] = ['G', 'B', 'O', 'O', 'Y', 'G', 'R', 'R', 'G']
    # c.cube['D'] = ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']
    c.scramble()
    temp_cube = copy.deepcopy(c.cube)

    window = CubeVisualizer(c.cube,title='ver1')
    window.show()
    app.exec_()
    window.close()
   
    c.solve()
    verified_steps = copy.deepcopy(c.steps)[20:]

    print('before optimization',len(verified_steps))
    optimized_steps = c.optimize_steps(verified_steps)
    print('after optimization',len(optimized_steps))

    window = CubeVisualizer(c.cube, title='ver1')
    window.show()
    app.exec_()
    window.close()

    c.cube = temp_cube

    window = CubeVisualizer(c.cube, title='ver1')
    window.show()
    app.exec_()
    window.close()

    for step in optimized_steps:
        c.rotate_face(step[0],step[1])

    window = CubeVisualizer(c.cube, title='ver1')
    window.show()
    app.exec_()
    window.close()

