"""
Agraemeio!
"A great game for the whole family!"
By: Graeme Woods
Last Edit: January 23rd, 2016

Agraemeio is an addictive singleplayer
game where you must collect dots to
increase your highscore without touching
bad dots or getting eaten by the AI player.
"""

#import modules and initialize pygame
import random, math, pygame
pygame.init()

def game(screen, background, colour, compliment, speed, pause):
    """The game function that runs the actual game.
    the parameters are screen and background which are created in the main function and are required for graphics
    the colour and compliment parameters are for the colour of the player, enemy and the different blobs
    the speed parameter is the gamespeed that the player moves at
    the pause parameter indicates if the player has paused the menu music. If so, the game music does not start playing
    """

    beep = pygame.mixer.Sound("files/beep.ogg")
    #loads the beep sound
    finalBeep = pygame.mixer.Sound("files/finalBeep.ogg")
    #loads final beep sound
    music = pygame.mixer.music
    #sets music variable for streaming music

    gamespeed = speed
    #sets passed speed variable to game speed

    g = []
    b = []
    #create list that will store list of good and bad sprites

    xGPoints, yGPoints = coordinates(0,1700,0,900,200,100)
    xBPoints, yBPoints = coordinates(0,1700,0,900,200,100)
    #creates lists of x and y points for good and bad blobs

    for i in range(0,len(xGPoints),1):
        g.append(Blobs(gamespeed,xGPoints[i],yGPoints[i],colour))
    for i in range(0,len(xBPoints),1):
        b.append(Blobs(gamespeed,xBPoints[i],yBPoints[i],compliment))
    #run through coordinate list and create list of sprites for all the blobs with parameters: gamespeed, xPoint, yPoint, colour

    good = pygame.sprite.Group(g)
    bad = pygame.sprite.Group(b)
    #create sprite group for good and bad blobs


    playerCollideSprite = Player(35,0)
    playerCollide = pygame.sprite.Group(playerCollideSprite)
    #create player collision sprite and sprite group

    playerSprite = Player(50,colour)
    player = pygame.sprite.Group(playerSprite)
    #create player sprite and sprite group

    enemySprite = Enemy(gamespeed,compliment)
    enemy = pygame.sprite.Group(enemySprite)
    #create enemy sprite and sprite group

    mapSprite = Map(gamespeed)
    map = pygame.sprite.Group(mapSprite)
    #create map sprite and sprite group

    scoreSprite = Label(20)
    scoreSprite.location = (750,10)
    #create score text sprite and set location

    countSprite = Label(100)
    countSprite.location = (465,75)
    #create countdown text sprite and set location

    clock = pygame.time.Clock()
    #set clock as pygame clock function

    keepGoing = True
    countdown = True
    #sentinel variables

    scoreValue = 0
    #initial score value

    speedChange = 0
    #variable used to count loops of the game that will affect how fast the AI player increases its speed

    skip = False
    #variable that bypasses the retry screen if it is True so if player clicks q bypass the retry screen


    once = True
    #variable to update map, player enemy, and the blobs one time but then don't update after that

    loop = 0
    #variable used for the countdown timer

    #initial countdown timer value
    num = 5

    #while loop for countdown screen
    while countdown:
        clock.tick(30)
        #limit FPS to 30

        loop +=1
        #add one to loop variable

        if loop > 15:
            num -=1
            loop = 0
            #after 15 loops, subtract one from the countdown timer, set loop back to 0
            if num > 1:
                #play beep when countdown is at a number greater than 1
                beep.play()
            elif num == 1:
                #play different beep when the countdown is at 1
                finalBeep.play()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                countdown = False
                keepGoing = False
                skip = True
                #stop loop, don't start main loop and skip retry screen if window is exited

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    countdown = False
                    keepGoing = False
                    skip = True
                    #stop loop, don't start main loop and skip retry screen if q is pressed

        if num <1:
            countdown = False
            #stop loop when countdown gets to 0

        numbers = str(num)
        countSprite.text = numbers
        #convert num to a string and set num as text for countSprite

        count = pygame.sprite.Group(countSprite)
        #create group for countSprite



        map.clear(screen, background)
        player.clear(screen, background)
        good.clear(screen, background)
        bad.clear(screen, background)
        count.clear(screen,background)
        enemy.clear(screen,background)
        #clear all visible objects

        if once:
            map.update(playerSprite)
            player.update()
            good.update()
            bad.update()
            enemy.update()
            once = False
            #update map, player enemy, and the blobs once to simulate freeze frame then set once to  false so it isn't run again

        count.update()
        #update countdown text


        map.draw(screen)
        good.draw(screen)
        bad.draw(screen)
        player.draw(screen)
        enemy.draw(screen)
        count.draw(screen)
        #draw all visible objects


        pygame.display.flip()
        #flip everything to the screen

    if pause == 0:
        music.load("files/game.ogg")
        music.play()
        muteState = False
    else:
        music.load("files/game.ogg")
        muteState = True
    """check to see if music was paused on the menu
    If not, load game music and play and set muteState to False
    If so, load game music in case player wants to play music later but pause it and set muteState to True
    """

    while keepGoing:
        clock.tick(30)
        #limit FPS to 30

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                #stop loop and skip retry screen if window is exited


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    keepGoing = False
                    skip = True
                    #stop loop and skip retry screen if q is pressed

                elif event.key == pygame.K_p:
                    if muteState==False:
                        music.pause()
                        muteState = True
                    else:
                        music.unpause()
                        muteState = False
                    #change mute state and play/pause music if p is pressed

                elif event.key == pygame.K_g:
                    #EASTER EGG!!!!!!! :)
                        supriseScreen = pygame.display.set_mode((591,412),pygame.FULLSCREEN)
                        pygame.display.set_caption('Hotline Bling!')
                        music.stop()
                        bling = pygame.image.load('files/bling.gif')

                        music.load("files/bling.ogg")
                        music.play(-1)

                        clock = pygame.time.Clock()
                        keepErGoing = True
                        while keepErGoing == True:
                            clock.tick(30)
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    keepErGoing = False
                                    keepGoing = False
                                    skip = True
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_q:
                                        keepErGoing = False
                                        keepGoing = False
                                        skip = True

                            supriseScreen.blit(bling,(0,0))
                            pygame.display.flip()

        mapX = mapSprite.x_value()
        mapY = mapSprite.y_value()
        #set MapX,MapY to x,y value of map sprite

        if pygame.sprite.groupcollide(playerCollide, bad, False, True):
            keepGoing = False
            #if player collides with bad blobs stop loop

        if pygame.sprite.groupcollide(playerCollide, good, False, True):
            #if player collides with good blobs: delete the blob sprite, increase score value by 50, and up the speedChange counter by 1
            scoreValue += 50
            speedChange +=1

        if playerCollideSprite.rect.colliderect(enemySprite.rect):
            #if player collides with enemy sprite, stop loop
            keepGoing = False

        if speedChange > 10:
            #if speedChange counter gets to be greater than 10, speed up enemy and set speedChange counter to 0
            enemySprite.speedChange()
            speedChange = 0


            #Lines 276 - 303 are code for reblitting the blobs every 500 points


            xStart = int(mapX*-1+500)
            xStop = int(mapX*-1+2200)
            yStart = int(mapY*-1+300)
            yStop = int(mapY*-1+1200)
            """This code sets Start and Stop variables for x and y coordinates depending on where the player is on the map.
            This is done by checking the value for mapX and mapY. The location of the map will indicate where the player
            appears to be on the map when in reality only the map is moving and the player is static. With this location
            data the start and stop values are calculated to pass the proper numbers in to the coordinate function. This
            ensures that no blobs are blitted off of the map.
            """

            xStep = 600
            yStep = 300
            #initial xStep/yStep that will decrease over time so less blobs are blitted to the screen every 500 points

            xGPoints, yGPoints = coordinates(xStart,xStop,yStart,yStop,xStep,yStep)
            #creates new lists of x and y points for good blobs

            for i in range(0,len(xGPoints),1):
                g.append(Blobs(gamespeed,xGPoints[i],yGPoints[i],colour))
                #add new coordinates to list of the good blob sprites with parameters: gamespeed, xPoint, yPoint, colour

            good = pygame.sprite.Group(g)
            #add list of sprites to sprite group "good"

            xStep += 50
            yStep += 50
            #increasing xStep/yStep so less new blobs are blitted to the screen every 500 points


        text  = "Score: {}".format(scoreValue)
        scoreSprite.text = text
        score = pygame.sprite.Group(scoreSprite)
        #update score sprite with the score value and creates score sprite group

        stopX, stopY = checkMap(mapSprite,playerSprite)
        """checkMap function checks to see if the player is at a boundary on the map
        if the player is at the top or the bottom of the map, stopY = True
        if the player is at either far side of the map, stopX = True
        Lines 319 - 324 tell the blobs and enemy sprites if player is at the boundary
        if so, the blobs and enemy will stop moving
        """

        for i in range(0,len(b),1):
            b[i].stopCheck(stopX,stopY)
        for i in range(0,len(g),1):
            g[i].stopCheck(stopX,stopY)

        enemySprite.stopCheck(stopX,stopY)

        map.clear(screen, background)
        player.clear(screen, background)
        good.clear(screen, background)
        bad.clear(screen, background)
        score.clear(screen, background)
        enemy.clear(screen, background)
        #clear all visible objects

        map.update(playerSprite)
        player.update()
        good.update()
        bad.update()
        score.update()
        enemy.update()
        #update all visible objects

        map.draw(screen)
        good.draw(screen)
        bad.draw(screen)
        enemy.draw(screen)
        player.draw(screen)
        score.draw(screen)
        #draw all visible objects


        pygame.display.flip()
        #flip everything to the screen


    try:
        #attempt to open highscore file and get highscore
        file = open( "files/highscore.txt", "r" )
        highscore = file.readline()
        file.close()

    except:
        #if file does not exist create file and save current scoreValue as highscore also make highscore > scoreValue so next if statement is not run
        file = open("files/highscore.txt", "w+")
        file.write(str(scoreValue))
        file.close()
        highscore = scoreValue+1

    if scoreValue > int(highscore):
        #if scoreValue is higher than the highscore from file, add new highscore to file
        file = open("files/highscore.txt", "w")
        file.write(str(scoreValue))
        file.close()

    music.stop()
    #stop music

    return skip,scoreValue,pause
    #return skip, scoreValue, and pause state. (skip variable tells program whether or not to skip retry screen)

