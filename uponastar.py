# Hello World Team

# Upon A Star

# Eva

# RUN THIS FILE FOR GAME


import pygame
from menu import *

# music 
from pygame import mixer

# For Camera 
vec = pygame.math.Vector2
from abc import ABC, abstractmethod

# frame rate
clock = pygame.time.Clock()
FPS = 60

class User(pygame.sprite.Sprite):
    
    def __init__(self, x, y, scale, speed):
        super().__init__()
        # User attributes
        self.speed = speed
        self.direction = 1
        # Image flip by direction
        self.flip = False
        # Gravity to stay down and speed of jump
        self.gravity = 0.5
        self.jumpSpeed = -7

        self.velY = 0

        # Image
        imgRocket = pygame.image.load('rocket.png')
        self.image = pygame.transform.scale(imgRocket,(imgRocket.get_width()*scale, (imgRocket.get_height()*scale)))

        # Get methods used for retrieving values 
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Rectangular area - allows storing and manipulation
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        # 'camera' ground - where camera focuses from
        self.groundY = 580
        
    # User controls
    def movement(self):

        keyInput = pygame.key.get_pressed()
        # Set values to 0 
        dx = 0
        dy = 0 
         
        # moving left or right controls
        if keyInput[pygame.K_LEFT]:
            dx = -self.speed 
            self.flip = True
            self.direction = 1
          
            
        elif keyInput[pygame.K_RIGHT]:
            dx = self.speed 
            self.flip = False
            self.direction = 1
         
        # jumping control
        elif keyInput[pygame.K_UP]:
            self.jump()

        # coordinate change when moving
        self.rect.x += dx

    # jump method   
    def jump(self):
        self.direction = self.jumpSpeed
        
    # Gravity method 
    def worldGravity(self):
        self.direction += self.gravity
        self.rect.y += self.direction

    # Floor collision
    def checkCollisions(self):
        # Initialized before referenced
        dy = 0
        # Does not move below ground
        if self.rect.bottom + dy > 670:
            dy = 670 - self.rect.bottom

        self.rect.y += dy
        
