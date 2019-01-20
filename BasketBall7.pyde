import random
from leaderBoard import *
def setup():
    Init()
    size (800, 600)
    global sizeX, sizeY
    sizeX, sizeY = 800, 600

def Init():
    global basketball, goal, status, whichSquare
    global pSX, pSY, pSW, pSH, barX, barY, barW, barH, angle, lX, lY, lW, lH
    global sX, sY, selecting, selectingPower, score
    global timeAllowed, scored, lbound, rbound, incrx
    #lbound and rbound determines the range of location in which the hoop will randomly regenerate
    #incrx is the movement of the hoop
    incrx = 1
    lbound = 400
    rbound = 700
    lX = 400
    lY = 200
    lW = 100
    lH = 100
    scored = False
    timeAllowed = 20
    score = 0
    selectingPower = False
    sX = 50.0
    sY = 550.0
    selecting = False
    angle = PI/4
    barX = 200
    barY = 350
    barW = 50
    barH = 50
    pSX = 200
    pSY = 200
    pSW = 50
    pSH = 200
    whichSquare = -1
    ##status: inGame, startMenu, exitMenu, optionMenu
    status  = 'startMenu'
    basketball = ball(PI/3, 0)
    goal = hoop( 500, 0 )
    start1()
    
def start1():
    global allBoundaries, numSquares, anglePressed
    allBoundaries = []
    numSquares = 2
    allBoundaries.append ([[100, 100], [200, 200]])
    allBoundaries.append ([[100, 300], [200, 400]])
    anglePressed = False
def endGame ():
    global allBoundaries, numSquares, whichSquare, status
    background(0)
    allBoundaries = []
    numSquares = 2
    fill(255)
    rect (100, 100, 100, 100)
    rect (100, 300, 100, 100)
    allBoundaries.append ([[100, 100], [200, 200]])
    allBoundaries.append ([[100, 300], [200, 400]])
    if whichSquare == 0:
        status = 'startMenu'
        Init()
    if whichSquare == 1:
        status = 'leaderboard'
        initiateLeaderboard()
def startNewGame():
    global startTime, status
    startTime = second()
    status = 'preGame'
def time():
    global startTime, timeAllowed, status
    if second()>startTime and second()-startTime >= timeAllowed:
        status = 'endGame'
    elif startTime > second() and 60-startTime + second() >= timeAllowed:
        status = 'endGame'
def draw():
    global basketball, goal, status
    #print (status)
    if status == 'startMenu':
        startMenu()
    if status == 'inGame':
        inGame()
    if status == 'optionMenu':
        optionMenu()
    if status == 'preGame':
        preGame()
    if status == 'startNewGame':
        startNewGame()
    if status == 'endGame':
        endGame()
    if status == 'leaderboard':
        leaderboard()

def printScore():
    global score,startTime, timeAllowed
    fill(0)
    text ('Your score: '+str(score), 550, 100)

    if second()>startTime:
        text ('Time left: ' + str(timeAllowed- (second ()- startTime) ), 550, 200)
    elif startTime > second():
        text ('Time left: ' + str(timeAllowed - ( 60-startTime + second())), 550, 200)
    fill(255)

def startMenu():
    global status
    global whichSquare
    background(0)
    rect (100, 100, 100, 100)
    rect (100, 300, 100, 100)
    if whichSquare == 0:
        status = 'startNewGame'
    if whichSquare == 1:
        status = 'optionMenu'


def optionMenu():
  global status
  global allBoundaries, numSquares, whichSquare
  background(0)
  allBoundaries = []
  numSquares = 1
  allBoundaries.append ([[200, 200], [300, 300]])
  rect (200, 200, 100, 100)
  if whichSquare == 0:
      status = 'startMenu'
      whichSquare = -1
      #print("here")
    

def preGame():
    global status, angle, power, goal, basketball, anglePressed, scored, score
    moveHoop()
    if scored and score<3:
        goal.x = random.randint (lbound, rbound)
    scored = False
    background(255)
    printScore()
    power = -1
    time()
    drawHoop(goal)
    #angle = drawAngleSelector()
    angle = angleSelector()
    power = powerSelector()
    stroke(0)
    ellipse( goal.getRim()[0], goal.getRim()[1], goal.getRad() * 2, goal.getRad() * 2 )
    ellipse (basketball.getX(), basketball.getY(), basketball.getRad()*2, basketball.getRad()*2)
    if power!=-1:
        basketball = ball(angle, power/6)
        status = 'inGame'

