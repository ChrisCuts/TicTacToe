# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 19:27:43 2017

@author: ChrisCuts
"""

import matplotlib.pyplot as plt
import numpy as np

class _Playboard():
    
    SYMBOL_WIDTH = 0.5
    TITLE = 'TicTacToe'
    
    def __init__(self, eventfcn):
        
        self._prepare_board()
        self._eventfcn = eventfcn
        
    def draw(self, symbol, position):
        
        assert position >= 0 and position <= 9, 'Position ' + str(position) + ' out of range!'
        
        
        x = (position - 1) % 3 + 1
        y = (position - 1) // 3 + 1
        
        if symbol == 'cross':
            self._draw_cross(x, y)
        elif symbol == 'circ':
            self._draw_circ(x, y)
            
        self.ax.figure.canvas.draw()
    def clear(self):
        
        if not plt.fignum_exists(self.TITLE):
            self._prepare_board()
        else:
            self.ax.cla()
            self._draw_grid()
        
        self.ax.figure.canvas.draw()
    def _prepare_board(self):
        
        self.fig = plt.figure(self.TITLE, facecolor= 'white', figsize=(7,7))
        #mngr = plt.get_current_fig_manager()
        #mngr.window.setGeometry(1920 /2 + 80, 100, 800, 800)
        self.ax = plt.axes([0, 0, 1, 1], frameon= False, aspect= 'equal')
        plt.tick_params(axis='both', bottom= 'off', top= 'off', left= 'off', right= 'off',
                        labelbottom= 'off', labelleft= 'off')
        
        self.fig.canvas.mpl_connect('key_press_event', lambda e: self._eventfcn(e))
        
        self._draw_grid()
        
    def update(self, interval):
        
        plt.pause(interval)
        
    def _draw_grid(self):
        
        # paint grid
        gridx, gridy = np.meshgrid([1.5, 2.5], [0.5, 3.5])
        self.ax.plot(gridx, gridy, color= 'black', linewidth= 15)
        self.ax.plot(gridy, gridx, color= 'black', linewidth= 15)


    def _draw_cross(self, x, y):
        
        
        x = [x-self.SYMBOL_WIDTH/2, x+self.SYMBOL_WIDTH/2]
        y = [y-self.SYMBOL_WIDTH/2, y+self.SYMBOL_WIDTH/2]
        
        self.ax.plot(x, y, axes= self.ax, color= 'black', linewidth= 15)
        x.reverse()
        self.ax.plot(x, y, axes= self.ax, color= 'black', linewidth= 15)
        
    def _draw_circ(self, x, y):
        
        circ = plt.Circle((x, y), self.SYMBOL_WIDTH/2, facecolor= 'none', edgecolor= 'black', linewidth= 15)
        self.ax.add_artist(circ)
        

class TicTacToe():
    
    SYMBOL = {'X': 'cross', 'O': 'circ'}
    
    def __init__(self, pauseafterrestart=1):
        
        self._pb = _Playboard(self._pb_key_pressed)
        
        ### State
        #
        # 0: no mark
        # 1: cross
        # 2: circ
        
        self._state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._player = 'X'
        
        self._winner = None
        
        self._pauseafterrestart = pauseafterrestart
        
        self._pb.clear()
        
    def set_token(self, position):
        
        assert position >= 1 and position <= 9, 'Position out of range!'
        
        position -= 1
        
        if self._winner != None or self._winner == -1:
            raise Exception('Game finished.')
        
        if self._state[position] != 0:
            raise Exception('Position already taken!')

        self._state[position] = self._player
        
        self._pb.draw(self.SYMBOL[self._player], position+1)
            
        # check for winner
        if self._state[0 : 9 : 3].count(self._player) == 3          \
            or self._state[1 : 9 : 3].count(self._player) == 3      \
            or self._state[2 : 9 : 3].count(self._player) == 3      \
            or self._state[0 : 3 : 1].count(self._player) == 3      \
            or self._state[3 : 6 : 1].count(self._player) == 3      \
            or self._state[6 : 9 : 1].count(self._player) == 3      \
            or self._state[0 : 9 : 4].count(self._player) == 3      \
            or self._state[2 : 7 : 2].count(self._player) == 3:
                self._winner = self._player
                
                print('Player ' + self._player + ' wins!')
                
        # tie?
        if all(self._state):
            self._winner = -1
            print('Tie!')
            
        # next one
        if self._player == 'X':
            self._player = 'O'
        else:
            self._player = 'X'

    def _pb_key_pressed(self, event):
        
        if event.key.isdigit():
            
            self.set_token(int(event.key))
        elif event.key == 'r':
            self.restart()
            
    def get_winner(self):
        
        return self._winner

    def get_state(self):
        
        return self._state
    
    def restart(self, player):
        
        if self._pauseafterrestart:
            self.sleep(self._pauseafterrestart)
        
        self._pb.clear()
        self._state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._player = player
        self._winner = None
    
        print('Player ' + player + ' started')
            
    def sleep(self, interval):
        
        self._pb.update(interval)
        
if __name__ == '__main__':
    ttt = TicTacToe()

