# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 21:38:58 2017

@author: ChrisCuts
"""

from TicTacToe import TicTacToe
from random import choice, random

import matplotlib.pyplot as plt
        
PAUSE = None

### Create game
# Pause after restart is sensible, without pause the game is not updated
game = TicTacToe(pauseafterrestart=0.0000001)

# Create statistics panel
fig = plt.figure('Stats')
ax_Qs = plt.subplot(2, 1, 1)
plt.hold(True)
ax_Ps = plt.subplot(2, 1, 2)
plt.hold(True)
ax_Qs.cla()
ax_Ps.cla()

# Count points
points = {'X': [0], 'O': [0]}

def pause():
    if PAUSE:
        game.sleep(PAUSE)

# Statistics panel update function
def plot_stats(path, path2, winner):
    ax_Qs.cla()
    #print(winner, path, path2)
    if winner == 'X':
        ax_Qs.plot(path)
        ax_Qs.plot(path2)
        
        points['X'].append(points['X'][-1] + 1)
        points['O'].append(points['O'][-1])
    else:
        ax_Qs.plot(path2)
        ax_Qs.plot(path)
        
        points['O'].append(points['O'][-1] + 1)
        points['X'].append(points['X'][-1])
        
    ax_Ps.cla()
    ax_Ps.plot(points['X'])
    ax_Ps.plot(points['O'])
    plt.legend(('X', 'O'))
    

class Learner():   
    '''Reinforcement Q learner'''
    
    # learning rate
    ALPHA = 0.5
    # discount factor
    DISCOUNT = 0.1
    
    Q_INIT = 0
    
    def __init__(self, name, greedy=1):
        self.Qs = {}
        self.path = []
        
        # initialize state and action
        self.old_state = (0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.old_action = 0
        
        self.name = name
        
        # initialize greedy factor
        self.greedy = greedy
        
    def rotate(x):
        '''rotate game board 90°'''
        return [x[6], x[3], x[0], x[7], x[4], x[1], x[8], x[5], x[2]]
        
    def Q(self, s, a):
        '''get Q if there is one for this action'''
        if s in self.Qs and a in self.Qs[s]:
            return self.Qs[s][a]
        else:
            return self.Q_INIT
    
    def update_q(self, r, q_max):
        '''learn Q'''
        s = self.old_state
        a = self.old_action
        
        # create status
        if s not in self.Qs:
            self.Qs[s] = {}
            
        # create action in status and initialize
        if a not in self.Qs[s]:
            self.Qs[s][a] = self.Q_INIT
        
        # learn
        self.Qs[s][a] += self.ALPHA * (r + self.DISCOUNT * q_max - self.Qs[s][a])
        
        # append Q to statistic
        self.path.append(self.Qs[s][a])
            
    def possible_actions(self, s):
        '''determine which squares on play board is empty ( == 0 )'''
        return [num for num, field in enumerate(s) if field == 0]
        
    
    def go(self):
        '''do the next move and learn from it'''
        s = tuple(game.get_state())
        
        # is it the first or second move in game? -> reset path
        if s.count(0) >= 8:
            self.path = []
        
        if game._player != self.name:
            raise Exception('oh no')
            
        
        # find best action        
        possible_a = self.possible_actions(s)
        
        # get q values for possible actions 
        q = list(map(lambda a: self.Q(s, a), possible_a))
        q_max = max(q)
        
        # get best action / actions
        a_max = [a for i, a in enumerate(possible_a) if q[i] == q_max]
        a_max = choice(a_max)
        
#        # greedy?
#        if random() < self.greedy:
#            a_max = [a for i, a in enumerate(possible_a) if q[i] == q_max]
#            a_max = choice(a_max)
#            
#            #print(q)
#        else:
#            a_max = choice(possible_a)
            
        
        # run best action
        try:
            game.set_token(a_max+1)
        except Exception:
            # Tie
            print('Game finished.')
            print('Restart')
            if self.name == 'X':
                game.restart('O')
            else:
                game.restart('X')
            return
        
        # is there a winner?
        winner = game.get_winner()
        
        # determine reward
        if winner != None:
            r = 5
        else:
            r = 0
        
        # update q mapping
        self.update_q(r, q_max)
        
        self.old_state = s
        self.old_action = a_max
        
        if winner != None:
            
            # Penalty for opponent
            opp = self.opponent
            opp.update_q(-5, 0)
            
            # update stats
            self.path.append(r)
            plot_stats(self.path, opp.path, self.name)
            
            if self.name == 'X':
                game.restart('O')
            else:
                game.restart('X')
            
### create players
# greedy = 1 -> no randomization
# greedy = 0 -> complete random (no learning) 
X = Learner('X', greedy=1)
O = Learner('O', greedy=1)

X.opponent = O
O.opponent = X

while(True):
    
    pause()
    X.go()
    pause()
    O.go()
    pause()
    