def moveHoop():
    global score, goal, incrx
    if score >= 3:
        goal.x+=incrx
        if goal.x>=rbound or goal.x <=lbound:
            incrx*=-1
            
def inGame():
    global lbound, rbound, score
    global basketball, goal, status
    scoreCheck()
    background( 255 )
    printScore()
    moveHoop()
    fill(255)
    stroke(0)
    time()
    basketball.animate()
    goal.collisionDetect( basketball )
    goal.collisionBackboard( basketball )
    #print( goal.getRim()[0], goal.getRim()[1] )
    ellipse( goal.getRim()[0], goal.getRim()[1], goal.getRad() * 2, goal.getRad() * 2 )
    ellipse (basketball.getX(), basketball.getY(), basketball.getRad()*2, basketball.getRad()*2)
    #print (basketball.getX(), " ", basketball.getY())
    drawHoop(goal)
    frameRate(25)
    if basketball.getY() >= 575:
        basketball.x = sX
        basketball.y = sY
        status = 'preGame'
      


    basketball.getRad()*2
    #print (basketball.getX(), " ", basketball.getY())
    drawHoop(goal)
    frameRate(25)
  
def mouseReleased():
  global allBoundaries, whichSquare, removeSquare, activeSquares, numSquares, selecting, selectingPower
  if selecting:
      selecting = False
  if selectingPower:
      selectingPower = False
  whichSquare = - 1
  for i in range( numSquares ):
      validXRange = allBoundaries[i][0][0] <= mouseX <= allBoundaries[i][1][0]
      validYRange = allBoundaries[i][0][1]  <= mouseY <= allBoundaries[i][1][1]
      validLocation = validXRange and validYRange
      if validLocation:
          whichSquare = i
          break
  print ( whichSquare )
      
def keyPressed():
    global choices, whichSquare, keyChosen
    
    keyChosen = key
    
    if keyCode == 8:
        keyChosen = "BACK"
    elif keyCode == 127:
        keyChosen = "DEL"
        
    elif key == CODED:
        #print("ping")
        if keyCode == 38:
            keyChosen = "UP"
        elif keyCode == 37:
            keyChosen = "LEFT"
        elif keyCode == 39:
            keyChosen = "RIGHT"
        elif keyCode == 40:
            keyChosen = "DOWN"
        elif keyCode == 17:
            keyChosen = "CONTROL"
        elif keyCode == 20:
            keyChosen = "CAPS"
        elif keyCode == 16:
            keyChosen = "SHIFT"
        elif keyCode == 18:
            keyChosen = "ALT"      
      
      
def scoreCheck():
    global goal, basketball, score, scored
    if not scored and basketball.getX() > goal.getRim()[0] and basketball.getX() < goal.getBackboard()[0] and basketball.getY() <= goal.getRim()[1] + 7 and basketball.getY() >= goal.getRim()[1] - 7:
        print('score ', score)
        scored = True
        score +=1
    
        
      
      



class ball:
  global sX, sY
  def __init__ (self, angle, force):
      self.x = sX # Location of the ball
      self.y = sY # Location of the ball
      self.rad = 25 # Size of the ball
      self.collidedCounter = 0
      tempX = cos( angle ) * force # Initial velocity of the ball
      tempY = -sin( angle ) * force # Initial Velocity of the ball
      
      self.velocity = { 'x': tempX , 'y': tempY }
  def animate(self):
      #Assume ball has mass m = 1 kg, simulating real life
      self.x += self.velocity['x']
      self.y += self.velocity['y']
      self.velocity['x'] *= 0.98 #air resistance constant, can be changed
      self.velocity['y'] += 1 #gravitation constant, can also be changed
      #print( self.velocity['x'], self.velocity['y'])
      self.collidedCounter -= 1
      
  # manipulate function prevents the ball from going into the loop
  def manipulate( self, xIncr, yIncr ):
      #print( xIncr, yIncr )
      self.x += xIncr
      self.y += yIncr    

  def bounceX( self ):
      self.velocity['x'] *= -0.9
  def bounceY( self ):
      self.velocity['y'] *= -0.9
  def getX ( self ):
      return self.x
  def getY ( self ):
      return self.y
  def getVelocity( self ):
      return self.velocity
  def getRad( self ):
      return self.rad
  def getCollidedCounter( self ):
      return self.collidedCounter
  def recreate( self, angle ):
      myVelocity = ( ( ( self.velocity['x'] ** 2 + self.velocity['y'] ** 2 ) ) ** 0.5 ) * 0.7
      
      tempX = cos( angle ) * myVelocity# * 0.9
      tempY = sin( angle ) * myVelocity# * 0.9
      print( tempX, tempY )
      self.velocity = { 'x': tempX , 'y': tempY }
      self.collidedCounter = 1

