from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.uic import loadUi
import random
import time

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random
     
class MatplotlibWidget(QMainWindow):

    # Declare class var
    xdata = None
    ydata = None
    t = 0.01

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

        # Update Graph when spin-box is changed
        self.spnBars.valueChanged.connect(self.update_new_graph)

        # Call scramble method when clicked
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
        
        # Send scrambled data to class var
        self.ydata = scram_ys.copy()
        self.xdata = xs.copy()

        # Draw new data onto graph
        self.draw_graph(xs, scram_ys, None)


    def update_new_graph(self):
        # Update canvas on change event from the spin edit
        self.MplWidget.canvas.axes.clear()

        # Create new dataset with changed size
        bar_count = self.spnBars.value()
        ys = [i for i in range(1, bar_count +1)]
        xs = ys.copy()

        # Send data to class var
        self.ydata = ys.copy()
        self.xdata = xs.copy()

        # Draw new data onto graph
        self.draw_graph(xs, ys, None)
        

    def initial_graph(self):
        # Startup with bars, not empty graph
        self.update_new_graph()


    def draw_graph(self, xs, ys, bar_color):
        # Draw graph from x-list and y-list
        if bar_color is None:
            self.MplWidget.canvas.axes.bar(xs, ys, color = "#00A7E1")
        else:
            # Color parameter will highlight selected bar (Bar that is being moved)
            self.MplWidget.canvas.axes.bar(xs, ys, color = bar_color)

        self.MplWidget.canvas.draw()


    def bubble_sort(self):
        # Copy dataset
        yarray = self.ydata

        # Loop through all elements
        for i in range(len(yarray)):
            # Determine new endpoint as last i elements will be sorted (efficientcy)
            endp = len(yarray) - i
            
            # Iterate over new resized dataset
            for j in range(0 , endp):
                
                # Prevent loop reaching out of list
                if j+1 == len(yarray):
                    pass
                else:
                    if yarray[j] > yarray[j+1]:

                        # Swap elements if not ascending 
                        yarray[j], yarray[j+1] = yarray[j+1], yarray[j]

                        # Update class var
                        self.ydata = yarray

                        # Sleep to create a more pleasing animation
                        # time.sleep(0.001)
                        self.MplWidget.canvas.axes.clear()

                        # Create colour list to indicate which bar is highlighted
                        bar_color = ["#00A7E1"] * (len(yarray)-1)
                        bar_color.insert(j+1,"#ffa500")
                        self.draw_graph(self.xdata, self.ydata, bar_color)

                        # Process pending envents for the MPL graph
                        QtCore.QCoreApplication.processEvents()
                    else:
                        # Pass if 2 comparing data is in ascending order
                        pass
                    
                               
    def ani_time(self):
        # Determine sort wait time scaled to bars amount
        if self.ydata:
            return 1/(2*len(self.ydata))


app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()