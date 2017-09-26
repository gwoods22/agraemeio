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

def game(screen, background, colour,compliment,speed,pause):
    beep = pygame.mixer.Sound("files/beep.ogg")
    finalBeep = pygame.mixer.Sound("files/finalBeep.ogg")
    music = pygame.mixer.music

    gamespeed = speed
    g = []
    b = []

    xGPoints, yGPoints = coordinates(0,1700,0,900,200,100)
    xBPoints, yBPoints = coordinates(0,1700,0,900,200,100)

    for i in range(0,len(xGPoints),1):
        g.append(Blobs(gamespeed,xGPoints[i],yGPoints[i],colour))

    for i in range(0,len(xBPoints),1):
        b.append(Blobs(gamespeed,xBPoints[i],yBPoints[i],compliment))

    good = pygame.sprite.Group(g)
    bad = pygame.sprite.Group(b)

    playerCollideSprite = Player(35,0)
    playerCollide = pygame.sprite.Group(playerCollideSprite)

    playerSprite = Player(50,colour)
    player = pygame.sprite.Group(playerSprite)

    enemySprite = Enemy(gamespeed,compliment)
    enemy = pygame.sprite.Group(enemySprite)

    mapSprite = Map(gamespeed)
    map = pygame.sprite.Group(mapSprite)

    scoreSprite = Label(20)
    scoreSprite.location = (750,10)

    countSprite = Label(100)
    countSprite.location = (465,75)

    clock = pygame.time.Clock()
    keepGoing = True

    scoreValue = 0
    speedChange = 0
    skip = False

    countdown = True
    once = True
    loop = 0
    num = 5

    while countdown:
        clock.tick(30)

        loop +=1

        if loop > 15:
            num -=1
            loop = 0
            if num > 1:
                beep.play()
            elif num == 1:
                finalBeep.play()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                countdown = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    countdown = False
                    keepGoing = False
                    skip = True

        if num <1:
            countdown = False

        numbers = str(num)
        countSprite.text = numbers
        count = pygame.sprite.Group(countSprite)

        if pygame.sprite.groupcollide(playerCollide, bad, False, True):
            pass

        map.clear(screen, background)
        player.clear(screen, background)
        good.clear(screen, background)
        bad.clear(screen, background)
        count.clear(screen,background)
        enemy.clear(screen,background)

        if once:
            map.update(playerSprite)
            player.update()
            good.update()
            bad.update()
            enemy.update()
            loop +=10

        count.update()
        once = False

        map.draw(screen)
        good.draw(screen)
        bad.draw(screen)
        player.draw(screen)
        enemy.draw(screen)
        count.draw(screen)


        pygame.display.flip()

    if pause == 0:
        music.load("files/game.ogg")
        music.play()
        muteState = False
    else:
        music.load("files/game.ogg")
        music.play()
        music.pause()
        muteState =True

    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    keepGoing = False
                    skip = True
                elif event.key == pygame.K_p:
                    if muteState==False:
                        music.pause()
                        muteState = True
                    else:
                        music.unpause()
                        muteState = False
                elif event.key == pygame.K_g :
                    supriseScreen = pygame.display.set_mode((591,412),pygame.FULLSCREEN)
                    pygame.display.set_caption('Agraemeio!')

                    drakeSprite = Drake()
                    drake = pygame.sprite.Group(drakeSprite)

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

                        drake.clear(supriseScreen,background)
                        drake.draw(supriseScreen)


        mapX = mapSprite.x_value()
        mapY = mapSprite.y_value()

        if pygame.sprite.groupcollide(playerCollide, bad, False, True):
            keepGoing = False

        if pygame.sprite.groupcollide(playerCollide, good, False, True):
            scoreValue += 50
            speedChange +=1

        if playerCollideSprite.rect.colliderect(enemySprite.rect):
            keepGoing = False

        if speedChange > 5:
            enemySprite.speedChange()
            speedChange = 0




            xStart = int(mapX*-1+500)
            xStop = int(mapX*-1+2200)
            yStart = int(mapY*-1+300)
            yStop = int(mapY*-1+1200)

            xStep = 600
            yStep = 300

            xGPoints, yGPoints = coordinates(xStart,xStop,yStart,yStop,xStep,yStep)

            for i in range(0,len(xGPoints),1):
                g.append(Blobs(gamespeed,xGPoints[i],yGPoints[i],colour))

            good = pygame.sprite.Group(g)

            xStep += 50
            yStep += 50


        text  = "Score: {}".format(scoreValue)
        scoreSprite.text = text
        score = pygame.sprite.Group(scoreSprite)

        stopX, stopY = checkMap(mapSprite,playerSprite)

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

        map.update(playerSprite)
        player.update()
        good.update()
        bad.update()
        score.update()
        enemy.update()

        map.draw(screen)
        good.draw(screen)
        bad.draw(screen)
        enemy.draw(screen)
        player.draw(screen)
        score.draw(screen)


        pygame.display.flip()


    try:
        file = open( "files/highscore.txt", "r" )
        highscore = file.readline()
        file.close()

    except:
        file = open("files/highscore.txt", "w+")
        file.write(str(scoreValue))
        file.close()
        highscore = -1

    if scoreValue > int(highscore):
        file = open("files/highscore.txt", "w")
        file.write(str(scoreValue))
        file.close()
    music.stop()
    return skip,scoreValue,pause

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
        #function for editing text
        self.text = text

