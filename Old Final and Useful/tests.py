import pygame
pygame.init()

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

def instructions(screen):
    #instructions function that tells the player how to play

    map = Map(10)
    #create map sprite

    """music = pygame.mixer.music
    music.load("files/menu.ogg")
    music.play()"""
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

    red = pygame.Surface((110,100))
    blue = pygame.Surface((110,100))
    green = pygame.Surface((110,100))
    pink = pygame.Surface((110,100))

    greenColour = (227,96,0)        #orange
    redColour = (0,141,126)         #teal
    blueColour = (160,215,0)        #green
    pinkColour = (169,0,122)        #purple

    my_font = pygame.font.SysFont("Helvetica", 27)

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
                """elif event.key == pygame.K_p:
                    if muteState==False:
                        music.pause()
                        pause = 1
                        muteState = True
                    else:
                        music.unpause()
                        pause = 0
                        muteState = False"""


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
    """music.stop()"""
    return done_playing,colour,compliment,pause

instructions(pygame.display.set_mode((1000, 600)))