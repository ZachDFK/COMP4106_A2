#game gui class

from appJar import gui
import random
import copy
import player

class gameapp:
    
    def __init__(self,type):
        self.game_model = gamemodel()
        self.game_control = gamecontroller(self.game_model)        
        self.game_view = gameview(self.game_model)
        self.game_model.set_listener(self.game_view)
        if type == 2:
            self.set_game_2ai()
        elif type == 1:
            self.set_game_1ai()
        else:
            self.set_game_0ai()
    
    def set_game_0ai(self):
        self.player1 = player.playerhuman(1)
        self.player2 = player.playerhuman(2)
    def set_game_1ai(self):
        self.player1 = player.playerhuman(1)
        self.player2 = player.playerai(1)
        self.active_player = self.player1
    def set_game_2ai(self):
        self.player1 = player.playerai(1)
        self.player2 = player.playerai(2)
        self.active_player = self.player1
    def run_game(self):

        while not (self.game_model.is_game_over()):
            if turn%2 == 0 :
                self.active_player = self.player1
            else:
                self.active_player = self.player2
            
            temp_move = player.pick_move(self.game_model)
            print(self.game_model.active_player + " made move " + temp_move)        
class gameview:
    
    def __init__(self,game_model,type=0):
        self.gui = gui("Focus game","1280x720")
        self.gui.setBg("lightgrey")
        self.game_model = game_model
        self.draw_grid_layout()
        self.draw_stack()
        self.draw_spares_area()
        self.reset_flags()
    
    def reset_flags(self):
        self.locked_stack = False
        self.split_selected = False
        self.loc1_selected =  False
        self.available_spaces = []
        
    def draw_grid_layout(self):
        self.gui.startLabelFrame("Game Grid",0,0)
        self.gui.setSticky("news")        
        for row in range(0,8):
            for col in range(0,8):
                titleStr = str(row)+ "-" + str(col)
                grid_space_array = self.get_array_from_grid(titleStr)                
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
                    self.gui.setLabelFunction(titleStr,self.select_space)
                    self.gui.setLabelOverFunction(titleStr,self.show_stack)
        
        self.gui.stopLabelFrame()
    
    def update_grid_layout_and_spares(self):
        for row in range(0,8):
            for col in range(0,8):
                titleStr = str(row)+ "-" + str(col)
                grid_space_array = self.get_array_from_grid(titleStr)                
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
                self.gui.setLabelBg(titleStr,color)     
        self.gui.setLabel("G",str(len(self.game_model.player_green_spare_tokens)))
        self.gui.setLabel("R",str(len(self.game_model.player_red_spare_tokens)))
        self.gui.setLabel("active_player","The active player is :" + self.game_model.active_player)
    
    def draw_spares_area(self):
        self.gui.startLabelFrame("Green Player Spare",1,0)
        self.gui.setSticky("news")        
        self.gui.addLabel("G","0",0,0)
        self.gui.setLabelBg("G","green")
        self.gui.setLabelFunction("G",self.move_spare)        
        self.gui.stopLabelFrame()
    
        self.gui.startLabelFrame("Red Player Spare",1,1)
        self.gui.setSticky("news")        
        self.gui.addLabel("R","0",0,0)
        self.gui.setLabelBg("R","red")
        self.gui.setLabelFunction("R",self.move_spare)        
        self.gui.stopLabelFrame()
        self.gui.addLabel("active_player","The active player is :" + self.game_model.active_player,2,0)
    def draw_stack(self):
        self.gui.startLabelFrame("Selected Stack",0,1)
        self.gui.setSticky("news")              
        for index in range(0,5):
            color = "lightgrey"
            titleStr = str(5-index)
            self.gui.setSticky("news")
            self.gui.addLabel(titleStr,"",4-index,0)
            self.gui.setLabelBg(titleStr,color)
            self.gui.setLabelFunction(titleStr,self.select_split)
        self.gui.stopLabelFrame()
    
    
    
    def game_over_message(self):
        self.gui.warningBox("Game Over", "Loser is player: " + self.game_model.active_player)
        self.puzapp.setWarningBoxFunction("Game Over",self.gui.stop())
    def show_stack(self,space):
        if self.locked_stack:
            return
        grid_space_array = self.get_array_from_grid(space)
        for index in range(0,5):
            if len(grid_space_array) <= index :                    
                color = "lightgrey"
            else:
                if grid_space_array[index] == "G":
                    color = "green"
                else:
                    color = "red"
            
            titleStr = str(5-index)
            self.gui.setSticky("news")
            self.gui.setLabelBg(titleStr,color)
            
    
    def select_split(self, split):
        if self.loc1_selected:
            split_adjustment = 5 - self.max_stack
            grid_space_array = self.get_array_from_grid(self.loc1)
            if not(int(split) - split_adjustment > 0) :
                self.split = 1
            else:
                self.split = int(split) - split_adjustment
            self.split_selected = True
            print(self.split)
                  
            self.show_available_moves()
            self.locked_stack = False
            
    def move_spare(self,color):
        if int(self.gui.getLabel(color)) < 1:
            return
        elif color != self.game_model.active_player:
            return
        else:
            self.loc1 = "spare"
            self.loc1_selected = True
    def select_space(self,space):
        if not self.loc1_selected:
            last_element = self.get_array_from_grid(space).pop()
            if last_element == self.game_model.active_player:
                self.max_stack = len(self.get_array_from_grid(space))
                if self.max_stack != 0:
                    self.loc1 = space
                    self.loc1_selected = True
                    self.locked_stack = True            
        elif self.split_selected and space in self.available_spaces:
            self.loc2 = space
            result =  self.game_model.move_space(self.loc1,self.loc2,self.split)
            self.reset_flags()
            self.update_grid_layout_and_spares()
            if result == "Done":
                self.game_over_message()
        elif self.loc1 == "spare":
            self.loc2 = space
            result = self.game_model.move_spare(self.loc2)
            self.reset_flags()
            self.update_grid_layout_and_spares()            
            if result == "Done":
                self.game_over_message()
            
    def get_array_from_grid(self,space):
        row,col = space.split("-")
        row = int(row)
        col = int(col)
        grid_space_array = copy.deepcopy(self.game_model.grid[row][col])
        return grid_space_array
    
    def show_available_moves(self):
          
        self.available_spaces =  self.game_model.available_moves_from(self.loc1,self.split)
        print(self.available_spaces)
        for row in range(0,8):
            for col in range(0,8):
                space = str(row) + "-" + str(col)
                if space in self.available_spaces:
                    self.gui.setLabelBg(space,"yellow")
        
