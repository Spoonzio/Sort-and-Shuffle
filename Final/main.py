from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import random
import time

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random
     
class MatplotlibWidget(QMainWindow):

    scrambled = None
    xdata = None
    ydata = None

    def __init__(self):
        # Constructor
        QMainWindow.__init__(self)

        # Read UI
        loadUi("C:\workspace\Sort-and-Shuffle\Final\qt_designer.ui",self)
        
        # self.setWindowIcon("icon.png")
        self.initial_graph()
        self.MplWidget.canvas.axes.get_xaxis().set_visible(False)

        # Connect methods to buttons :
        self.btn_Bubble.clicked.connect(self.bubble_sort)
        # self.btn_Insertion.clicked.connect()
        # self.btn_Merge.clicked.connect()
        # self.btn_Quick.clicked.connect()

        self.spnBars.valueChanged.connect(self.update_new_graph)

        self.btn_Scramble.clicked.connect(self.scramble_bars)

    def scramble_bars(self):
        # Scramble bars in canvas
        self.MplWidget.canvas.axes.clear()

        bar_count = self.spnBars.value()
        
        scram_ys = [i for i in range(1, bar_count +1)]
        xs = scram_ys.copy()
        
        for j in range(0, len(scram_ys)-1):
            target = random.randint(j, len(scram_ys)-1)
            scram_ys[j] , scram_ys[target] = scram_ys[target], scram_ys[j]
        
        self.scrambled = True
        self.ydata = scram_ys.copy()
        self.xdata = xs.copy()

        print(self.xdata)
        print(self.ydata)
        self.draw_graph(xs, scram_ys)


    def update_new_graph(self):
        # Update canvas on change event from the spin edit
        self.MplWidget.canvas.axes.clear()

        bar_count = self.spnBars.value()
        ys = [i for i in range(1, bar_count +1)]
        xs = ys.copy()
        self.scrambled = False
        self.ydata = ys.copy()
        self.xdata = xs.copy()

        self.draw_graph(xs,ys)
        

    def initial_graph(self):
        # Startup with bars, not empty graph
        self.update_new_graph()


    def draw_graph(self, xs, ys):
        # Draw graph from x-list and y-list
        self.MplWidget.canvas.axes.bar(xs, ys, color = "#00A7E1")
        self.MplWidget.canvas.draw()


    def bubble_sort(self):
        yarray = self.ydata
        for i in range(len(yarray)):
            endp = len(yarray) - i

            for j in range(0 , endp):
                
                if j+1 == len(yarray):
                    pass
                else:
                    if yarray[j] > yarray[j+1]:
                        yarray[j], yarray[j+1] = yarray[j+1], yarray[j]

                        self.ydata = yarray
                        time.sleep(0.05)
                        self.MplWidget.canvas.axes.clear()
                        self.draw_graph(self.xdata, self.ydata)
                    
                    else:
                        pass
                    
                               
    def swap(self, v1, v2):
        return (v2, v1)



app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()