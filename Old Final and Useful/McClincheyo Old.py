import pygame
pygame.init()

def game(screen,background):
    playerSprite=Player()
    mapSprite = Map()



    player  = pygame.sprite.Group(playerSprite)
    map  = pygame.sprite.Group(mapSprite)
    blobs  = pygame.sprite.Group(mapSprite.blobSprite)



    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)

        #quit command
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False



        map.clear(screen, background)
        player.clear(screen, background)
        blobs.clear(screen, background)

        map.update()
        player.update()
        blobs.update()

        map.draw(screen)
        blobs.draw(screen)
        player.draw(screen)


        pygame.display.flip()

class Map(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('files/background.png')
        self.rect = self.image.get_rect()
        self.X = 500
        self.Y = 300
        self.speed = 10
        self.blobSprite = Blobs()
        self.blobStopX = False
        self.blobStopY = False

    def update(self):
        self.X, self.Y = self.move(self.X,self.Y,self.speed)
        self.boundaries()
        self.rect.topleft = (-self.X,-self.Y)
        self.blobSprite.boundaries(self.blobStopX,self.blobStopY)
        self.blobStopX = False
        self.blobStopY = False

    def move(self, X,Y,speed):
        mouseX, mouseY = pygame.mouse.get_pos()
        if mouseX > 500 and mouseY > 300:
            x = mouseX-500
            y = mouseY-300

            if x > y:
                X += speed
                ratio = float(y)/float(x)
                Y += speed*ratio

            if x < y:
                Y += speed
                ratio = float(x)/float(y)
                X += speed*ratio

        if mouseX > 500 and mouseY < 300:
            x = mouseX-500
            y = 300-mouseY

            if x > y:
                X += speed
                ratio = float(y)/float(x)
                Y -= speed*ratio

            if x < y:
                Y -= speed
                ratio = float(x)/float(y)
                X += speed*ratio

        if mouseX < 500 and mouseY > 300:
            x = 500-mouseX
            y = mouseY-300

            if x > y:
                X -= speed
                ratio = float(y)/float(x)
                Y += speed*ratio

            if x < y:
                Y += speed
                ratio = float(x)/float(y)
                X -= speed*ratio

        if mouseX < 500 and mouseY < 300:
            x = 500-mouseX
            y = 300-mouseY

            if x > y:
                X -= speed
                ratio = float(y)/float(x)
                Y -= speed*ratio

            if x < y:
                Y -= speed
                ratio = float(x)/float(y)
                X -= speed*ratio


        return X,Y
    def boundaries(self):
        if self.X < -450:
            self.X = -450
            self.blobStopX = True

        if self.X > 1370:
            self.X = 1370
            self.blobStopX = True
        if self.Y < -250:
            self.Y = -250
            self.blobStopY = True
        if self.Y > 802:
            self.Y = 802
            self.blobStopY = True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image  = pygame.Surface([100,100], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (500, 300)
        self.radius = 50

    def update(self):
        pygame.draw.circle(self.image,(255,0,0),(50,50),self.radius)

class Blobs(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 60
        self.image  = pygame.Surface([self.radius*2,self.radius*2], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image,(0,255,0),(self.radius,self.radius),self.radius)
        self.X = -700
        self.Y = -50
        self.speed = 10
        self.stopX = False
        self.stopY = False

    def update(self):
        if self.stopY == False:
            tempx = self.X
            self.X, self.Y = self.move(self.X,self.Y,self.speed)
            self.rect.center = (-tempx,-self.Y)

        if self.stopX == False:
            tempy = self.Y
            self.X, self.Y = self.move(self.X,self.Y,self.speed)
            self.rect.center = (-self.X,-tempy)



    def boundaries(self, stopx, stopy):
        self.stopx = stopx
        self.stopy = stopy

    def move(self, X,Y,speed):
        mouseX, mouseY = pygame.mouse.get_pos()
        if mouseX > 500 and mouseY > 300:
            x = mouseX-500
            y = mouseY-300

            if x > y:
                X += speed
                ratio = float(y)/float(x)
                Y += speed*ratio

            if x < y:
                Y += speed
                ratio = float(x)/float(y)
                X += speed*ratio

        if mouseX > 500 and mouseY < 300:
            x = mouseX-500
            y = 300-mouseY

            if x > y:
                X += speed
                ratio = float(y)/float(x)
                Y -= speed*ratio

            if x < y:
                Y -= speed
                ratio = float(x)/float(y)
                X += speed*ratio

        if mouseX < 500 and mouseY > 300:
            x = 500-mouseX
            y = mouseY-300

            if x > y:
                X -= speed
                ratio = float(y)/float(x)
                Y += speed*ratio

            if x < y:
                Y += speed
                ratio = float(x)/float(y)
                X -= speed*ratio

        if mouseX < 500 and mouseY < 300:
            x = 500-mouseX
            y = 300-mouseY

            if x > y:
                X -= speed
                ratio = float(y)/float(x)
                Y -= speed*ratio

            if x < y:
                Y -= speed
                ratio = float(x)/float(y)
                X -= speed*ratio


        return X,Y

def main():
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption('McClinchey.o')

    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))


    done_playing = False

    while done_playing == False:
        #instructions(screen, score)
        if not done_playing:
            score, done_playing = game(screen,background)

if __name__ == "__main__":
    main()