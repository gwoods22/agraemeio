import pygame, math
pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('Agraeme.io')
back = pygame.Surface(screen.get_size())
back.fill((0,0,0))
background = pygame.image.load('files/background.gif')
ball = pygame.Surface([640,480], pygame.SRCALPHA, 32)
ball = ball.convert_alpha()
pygame.draw.circle(ball,(255,0,0),(50,50),50)


#variables
X = 500
Y = 300
ballX = 500
ballY = 300
speed = 10

clock = pygame.time.Clock()
keepGoing = True
#game loop
while keepGoing:
    clock.tick(30)

    #quit command
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepGoing = False


    mouseX, mouseY = pygame.mouse.get_pos()

    angle =math.atan2(mouseY - 300, mouseX - 500)

    x=math.cos(angle)
    y=math.sin(angle)

    X = speed*x
    Y = speed*y



    #Boundaries
    if X < -450:
        X = -450

    if X > 1370:
        X = 1370

    if Y < -250:
        Y = -250

    if Y > 802:
        Y = 802

    #blit
    screen.blit(back,(0,0))
    #screen.blit()
    screen.blit(background, (-X, -Y))
    screen.blit(ball, (ballX-50, ballY-50))
    pygame.display.flip()

