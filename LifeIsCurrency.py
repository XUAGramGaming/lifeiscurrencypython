import pygame, sys, random
from pygame.locals import *
 
class Player():
    def __init__(self, color, x, y, width, height, life=500, font=20, velocity=0):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height    
        self.life = life
        self.font = font
        self.velocity = velocity
    
    def draw(self, win, outline=None, color=(0,0,0)):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        lifeText = str(self.life)
        font = pygame.font.SysFont('comicsans', self.font)
        text = font.render(lifeText, 1, color)
        win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
        
    def moveX(self):
        if(self.velocity > 0):
            if(self.x < (windowWidth - self.width)):
                self.x += self.velocity
            else:
                self.velocity = 0
        if(self.velocity < 0):
            if(self.x > 0):
                self.x += self.velocity
            else:
                self.velocity = 0
        self.life -= abs(self.velocity)

class FallingBlock():
    def __init__(self, color, x, y, width, height, taken = False, life=0, font=20, countdown=20):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.taken = taken
        self.life = life
        self.font = font
        self.countdown = countdown

    def countdown():
        self.countdown -= 1
    
    def draw(self, win, outline=True, color=(0,0,0)):
        if(self.taken == False):  
            if outline:
                pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
            if(self.life > 0):
                self.color = BRIGHT_GREEN
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

            lifeText = str(self.life)
            font = pygame.font.SysFont('comicsans', self.font)
            text = font.render(lifeText, 1, color)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
            
class Label:
    def __init__(self, x, y, text="", font=30, color=(0,0,0)):
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.color = color
    
    def draw(self, win):
        font = pygame.font.SysFont('comicsans', self.font, color)
        text = font.render(self.text, 1, self.color)
        win.blit(text, (self.x, self.y))

class RandomLayer:
    def __init__(self, min, max, height, dropping=False):
        self.BlockLives = []
        self.min = min
        self.max = max
        self.height = height
        self.dropping = dropping
        #0,50 50,100 100,150 150,200 200,250 
        for i in range(0, 14):
            self.BlockLives.append(FallingBlock(BRIGHT_RED, i*50, self.height, 50, 50, False, random.randint(self.min, self.max+1), font=20))
        
    def addLife(self, minX, maxX):
        i = 0
        while i < len(self.BlockLives):
            if(self.BlockLives[i].taken == False):
                xBlockMin = self.BlockLives[i].x
                xBlockMax = self.BlockLives[i].x + self.BlockLives[i].width
                value = (minX > xBlockMin)
                value2 = (minX < xBlockMax)
                if(minX >= xBlockMin and minX <= xBlockMax):
                    self.BlockLives[i].taken = True
                    player1.life += self.BlockLives[i].life
                if(maxX >= xBlockMin and maxX <= xBlockMax):
                    self.BlockLives[i].taken = True
                    player1.life += self.BlockLives[i].life
            i += 1

        
    
    def drop(self, DropBy):
        i = 0
        while i < len(self.BlockLives):
            self.BlockLives[i].y += DropBy
            self.height = self.BlockLives[i].y
            i += 1
        

    def drawBlocks(self, win):
        i = 0
        while i < len(self.BlockLives):
            self.BlockLives[i].draw(win)
            i += 1
        
    
    def reset(self, min, max, height):
        self.BlockLives = []
        self.min = min
        self.max = max
        self.height = height
        for i in range(0, 14):
            self.BlockLives.append(FallingBlock(BRIGHT_RED, i*50, self.height, 50, 50, False, random.randint(self.min, self.max+1), font=20))


        

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

gameTime = float(0.00)
FPS = 30
fpsClock = pygame.time.Clock()
windowWidth = 700
windowHeight = 500
DISPLAYSURF = pygame.display.set_mode((windowWidth, windowHeight), 0, 32)
pygame.display.set_caption('Raining Life')
WHITE = (255, 255, 255)
BLUE = (41, 52, 98)
RED = (166, 73, 66)
BRIGHT_RED = (254, 95, 85)
DARK_WHITE = (255, 241, 193)
GREEN = (82, 189, 114)
BRIGHT_GREEN = (68, 219, 113)
dead = False
tillNextDrop = 5
win = False
BlockLayer = RandomLayer(0, 5, 50, False)
player1 = Player(DARK_WHITE, windowWidth / 2, windowHeight - 50, 50, 50, 1000, 20)
dead_text = Label(50, windowHeight / 2 - 50, "Oh no, you have died! Better luck next time.", font=30, color=DARK_WHITE)
dead2_text = Label(50, windowHeight / 2, "Press <R> to play again!", font=28, color=DARK_WHITE)
win_text = Label(50, windowHeight / 2 - 50, "CONGRADULATIONS KID! You played well.", font=30, color=DARK_WHITE)
win2_text = Label(50, windowHeight / 2, "Press <R> to play again!", font=28, color=DARK_WHITE)
winTime_text = Label(50, windowHeight / 2 + 50, "Game Time: LOADING", font=28, color=DARK_WHITE)

