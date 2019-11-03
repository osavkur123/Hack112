import math, copy, random

from cmu_112_graphics import *
from hackathon import *
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
        self._root.configure(cursor='none')
        self.mealVariants = getMealSchedule() 
        self.scrollX = [0 for i in range (4)]
        self.cursorX = self.width // 2
        self.cursorY = self.width // 2
        self.margin = 20
        self.draggingScoller = None
<<<<<<< HEAD
        mouseUrl = "https://pngriver.com/wp-content/uploads/2017/12/" + \
            "download-mouse-Cursor-PNG-transparent-images-transparent-" + \
=======
        mouseUrl = "https://pngriver.com/wp-content/uploads/2017/12/"+\
            "download-mouse-Cursor-PNG-transparent-images-transparent-"+\
>>>>>>> f37213f593b4e93c1b1abd3ee650d9f0ede568cd
            "backgrounds-PNGRIVER-COM-851913_hand-o-pointer_512x512.png"
        ogMouseImage = self.loadImage(mouseUrl)
        self.mouseImage =  self.scaleImage(ogMouseImage, 1/40)
        self.horizonScollers = []
        self.scrollerSize = 20
        for i in range (4):
            horizonScoller = (0,self.height//4 * i, self.scrollerSize, \
                            self.height//4*i + self.scrollerSize, \
                            "yellow")
            self.horizonScollers.append(horizonScoller)
        self.options = self.pictureInput(4, 9)
        self.chosenOption = [{} for i in range (4)]

    def getFinalSurvey(self):
        result = [[] for i in range (4)]
        for meal in self.chosenOption:
            for keys in meal:
                findId = keys[1] + len(self.options[keys[0]])*keys[0] + 1
                result[keys[0]].append(self.mealVariants[findId])
        return result



    def mousePressed(self, event):
        self.selectedScroller = self.checkSelection(event.x, event.y)
        self.selectedPicture = self.checkPicSelection(event.x, event.y)
        if self.selectedScroller != None:
            self.draggingScoller = (self.selectedScroller, \
                                    self.horizonScollers[self.selectedScroller])
        if self.selectedPicture != None:
            (row, col) = self.selectedPicture
            if (row,col) in self.chosenOption[row]:
                del self.chosenOption[row][(row,col)]
            elif (row,col) not in self.chosenOption[row] \
                and (len(self.chosenOption[row]) < 3):
                    self.chosenOption[row][(row,col)] = self.options[row][col]

    def keyPressed(self, event):
        if event.key == "O":
            print("Getting stuff")
            surveyInstances = self.getFinalSurvey()
            mealSchedule = getMealSchedule(surveyInstances)
            print(mealSchedule)


    
    def mouseDragged(self, event):
        self.cursorX = event.x
        if self.draggingScoller != None:
            self.OGselectedScoller = self.draggingScoller[1]
            newLocation = event.x
            x0,y0,x1,y1,fill = self.OGselectedScoller
            self.newScoller =  (event.x,y0,  \
                            event.x + self.scrollerSize, y1, "green")
            index = self.draggingScoller[0]
            self.horizonScollers[index] =  self.newScoller
            self.scrollX[index] = self.horizonScollers[index][0] * 2

        
    def mouseReleased(self, event):
        if self.selectedScroller != None:
            index = self.draggingScoller[0]
            print(event.x, self.newScoller[2])
            self.horizonScollers[index] =  self.newScoller[:-1]+("yellow",)
            self.selectedScroller = None
            self.draggingScoller = None
            self.OGselectedScoller = None

    def mouseMoved(self, event):
        self.cursorX = event.x
        self.cursorY = event.y

    def checkSelection(self, x, y): 
        for item in self.horizonScollers:
            if item[0] <= x <= item[2] and item[1] <= y <= item[3]:
                selection = self.horizonScollers.index(item)
                return selection
        return None
    
    def checkPicSelection(self, x, y):
        for row in range (len(self.options)):
            item = self.options[row]
            for col in range (len(item)):
                coordinate = item[col]
                if coordinate[0] <= x+self.scrollX[row] <= coordinate[2] \
                     and coordinate[1] <= y <= coordinate[3]:
                        selection = (row,col)
                        return selection
        return None
    
    def pictureInput(self, rows, cols):
        finalList = [[]for i in range (rows)]
        for i in range (rows):
            rowList = []
            for j in range (cols):
                x0 = self.width//3 * j
                x1 = x0 + self.width//3
                y0 = self.height//4 * i + self.margin
                y1 = y0 + self.height//4 - self.margin*2
                newLocation = [x0,y0,x1,y1]
                rowList.append(newLocation)
            finalList[i] = rowList
        return finalList



    def redrawAll(self, canvas):
        #A diction, key => id, value => instance
        canvas.create_rectangle(0,0,self.width,self.height, fill = "white")
        for i in range (4):
            self.drawHorizontalScroller(canvas)
        self.drawCursor(canvas)

        for row in range (len(self.options)):
            rowL = self.options[row]
            scrollx = self.scrollX[row]
            for col in range (len(rowL)):
                item = rowL[col]
                x0,y0,x1,y1 = item[0]-scrollx, item[1],item[2]-scrollx,item[3]
                cx, cy = (x0+x1)/2, (y0+y1)/2
                ID = col + len(self.options[row])*row + 1 
                text = self.mealVariants[ID].name
                if (row,col) not in self.chosenOption[row]:
                    fill = "red"
                else:
                    fill = "green"
                canvas.create_rectangle(x0,y0,x1,y1, fill = fill)
                canvas.create_text(cx,cy, text= text, font='Arial 8 bold')
        self.drawHorizontalScroller(canvas)
        self.drawCursor(canvas)
    
    def drawCursor(self, canvas):
        canvas.create_image(self.cursorX, self.cursorY, \
                            image= ImageTk.PhotoImage(self.mouseImage), \
                            anchor = NW)
                                
    def drawHorizontalScroller(self,canvas):
        for i in range (4):
            canvas.create_rectangle(0, (self.height//4 * i), \
                                    self.width, \
                                    (self.height//4 * i+ self.margin),  \
                                    fill = "black")
        for item in self.horizonScollers:
            x0,y0,x1,y1,fill = item
            canvas.create_rectangle(x0,y0,x1,y1, fill = fill)




UserBehavior(width = 700, height = 800)


