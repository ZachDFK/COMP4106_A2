class player:
    
    def __init__(self,name):
        self.name = name
    
    def get_color  (number):
        if number == 1:
            return "R"
        else:
            return "G"
class playerai(player):
    
    
    def __init__(self,heuristic ):
        self.name = "AI " + str(heuristic)
        self.heuristic = playerai.get_heuristic(heuristic)
        self.is_ai = True
        self.color = player.get_color(heuristic)
    def get_heuristic(type):
        
        if type == 1:
            return playerai.heuristic1
        else: 
            return playerai.heuristic2
        
    def heuristic1():
        pass
    
    def heuristic2():
        pass
    
    
    def make_move(self,game_model,level,alpha,beta):
        pass
class playerhuman(player):
    
    def __init__(self,num):
        self.name = "HMN " + str(num)
        self.is_ai = False
        self.color = player.get_color(num)