class hoop:
    
  def __init__( self, initX, initMotion ):
      self.x = initX
      self.motion = initMotion
      self.rad = 0
      self.bounds = [400, 600]
      self.backboard = { 'x': 0, 'y': 375 }
      self.rim = { 'x': -90, 'y': 450 } # Y constant height
      self.top = { 'x': 0, 'y': self.backboard['y'] + 5 }
      self.back = {'x': -20, 'y': self.rim['y'] }
      self.points = [ self.rim, self.top, self.back ]
      
  def collisionDetect( self, ball ):
      #print( ( ball.getX() - self.x + self.rim['x'] ) )
      for i in range(len(self.points)):
        if ball.getCollidedCounter() <= 0:
            if ( ( ball.getX() - ( self.x + self.points[i]['x'] ) ) ** 2 + ( ball.getY() - self.points[i]['y'] ) ** 2 ) ** 0.5 <= ball.getRad() + self.rad:
                while ( ( ball.getX() - ( self.x + self.points[i]['x'] ) ) ** 2 + ( ball.getY() - self.points[i]['y'] ) ** 2 ) ** 0.5 <= ball.getRad() + self.rad:
                    #print ( ball.getX(), ball.getY() )
                    ball.manipulate( (ball.getVelocity())['x'] * (-0.01) , (ball.getVelocity()['y'] * (-0.01)) )
                self.collision( ball, i )
              
  def collisionBackboard( self, ball ):
      if ball.getCollidedCounter() <= 0:
        if (self.x - ball.getX()) < ball.getRad() and (ball.getY() + ball.getRad() - 1) > self.backboard['y'] and (ball.getX() - self.x) < ball.getRad():
            print("ping")
            while (self.x - ball.getX()) < ball.getRad() and (ball.getY() + ball.getRad()) >= self.backboard['y']:
                  ball.manipulate( (ball.getVelocity())['x'] * (-0.01) , (ball.getVelocity()['y'] * (-0.01)) )
            ball.bounceX()
            
    
  def collision( self, ball, index ):
      angleBall = atan( ball.getVelocity()['y'] / ball.getVelocity()['x'] )
      angleCollision = atan( ( ball.getY() - ( self.points[index]['y'] ) ) / ( ball.getX() - ( self.x + self.points[index]['x'] ) ) )
      if ( ball.getX() - ( self.x + self.points[index]['x'] ) ) <= 0:
        angleCollision -= PI
      #print( angleCollision, angleBall )
      angleNew = 2 * abs(angleCollision) + abs(angleBall) - PI
      #print( abs(angleCollision), abs(angleCollision) - abs(angleBall) )
      #if abs(angleCollision) > PI - abs(angleCollision) - abs(angleBall):
      #    ball.recreate( -angleNew )
      #else:
      print(degrees(angleBall), degrees(angleCollision), degrees(angleNew))
      ball.recreate( -angleNew )
      
  def getRim( self ):
      return [ self.x + self.rim['x'], self.rim['y'] ]
  def getBackboard( self ):
      return [ self.x + self.backboard['x'], self.backboard['y'] ]
  def getRad( self ):
      return self.rad
  def getPos( self ):
      return self.x
  
  
    

def drawHoop( hoop ):
    strokeWeight(4)
    line ( hoop.getPos(), 600, hoop.getPos(), hoop.getBackboard()[1] )
    line ( hoop.getPos(), hoop.getRim()[1], hoop.getRim()[0], hoop.getRim()[1] )
    line ( hoop.getBackboard()[0], hoop.getRim()[1] + 20, hoop.getBackboard()[0] - 20, hoop.getRim()[1])

def angleSelector():
    global angle, selecting, sX, sY
    
    lineLength = 144
    eX = sX + lineLength * cos(angle)
    eY = sY - lineLength * sin(angle)
    
    line (sX, sY, eX, eY)
    sSize = 20
    ellipse (eX, eY, sSize, sSize)
    if mousePressed and ((eX - sSize <= mouseX <= eX + sSize and eY - sSize <= mouseY <= eY + sSize) or selecting )and mouseX > sX and mouseY < sY:
        selecting = True
        angle = atan (float(sY - mouseY)/float(mouseX - sX))
    return (angle)


