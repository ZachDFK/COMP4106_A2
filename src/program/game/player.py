import copy
import threading
import random
from ..game import game_file
class player:
    
    def __init__(self,name):
        self.name = name
    
    def get_color  (number):
        if number == 1:
            return "R"
        else:
            return "G"
class playerai(player):
    __max_level = 3
    
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
    ### Heuristic focuses on maxing the number of options for a player
    def heuristic1(game_model,color):
        
        if color == "G" :
            opposite_color = "R"
        else:
            opposite_color = "G"
            
        number_of_movable_tokens = len(game_model.get_available_location1(color))
        number_of_opposite_movable_tokens = len(game_model.get_available_location1(opposite_color))
        
        spare_tokens = len(game_model.get_spare_tokens_of_color(color))
        opposite_spare_tokens = len(game_model.get_spare_tokens_of_color(opposite_color))
        
        positive = number_of_movable_tokens + spare_tokens
        negative = number_of_opposite_movable_tokens + opposite_spare_tokens
        
        
        return positive - negative + playerai.randomizer()

    ### Heuristic focuses on maxing the number of tokens for a player
    def heuristic2(game_model,color):
        if color == "G" :
            opposite_color = "R"
        else:
            opposite_color = "G"
        
        positive = game_model.get_number_of_tokens_for_color(color)
        negative = game_model.get_number_of_tokens_for_color(opposite_color)
        
        return positive - negative + playerai.randomizer()
    def randomizer():
        value = random.randint(1,1000)
    
        if value%1000 == 0:
            value = 1
            if random.randint(1,2) ==2:
                value = value *-1        
        else:
            value = 0
        return value
        
    def make_move(self,game_model,level,alpha,beta):
        best_loc1 = "99-99"
        best_loc2 = "99-99"
        best_split = "99"
        best_move_array = [best_loc1,best_loc2,best_split]
        if(level%2 != 0):
            if self.color == "G":
                color = "R"
            else:
                color = "G"
        else:
            color = self.color
        if(game_model.is_game_over() or level == playerai.__max_level):
            current_score = self.heuristic(game_model,color)
            move_array = [best_loc1,best_loc2,best_split]
            return [move_array,current_score]
        else:
            next_moves = game_model.assemble_all_possible_combos_for_ai(color)            
            for move in next_moves:
                curr_loc1 = move[0]
                curr_loc2 = move[1]         
                if curr_loc1 != "spare":
                    curr_split = move[2]
                    game_model.move_space(curr_loc1,curr_loc2,curr_split,False,level)
                else:
                    curr_split = "99"
                    game_model.move_spare(curr_loc2,False,level)
                current_move_array  = [curr_loc1,curr_loc2,curr_split]
                
                current_score_array = self.make_move(game_model,level+1,alpha,beta)
                current_score = current_score_array[1]
                #compare alpha
                if level%2 ==0:
                    is_alpha = True
                    if current_score > alpha:
                        alpha = current_score
                        best_move_array = current_move_array
                else:
                    is_alpha = False                    
                    if current_score < beta:
                        beta = current_score
                        best_move_array = current_move_array
                
                game_model.undo_move(current_move_array,level)
                if alpha >=beta :
                    break
            if is_alpha:
                bscore  = alpha
            else:
                bscore = beta
            
            return [best_move_array,bscore]
                
class playerhuman(player):
    
    def __init__(self,num):
        self.name = "HMN " + str(num)
        self.is_ai = False
        self.color = player.get_color(num)