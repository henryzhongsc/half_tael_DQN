
"""
Reinforcement learning maze example.
Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].
This script is the environment part of this example.
The RL is in RL_brain.py.
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""



import numpy as np
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

UNIT = 40   # pixels
MAZE_H = 4  # grid height
MAZE_W = 4  # grid width


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.n_features = 2
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()
        
    
        
    '''    
    def __init__(self): # GRAPHEN
        super(Maze, self).__init__()
        self.action_space = ['hold','buy_100','sell_100','buy_200','sell_200','buy_300','sell_300']
        self.n_actions = len(self.action_space)
        self.n_features = 300 # each time, we consider 300 days historical records
        self.title('maze')
        self._build_maze()
        self.step_count = 0
    '''
    
    '''
    def _build_maze(self): # GRAPHEN
        df = pd.read_csv('/Users/xingdanmou/Downloads/forex-master 2/Historical_Data/M1/EUR_GBP.csv')
        self.data_env = list(df['avg'].iloc[0:4799])
        self.start_day = 300 # each time we trade, our state is 300 historical price
        
        
        # create start balance 
        self.balance = 100000
        # create trading exchange account
        self.trade_account = 0
        # create current observation (也就是 例子中的 red rect)
        self.obs = data_env[(0):(self.start_day)]
        
    '''    
        
        
        
    
    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([20, 20])

        # hell
        hell1_center = origin + np.array([UNIT * 2, UNIT])
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - 15, hell1_center[1] - 15,
            hell1_center[0] + 15, hell1_center[1] + 15,
            fill='black')
        # hell
        # hell2_center = origin + np.array([UNIT, UNIT * 2])
        # self.hell2 = self.canvas.create_rectangle(
        #     hell2_center[0] - 15, hell2_center[1] - 15,
        #     hell2_center[0] + 15, hell2_center[1] + 15,
        #     fill='black')

        # create oval
        oval_center = origin + UNIT * 2
        self.oval = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')

        # create red rect
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')

        # pack all
        self.canvas.pack()
    
    
    ''' 
    def reset(self): #GRAPHEN
        time.sleep(0.1)
        
        self.balance = 100000
        self.trade_account = 0 # 用于记录 日元 的 持有量
        self.obs = data_env[0:self.start_day]
        self.step_count = 0
        
        return np.asarray(data_env[0:self.start_day]) #输出是一个 1D array
    '''
    
        
    
    def reset(self):
        self.update()
        time.sleep(0.1)
        self.canvas.delete(self.rect)
        origin = np.array([20, 20])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        # return observation
        #print((np.array(self.canvas.coords(self.rect)[:2]) - np.array(self.canvas.coords(self.oval)[:2]))/(MAZE_H*UNIT))
        print(((np.array(self.canvas.coords(self.rect)[:2]) - np.array(self.canvas.coords(self.oval)[:2]))/(MAZE_H*UNIT)).shape)
        return (np.array(self.canvas.coords(self.rect)[:2]) - np.array(self.canvas.coords(self.oval)[:2]))/(MAZE_H*UNIT)
    
    
    '''
    def step(self, action):
        s = self.obs
        
        if action == 0:
            self.trade_account += 0
            self.balance += 0
            self.step_count += 1
            
        elif action == 1:
            self.trade_account += 100
            self.balance -= s[-1]*100 # s[-1] 代表当前价格
            self.step_count += 1
            
        elif action == 2:
            self.trade_account -= 100
            self.balance += s[-1]*100
            self.step_count += 1
            
        elif action == 3:
            self.trade_account += 200
            self.balance -= s[-1]*200
            self.step_count += 1
        
        elif action == 4:
            self.trade_account -= 200
            self.balance += s[-1]*200
            self.step_count += 1
            
        elif action == 5:
            self.trade_account += 300 #买入 300
            self.balance -= s[-1]*300
            self.step_count += 1
            
        elif action == 6:
            self.trade_account -= 300 #卖出 300
            self.balance += s[-1]*300
            self.step_count += 1
            
        
        # 更新 observation 的状态
        if self.step_count < 4500:
            self.obs = data_env[(0 + self.step_count):(self.start_day + self.step_count)]
        elif self.step_count == 4500:
            self.obs = data_env[(0 + self.step_count):(self.start_day + self.step_count-1)]+data_env[-1]
        
        
        # reward function
        
        if (self.balance >10000) & (self.step_count == 4500):
            reward = 1
            done = True
        elif (self.balance <= 10000)  & (self.step_count == 4500):
            reward = -1
            done = True
        
        else:
            reward = 0
            done = False
            
            
        s_ = self.obs
        
        return s_, reward, done
        
    '''
    
    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

        next_coords = self.canvas.coords(self.rect)  # next state

        # reward function
        if next_coords == self.canvas.coords(self.oval):
            reward = 1
            done = True
        elif next_coords in [self.canvas.coords(self.hell1)]:
            reward = -1
            done = True
        else:
            reward = 0
            done = False
        s_ = (np.array(next_coords[:2]) - np.array(self.canvas.coords(self.oval)[:2]))/(MAZE_H*UNIT)
        print('s_, reward, done: ', s_, reward, done)#####################################################
        return s_, reward, done

    def render(self):
        # time.sleep(0.01)
        self.update()