class Drake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('files/drake.gif')
        self.rect = self.image.get_rect()

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
    """player class to display the user's player
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
    """class for the AI enemy that follows the user around the map
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
        return self.chaseSpeed

    def stopCheck(self,stopX,stopY):
        self.stopX = stopX
        self.stopY = stopY

    def update(self):
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
        self.stopX = stopX
        self.stopY = stopY

    def update(self):
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
    mouseX, mouseY = pygame.mouse.get_pos()
    angle =math.atan2(mouseY - 300, mouseX - 500)

    x=math.cos(angle)
    y=math.sin(angle)

    X += speed*x
    Y += speed*y
    return X,Y

def enemyMove(X,Y,speed):
    angle = math.atan2(-300-Y, -500-X)

    x=math.cos(angle)
    y=math.sin(angle)

    X += speed*x
    Y += speed*y

    return X,Y

def coordinates(xStart,xStop,yStart,yStop,xStep,yStep):
    xPoints = []
    yPoints = []
    loop = 0
    while loop <5:
        for i in range(xStart,xStop,xStep):
            temp = random.randint(20+i,200+20+i)
            if temp < 910 or temp > 1010:
                xPoints.append(temp)


        for i in range(yStart,yStop,yStep):
            temp = random.randint(20+i,100+20+i)
            if temp < 526 or temp > 626:
                yPoints.append(temp)

        loop +=1

    notEqual = True

    while notEqual:
        if len(xPoints) > len(yPoints):
            xPoints.pop()
        elif len(xPoints) < len(yPoints):
            yPoints.pop()
        elif len(xPoints) == len(yPoints):
            notEqual = False


    random.shuffle(xPoints)
    random.shuffle(yPoints)

    return xPoints, yPoints

