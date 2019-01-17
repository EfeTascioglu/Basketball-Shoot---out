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
