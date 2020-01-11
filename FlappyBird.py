import pygame
import math
import random
import sys, os

class Pipe:
    heightBetweenPipes = 200
    pipeExtremitySize = 48
    pipeRespawned = False

    def __init__(self, x, height, ground, pipeWidth):      # x, y equals to the left corner of the topPipe
        self.x = x
        self.ground = ground
        self.y = random.randint(self.pipeExtremitySize, height - self.heightBetweenPipes - self.ground - self.pipeExtremitySize)
        self.height = height
        self.pipeWidth = pipeWidth
        pipePNG = pygame.image.load(path + '/pipe.png').convert_alpha()
        self.bottomPipeImage = pygame.transform.scale(pipePNG, (self.pipeWidth, pipePNG.get_height()*self.pipeWidth//pipePNG.get_width()))
        self.topPipeImage = pygame.transform.flip(self.bottomPipeImage, False, True)

    def update(self, numberOfPipes, widthBetweenPipes, fps):
        vx = 180 / fps
        self.x -= vx

        if(self.x < -self.pipeWidth):
            self.pipeRespawned = True
            self.x += widthBetweenPipes * numberOfPipes
            self.y = random.randint(self.pipeExtremitySize , self.height  -self.heightBetweenPipes - self.ground - self.pipeExtremitySize)
            
    def show(self):
        DISPLAY.blit(self.topPipeImage, (self.x, self.y - self.topPipeImage.get_height()))
        DISPLAY.blit(self.bottomPipeImage, (self.x, self.y + self.heightBetweenPipes))

class Bird:     # x, y equals to the center of the bird
    x = 100
    vy = 250
    ay = 2000
    radius = 24

    def __init__(self, height, ground):
        self.y = height/2
        self.height = height
        self.ground = ground
        self.birdImage = []
        self.birdImage.append(pygame.transform.scale(pygame.image.load(path + '/birdUp.png').convert_alpha(), (68, self.radius*2)))
        self.birdImage.append(pygame.transform.scale(pygame.image.load(path + '/birdMiddle.png').convert_alpha(), (68, self.radius*2)))
        self.birdImage.append(pygame.transform.scale(pygame.image.load(path + '/birdDown.png').convert_alpha(), (68, self.radius*2)))
        self.birdImage.append(pygame.transform.scale(pygame.image.load(path + '/birdMiddle.png').convert_alpha(), (68, self.radius*2)))

    def update(self, timeSinceLastSpace, fps):  # jump power change with fps, either find the good code or update 60 fps static
        self.y += self.vy / fps + self.ay / 2 / (fps**2)
        if self.y < self.height - self.ground:
            self.vy += self.ay / fps
        if self.y < -500:
            self.y = -500
        if (self.vy > 1500):
            self.vy = 1500

    def show(self, animationFrame):
        angle = -self.vy * 0.06 + 15
        if angle > 15:
            angle = 15
        altitude = int(self.y + math.cos(animationFrame * math.pi / 2) * 3)-self.radius
        if altitude > self.height - self.ground - self.radius * 2:
            altitude = self.height - self.ground - self.radius * 2
        DISPLAY.blit(pygame.transform.rotate(self.birdImage[animationFrame], angle), (self.x-self.radius, altitude))

def collision(flappy, pipe):
    birdMask = pygame.mask.from_surface(flappy.birdImage[1])
    bottomPipeMask = pygame.mask.from_surface(pipe.bottomPipeImage)
    topPipeMask = pygame.mask.from_surface(pipe.topPipeImage)

    deltaX = int(pipe.x - flappy.x + flappy.radius)

    if birdMask.overlap(bottomPipeMask, (deltaX, int(pipe.y + pipe.heightBetweenPipes - flappy.y + flappy.radius))):
        return True
    if birdMask.overlap(bottomPipeMask, (deltaX, int(pipe.y - pipe.topPipeImage.get_height() - flappy.y + flappy.radius))):
        return True
    return False


pygame.init()
clock = pygame.time.Clock()
path = os.path.dirname(sys.argv[0])
pygame.display.set_icon(pygame.image.load(path + '/icon.png'))

display_width = 900
display_height = 600
DISPLAY = pygame.display.set_mode([display_width, display_height], pygame.RESIZABLE)

pipeWidth = 96
widthBetweenPipes = 300
numberOfPipes = (display_width + pipeWidth) // widthBetweenPipes + 1
score = 0
ground = 100
animationFrame = 0
timeSinceLastSpace = 0
timeOfDeath = 0
lastFrameMillis = 0
fps = 60

pipes = []
for i in range(numberOfPipes):
    pipes.append(Pipe(display_width + widthBetweenPipes*i, display_height, ground, pipeWidth))
flappy = Bird(display_height, ground)

background = pygame.transform.scale(pygame.image.load(path + '/background.png').convert(), (display_width, display_height - ground))
groundImage = pygame.transform.scale(pygame.image.load(path + '/ground.png').convert(), (336*2, 112*2))
logo = pygame.transform.scale(pygame.image.load(path + '/logo.png').convert_alpha(), (400, 100))
backgroundPosition = 0

# RENDERING TEXT
pygame.display.set_caption('FLAPPY BIRD')
font = pygame.font.Font(path + '/squareLetter.ttf', 64)
instructionText = font.render('PRESS SPACE TO JUMP!', True, (0, 0, 0))
deadText = font.render('YOU DIED', True, (255, 0, 0))
textRect2 = instructionText.get_rect()
textRect2.center = (display_width//2, 400)

# mode 0:menu 1:playing 2:dying
mode = 0
running = True
while running:
    DISPLAY.blit(background, (-(backgroundPosition % background.get_width()), 0))
    DISPLAY.blit(background, (-(backgroundPosition % background.get_width()) + background.get_width(), 0))

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
            break
        elif event.type == pygame.VIDEORESIZE:
            display_width, display_height = event.size
            DISPLAY = pygame.display.set_mode([display_width, display_height], pygame.RESIZABLE)
            
            numberOfPipes = (display_width + pipeWidth) // widthBetweenPipes + 1
            
            pipes = []
            for i in range(numberOfPipes):
                pipes.append(Pipe(display_width + widthBetweenPipes*i, display_height, ground, pipeWidth))
            flappy = Bird(display_height, ground)

            background = pygame.transform.scale(pygame.image.load(path + '/background.png').convert(), (display_width, display_height - ground))
            textRect2.center = (display_width//2, 400)
    
        elif (event.type == pygame.KEYDOWN):
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                if mode == 0:
                    mode = 1
                    score = 0
                if mode != 2:
                    flappy.vy = -500
                    timeSinceLastSpace = pygame.time.get_ticks()
                    pygame.mixer.Channel(2).stop()
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound(path + '/wing.wav'))
            elif key[pygame.K_ESCAPE]:
                pygame.quit()

    if mode != 2:
        backgroundPosition += 60 / fps

    if mode == 0:
        animationFrame = (pygame.time.get_ticks()//100) % 4
        DISPLAY.blit(logo, ((display_width - logo.get_width())//2, (display_height - logo.get_height())//2))
        DISPLAY.blit(instructionText, textRect2)

    elif mode == 1:
        for i in range(len(pipes)):
            pipes[i].update(numberOfPipes, widthBetweenPipes, fps)
            if pipes[i].pipeRespawned:
                pipes[i].pipeRespawned = False
                score += 1
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(path + '/point.wav'))
        
        for pipe in pipes:
            if collision(flappy, pipe):
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(path + '/hit.wav'))
                timeOfDeath = pygame.time.get_ticks()
                mode = 2
            
        if flappy.y + flappy.radius > display_height - ground:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(path + '/hit.wav'))
            timeOfDeath = pygame.time.get_ticks()
            mode = 2

        animationFrame = 2 - (pygame.time.get_ticks() - timeSinceLastSpace)//100
        if animationFrame < 0:
            animationFrame = 0
        flappy.update(timeSinceLastSpace, fps)

    elif mode == 2:
        flappy.update(timeSinceLastSpace, fps)
        if (pygame.time.get_ticks() - timeOfDeath) > 1000:
            mode = 0

            del pipes
            del flappy
            
            pipes = []
            for i in range(numberOfPipes):
                pipes.append(Pipe(display_width + widthBetweenPipes*i, display_height, ground, pipeWidth))
            flappy = Bird(display_height, ground)

    for i in range(len(pipes)):
        pipes[i].show()
    flappy.show(animationFrame)

    for i in range(display_width//groundImage.get_width() + 2):
        DISPLAY.blit(groundImage, (groundImage.get_width()*i - (3* backgroundPosition % groundImage.get_width()), display_height - ground))

    DISPLAY.blit(font.render("Score = "+str(score), 1, (255, 255, 255)), (10, 10))

    if mode == 2:
        DISPLAY.blit(deadText, ((display_width - deadText.get_width())//2, (display_height - deadText.get_height())//2))

    pygame.display.update()
    clock.tick_busy_loop(120) 

    fps = 1000 / (pygame.time.get_ticks() - lastFrameMillis)
    pygame.display.set_caption('FLAPPY BIRD  fps = ' + str(int(fps)))
    lastFrameMillis = pygame.time.get_ticks()