class Label(pygame.sprite.Sprite):
    """class for the score text in the game function
    class variables: text, location"""
    def __init__(self,size):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Verdana", size)
        self.text = ""
        self.location = (0,0)

    def update(self):
        #update code to re-render the image and change the top left coordinate of the rect
        self.image = self.font.render(self.text, 1, (255,0,0),(0,0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.location

    def text(self,text):
        #function for editing label text
        self.text = text

class Map(pygame.sprite.Sprite):
    """map class for the grid map that acts as a background in the game function
    class variables: X and Y coordinate on screen, speed"""
    def __init__(self,gamespeed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('files/background.gif')
        self.rect = self.image.get_rect()
        self.X = 500
        self.Y = 300
        self.speed = gamespeed

    def update(self,player):
        """update the background by moving the coordinates using the move function
        check coordinates to ensure they stay in the boundaries and then assign to the rect"""
        self.X, self.Y = move(self.X,self.Y,self.speed)
        self.boundaries(player)
        self.rect.topleft = (-self.X,-self.Y)

    def boundaries(self,player):
        #function to prevent the map from moving off the screen when the player hits the edge of the map
        if self.X < -500+player.radius:
            self.X = -500+player.radius

        if self.X > 1420-player.radius:
            self.X = 1420-player.radius

        if self.Y < -300+player.radius:
            self.Y = -300+player.radius

        if self.Y > 852-player.radius:
            self.Y = 852-player.radius


    def x_value(self):
        #return current X coordinate
        return self.X

    def y_value(self):
        #return current Y coordinate
        return self.Y

class Player(pygame.sprite.Sprite):
    """player class to display the player's player
    class variables: colour, radius, rect.center"""
    def __init__(self,radius,colour):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.image  = pygame.Surface([self.radius*2,self.radius*2], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (500, 300)
        self.colour = colour

    def radius(self):
        return self.radius

    def update(self):
        #update function that re-draws the circle if the colour or radius happens to change
        pygame.draw.circle(self.image,(self.colour),(self.radius,self.radius),self.radius)

class Enemy(pygame.sprite.Sprite):
    """class for the AI enemy that follows the player around the map
    class draws a circle on a surface that is the opposite colour of the player
    class variables: radius, logicalX, logicalY, X, Y, stopX, stopY, speed, chaseSpeed"""
    def __init__(self,speed,colour):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 50
        self.image  = pygame.Surface([self.radius*2,self.radius*2], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image,colour,(self.radius,self.radius),self.radius)
        """logical coordinates are the coordinates where the enemy will start in reference to the 1920x1152 background image
        ie. if logical coordinates are (700,400) then the intial coordinates on the screen would be (200,100)"""
        self.logicalX = 505
        self.logicalY = 305
        self.X = -self.logicalX+500
        self.Y = -self.logicalY+300
        self.speed = speed
        self.stopX = False
        self.stopY = False
        self.chaseSpeed = 2

    def speedChange(self):
        #increasing shape speed by 2
        self.chaseSpeed += 2

    def getSpeed(self):
        #returns chaseSpeed
        return self.chaseSpeed

    def stopCheck(self,stopX,stopY):
        #passes stopX and stopY into class variables stopX and stopY
        self.stopX = stopX
        self.stopY = stopY

    def update(self):
        """Depending on the state of stopY and stopX, the update function passes x and y class variables
        in to the move function along with speed. If both stopX and stopY are true, this doesn't happen
        and no movement occurs. If just one of stopX and stopY is true, both class variables x and y are
        still passed in to the movement function however only one of them is updated. If both stopX and
        stopY are false than regular movement occurs. Then the function enemyMove is run which adds the
        AI element to the enemy's movement so it follows the player around. Lastly, the class variable
        rect.center is updated with the current x and y values.
        """
        if self.stopY == True and self.stopX == True:
            pass
        elif self.stopX == True:
            blah, self.Y = move(self.X,self.Y,self.speed)
        elif self.stopY == True:
            self.X, blah = move(self.X,self.Y,self.speed)
        else:
            self.X, self.Y = move(self.X,self.Y,self.speed)
        self.X, self.Y = enemyMove(self.X,self.Y,self.chaseSpeed)
        self.rect.center = (-self.X,-self.Y)

class Blobs(pygame.sprite.Sprite):
    """class for the all the blobs on the map
    a circle is drawn on the surface which is drawn on top of the sprite
    class variables: radius, logicalX, logicalY, X, Y, stopX, stopY, speed"""
    def __init__(self,gamespeed,X,Y,colour):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 20
        self.image  = pygame.Surface([self.radius*2,self.radius*2], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image,colour,(self.radius,self.radius),self.radius)
        self.logicalX = X
        self.logicalY = Y
        self.X = -self.logicalX+500
        self.Y = -self.logicalY+300
        self.speed = gamespeed
        self.stopX = False
        self.stopY = False


    def stopCheck(self,stopX,stopY):
        #passes stopX and stopY into class variables stopX and stopY
        self.stopX = stopX
        self.stopY = stopY

    def update(self):
        """Depending on the state of stopY and stopX, the update function passes x and y class variables
        in to the move function along with speed. If both stopX and stopY are true, this doesn't happen
        and no movement occurs. If just one of stopX and stopY is true, both class variables x and y are
        still passed in to the movement function however only one of them is updated. If both stopX and
        stopY are false than regular movement occurs. Lastly, the class variable rect.center is updated
        with the current x and y values.
        """
        if self.stopY == True and self.stopX == True:
            self.rect.center = (-self.X,-self.Y)
        elif self.stopX == True:
            blah, self.Y = move(self.X,self.Y,self.speed)
            self.rect.center = (-self.X,-self.Y)
        elif self.stopY == True:
            self.X, blah = move(self.X,self.Y,self.speed)
            self.rect.center = (-self.X,-self.Y)
        else:
            self.X, self.Y = move(self.X,self.Y,self.speed)
            self.rect.center = (-self.X,-self.Y)

def checkMap(map,player):
    """A function that checks to see if player is at boundary by checking where the map is relative to the center of the
    window where the player always is +/- the player's radius. If the player is at the top or the bottom of the map,
    stopY = True. If the player is at either far side of the map, stopX = True.
    """

    stopX = False
    stopY = False
    if map.x_value() < -499+player.radius:
        stopX = True
        #left
    elif map.x_value() > 1419-player.radius:
        stopX = True
        #right
    if map.y_value() < -299+player.radius:
        stopY = True
        #top
    elif map.y_value() > 851-player.radius:
        stopY = True
        #bottom
    return stopX, stopY

def move(X,Y,speed):
    """Function that moves the game elements (map, enemy, blobs) in accordance with where the mouse is to simulate a
    scrolling feeling as the player moves across the map.
    """
    mouseX, mouseY = pygame.mouse.get_pos()
    #get mouse position and set to mouseX and mouseY

    angle =math.atan2(mouseY - 300, mouseX - 500)
    #calculate the angle from the horizontal to the line between the player's center and the mouse's position

    x=math.cos(angle)
    y=math.sin(angle)
    #find sine and cosine of the above angle to represent the x and y components of that angle

    X += speed*x
    Y += speed*y
    #add the respective x and y components to the X and Y coordinates passed in to the function

    return X,Y
    #return new x and y coordinates

def enemyMove(X,Y,speed):
    #Function that moves the enemy towards the player

    angle = math.atan2(-300-Y, -500-X)
    #calculate the angle from the horizontal to the line between the enemy's center to the player's center

    x=math.cos(angle)
    y=math.sin(angle)
    #find sine and cosine of the above angle to represent the x and y components of that angle

    X += speed*x
    Y += speed*y
    #add the respective x and y components to the X and Y coordinates passed in to the function

    return X,Y
    #return new x and y coordinates

def coordinates(xStart,xStop,yStart,yStop,xStep,yStep):
    #function that creates coordinate lists for the blobs

    xPoints = []
    yPoints = []
    #creates x list and y list

    loop = 0
    #sentinel variable for while loop below

    while loop <5:
        #loop that gets creates the coordinates using rand function 5 times

        for i in range(xStart,xStop,xStep):
            #for loop that uses xStart,xStop,xStep that have been passed in
            temp = random.randint(20+i,220+i)
            #get random integer that is between i+20 and i+220 (i is from the for loop above)
            if temp < 910 or temp > 1010:
                #as long coordinates aren't too close to the boundary, add to list
                xPoints.append(temp)


        for i in range(yStart,yStop,yStep):
            #for loop that uses yStart,yStop,yStep that have been passed in
            temp = random.randint(20+i,120+i)
            #get random integer that is between i+20 and i+120 (i is from the for loop above)
            if temp < 526 or temp > 626:
                #as long coordinates aren't too close to the boundary, add to list
                yPoints.append(temp)

        loop +=1
        #increase sentinel variable

    notEqual = True
    #sentinel variable for while loop below

    while notEqual:
        #while loop that makes sure that x and y lists are parallel and the same length
        if len(xPoints) > len(yPoints):
            xPoints.pop()
        elif len(xPoints) < len(yPoints):
            yPoints.pop()
        elif len(xPoints) == len(yPoints):
            notEqual = False


    random.shuffle(xPoints)
    random.shuffle(yPoints)
    #shuffles x and y lists

    return xPoints, yPoints
    #returns  x and y lists

def instructions(screen):
    #instructions function that tells the player how to play

    map = Map(10)
    #create map class

    music = pygame.mixer.music
    music.load("files/menu.ogg")
    music.play()
    #create music variable for pygame.mixer.music shortcut, load menu music, and play music

    try:
        #try to open highscore file and get highscore
        file = open( "files/highscore.txt", "r" )
        highscore = file.readline()
        file.close()

    except:
        #if file does not exist, set highscore to 0
        highscore = 0


    textBackground = pygame.Surface((430,360))
    textBackground.fill((36,120,0))
    #create dark green text background

    teal = pygame.Surface((110,100))
    green = pygame.Surface((110,100))
    orange = pygame.Surface((110,100))
    purple = pygame.Surface((110,100))
    #create 4 colour choice surfaces

    orangeColour = (227,96,0)
    tealColour = (0,141,126)
    greenColour = (160,215,0)
    purpleColour = (169,0,122)
    #assign colours to colour variables

    my_font = pygame.font.SysFont("Helvetica", 27)
    #create font variable

    #instruction message
    instructions = (
    "    Welcome to Agraemeio!",
    "Move your player around the",
    "map collecting blobs that are",
    "the same colour as you are to",
    "  increase your score. Don't",
    "    touch the blobs with the",
    "  opposite colour or the evil",
    "     blob that follows you!",
    "",
    "  Click any colour to start!",
    "        Press Q to quit."
    )

    """Lines 735 - 738 renders each line of the instructions bright green with the font called above.
    Then each line is added to the list instruction_label.
    """

    instruction_label = []
    for line in instructions:
        temp_label = my_font.render(line, 1, (101,229,47))
        instruction_label.append(temp_label)

    text = "Highscore: {}".format(highscore)
    high = my_font.render(text,1,(101,229,47),(36,120,0))
    #render higchscore text as surface

    colour= (255,255,255)
    #set initial value of colour

    clock = pygame.time.Clock()
    #pygame clock

    first = True
    muteState = False
    pause = 0
    done_playing = False
    #initial states of first, muteState, pause, and done_playing variable

    keep_going = True
    #sentinel variable for below loop

    while keep_going == True:
        #instructions loop

        clock.tick(30)
        #limit FPS to 30

        mouseX, mouseY = pygame.mouse.get_pos()
        #get mouse position
        
        if first:
            #fix to the bug where the colour choice boxes would go black if the program started with the mouse on top of one of the boxes
            mouseX = 0
            mouseY = 0
            first = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #if player exits window, stop instructions loop and set done_playing to True to quit
                keep_going = False
                done_playing = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    #if player presses q, stop instructions loop and set done_playing to True to quit
                    keep_going = False
                    done_playing = True
                elif event.key == pygame.K_p:
                    #if player presses p, change state of muteState and play/pause music
                    if muteState==False:
                        music.pause()
                        pause = 1
                        muteState = True
                    else:
                        music.unpause()
                        pause = 0
                        muteState = False


            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouseY > 400 and mouseY < 500 and mouseX > 111 and mouseX < 222:
                    #if player clicks teal box, set colour to teal, compliment to the compliment of teal, stop instructions loop, and continue game
                    colour = tealColour
                    compliment = orangeColour
                    keep_going = False
                    done_playing = False
                if mouseY > 400 and mouseY < 500 and mouseX > 333 and mouseX < 444:
                    #if player clicks orange box, set colour to orange, compliment to the compliment of orange, stop instructions loop, and continue game
                    colour = orangeColour
                    compliment = tealColour
                    keep_going = False
                    done_playing = False
                if mouseY > 400 and mouseY < 500 and mouseX > 555 and mouseX < 666:
                    #if player clicks green box, set colour to green, compliment to the compliment of green, stop instructions loop, and continue game
                    colour = greenColour
                    compliment = purpleColour
                    keep_going = False
                    done_playing = False
                if mouseY > 400 and mouseY < 500 and mouseX > 777 and mouseX < 888:
                    #if player clicks purple box, set colour to purple, compliment to the compliment of purple, stop instructions loop, and continue game
                    colour = purpleColour
                    compliment = greenColour
                    keep_going = False
                    done_playing = False

        if mouseY > 400 and mouseY < 500 and mouseX > 111 and mouseX < 222:
            #if player hovers over teal box, change player to - and draw border around button
            pygame.draw.rect(teal,(0,0,0),((5,5), (100,90)),2)
            colour = tealColour
        else:
            pygame.draw.rect(teal,tealColour,((0,0), (110,100)))

        if mouseY > 400 and mouseY < 500 and mouseX > 333 and mouseX < 444:            
            #if player hovers over orange box, change player to orange and draw border around button
            pygame.draw.rect(orange,(0,0,0),((5,5), (100,90)),2)
            colour = orangeColour
        else:
            pygame.draw.rect(orange,orangeColour,((0,0), (110,100)))

        if mouseY > 400 and mouseY < 500 and mouseX > 555 and mouseX < 666:
            #if player hovers over green box, change player to green and draw border around button
            pygame.draw.rect(green,(0,0,0),((5,5), (100,90)),2)
            colour = greenColour
        else:
            pygame.draw.rect(green,greenColour,((0,0), (110,100)))

        if mouseY > 400 and mouseY < 500 and mouseX > 777 and mouseX < 888:
            #if player hovers over purple box, change player to purple and draw border around button
            pygame.draw.rect(purple,(0,0,0),((5,5), (100,90)),2)
            colour = purpleColour
        else:
            pygame.draw.rect(purple,purpleColour,((0,0), (110,100)))


        player = Player(50,colour)
        #create player class

        player.update()
        #update player class

        screen.blit(map.image, (map.rect.topleft))
        screen.blit(player.image, (player.rect.topleft))
        screen.blit(teal,(110,400))
        screen.blit(orange,(330,400))
        screen.blit(green,(550,400))
        screen.blit(purple,(770,400))
        screen.blit(textBackground,(5,5))
        screen.blit(high,(625,125))
        #blit map background, player, 4 colour choice boxes, text background, and the highscore


        for i in range(len(instruction_label)):
            #loop to blit all the instructions
            screen.blit(instruction_label[i], (17, 30*i + 15))

        pygame.display.flip()
        #flip all blitted objects to the screen

    music.stop()
    #stop menu music

    return done_playing,colour,compliment,pause
    #return done_playing to tell whether or not the player has quit the game and colour, compliment, and pause for the game function

def retry(screen,colour,score):
    #retry screen after player dies

    map = Map(10)
    #create map class

    sad = pygame.mixer.Sound("files/sad.ogg")
    #load sad sound

    textBackground = pygame.Surface((505,345))
    textBackground.fill((36,120,0))
    #create dark green text background

    my_font = pygame.font.SysFont("Verdana", 45)
    #create font

    try:
        #try to open highscore file and get highscore
        file = open( "files/highscore.txt", "r" )
        highscore = file.readline()
        file.close()

    except:
        #if file does not exist, set highscore to 0
        highscore = 0

    #screen  message
    message = (
    "         Good Try",
    "      But You Died!",
    "Press Space to Retry",
    "    Press Q to Quit",
    "   Last Score: {}".format(score),
    "   Highscore: {}".format(highscore)
    )

    """Lines 921 - 924 renders each line of the message bright green with the font called above.
    Then each line is added to the list message_label.
    """

    message_label = []
    for line in message:
        temp_label = my_font.render(line, 1, (101,229,47))
        message_label.append(temp_label)

    face = pygame.Surface([200,140], pygame.SRCALPHA, 32)
    face = face.convert_alpha()
    #create transparent surface face

    pygame.draw.circle(face,(243,50,84),(50,25),25)
    pygame.draw.circle(face,(243,50,84),(150,25),25)
    pygame.draw.circle(face,(243,50,84),(100,70),15)
    pygame.draw.circle(face,(243,50,84), (100,150),50,10)
    #draw 2 eyes, a nose, and a mouth on surface face



    clock = pygame.time.Clock()
    #pygame clock

    keep_going = True
    #sentinel variable for below loop

    sad.play()
    #play sad sound

    while keep_going == True:
        #loop for the retry screen

        clock.tick(30)
        #limit FPS to 30

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #if player exits window, stop retry loop and set done_playing to True to quit
                keep_going = False
                done_playing = True
            elif event.type == pygame.KEYDOWN:
                #if player presses q, stop retry loop and set done_playing to True to quit
                if event.key == pygame.K_q:
                    keep_going = False
                    done_playing = True
                elif event.key == pygame.K_SPACE:
                    #if player presses space, stop retry loop and set done_playing to False to play again
                    keep_going = False
                    done_playing = False



        screen.blit(map.image, (map.rect.topleft))
        screen.blit(textBackground,(247,55))
        screen.blit(face, (400,430))
        #blit map background, text background, and sad face


        for i in range(len(message_label)):
            #loop to blit the message
            screen.blit(message_label[i], (262, 55*i + 60))

        pygame.display.flip()
        #flip all blitted items to screen

    return done_playing
    #return done_playing to check to see if player has quit

def main():
    #main function

    screen = pygame.display.set_mode((1000, 600),pygame.FULLSCREEN)
    #create screen variable as pygame display

    pygame.display.set_caption('Agraemeio!')
    #set display set caption

    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))
    #create black background surface

    speed = 10
    #set gamespeed

    done_playing,colour,compliment,pause = instructions(screen)
    """run instructions function and return done_playing to see if player has quit the
    game and colour, compliment, and pause to pass in to the game function
    """

    while done_playing == False:
        #game retry loop

        skip,score,pause = game(screen, background, colour, compliment, speed, pause)
        """run game function and return skip to see if program should skip retry screen, score to
        pass in to the retry screen, and pause to pass back in to game loop if player plays again
        """

        if skip == False:
            #if player manually quits game, skip retry screen
            done_playing = retry(screen,colour,score)
            #return done_playing to see if player has quit the game
        else:
            done_playing = True
            #quit loop if skip = true

if __name__ == "__main__":
    #run main as long as there are no file issues
    main()