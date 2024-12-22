from visualizer import CubeVisualizer
from solver import CubeSolver
from PyQt5.QtWidgets import QApplication
import sys
import time

if __name__ == '__main__':
    app = QApplication(sys.argv)
    c = CubeSolver(None)
    c.initialize_cube()
    c.scramble()
    # window = CubeVisualizer(c.cube,title='ver1')
    # window.show()
    # app.exec_()
    # time.sleep(3)
    # window.close()
    # # c.rotate_face('L','CW')
    # # c.rotate_face('D','CnW')
    # window = CubeVisualizer(c.cube,title='ver1')
    # window.show()
    # app.exec_()
    # time.sleep(3)
    # window.close()
    # window = CubeVisualizer(c.cube,title='ver1')
    # window.show()

    while len(c.white_sides['U']) != 4:
        window = CubeVisualizer(c.cube, title='ver1')
        window.show()
        app.exec_()
        window.close()
        c.white_cross() 
        window = CubeVisualizer(c.cube, title='ver1')
        window.show()
        app.exec_()
        window.close()
        break

    # c.white_corners()
    # window = CubeVisualizer(c.cube, title='ver1')
    # window.show()  
    # app.exec_()
    # window.close()

    # print(c.steps)
    c.optimize_steps()
 
    # window = CubeVisualizer(c.cube,title='ver2')
    # window.show()
