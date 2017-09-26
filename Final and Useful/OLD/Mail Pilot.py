import pygame, random
pygame.init()

def instructions(screen, score):
    """ Instructions screen """
    plane = Plane()
    sea   = Sea(screen)

    my_font = pygame.font.SysFont("Victoria", 30) #sync font size by passing veriable

    instructions = (
    "Welcome to Mail Pilot! Last Score: %d" %score,
    "These letters must be delivered to the archipelago,",
    "but there's a storm brewing!",
    "",
    "Use the mouse to move left and right.",
    "Avoid the storm clouds or the plane will be destroyed.",
    "Fly over the islands to drop the mail!",
    "",
    "click to continue, escape to exit"
    )

    instruction_label = []
    for line in instructions:
        temp_label = my_font.render(line, 1, (255,255,255))
        instruction_label.append(temp_label)

    keep_going = True
    done_playing = False
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    while keep_going == True:
        clock.tick(30) #Sync with game clock with passed variables
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                done_playing = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keep_going = False
                done_playing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keep_going = False
                    done_playing = True

        sea.update(screen)
        plane.update()

        screen.blit(sea.image, (0,sea.rect.height * -2/3))
        screen.blit(plane.image, (plane.rect.topleft))

        for i in range(len(instruction_label)):
            screen.blit(instruction_label[i], (50, 30*i + 30))

        pygame.display.flip()

    return done_playing

def game(screen, background):
    sea    = Sea(screen)
    island = Island(screen)
    plane  = Plane()
    cloud1 = Cloud(screen)
    cloud2 = Cloud(screen)
    cloud3 = Cloud(screen)
    scoreboard = Scoreboard()

    #Review organization of the sprite groups.
    sea_sprite  = pygame.sprite.Group(sea)
    island_sprite = pygame.sprite.Group(island)
    plane_sprite  = pygame.sprite.Group(plane)
    cloud_sprites = pygame.sprite.Group(cloud1, cloud2, cloud3)
    scoreboard_sprite = pygame.sprite.Group(scoreboard)

    keep_going = True
    done_playing = False
    clock = pygame.time.Clock()

    while keep_going == True:
        clock.tick(30)
        pygame.mouse.set_visible(False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                done_playing = True #Indicating that they want to shut down the game

#Collision Detection

    #Need Sounds. Record sounds via Audacity.
        if plane.rect.colliderect(island.rect):
            plane.yay.play()
            scoreboard.score += 100
            island.reset(screen)

    #This is from Harris's book, pg. 319
        hit_clouds = pygame.sprite.spritecollide(plane, cloud_sprites, False)
        if hit_clouds:
            plane.thunder.play()
            scoreboard.lives -= 1
            if scoreboard.lives == 0:
                keep_going = False #Returns to instructions, but does not shut off game.
                done_playing = False
            for the_cloud in hit_clouds:
                the_cloud.reset(screen)

#Update graphics
        sea_sprite.clear(screen, background)
        island_sprite.clear(screen, background)
        plane_sprite.clear(screen, background)
        cloud_sprites.clear(screen, background)
        scoreboard_sprite.clear(screen, background)

        sea_sprite.update(screen)
        island_sprite.update(screen)
        plane_sprite.update()
        cloud_sprites.update(screen)
        scoreboard_sprite.update()

        sea_sprite.draw(screen)
        island_sprite.draw(screen)
        plane_sprite.draw(screen)
        cloud_sprites.draw(screen)
        scoreboard_sprite.draw(screen)

        pygame.display.flip()

    return scoreboard.score, done_playing

SCROLLING_SPEED = 5

class Sea(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sea.gif')
        self.rect = self.image.get_rect()

        #Check if the sea image will work
        if self.rect.height != screen.get_height() * 3 or self.rect.width != screen.get_width():
            print("Error: The sea image is an abnormal size (not screen_height * 3). The sea will not look right.")

        self.reset(screen)

        self.dy = SCROLLING_SPEED

    def update(self, screen):
        #Scroll the sea down, dy should be constant with island speed.
        self.rect.top += self.dy

        if self.rect.top == 0:
            self.reset(screen)

    def reset(self, screen):
        self.rect.top = screen.get_height() * -2

class Plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/plane.gif")
        self.rect = self.image.get_rect()
        self.yay = pygame.mixer.Sound("assets/yay.ogg")
        self.thunder = pygame.mixer.Sound("assets/thunder.ogg")
        self.engine = pygame.mixer.Sound("assets/plane_engine.ogg")

    def update(self):
        current_x, y = pygame.mouse.get_pos()
        self.rect.center = (current_x, 440)

class Island(pygame.sprite.Sprite):
    def __init__(self, screen): #here is where the parameters must be listed.
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/island.gif")
        self.rect = self.image.get_rect()

        self.reset(screen)

    def update(self, screen):
        self.dy = SCROLLING_SPEED
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset(screen)

    def reset(self, screen):
        #reset rect above the screen, so it scrolls in
        self.rect.bottom = 0
        #Reset x position
        #"self.rect.width/2" ensures that the whole island will always be on screen.
        self.rect.centerx = random.randrange(0 + self.rect.width/2, screen.get_width() - + self.rect.width/2)

class Cloud(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/cloud.gif")
        self.rect = self.image.get_rect()

        self.reset(screen)

    def update(self, screen):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top >= screen.get_height():
            self.reset(screen)

        if self.rect.left > screen.get_width():
            self.reset(screen)

        if self.rect.right < 0:
            self.reset(screen)

    def reset(self, screen):
        #reset rect above the screen, so it scrolls in
        self.rect.bottom = 0
        #Reset x position
        #midpoint ensures that the whole island will always be on screen. Positions center based on it.
        midpoint = int(self.rect.width/2)
        self.rect.centerx = random.randrange(0 + midpoint, screen.get_width() - midpoint)

        self.dy = random.randrange(SCROLLING_SPEED+1, 10) #SCROLLING_SPEED+1 so clouds never appear to be still.
        self.dx = random.randrange(-3,3)

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.lives = 5
        self.score = 0

        self.font = pygame.font.SysFont("None", 30)

    def update(self):
        self.text  = "Planes: %d, Score: %d" %(self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (20, 20)

def main():
    resolution = 640, 480
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Mail Pilot")

    background = pygame.Surface(screen.get_size())
    background.fill((0,255,0))

    score = 0 #Dummy text
    done_playing = False

    while done_playing == False:
        done_playing = instructions(screen, score)
        if not done_playing:
            score, done_playing = game(screen, background)

    pygame.mouse.set_visible(True)



if __name__ == "__main__":
    main()