def powerSelector():
    global pSX, pSY, pSW, pSH, barX, barY, barW, barH, lX, lY, lW, lH, selecting, selectingPower
    
    
    stroke(0)
    rect (pSX, pSY, pSW, pSH)
    fill (140,140 , 0)
    rect (barX, barY, barW, barH)
    fill (255)
    if mousePressed and pSX <= mouseX <= pSX + pSW and pSY+25 <= mouseY <= pSY + pSH-25 and not selecting:
        selectingPower = True
        barY = mouseY - 25
        
    rect (lX, lY, lW, lH)
    fill(0)
    text ('launch', lX, lY, lX+ lW, lY+lH)
    fill(255)
    if mousePressed and lX <= mouseX <= lX + lW and lY <= mouseY <= lY + lH and not selecting and not selectingPower:
        return ((pSH - (barY- pSY))*1.2)
    return (-1)


def initiateLeaderboard( ): ####### Leaderboard #######
    global activeSquares, pointer, scoreDictionary, sizeX, sizeY, choices, outputString, pointerCounte, allBoundaries, numSquares, keyChosen
    monoFont = loadFont("DejaVuSansMono-48.vlw")
    textFont(monoFont, 26)
    
    
    choices = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    global startSquareX, startSquareY, squareHeight, squareWidth, pointerCounter, submited
    startSquareX = 135
    startSquareY = 470
    squareXShow = startSquareX
    squareYShow = startSquareY
    squareHeight = 40
    squareWidth = 20
    
    activeSquares = [True for i in range(26)]
    file = open("score.txt")
    scoreDictionary = {}
    text = file.readlines()
    pointer = 0
    gdkey = -1
    for line in text:
        line = line.strip()
        row = ""
        for c in line:
            row = row + c
        temprow = row.split( ",")
        gdkey = gdkey + 1
        scoreDictionary[ gdkey ] = ( temprow[0], int( temprow[1] ))
    file.close()
    allBoundaries = []
    numSquares = 26
    #print(squareXShow, squareYShow)
    for i in range( numSquares ):
        upperLeft =  [ squareXShow, squareYShow ]
        #print(upperLeft)
        lowerRight = [ squareXShow + squareWidth, squareYShow + squareHeight ]
        clickBoundary = [ upperLeft, lowerRight ]
        #print(clickBoundary)
        squareXShow = squareXShow + squareWidth
        allBoundaries.append( clickBoundary )
        #print(allBoundaries)
    allBoundaries.append( [ [ 50, sizeY-80 ] , [ 165, sizeY-30 ] ] ) # Special Squares
    allBoundaries.append( [ [ sizeX-200, sizeY-90 ] , [ sizeX-50, sizeY-50 ] ] )
    allBoundaries.append( [ [ 225, 375 ] , [ 365, 425 ] ] )
    numSquares = 29
    print(allBoundaries)
    print(len(allBoundaries))
    
    outputString = ""
    pointerCounter = 0
    submited = False
    keyChosen = -1


def reverseBubbleSortDict( arrayList ):
    temp = 0
    
    for i in range(len(arrayList)):
        print(arrayList)
        sorted = True
        for j in range(0, len(arrayList)-1-i):
            if arrayList[j][1] < arrayList[j+1][1]:
                sorted = False
                temp = arrayList[j+1]
                arrayList[j+1] = arrayList[j]
                arrayList[j] = temp
        print(sorted)
        if sorted:
            break
    return arrayList

def leaderboard():
    
    global pointerCounter, allBoundaries, numSquares, whichSquare, keyChosen
    
    
    #print(numSquares)
    background(255)
    #print("ping")
    displayText( "Leaderboard" , 50, [0], 220, 50, 500, 500 )
    
    strokeWeight(3) # Sumbmit Box
    fill( 50,50,255 )
    rect( sizeX-165, sizeY - 90, 115, 50 )
    rect( allBoundaries[26][0][0], allBoundaries[26][0][1], allBoundaries[26][1][0] - allBoundaries[26][0][0], allBoundaries[26][1][1] - allBoundaries[26][0][1] )
    fill( 255 )
    textSize( 24 )
    text("Submit", sizeX-150, sizeY - 75, 150, 50 )
    text( "Back", allBoundaries[26][0][0] + 20, allBoundaries[26][0][1] + 10, 500, 500 )
            
    scoreboard( scoreDictionary, 250, 450, 150, 200, 30, 5 )  
    
    displayText( "Your Score is: " + str(score), 32, [0], 240, 340, 500, 500 )
    
    displayChoices( choices, [True for i in range(26) ], startSquareX, startSquareY, squareWidth, squareHeight )
    
    strokeWeight(3)
    
    line( 300, 450, 500, 450 )
    
    displayText( outputString, 32, [0], sizeX/2 - 9.5 * len(outputString), 420, 400, 100 )
    
    pointerCounter = drawPointer( pointer, pointerCounter, len(outputString), sizeX, sizeY )
    
    if whichSquare != -1:
        mouseRoutine()
        whichSquare = -1
    if keyChosen != -1:
        keyRoutine()
        keyChosen = -1

