#game gui class

from appJar import gui

class gameview:
    
    def __init__(self,type):
        self.game_view = gui("Focus game","800x600")
        
    
    
    
    def draw_grid_layout(self):
        pass
    

class gamemodel:
    
    def __init__(self):
        self.grid = gamemodel.initialize_grid()
        
    
    def initialize_grid():
        row_len = 8
        col_len = 8
        no_grid_list = ["00","01","06","07","10","17","60","67","70","71","76","77"]
        outer_ring_list = ["02","03","04","05","20","27","30","37","40","47","50","57","72","73","74","75"]
        
        
        for row in range(0,row_len):
            for col in range(0,col_len):
                