# Stars throughout 
class Star(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('star.png')
        self.rect = self.image.get_rect(topleft = pos)
        
# Crater throughout map 
class Crater(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('block.png')
        self.rect = self.image.get_rect(topleft = pos)
        
        
# Layout     
class Layout(pygame.sprite.Sprite):
    def __init__(self, levelData, surface):
        self.displaySurface = surface
        self.layoutMap(levelData)

    def layoutMap(self, layout):
        self.craters = pygame.sprite.Group()
        self.stars= pygame.sprite.Group()
        # Iteration, each time 'X' appears a block is added  (crater 0r star)
        for rowIndex, row in enumerate (layout):
            for colIndex, cell in enumerate(row):
                x = colIndex *blockSize - camera.offset.x
                y = rowIndex *blockSize - camera.offset.y
                if cell == 'X':
                    crater = Crater((x,y), blockSize)
                    self.craters.add(crater)
                if cell == 'S':
                    star = Star((x,y), blockSize)
                    self.stars.add(star)               
                            
    def run(self):
        # Blocks
        self.craters.draw(self.displaySurface)
        # Stars
        self.stars.draw(self.displaySurface)

layoutMap = [
'                                                                    ',
'                                                                    ',
'                    S                                               ',
'                                                                    ',
'                                       S                            ',
'                                                                    ',
'                                                                    ',
'          S                                                         ',
'                                           S                        ',
'                           S                                        ',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']
blockSize = 64
displayWidth = len(layoutMap)*blockSize
displayHeight = len(layoutMap)*blockSize



# Cameras 
class playerCamera:
    def __init__(self, player):
        self.player = player
        # when moved
        self.offset = vec(0, 0)
        self.offsetFloat = vec(0, 0)
        # screen dimensions for camera movement
        self.displayWidth = 1040
        self.displayHeight = 700
        # camera constant - when it moves along, starts
        self.CONST = vec(-self.displayWidth / 2 + player.rect.w / 2, -self.player.groundY + 20)

    def setMethod(self, method):
        self.method = method

    def scrolling(self):
        self.method.scrolling()

class CamScroll(ABC):
    def __init__(self, camera,player):
        self.camera = camera
        self.player = player
        
# Camera to follow player
class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)
        
    # Follows player movement 
    def scrolling(self):
        self.camera.offsetFloat.x += (self.player.rect.x - self.camera.offsetFloat.x + self.camera.CONST.x)
        self.camera.offsetFloat.y += (self.player.rect.y - self.camera.offsetFloat.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offsetFloat.x), int(self.camera.offsetFloat.y)


class Game():
    # Allows access to pygame features
    def __init__(self):
        # Changes title
        pygame.display.set_caption('Upon A Star')
        # Changes icon of window
        iconStar = pygame.image.load("star.png")
        pygame.display.set_icon(iconStar)
        pygame.init()
        
        # Game states
        self.running = True
        self.playing = False
        
        # Control inputs
        self.escKey = False
        self.downKey = False
        self.upKey = False
        self.spaceBar = False
        self.enterKey = False
        
        # Canvas dimension
        self.displayWidth = 1200
        self.displayHeight = 750
        
        # Canvas
        self.display = pygame.Surface((self.displayWidth, self.displayHeight))
        self.monitor = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.window = pygame.display.set_mode(((self.displayWidth, self.displayHeight)))
        
        
        self.background = pygame.Surface((self.displayWidth, self.displayHeight))
        # Where to find font file
        self.fontName = 'ChailceNogginRegular-2OxoW.ttf'
        
        # colours 
        self.Black, self.White = (0,0,0),(255,255,255)
        # Halfway through the display
        self.midW = self.displayWidth/2
        self.midH = self.displayHeight/2
        
                
        #Options
        self.options = menuOptions(self)
        self.controls = displayControls(self)
        self.information = displayInfo(self)
        self.contacts= displayContact(self)
        self.runMenu = self.options

    # Background fill 
    Backgr = (0,0,0)
    def drawBackgr(self):
        self.window.fill(self.Backgr)
        
        
    def checkEvents(self):
        for event in pygame.event.get():
             
            # Closes when window button x pressed 
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                self.running = False
                self.playing = False
                self.runDisplay = False
                
            # Has the player entered a key
            if event.type == pygame.KEYDOWN:
                # space bar
                if event.key == pygame.K_SPACE:
                    self.spaceBar = True
                # up key
                elif event.key == pygame.K_UP:
                    self.upKey = True
                # down key
                elif event.key == pygame.K_DOWN:
                    self.downKey = True
                # enter key
                elif event.key == pygame.K_k:
                    self.enterKey = True

                # Inputs for camera
                # Camera follows player
                elif event.key == pygame.K_c:
                    camera.setMethod(follow)
                        
                # esc key - shorthand quit
                if event.key == pygame.K_ESCAPE:
                    self.escKey = True
                    pygame.quit()
                    exit()
                    

    # stopped pressing               
    def reset_keyInput(self):
        self.escKey = False
        self.downKey =  False
        self.upKey = False
        self.spaceBar = False

    # Screen text
    def displayText(self, text, size, x, y ):
        font = pygame.font.Font(self.fontName,size)
        textSurface = font.render(text, True, self.White)
        textRect = textSurface.get_rect()
        # center text
        textRect.center = (x,y)
        # text displayed 
        self.display.blit(textSurface,textRect)

    # Screen cursor image 
    def displayBread(self, x, y, scale):

        # Image 
        imgBreadcur = pygame.image.load('cursor.png')
        # bread png scaled to fit screen
        image = pygame.transform.scale(imgBreadcur,(imgBreadcur.get_width()*scale, (imgBreadcur.get_height()*scale)))
        width = image.get_width()
        height = image.get_height()
        imgRect = image.get_rect()
        imgRect.center = (x,y)
        # image displayed 
        self.display.blit(image,imgRect)

    # Scrolling Experience
    def gameLoop(self):
        while self.playing:

            clock.tick(FPS)

            # Background fill per frame
            self.drawBackgr()
            
            # Background change --> Title start 
            self.background = pygame.image.load('bg.jpg')
            # lining window/display
            self.window.blit(self.background, (0 - camera.offset.x,0 - camera.offset.y))
            
            # Title 
            font = pygame.font.Font('ChailceNogginRegular-2OXoW.ttf',20)
            self.title = font.render('''Upon A Star! ''',True,self.White)
            self.title.blit(self.title, (100 - camera.offset.x, 100 - camera.offset.y))

            # Layout placed
            layout = Layout(layoutMap , self.window)
            layout.run()
            
            #Camera moves with the player 
            self.window.blit(pygame.transform.flip(user.image,user.flip, False), (user.rect.x - camera.offset.x, user.rect.y - camera.offset.y))

            # Player moving called to run
            user.movement()     

            # Gravity added
            user.worldGravity()

            # Collisions
            user.checkCollisions()
            
            # Camera moves with player movement 
            camera.scrolling()

            # Has the user pressed a key 
            self.checkEvents()

            # Spacebar pressed - back to Menu
            if self.spaceBar:
                
                self.playing = False
            
            
            #Reset inputs and display
            pygame.display.update()
            self.reset_keyInput()

    
# x-pos, y-pos, scaling, speed
# Instantiation
user = User(550, 600, 1, 20)

# Scroll Player Camera 
camera = playerCamera (user)
follow = Follow (camera, user)
camera.setMethod(follow)


# Runs Game 
g = Game()

while g.running:
    # Runs Menu
    g.runMenu.displayMenu()
    # Runs Game
    g.gameLoop()
