import pygame
pygame.init()

def game(screen,background):
    playerSprite=Player()
    mapSprite = Map()
    blobSprite = Blobs()

    player  = pygame.sprite.Group(playerSprite)
    map  = pygame.sprite.Group(mapSprite)
    blobs  = pygame.sprite.Group(blobSprite)



    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)

        #quit command
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
        blobSprite.checkMap(mapSprite)

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
        self.hitBoundary = False


    def update(self):
        self.X, self.Y = move(self.X,self.Y,self.speed)
        self.boundaries()
        self.rect.topleft = (-self.X,-self.Y)

    def boundaries(self):
        self.hitBoundary = False
        if self.X < -450:
            self.X = -450
            self.hitBoundary = True

        if self.X > 1370:
            self.X = 1370
            self.hitBoundary = True

        if self.Y < -250:
            self.Y = -250
            self.hitBoundary = True

        if self.Y > 802:
            self.Y = 802
            self.hitBoundary = True

    def x_value(self):
        return self.X

    def y_value(self):
        return self.Y
    def checkBoundary(self):
        return self.hitBoundary

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
        self.X = 0
        self.Y = 0
        self.speed = 10
        self.go = True
        self.stopX = False
        self.stopY = False
        self.stop = False


    def checkMap(self,map):
        self.stop = map.checkBoundary()
        self.go = True
        if map.x_value() < -449:
            self.go = False
            self.stopY = True
        if map.x_value() > 1371:
            self.go = False
            self.stopY = True
        if map.y_value() < -249:
            self.go = False
            self.stopX = True
        if map.y_value() > 803:
            self.go = False
            self.stopX = True

    def update(self):
        #if self.go == True:
        #    if self.stopX == True:
        if self.stop:
                X = self.X
                self.X, self.Y = move(self.X,self.Y,self.speed)
                self.rect.center = (-X,-self.Y)
                """
            elif self.stopY == True:
                Y = self.Y
                self.X, self.Y = move(self.X,self.Y,self.speed)
                self.rect.center = (-self.X,-Y)
            else:
                self.X, self.Y = move(self.X,self.Y,self.speed)
                self.rect.center = (-self.X,-self.Y)"""

def move(X,Y,speed):
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
    pygame.display.set_caption('Agraeme.io')

    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))


    done_playing = False

    while done_playing == False:
        #instructions(screen, score)
        if not done_playing:
            score, done_playing = game(screen,background)

if __name__ == "__main__":
    main()