class gamemodel:
    
    def __init__(self,is_random = False):
        self.grid = self.initialize_grid(is_random)
        self.available_spaces = []
        self.active_player = "R"
    def set_listener(self,game_view):
        self.game_view = game_view
    def initialize_tokens(self):
        self.player_red_spare_tokens = []
        self.player_green_spare_tokens = []
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
        
    
    def available_moves_from(self,loc,split):
        row,col = loc.split("-")
        row = int(row)
        col = int(col)
        available_positions = []
        cardinals = [[1,-1],[-1,-1],[-1,1],[1,1]]
        
        while(split >0):        
            cardinal_index = 0            
            origin_row = row 
            origin_col = col + split
            temp_row = origin_row
            temp_col = origin_col 
            do = False
            inter = 0
            while not (do and (origin_row == temp_row and origin_col == temp_col)):
                do = True
                if  (gamemodel.outofbounds(temp_row,temp_col)):
                    space = str(temp_row) + "-" + str(temp_col)
                    available_positions.insert(0,space)
                                
                if split == inter:
                    inter = 0
                    cardinal_index += 1
                
                inter +=1
                temp_row += cardinals[cardinal_index][0]
                temp_col += cardinals[cardinal_index][1]                
                
            split -= 1
        return available_positions
    def outofbounds(x,y):
        coor = str(x) + str(y)
        if x > 7 or y > 7:
            return False
        elif x < 0 or y < 0:
            return False
        elif coor in ["00","01","06","07","10","17","60","67","70","71","76","77"]:
            return False
        else:
            return True
        
    def move_space(self,loc1,loc2,split):
        grid_array_l1 = self.get_array_from_grid(loc1)
        grid_array_l2 = self.get_array_from_grid(loc2)
        
        splited_array = []
        for num in range(0,split):
            splited_array.insert(0,grid_array_l1.pop())
        for token in splited_array:
            grid_array_l2.append(token)
        while len(grid_array_l2) > 5:
            temp_token = grid_array_l2.pop(0)
            if temp_token == "G":
                if self.active_player == "G":   
                    self.player_green_spare_tokens.append(temp_token)
            else:
                if self.active_player == "R":
                    self.player_red_spare_tokens.append(temp_token)
        
        self.change_array_on_grid(loc1,grid_array_l1)
        self.change_array_on_grid(loc2,grid_array_l2)
        
   
        self.change_active_player()
        if self.is_game_over():
            return "Done"                
    def move_spare(self,space):
        grid_array_l2 = self.get_array_from_grid(space)        
        grid_array_l2.append(self.active_player)
        while len(grid_array_l2) > 5:
            temp_token = grid_array_l2.pop(0)
            if temp_token == "G":
                if self.active_player == "G":   
                    self.player_green_spare_tokens.append(temp_token)
            else:
                if self.active_player == "R":
                    self.player_red_spare_tokens.append(temp_token)
        self.change_array_on_grid(space,grid_array_l2)
        if self.active_player == "G":
            self.player_green_spare_tokens.pop()
        else:
            self.player_red_spare_tokens.pop()
            
            
       
        self.change_active_player()
        if self.is_game_over():
            return "Done"        
    def change_array_on_grid(self,space,new_array):
        row,col = space.split("-")
        row = int(row)
        col = int(col)
        self.grid[row][col] = copy.deepcopy(new_array)
    def change_active_player(self):
        if self.active_player == "G":
            self.active_player = "R"
        else:
            self.active_player = "G"
    def get_array_from_grid(self,space):
        row,col = space.split("-")
        row = int(row)
        col = int(col)
        grid_space_array = copy.deepcopy(self.grid[row][col])
        return grid_space_array
    
    def is_game_over(self):
        if self.active_player == "G" and len(self.player_green_spare_tokens) != 0:
            return False
        elif self.active_player == "R" and len(self.player_red_spare_tokens) != 0:
            return False
        else:
            for row in range(0,8):
                for col in range(0,8):
                    titleStr = str(row) + "-" + str(col)
                    grid_space_array = self.get_array_from_grid(titleStr)
                    if len(grid_space_array) >0:
                        last_element = grid_space_array.pop()
                        if last_element == self.active_player:
                            return False
                    
            return True
            
class gamecontroller:
    
    def __init__(self,gamemodel):
        self.gamemodel = gamemodel
    def move_space(btn):
        return btn
    
    