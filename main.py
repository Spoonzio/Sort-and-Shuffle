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
    loop_state = False

    def __init__(self):
        # Constructor
        QMainWindow.__init__(self)

        # Read UI
        loadUi("qt_designer.ui",self)
        
        # self.setWindowIcon("icon.png")
        self.initial_graph()
        self.MplWidget.canvas.axes.get_xaxis().set_visible(False)

        # Connect methods to buttons :
        self.btn_Bubble.clicked.connect(self.bubble_sort)
        self.btn_Insertion.clicked.connect(self.insert_sort)
        self.btn_Merge.clicked.connect(self.merge_sort)
        self.btn_Selection.clicked.connect(self.select_sort)

        # Update Graph when spin-box is changed
        self.spnBars.valueChanged.connect(self.update_new_graph)

        # Call scramble method when clicked
        self.btn_Scramble.clicked.connect(self.scramble_bars)
    
    
    def new_frame(self, highlight_bar):
         
        # Sleep to create a more pleasing animation
        time.sleep(self.ani_time())
        self.MplWidget.canvas.axes.clear()

        # Create colour list to indicate which bar is highlighted
        bar_color = ["#00A7E1"] * (len(self.ydata)-1)
        bar_color.insert(highlight_bar,"#ffa500")
        self.draw_graph(self.xdata, self.ydata, bar_color)

        # Process pending envents for the MPL graph
        QtCore.QCoreApplication.processEvents()


    def ani_time(self):
        # Determine sort wait time scaled to bars amount
        ani_speed = self.sldAnim_speed.value()

        # Linear formula that determine the sleep time from the slider value
        ani_interval = (-1/295)*ani_speed + 0.336
        return(ani_interval)
    
    
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


    def buttons(self, tfstate):
        self.btn_Bubble.setEnabled(tfstate)
        self.btn_Insertion.setEnabled(tfstate)
        self.btn_Merge.setEnabled(tfstate)
        self.btn_Selection.setEnabled(tfstate)
        self.btn_Scramble.setEnabled(tfstate)
    

    def bubble_sort(self):
        # Copy dataset
        yarray = self.ydata.copy()

        # Disable buttons
        self.buttons(False)

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

                        # Call to update graph
                        self.new_frame(j+1)

        self.buttons(True)


    def insert_sort(self):
        # Get class variable
        yarray = self.ydata.copy()

        # Disable buttons
        self.buttons(False)

        # Loop through list
        for i in range(len(yarray)):

            if (i+1) == len(yarray):
                # Prevent reading out of list
                break 
            else:
                # If pair not in ascending order
                if yarray[i] > yarray[i+1]:
                    # Using Swaping method for better animation / demostration. Delete and insert method is commented

                    # # Delete and Insert method---------------------------------------------
                    # # Read and remove
                    # temp = yarra.pop(i+1) 

                    # for j in range(i+1):
                    #     if yarray[j] > temp:
                    # 
                    #         # Find first elem that is bigger than Temp, insert at that position, shift the rest down
                    #         index = j
                    #         yarray.insert(index, temp)
                    #         self.new_frame(j)
                    #         break               
                    
                    # Swap method -----------------------------------------------------------
                    # Find the right place for the elem, from beginning till current spot in list
                    for k in reversed(range(i+1)):
                        if yarray[k+1] < yarray[k]:
                            yarray[k], yarray[k+1] = yarray[k+1] , yarray[k]

                            # Update class var
                            self.ydata = yarray

                            # Update graph
                            self.new_frame(k)
                        else:
                            break

        self.buttons(True)
         

    def merge_sort(self):
        # Get class variable
        yarray = self.ydata.copy()

        # Disable buttons
        self.disable_btn()

    
    def select_sort(self):
        # Get class variable
        yarray = self.ydata.copy()

        # Disable buttons
        self.buttons(False)

        # Loop through list
        for i in range(len(yarray)):

            #Place holder for smallest number in sublist
            holder = None

            # Iterate over unsorted sublist
            for j in range(i,len(yarray)):
                
                if (not holder):
                    holder = yarray[j]
                elif yarray[j] < holder:
                    holder = yarray[j]

                # Show iteration
                self.new_frame(j)
            

            # Read and insert lowest bar into sorted part
            shifter_index = yarray.index(holder)
            yarray.pop(shifter_index)
            yarray.insert(i, holder)

            # Update class var & graph
            self.ydata = yarray

            # Update graph
            self.new_frame(shifter_index)

        self.buttons(True)
        

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()