def scoreboard( dict, x1, x2, y, rowWidth, rowHeight, scoreboardlength ):
    
    fill(0)
    showX = x1
    showY = y

    for i in range(scoreboardlength):
        text(dict[i][0], showX, showY, rowWidth, rowHeight )
        showY += rowHeight
        
    showX = x2
    showY = y
    
    for i in range(scoreboardlength):
        text(str(dict[i][1]), showX, showY, rowWidth, rowHeight )
        showY += rowHeight
        
def updateLeaderboard():
    global outputString, score, scoreDictionary
    myTuple = ( outputString, score )
    scoreDictionary.update( { 5 : myTuple } )
  
    scoreDictionary = reverseBubbleSortDict( scoreDictionary )
    
    file = open("score.txt", "w")
    
    file.write( scoreDictionary[0][0] + ',' + str(scoreDictionary[0][1]) )
    
    for i in range(1, 5):
        file.write("\n")
        file.write( scoreDictionary[i][0] + ',' + str(scoreDictionary[i][1]) )
        
    file.close
    
def drawPointer( pointer, pointerCounter, myLength, sizex, sizeY ):
    strokeWeight(2)
    stroke(0)
    fill(0)

    if pointerCounter > 0:
        line( (sizeX/2 - 9.5 * myLength) + 19 * pointer, 420, (sizeX/2 - 9.5 * myLength) + 19 * pointer, 445 )
        if pointerCounter >= 20:
            pointerCounter = -20
    
    return pointerCounter+1
    return pointerCounter+1


def displayText( word, wordSize, colour, x, y, thisWidth, thisHeight ):
    textSize(wordSize)
    if len(colour) == 1:
        fill(colour[0])
    elif len(colour) == 3:
        fill(colour[0], colour[1], colour[2])
    else:
        fill(colour[0], colour[1], colour[2], colour[3])
    text( word, x, y, thisWidth, thisHeight )
    
    
def displayChoices(choices, activeChoices, startSquareX, startSquareY, squareWidth, squareHeight):
    showX = startSquareX
    showY = startSquareY
    fill(0)
    noStroke()
    
    for i in range(len(choices)): # Display chosen letters
        if activeChoices[i]:
            text(choices[i], showX, showY + squareHeight - 10 )
        showX += 20
    
    showX = startSquareX
    showY = startSquareY
    noFill()
    strokeWeight(1)
    stroke(0)
    for i in range(len(choices)):
        if activeChoices[i]:
            rect( showX, showY, squareWidth, squareHeight )
        showX += 20
        
        
        
def mouseRoutine():
    global whichSquare, submited, keyChosen, status
    if whichSquare == 27:
        if not(submited):
            submited = True
            updateLeaderboard()
    elif whichSquare < 26:
        keyChosen = choices[whichSquare]
    elif whichSquare == 26:
        status = 'endGame'
                        

def keyRoutine():
    global keyChosen, outputString, pointer
    if len(str(keyChosen)) == 1:
        if len(outputString) < 12:
            outputString = outputString[:pointer] + str(keyChosen) + outputString[pointer:]
            pointer += 1
    else:
        if keyChosen == "LEFT":
            if pointer > 0:
                pointer -= 1
        elif keyChosen == "RIGHT":
            if pointer < len(outputString):
                pointer += 1
        elif keyChosen == "BACK":
            if pointer > 0:
                outputString = outputString[:pointer-1] + outputString[pointer:] # Takes out character before pointer
                pointer -= 1
        elif keyChosen == "DEL":
            if pointer < len(outputString):
                outputString = outputString[:pointer] + outputString[pointer+1:] # Takes out character before pointer


      
