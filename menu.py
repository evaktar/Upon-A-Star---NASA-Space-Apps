# Menu
import pygame
# music 
from pygame import mixer
from tkinter import *
from tkinter import font

# Menu Music
class menuMus():
    def __init__(self):
        # Background music begins when option is selected 
        backgroundMusic = mixer.music.load('milkShake.mp3')
        # keeps repeating when music ends so set to -1 
        mixer.music.play(-1)
        
# Main Menu        
class Menu():
    def ___init__ (self, game):
        # Access to variables in game object
        self.game = game
        # When game running
        self.runDisplay = True
        self.cursorRect = pygame.Rect(0, 0, 30, 30)
        self.offset = -1

    def displayCursor(self):
        # Cursor appearance
        self.game.displayBread(self.cursorRect.x, self.cursorRect.y, 0.2)
        
    def blitScreen(self):
        # display update
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keyInput()

class menuOptions(Menu):
    def __init__ (self, game):
        # Access to variables in game object
        self.game = game

        # Halfway through the display, shorter than typing out .game everytime 
        self.midW = self.game.displayWidth/2
        self.midH = self.game.displayHeight/2

        self.cursorRect = pygame.Rect(0, 0, 30, 30)
        self.offset = - 100
        
        # Play
        self.state = 'Play'
        self.playx = self.midW 
        self.playy = self.midH + 30
        # Controls
        self.controlx = self.midW 
        self.controly = self.midH + 70
        # Information
        self.sBx = self.midW 
        self.sBy = self.midH + 110
        # Contacts
        self.cx = self.midW 
        self.cy = self.midH + 150
        # Credits
        self.ccx = self.midW 
        self.ccy = self.midH + 180
        # Quit
        self.quitx = self.midW 
        self.quity = self.midH + 220
        # Cursor start position
        self.cursorRect.midtop = (self.playx - self.offset, self.playy)

    # Menu display components - text and images
    def displayMenu(self):
        self.runDisplay = True
        menuMus()
        while self.runDisplay:
            # has player pressed a key 
            self.game.checkEvents()
            # method for states - change in display for options
            self.checkInput()
            self.game.display.fill(self.game.Black)
            # Title
            self.game.displayText('Upon A Star', 50, self.midW, self.midH - 100)
            # Menu
            self.game.displayText('Menu', 30, self.midW, self.midH - 15)
            # Play
            self.game.displayText('Play', 21, self.playx, self.playy)
            # Controls
            self.game.displayText('Controls', 21, self.controlx, self.controly)
            # Scoreboard
            self.game.displayText('Quiz', 21, self.sBx, self.sBy)
            # Background story
            self.game.displayText('Contacts', 21, self.cx, self.cy)
            self.game.displayText('and Credits', 20, self.ccx, self.ccy)
            # Quit
            self.game.displayText('Quit', 21, self.quitx, self.quity)
            self.displayCursor()
            self.blitScreen()

    def cursorMovement(self):
        # Going down options
        if self.game.downKey:
             # Play --> Controls
            if self.state == 'Play':
                self.cursorRect.midtop = (self.controlx - self.offset, self.controly)
                self.state = 'Controls'
            # Controls --> Information
            elif self.state == 'Controls':
                self.cursorRect.midtop = (self.sBx - self.offset, self.sBy)
                self.state = 'Information'
            # Information --> Contacts
            elif self.state == 'Information':
                self.cursorRect.midtop = (self.cx - self.offset, self.cy)
                self.state = 'Contacts'
                # Contacts  --> Quit
            elif self.state == 'Contacts':
                self.cursorRect.midtop = (self.quitx - self.offset, self.quity)
                self.state = 'Quit'
            # Quit --> Play
            elif self.state == 'Quit':
                self.cursorRect.midtop =(self.playx - self.offset, self.playy)
                self.state = 'Play'
                
        # Moving up options
        elif self.game.upKey:
            # Quit <-- Play
            if self.state == 'Play':
                self.cursorRect.midtop = (self.quitx - self.offset, self.quity)
                self.state = 'Quit'
            # Play <-- Controls
            elif self.state == 'Controls':
                self.cursorRect.midtop = (self.playx - self.offset, self.playy)
                self.state = 'Play'
            # Controls <-- Information
            elif self.state == 'Information':
                self.cursorRect.midtop = (self.controlx - self.offset, self.controly)
                self.state = 'Controls'
            # Scoreboard <-- Contacts 
            elif self.state == 'Contacts':
                self.cursorRect.midtop = (self.sBx - self.offset, self.sBy)
                self.state = 'Information'
            # Contacts  <-- Quit
            elif self.state == 'Quit' :
                self.cursorRect.midtop = (self.cx - self.offset, self.cy)
                self.state = 'Contacts'

    def checkInput(self):
        self.cursorMovement()
        # Spacebar pressed /Selection
        if self.game.spaceBar: 
            if self.state == 'Play':
                self.game.playing = True
            # If spacebar on Controls, displays screen with controls
            elif self.state == 'Controls':
                self.game.runMenu = self.game.controls
            # If spacebar on Scoreboard, displays screen with high scores 
            elif self.state == 'Information':
                self.game.runMenu = self.game.information
            # If spacebar on BgS, displays screen with text
            elif self.state == 'Contacts':
                self.game.runMenu = self.game.contacts
            # If spacebar on Quit, program closes
            elif self.state == 'Quit':
                # Quit game at menu 
                pygame.quit()
                exit()
                    
            #Go back to Menu when spacebar pressed
            self.runDisplay = False

