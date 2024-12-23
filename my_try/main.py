from visualizer import CubeVisualizer
from solver import CubeSolver
from PyQt5.QtWidgets import QApplication
import sys
import time

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

    c.white_corners()
    print('second layer',c.find_second_layer())
    window = CubeVisualizer(c.cube, title='ver1')
    window.show()  
    app.exec_()
    window.close() 

    c.second_layer()
    c.yellow_cross()
    c.align_all_4() 
    c.align_corners()
    window = CubeVisualizer(c.cube, title='ver1')
    window.show()  
    app.exec_()
    window.close()
    c.finish_cube()
    

    # c.second_layer()
    window = CubeVisualizer(c.cube, title='ver1')
    window.show()
    app.exec_()
    window.close()

    # print(c.steps)    window = CubeVisualizer(c.cube, title='ver1')

    c.optimize_steps()
 
    # window = CubeVisualizer(c.cube,title='ver2')
    # window.show()
 