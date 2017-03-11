#game gui class

from appJar import gui
import random

class gameapp:
    
    def __init__(self,type):
        self.game_model = gamemodel()
        self.game_control = gamecontroller(self.game_model)        
        self.game_view = gameview(self.game_model)
        self.game_view.gui.go()
        

class gameview:
    
    def __init__(self,game_model,type=0):
        self.gui = gui("Focus game","800x600")
        self.gui.setBg("lightgrey")
        self.game_model = game_model
        self.draw_grid_layout()
        
    
    
    def draw_grid_layout(self):
        self.gui.startLabelFrame("Game Grid")
        self.gui.setSticky("news")        
        for row in range(0,8):
            for col in range(0,8):
                grid_space_array = self.game_model.grid[row][col]
                titleStr = str(row)+ "-" + str(col)
                self.gui.setSticky("news")
                self.gui.setPadding([10,10])
                self.gui.setInPadding([10,10])
                if len(grid_space_array) == 0: 
                    color = "black"                    
                elif grid_space_array[0] == "X":
                    color = "lightgrey"
                else:
                    last_element = grid_space_array.pop()
                    grid_space_array.append(last_element)
                    if last_element == "R":
                        color = "red"
                    else:
                        color = "green"
                
                self.gui.addLabel(titleStr,"",row,col)
                self.gui.setLabelBg(titleStr,color)
                if color != "lightgrey":
                    self.gui.setLabelFunction(titleStr,gamecontroller.move_space)
        
        self.gui.stopLabelFrame()
        
    

class gamemodel:
    
    def __init__(self,is_random = False):
        self.grid = self.initialize_grid(is_random)
        
        
    
    def initialize_tokens(self):
        self.player_red_token = []
        self.player_green_token = []
        self.grid_tokens = []
        streak = 0
        flag = False
        for index in range(0,36):
            if streak > 1 :
                streak = 0
                flag = not flag
            if flag:
                token = "R"
            else:
                token = "G"
                
            self.grid_tokens.append(token)
            streak +=1
        print(self.grid_tokens)
    def initialize_grid(self,is_random=False):
        
        row_len = 8
        col_len = 8
        no_grid_list = ["00","01","06","07","10","17","60","67","70","71","76","77"]
        outer_ring_list = ["02","03","04","05","20","27","30","37","40","47","50","57","72","73","74","75"]
        self.initialize_tokens()
        grid = []
        for row in range(0,row_len):
            temp_row = []
            for col in range(0,col_len):
                coor_str = str(row) + str(col)
                if coor_str in no_grid_list:
                    temp_row.append(["X"])
                elif coor_str in outer_ring_list:
                    temp_row.append([])
                else:
                    temp_row.append([self.grab_token()])
            grid.append(temp_row)
        
        return grid
    def grab_token(self,is_random=False):
        
        if is_random :
            max_range = len(self.grid_tokens) -1
            return self.grid_tokens.pop(random.randint(0,max_range))
        else:
            return self.grid_tokens.pop()

class gamecontroller:
    
    def __init__(self,gamemodel):
        pass
    
    def move_space(btn):
        print(btn)
        