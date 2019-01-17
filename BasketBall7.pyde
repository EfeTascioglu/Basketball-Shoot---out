import math
def setup():
  global basketball, goal, status, whichSquare
  global pSX, pSY, pSW, pSH, barX, barY, barW, barH, angle
  global sX, sY, selecting, selectingPower, score
  global timeAllowed
  timeAllowed = 60
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
  size (800, 600)
  start1()


def start1():
    global allBoundaries, numSquares, anglePressed
    allBoundaries = []
    numSquares = 2
    allBoundaries.append ([[100, 100], [200, 200]])
    allBoundaries.append ([[100, 300], [200, 400]])
    allBoundaries.append ([])
    anglePressed = False
def endGame ():
    background (0)
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
    #print (second(), ' ', startTime)
def draw():
  #print (status)
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
  global status, angle, power, goal, basketball, anglePressed
  background(255)
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

def inGame():
  background( 255 )
  global basketball, goal, status
  fill(255)
  stroke(0)
  time()
  basketball.animate()
  goal.move()
  goal.collisionDetect( basketball )
  goal.collisionBackboard( basketball )
  goal.scored( basketball )
  #print( goal.getRim()[0], goal.getRim()[1] )
  ellipse( goal.getRim()[0], goal.getRim()[1], goal.getRad() * 2, goal.getRad() * 2 )
  ellipse (basketball.getX(), basketball.getY(), basketball.getRad()*2, basketball.getRad()*2)
  #print (basketball.getX(), " ", basketball.getY())
  drawHoop(goal)
  frameRate(25)
  if basketball.getY() >= 575:
      basketball.x = 50.0
      basketball.y = 550.0
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
      
  def move( self ):
      self.x += self.motion
      if self.x <= self.bounds[0]:
          self.motion *= -1
          self.x = self.bounds[0]
          
      elif self.x >= self.bounds[1]:
          self.motion *= -1
          self.x = self.bounds[1]
    #for i in 
          
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
  
  def scored( self, ball ):
      if ( 0 < ball.getX() - self.rim['x'] - self.x < self.back['x'] + self.x) and ball.getY() <= self.rim['y']:
          if ( self.rim['y'] - ball.getY()
          print("ping")
    

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
    lX = 400
    lY = 200
    lW = 100
    lH = 100
    
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
    global activeSquares, pointer
    activeSquares = [True for i in range(29)]
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
    print(scoreDictionary)
    return scoreDictionary


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
    global outputString, playerScore, scoreDictionary
    myTuple = ( outputString, playerScore )
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
