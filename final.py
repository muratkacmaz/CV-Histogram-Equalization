#Murat Kaçmaz 150140052

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QGroupBox, QAction, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QGridLayout,QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np 
import cv2

##########################################
## Do not forget to delete "return NotImplementedError"
## while implementing a function
########################################

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.showFullScreen()
        self.LoadedTarget=None
        self.LoadedInput =None
        self.window = QWidget(self)
        self.setCentralWidget(self.window)
        self.title = 'Histogram Equalization'
        self.toolbar= self.addToolBar('Equalize Histogram')
        
        EqAction = QAction("Equalize Histogram",self)
        EqAction.triggered.connect(self.histogramButtonClicked)
        self.toolbar.addAction(EqAction)
        
        action = QAction ("&Open Input",self)
        action.triggered.connect(self.openInputImage)
        
        action2 = QAction ("&Open Target",self)
        action2.triggered.connect(self.openTargetImage)
        
        action3 = QAction ("&EX1IT",self)
        action3.triggered.connect(self.closeApp)
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(action)
        fileMenu.addAction(action2)
        fileMenu.addAction(action3)
        
        
        self.initUI()

    def openInputImage(self):
        inputLabel = QLabel('input')
        filename = QFileDialog.getOpenFileName()
        imagePath = filename[0]
       
 
        self.InputImage = cv2.imread(imagePath)
        self.LoadedInput = self.InputImage
        self.InputImage  = cv2.cvtColor(self.InputImage , cv2.COLOR_BGR2RGB)
        
        self.InputRed= self.InputImage [:,:,0]
        self.InputGreen = self.InputImage [:,:,1]
        self.InputBlue = self.InputImage [:,:,2]
        
        row,column= self.InputRed.shape  #shapeler aynı
        bytesPerLine = 3 * column
        self.redArrayInput = [0]* 256
        self.greenArrayInput = [0]* 256
        self.blueArrayInput = [0]* 256
        
        
        for c in range(0,column):
            for r in range(0,row):
                temp = self.InputRed[r][c]
                self.redArrayInput[temp]+=1
                
        for c in range(0,column):
            for r in range(0,row):
                temp = self.InputGreen[r][c]
                self.greenArrayInput[temp]+=1         
         
        for c in range(0,column):
            for r in range(0,row):
                temp = self.InputBlue[r][c]
                self.blueArrayInput[temp]+=1
        
        
        
        inputPixmap = QImage(self.InputImage.data,column,row,bytesPerLine,QImage.Format_RGB888)
        inputLabel.setPixmap(QPixmap.fromImage(inputPixmap))
        inputLabel.setAlignment(Qt.AlignCenter)
        self.inputGridBox.layout().addWidget(inputLabel)
                
        redplot = self.figureInput.add_subplot(311)
        greenplot = self.figureInput.add_subplot(312)
        blueplot = self.figureInput.add_subplot(313)
        
        redplot.bar(range(256),self.redArrayInput,color = 'red')
        greenplot.bar(range(256),self.greenArrayInput,color = 'green')
        blueplot.bar(range(256),self.blueArrayInput,color = 'blue')
        
        self.canvasInput.draw()
        self.inputGridBox.layout().addWidget(self.canvasInput)
    
        return NotImplementedError

    
    def openTargetImage(self):
        targetLabel= QLabel('target')
        filename = QFileDialog.getOpenFileName()
        imagePath = filename[0]
       
 
        self.targetImage = cv2.imread(imagePath)
        self.LoadedTarget= self.targetImage 
        self.targetImage  = cv2.cvtColor(self.targetImage , cv2.COLOR_BGR2RGB)
        
        self.TargetRed= self.targetImage [:,:,0]
        self.TargetGreen = self.targetImage [:,:,1]
        self.TargetBlue= self.targetImage [:,:,2]
        
        row,column= self.TargetRed.shape  #shapeler aynı
        bytesPerLine = 3 * column
        self.redArrayTarget = [0]* 256
        self.greenArrayTarget = [0]* 256
        self.blueArrayTarget = [0]* 256
    
    
        for c in range(0,column):
            for r in range(0,row):
                temp = self.TargetRed[r][c]
                self.redArrayTarget[temp]+=1
                
        for c in range(0,column):
            for r in range(0,row):
                temp = self.TargetGreen[r][c]
                self.greenArrayTarget[temp]+=1         
         
        for c in range(0,column):
            for r in range(0,row):
                temp = self.TargetBlue[r][c]
                self.blueArrayTarget[temp]+=1
    
        
        
        targetPixmap = QImage(self.targetImage.data,column,row,bytesPerLine,QImage.Format_RGB888)
        targetLabel.setPixmap(QPixmap.fromImage(targetPixmap))
        targetLabel.setAlignment(Qt.AlignCenter)
        self.targetGridBox.layout().addWidget(targetLabel)
        
        redplot = self.figureTarget.add_subplot(311)
        greenplot = self.figureTarget.add_subplot(312)
        blueplot = self.figureTarget.add_subplot(313)
        
        
        redplot.bar(range(256),self.redArrayTarget,color = 'red')
        greenplot.bar(range(256),self.greenArrayTarget,color = 'green')
        blueplot.bar(range(256),self.blueArrayTarget,color = 'blue')
        
        self.canvasTarget.draw()
        self.targetGridBox.layout().addWidget(self.canvasTarget)
        
        return NotImplementedError
    
    def closeApp(self):
        app.quit()
        return NotImplementedError
  
    
    

        
        
        
    def initUI(self):
        # Write GUI initialization code
        self.gLayout = QGridLayout()
        
        self.figureInput = Figure()
        self.canvasInput =FigureCanvas(self.figureInput)
        self.figureTarget = Figure()
        self.canvasTarget =FigureCanvas(self.figureTarget)
        self.figureResult = Figure()
        self.canvasResult =FigureCanvas(self.figureResult)
        
        self.inputGridBox = QGroupBox('Input')
        inputLayout = QVBoxLayout()
        self.inputGridBox.setLayout(inputLayout)
        
        self.targetGridBox = QGroupBox('Target')
        targetLayout = QVBoxLayout()
        self.targetGridBox.setLayout(targetLayout)
        
        self.resultGridBox = QGroupBox('Result')
        resultLayout = QVBoxLayout()
        self.resultGridBox.setLayout(resultLayout)
        
        self.gLayout.addWidget(self.inputGridBox, 0, 0)
        self.gLayout.addWidget(self.targetGridBox, 0, 1)
        self.gLayout.addWidget(self.resultGridBox, 0, 2)
        
        self.window.setLayout(self.gLayout)
        self.setWindowTitle(self.title)
        self.show()







    def histogramButtonClicked(self):
        
        
        if  self.LoadedInput is None and  self.LoadedTarget is None:
            QMessageBox.about(self,"Error","Load input and target images")
            return NotImplementedError
        if  self.LoadedInput is None:
            QMessageBox.about(self,"Error","Load input image")
            return NotImplementedError
        elif self.LoadedTarget is None:
           QMessageBox.about(self,"Error","Load target image")
           return NotImplementedError
        
        self.calcHistogram()
        
        
    
    
    def calcHistogram(self):
        # Calculate histogram,
        #ÖNCE CDFLER BUL VE LUT YAP HER RENK İCİN
        resultLabel= QLabel('result')
        
        sumOfRedInput =np.sum(self.redArrayInput)
        self.cdfInputRed = np.cumsum(self.redArrayInput)/sumOfRedInput
        
        sumOfGreenInput =np.sum(self.greenArrayInput)
        self.cdfInputGreen = np.cumsum(self.greenArrayInput)/sumOfGreenInput
        
        sumOfBlueInput =np.sum(self.blueArrayInput)
        self.cdfInputBlue = np.cumsum(self.blueArrayInput)/sumOfBlueInput
        
        sumOfRedTarget =np.sum(self.redArrayTarget)
        self.cdfTargetRed = np.cumsum(self.redArrayTarget)/sumOfRedTarget
        
        sumOfGreenTarget =np.sum(self.greenArrayTarget)
        self.cdfTargetGreen = np.cumsum(self.greenArrayTarget)/sumOfGreenTarget
        
        sumOfBlueTarget =np.sum(self.blueArrayTarget)
        self.cdfTargetBlue = np.cumsum(self.blueArrayTarget)/sumOfBlueTarget
        
        self.LUTRed= np.zeros((256,1))
        self.LUTGreen= np.zeros((256,1))
        self.LUTBlue= np.zeros((256,1))
        
        j=0
        for i in range(256):
            while self.cdfTargetRed[j]<self.cdfInputRed[i] and j<=255:
                j=j+1
            self.LUTRed[i]=j
        
        j=0
        for i in range(256):
            while self.cdfTargetGreen[j]<self.cdfInputGreen[i] and j<=255:
                j=j+1
            self.LUTGreen[i]=j
            
        j=0
        for i in range(256):
            while self.cdfTargetBlue[j]<self.cdfInputBlue[i] and j<=255:
                j=j+1
            self.LUTBlue[i]=j
            
        redHistogram= np.zeros(self.InputRed.shape)
        resultRed = [0]*256
        greenHistogram = np.zeros(redHistogram.shape)
        resultGreen = [0]*256
        blueHistogram = np.zeros(redHistogram.shape)
        resultBlue = [0]*256
        
        row, column = redHistogram.shape
        
        #red
        for c in range(0,column):
            for r in range(0,row):
                redHistogram[r][c]= self.LUTRed[self.InputRed[r][c]]
                
        for c in range(0,column):
            for r in range(0,row):
                temp =redHistogram[r][c]
                resultRed[int(temp)]+=1
        
        #greeen
        for c in range(0,column):
            for r in range(0,row):
                greenHistogram[r][c]= self.LUTGreen[self.InputGreen[r][c]]
             
        for c in range(0,column):
            for r in range(0,row):
                temp =greenHistogram[r][c]
                resultGreen[int(temp)]+=1
        #blue    
        for c in range(0,column):
            for r in range(0,row):
                blueHistogram[r][c]= self.LUTBlue[self.InputBlue[r][c]]
        
        for c in range(0,column):
            for r in range(0,row):
                temp =blueHistogram[r][c]
                resultBlue[int(temp)]+=1
        
        self.InputImage[:,:,0] = redHistogram
        self.InputImage[:,:,1] = greenHistogram
        self.InputImage[:,:,2] = blueHistogram
        
        bytesPerLine = 3 * column
        
        self.resultImage = QImage(self.InputImage.data,column,row,bytesPerLine,QImage.Format_RGB888)
        resultLabel = QLabel('result')
        resultLabel.setPixmap(QPixmap.fromImage(self.resultImage))
        resultLabel.setAlignment(Qt.AlignCenter)
        self.resultGridBox.layout().addWidget(resultLabel)
        resultPlotRed = self.figureResult.add_subplot(311)
        resultPlotGreen = self.figureResult.add_subplot(312)
        resultPlotBlue= self.figureResult.add_subplot(313)
        
        
        resultPlotRed.bar(range(256),resultRed,color = 'red')
        resultPlotGreen.bar(range(256),resultGreen,color = 'green')
        resultPlotBlue.bar(range(256),resultBlue,color = 'blue')
        
        self.resultGridBox.layout().addWidget(self.canvasResult)
                
        return NotImplementedError

        
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())