wincondition_text = Label(370, 3, "Reach 2000 Life pts to win!", font=28, color=BRIGHT_GREEN)
pointsNeeded_text = Label(370, 30, "Life points to win: LOADING", font=20, color=GREEN)



timer_text = Label(200, 30, "Game time: LOADING", font=20, color=DARK_WHITE)

countdown_text = Label(0, 3, "Current Countdown: LOADING", font=30, color=BRIGHT_RED)
life_text = Label(0, 30, "Current Life: LOADING", font=20, color=RED)

pygame.mixer.music.load("BackgroundMusic.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

pygame.time.set_timer(USEREVENT+1, 1000)
pygame.time.set_timer(USEREVENT+2, 10)  
def gameTimer():
    global gameTime
    gameTime += 0.01
    gameTime = round(gameTime, 3)

while True:
    if(dead == False and win == False):
        DISPLAYSURF.fill(BLUE)
        player1.draw(DISPLAYSURF, False, (0, 0, 0))
        player1.moveX()
        countdown_text.draw(DISPLAYSURF)
        wincondition_text.draw(DISPLAYSURF)
        pointsNeeded_text.draw(DISPLAYSURF)
        BlockLayer.drawBlocks(DISPLAYSURF)
        timer_text.draw(DISPLAYSURF)
        timer_text.text = "Game time: %f" % gameTime
        pointsNeeded_text.text = "Points needed: %d" % abs((player1.life - 2000))
        life_text.text = "Current Life: %d" % player1.life
        life_text.draw(DISPLAYSURF)
        if(player1.life >= 2000):
            win = True

        if(BlockLayer.dropping == True):
            if(BlockLayer.height >= windowHeight-100):
                playerX = player1.x
                playerX_MAX = player1.x + player1.width
                BlockLayer.addLife(playerX, playerX_MAX)
                if(player1.life <= 0):
                    dead = True
            if(BlockLayer.height >= 800):
                BlockLayer.dropping = False
                tillNextDrop = 2
                BlockLayer.reset(-100, 100, 50)
            BlockLayer.drop(5)
            
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == USEREVENT+1:
                if(tillNextDrop > 0):
                    countdown_text.text = "Current Countdown: %d" % tillNextDrop
                    tillNextDrop -= 1
                if(tillNextDrop == 0):
                    BlockLayer.dropping = True
                    countdown_text.text = "Current Countdown: Dropping"
            if event.type == USEREVENT+2:
                gameTimer()
        #KEYBOARD LISTENER
        keyArray = pygame.key.get_pressed()

        if(player1.velocity > 0):
            player1.velocity -= 1
        if(player1.velocity < 0):
            player1.velocity += 1
        #WASD MOVING
        
        if(player1.life > 0):    
            if keyArray[pygame.K_a]:
                player1.velocity -= 3
            if keyArray[pygame.K_d]:
                player1.velocity += 3
        else:
            player1.velocity = 0
            player1.life = 0


    if(dead == True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(BLUE)
        dead_text.draw(DISPLAYSURF)
        dead2_text.draw(DISPLAYSURF)
        keyArray = pygame.key.get_pressed()
        if(keyArray[pygame.K_r]):
            tillNextDrop = 5
            player1.life = 1000
            player1.x = windowWidth / 2
            gameTime = 0.00
            BlockLayer.reset(-20, 20, 50)
            dead = False
            win = False

    if(win == True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(GREEN)
        win_text.draw(DISPLAYSURF)
        win2_text.draw(DISPLAYSURF)
        
        winTime_text.text = "Game Time: %f" % gameTime
        winTime_text.draw(DISPLAYSURF)

        keyArray = pygame.key.get_pressed()
        if(keyArray[pygame.K_r]):
            tillNextDrop = 5
            player1.life = 1000
            player1.x = windowWidth / 2
            BlockLayer.reset(-20, 20, 50)
            gameTime = 0.00
            dead = False
            win = False
            

    pygame.display.update()
    fpsClock.tick(FPS)
        
