from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import random

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random
     
class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("c:\workspace\Sort-and-Shuffle\youtube\qt_designer.ui",self)

        # self.setWindowIcon("")
        self.initial_graph()
        self.MplWidget.canvas.axes.get_xaxis().set_visible(False)

        self.spnBars.valueChanged.connect(self.change_graph)

        self.btn_Scramble.clicked.connect(self.scramble_bars)


    def scramble_bars(self):
        self.MplWidget.canvas.axes.clear()

        bar_count = self.spnBars.value()
        
        scram_xs = [i for i in range(1, bar_count +1)]
        ys = scram_xs.copy()
        for j in range(0, len(scram_xs)-1):
            target = random.randint(j, len(scram_xs)-1)
            scram_xs[j] , scram_xs[target] = scram_xs[target], scram_xs[j]

        self.draw_graph(scram_xs, ys)


    def change_graph(self):
        self.MplWidget.canvas.axes.clear()

        bar_count = self.spnBars.value()
        xs = [i for i in range(1, bar_count +1)]
        ys = xs.copy()
        self.draw_graph(xs,ys)
        

    def initial_graph(self):
        self.change_graph()


    def draw_graph(self, xs, ys):
        self.MplWidget.canvas.axes.bar(xs, ys, color = "#00A7E1")
        self.MplWidget.canvas.draw()




app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()