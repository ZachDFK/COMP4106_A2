class player:
    
    def __init__(self,name):
        self.name = name
    
    
class playerai(player):
    
    
    def __init__(self,heuristic ):
        self.name = "AI " + str(heuristic)
        self.heuristic = playerai.get_heuristic(heuristic)
    
    
    def get_heuristic(type):
        
        if type == 1:
            return playerai.heuristic1
        else: 
            return playerai.heuristic2
        
    def heuristic1():
        pass
    
    def heuristic2():
        pass
    
    
    def make_move_min_max():