def instructions(screen):
    map = Map(10)
    music = pygame.mixer.music
    music.load("files/menu.ogg")
    music.play()
    map = Map(10)
    try:
        file = open( "files/highscore.txt", "r" )
        highscore = file.readline()
        file.close()

    except:
        highscore = 0


    textBackground = pygame.Surface((430,360))
    textBackground.fill((36,120,0))

    red = pygame.Surface((110,100))
    blue = pygame.Surface((110,100))
    green = pygame.Surface((110,100))
    pink = pygame.Surface((110,100))

    greenColour = (227,96,0)        #orange
    redColour = (0,141,126)         #teal
    blueColour = (160,215,0)        #green
    pinkColour = (169,0,122)        #purple

    my_font = pygame.font.SysFont("Verdana", 27)

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

    instruction_label = []
    for line in instructions:
        temp_label = my_font.render(line, 1, (101,229,47))
        instruction_label.append(temp_label)

    text = "Highscore: {}".format(highscore)
    high = my_font.render(text,1,(101,229,47),(36,120,0))

    colour = (255,255,255)
    compliment = (255,255,255)

    keep_going = True
    done_playing = False
    clock = pygame.time.Clock()
    first = True
    muteState = False
    pause = 0
    while keep_going == True:
        clock.tick(30)
        mouseX, mouseY = pygame.mouse.get_pos()
        if first:
            mouseX = 0
            mouseY = 0
            first = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                done_playing = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    keep_going = False
                    done_playing = True
            elif event.key == pygame.K_p:
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
                    #red
                    colour = redColour
                    compliment = greenColour
                    keep_going = False
                    done_playing = False
                if mouseY > 400 and mouseY < 500 and mouseX > 333 and mouseX < 444:
                    #green
                    colour = greenColour
                    compliment = redColour
                    keep_going = False
                    done_playing = False
                if mouseY > 400 and mouseY < 500 and mouseX > 555 and mouseX < 666:
                    #blue
                    colour = blueColour
                    compliment = pinkColour
                    keep_going = False
                    done_playing = False
                if mouseY > 400 and mouseY < 500 and mouseX > 777 and mouseX < 888:
                    #pink
                    colour = pinkColour
                    compliment = blueColour
                    keep_going = False
                    done_playing = False

        if mouseY > 400 and mouseY < 500 and mouseX > 111 and mouseX < 222:
            pygame.draw.rect(red,(0,0,0),((5,5), (100,90)),2)
            colour = redColour
        else:
            pygame.draw.rect(red,redColour,((0,0), (110,100)))

        if mouseY > 400 and mouseY < 500 and mouseX > 333 and mouseX < 444:
            pygame.draw.rect(green,(0,0,0),((5,5), (100,90)),2)
            colour = greenColour
        else:
            pygame.draw.rect(green,greenColour,((0,0), (110,100)))

        if mouseY > 400 and mouseY < 500 and mouseX > 555 and mouseX < 666:
            pygame.draw.rect(blue,(0,0,0),((5,5), (100,90)),2)
            colour = blueColour
        else:
            pygame.draw.rect(blue,blueColour,((0,0), (110,100)))

        if mouseY > 400 and mouseY < 500 and mouseX > 777 and mouseX < 888:
            pygame.draw.rect(pink,(0,0,0),((5,5), (100,90)),2)
            colour = pinkColour
        else:
            pygame.draw.rect(pink,pinkColour,((0,0), (110,100)))


        player = Player(50,colour)

        player.update()

        screen.blit(map.image, (map.rect.topleft))
        screen.blit(player.image, (player.rect.topleft))
        screen.blit(red,(110,400))
        screen.blit(green,(330,400))
        screen.blit(blue,(550,400))
        screen.blit(pink,(770,400))
        screen.blit(textBackground,(5,5))
        screen.blit(high,(625,125))


        for i in range(len(instruction_label)):
            screen.blit(instruction_label[i], (17, 30*i + 15))

        pygame.display.flip()
    music.stop()
    return done_playing,colour,compliment,pause

def retry(screen,colour,score):
    map = Map(10)
    sad = pygame.mixer.Sound("files/sad.ogg")

    textBackground = pygame.Surface((505,345))
    textBackground.fill((36,120,0))

    my_font = pygame.font.SysFont("Verdana", 45)

    try:
        file = open( "files/highscore.txt", "r" )
        highscore = file.readline()
        file.close()

    except:
        highscore = 0

    instructions = (
    "         Good Try",
    "      But You Died!",
    "Press Space to Retry",
    "    Press Q to Quit",
    "   Last Score: {}".format(score),
    "   Highscore: {}".format(highscore)
    )




    instruction_label = []
    for line in instructions:
        temp_label = my_font.render(line, 1, (101,229,47))
        instruction_label.append(temp_label)

    face = pygame.Surface([200,140], pygame.SRCALPHA, 32)
    face = face.convert_alpha()
    pygame.draw.circle(face,(243,50,84),(50,25),25)
    pygame.draw.circle(face,(243,50,84),(150,25),25)
    pygame.draw.circle(face,(243,50,84),(100,70),15)
    pygame.draw.circle(face,(243,50,84), (100,150),50,10)

    keep_going = True
    done_playing = False
    clock = pygame.time.Clock()


    sad.play()
    while keep_going == True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                done_playing = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    keep_going = False
                    done_playing = True
                elif event.key == pygame.K_SPACE:
                    keep_going = False
                    done_playing = False



        screen.blit(map.image, (map.rect.topleft))
        screen.blit(textBackground,(247,55))
        screen.blit(face, (400,430))


        for i in range(len(instruction_label)):
            screen.blit(instruction_label[i], (262, 55*i + 60))

        pygame.display.flip()

    return done_playing

def main():
    screen = pygame.display.set_mode((1000, 600),pygame.FULLSCREEN)
    pygame.display.set_caption('Agraemeio!')

    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))

    speed = 10

    done_playing,colour,compliment,pause = instructions(screen)


    while done_playing == False:
        skip,score,pause = game(screen, background, colour, compliment, speed,pause)
        if skip == False:
            done_playing = retry(screen,colour,score)
        else:
            done_playing = True

if __name__ == "__main__":
    main()