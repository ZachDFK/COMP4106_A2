#the main file inside the src

from appJar import gui
from .game import game_file

class Main:
    
    def press(self,btn):
        type = -1 
        if btn == "Player vs. Player":
            type = 0
        elif btn == "Player vs. AI":
            type = 1
        elif btn == "AI vs. AI":
            type = 2
        else:
            self.app.stop()
            return
        
        game_app = game_file.gameapp(type, (self.app.getRadioButton("randomBoard") == "Random"))
        
    def __init__(self):
        self.app = gui("Assignment 2","800x600")
        self.app.addLabel("assignment2_title","Welcome to AI Assignment 2", 0, 0)
        self.app.addLabel("authorFiller","Name:\tZacharie Gauthier \nStudent ID:\t100897337",1,0)
        self.app.addButtons(["Player vs. Player","Player vs. AI", "AI vs. AI","Quit"],self.press,3,0,2)
        self.app.addRadioButton("randomBoard","Symetric",4,0)
        self.app.addRadioButton("randomBoard","Random",4,1)
        self.app.go()