# CONTROLS SCREEN
class displayControls(Menu):
    def __init__ (self, game):
        self.game = game
        # Halfway through the display
        self.midW = self.game.displayWidth/2
        self.midH = self.game.displayHeight/2

    def userControls(self):
        self.game.display.fill(self.game.Black)
        # Tells user the controls
        self.game.displayText('Right Arrow = Move Forwards', 20, self.midW, self.midH + 30)
        self.game.displayText('Left Arrow = Move Backwards', 20, self.midW, self.midH + 70)
        self.game.displayText('Up Arrow = Jump', 20, self.midW, self.midH + 110)
        self.game.displayText('Escape Key = Quit', 20, self.midW, self.midH + 190)


    def displayMenu(self):
        self.runDisplay = True
        while self.runDisplay:
            self.game.checkEvents()
            self.userControls()
            
            if self.game.spaceBar:
                # go back to main menu
                self.game.runMenu = self.game.options
                self.runDisplay = False
                
            # reset display call
            self.blitScreen()             
        

# INFORMATION SCREEN
class displayInfo(Menu):
    
    def __init__ (self, game):
        self.game = game
        # Halfway through the display
        self.midW = self.game.displayWidth/2
        self.midH = self.game.displayHeight/2
        
    def quizPlay(self):
        self.game.display.fill(self.game.Black)
        def next():
    
            global total,questionNum

            total = 0
            questionNum = 1
    
            if(value1.get()):
                selected_option = 1
            elif(value2.get()):
                selected_option = 2
            elif(value3.get()):
                selected_option = 3
            else:
                selected_option = -1
    
            if(Answers[questionNum-1] == selected_option):
                total += 1

            if(questionNum == totalQs-1):
                selectButton.config(text="Submit")
            questionNum = questionNum + 1

    

            if(questionNum > totalQs):
                root.pack_forget()
                total_output.place(relx=.45,rely=.45)
                total_output.config(text = "Total: " +str(total))

            else:
                value1.set(0) 
                value2.set(0) 
                value3.set(0) 
                question.config(text=Questions[questionNum-1])
                option1.config(text=Options[questionNum-1][0])
                option2.config(text=Options[questionNum-1][1])
                option3.config(text=Options[questionNum-1][2])

        def Check(Option):
            if(Option == 1):
                value2.set(0)
                value3.set(0)
        
        
            elif(Option == 2):
                value1.set(0)
                value3.set(0)
      
            elif(Option == 3):
                value1.set(0)
                value2.set(0)

        Questions = ["What is a variable star?" ,
                    "What are the two type of variabe stars?" , 
                    "Which one is an eclipsing binary star?",
                     "In what ways do stars vary?",
                     "What affects the luminosity of a star?"]
    
        Options = [["A star whose light varies","A star that explodes", "A star that blinks"],
                    ["Intristict and Extrinstinct","Intact and Extinct", "Intrinsic and Extrinsic"],
                    ["North Star","Alphecca", "Cepheids"],
                   ["In luminosity and surface area","In mass and colour", "Both"],
                   ["Temperature","Surface area", "Both"]]
    
        Answers = [1 , 3 , 2, 3, 3]

        totalQs = 5

        Win= Tk()
        Win.title("Quiz Time")

        root = Frame(Win)
        root.pack()

        question = Label(root,width = 40,font=('Arial', 30),text=Questions[0])
        question.pack(fill=X)
    
        value1 = IntVar()
        value2 = IntVar()
        value3 = IntVar()

        option1 = Checkbutton(root,variable=value1,text=Options[0][0],command=lambda:Check(1))
        option1.pack()

        option2 = Checkbutton(root,variable=value2,text=Options[0][1],command=lambda:Check(2))
        option2.pack()

        option3 = Checkbutton(root,variable=value3,text=Options[0][2],command=lambda:Check(3))
        option3.pack()

        selectButton= Button(root , text = "Select",command=next)
        selectButton.pack()

        total_output = Label(Win,font=(40))
        total_output.place_forget()

        Win.mainloop()
        
    def displayMenu(self):
        self.runDisplay = True
        while self.runDisplay:
            self.game.checkEvents()
            self.quizPlay()
            if self.game.spaceBar:
                self.game.runMenu = self.game.options
                self.runDisplay = False
                
            # reset display call
            self.blitScreen()
            
# CONTACTS SCREEN
class displayContact(Menu):
    # Initialisation
    def __init__ (self, game):
        self.game = game
        # Halfway through the display
        self.midW = self.game.displayWidth/2
        self.midH = self.game.displayHeight/2

    def Credits_References(self):
        self.game.display.fill(self.game.Black)
        # Email
        self.game.displayText('eva.mohamedmala@mail.bcu.ac.uk', 22, self.midW, self.midH + 30)
        # Email
        self.game.displayText('shanza.babar@mail.bcu.ac.uk', 21, self.midW, self.midH + 70)
        # Reference Websites
        self.game.displayText('Websites used for info:', 20, self.midW, self.midH + 120)
        self.game.displayText('Brittanica, Space.com, atnf.csiro.au, NASA, Forbes ', 18, self.midW, self.midH + 150)

    def displayMenu(self):
        
        self.runDisplay = True
        while self.runDisplay:
            self.game.checkEvents()
            self.Credits_References()
            if self.game.spaceBar:
                self.game.runMenu = self.game.options
                self.runDisplay = False
            
            # reset display call
            self.blitScreen()
