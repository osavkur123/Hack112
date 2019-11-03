import math, copy, random

from cmu_112_graphics import *
from tkinter import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

###########################################################################

class UserBehavior(App):

    def appStarted(self):
        self.scrollX = [0 for i in range (4)]
        self.cursorX = self.width // 2
        self.cursorY = self.width // 2
        self.margin = 20
        self.draggingScoller = None
        mouseUrl = "https://image.shutterstock.com/image-vector" +\
                    "/cursor-arrow-computer-symbol-600w-1050982217.jpg"
        ogMouseImage = self.loadImage(mouseUrl)
        self.mouseImage =  self.scaleImage(ogMouseImage, 1/40)
        self.horizonScollers = []
        self.spriteSheet = [[] for i in range (4)]
        self.scrollerSize = 20
        for i in range (4):
            horizonScoller = (0,self.height//4 * i, self.scrollerSize, \
                            self.height//4*i + self.scrollerSize, \
                            "yellow")
            self.horizonScollers.append(horizonScoller)
#        for j in range (12):
#            option = (self.width//12*j, \
#                        self.margin, \
#                        self.width//12*(j+1) + 20, \
#                        self.height//4)
#            self.spriteSheet[0].append(option)
        self.spriteSheet[0] = (0, self.margin,\
                                self.width//6, self.height//4)
            


    def mousePressed(self, event):
        self.selectedScroller = self.checkSelection(event.x, event.y)
        print(self.selectedScroller)
        if self.selectedScroller != None:
            self.draggingScoller = (self.selectedScroller, \
                                    self.horizonScollers[self.selectedScroller])


    
    def mouseDragged(self, event):
        self.cursorX = event.x
        if self.draggingScoller != None:
            self.OGselectedScoller = self.draggingScoller[1]
            newLocation = event.x
            x0,y0,x1,y1,fill = self.OGselectedScoller
            newScoller =  (event.x,y0,  \
                            event.x + self.scrollerSize, y1, "green")
            index = self.draggingScoller[0]
            self.horizonScollers[index] =  newScoller

        
    def mouseReleased(self, event):
        if self.selectedScroller != None:
            index = self.draggingScoller[0]
            self.scrollX[index] = event.x  - (self.draggingScoller[1][0])
            self.horizonScollers[index] = self.horizonScollers[index][:-1] \
                                             + ("yellow",)

            self.selectedScroller = None
            self.draggingScoller = None
            self.OGselectedScoller = None
            print(self.scrollX)
            self.scrollX[index] = 0


    def mouseMoved(self, event):
        self.cursorX = event.x
        self.cursorY = event.y

    def checkSelection(self, x, y): 
        for item in self.horizonScollers:
            if item[0] <= x <= item[3] and item[1] <= y <= item[3]:
                selection = self.horizonScollers.index(item)
                return selection
        return None
        


        

    def redrawAll(self, canvas):
        canvas.create_rectangle(0,0,self.width,self.height, fill = "white")
#        self.drawOptions(canvas)
        self.drawHorizontalScroller(canvas)
        self.drawCursor(canvas)
        
    
    def drawCursor(self, canvas):
        canvas.create_image(self.cursorX, self.cursorY, \
                            image= ImageTk.PhotoImage(self.mouseImage))
                                
    def drawHorizontalScroller(self,canvas):
        for i in range (4):
            canvas.create_rectangle(0, (self.height//4 * i), \
                                    self.width, \
                                    (self.height//4 * i+ self.margin),  \
                                    fill = "black")
        for item in self.horizonScollers:
            x0,y0,x1,y1,fill = item
            canvas.create_rectangle(x0,y0,x1,y1, fill = fill)
    
    def drawOptions(self, canvas):
#        for item in self.spriteSheet[0]:
        newx0 = self.spriteSheet[0][0] - self.scrollX[0]
        y0 = self.spriteSheet[0][1]
        newx1 = self.spriteSheet[0][3] - self.scrollX[0]
        y1 = self.spriteSheet[0][2]
        print(newx0,newx1,self.scrollX[0])
        canvas.create_rectangle(newx0,y0,newx1,y1, fill = "blue")

        

UserBehavior(width = 500, height = 800)


