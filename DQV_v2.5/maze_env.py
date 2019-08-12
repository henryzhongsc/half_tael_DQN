
import pandas as pd
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


class Maze:#(tk.Tk, object):

    def __init__(self): # GRAPHEN
            #super(Maze, self).__init__()
            self.action_space = ['hold','buy_100','sell_100','buy_200','sell_200','buy_300','sell_300']
            self.n_actions = len(self.action_space)
            self.n_features = 300 # each time, we consider 300 days historical records
            #self.title('maze')
            #self._build_maze()
            self.step_count = 0

            # 零假空 初始化 环境变量
            self.balance = 0
            self.trade_account = 0
            self.start_day = 300
            self.obs = []
            self.data_env = []
            df = pd.read_csv('./EUR_GBP.csv')
            # 把两个 1d array 拼成一个 2d array
            self.tempDf = list(df['avg'].iloc[0:4799])
            self.temp = np.asarray(self.tempDf[0:4799]).reshape((1, 4799))
            self.data_env = np.concatenate((self.temp,self.temp), axis=0)

            self.obs = self.data_env[:,0:self.start_day].reshape((600,))
            print(self.obs.shape)
            self._build_maze()
            #self.obs = np.concatenate(np.asarray(self.data_env[0:self.start_day]),np.asarray(self.data_env[0:self.start_day]))

    def _build_maze(self): # GRAPHEN
            #df = pd.read_csv('/Users/xingdanmou/Downloads/forex-master 2/Historical_Data/M1/EUR_GBP.csv')
            #self.data_env = list(df['avg'].iloc[0:4799])
            self.start_day = 300 # each time we trade, our state is 300 historical price


            # create start balance
            self.balance = 100000
            # create trading exchange account
            self.trade_account = 0
            # create current observation (也就是 例子中的 red rect)
            #self.obs = self.data_env[(0):(self.start_day)]

            #print((np.asarray(self.data_env[0:self.start_day]).shape))
            #print(np.asarray(self.data_env[0:self.start_day]).reshape((1, 300)).shape)
            #temp = np.asarray(self.data_env[0:4799]).reshape((1, 4799))


            #self.obs = np.concatenate((temp,temp), axis=0)

            #np.concatenate((array2D_1, array2D_2))




    def reset(self): #GRAPHEN
            time.sleep(0.1)

            self.balance = 100000
            self.trade_account = 0 # 用于记录 日元 的 持有量
            #self.obs = self.data_env[0:self.start_day]
            self.obs = self.data_env[:,0:self.start_day].reshape((600,))
            self.step_count = 0
            print(self.obs.shape)
            #print(np.asarray(self.data_env[0:self.start_day]).shape)
            #return np.asarray(self.data_env[0:self.start_day]) #输出是一个 1D array
            print("reset(self): self.obs:  ",self.obs.shape )
            return self.obs # 输出是一个 2D array

    def step(self, action):
            s = self.obs

            if action == 0:
                self.trade_account += 0
                self.balance += 0
                self.step_count += 1

            elif action == 1 :
                self.trade_account += 100
                self.balance -= s[-1]*100 # s[-1] 代表当前价格
                self.step_count += 1

            elif action == 2 :
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
                #self.obs = self.data_env[(0 + self.step_count):(self.start_day + self.step_count)]
                self.obs = self.data_env[:,(0+self.step_count):(self.start_day + self.step_count)].reshape((600,))
                #self.obs =np.concatenate(np.asarray(self.data_env[(0+self.step_count):(self.start_day + self.step_count)]),
                #                         np.asarray(self.data_env[(0+self.step_count):(self.start_day + self.step_count)]))
                #print(self.obs.shape)
            elif self.step_count == 4500:
#                 print("############# self.data_env[] ##########################")
#                 print(type(self.data_env[(0 + self.step_count):(self.start_day + self.step_count-1)]))
#                 print("################# self.data_env[] ######################")
#                 print("################# self.data_env[-1] ######################")
#                 print(type(list(self.data_env[-1])))
#                 print("################# self.data_env[-1] ######################")
                #self.obs = self.data_env[(0 + self.step_count):(self.start_day + self.step_count-1)]
                self.obs = self.data_env[:,(0+self.step_count):(self.start_day + self.step_count)].reshape((600,))
                #self.obs = self.obs =np.concatenate(np.asarray(self.data_env[(0+self.step_count):(self.start_day + self.step_count)]),
                #                                    np.asarray(self.data_env[(0+self.step_count):(self.start_day + self.step_count)]))
                #self.obs.append(self.data_env[-1])
                #print
                #print(self.obs)

            # reward function

            if (self.balance >100000) & (self.step_count == 4500):
                reward = 1
                done = True
            elif (self.balance <= 100000)  & (self.step_count == 4500):
                reward = -1
                done = True

            else:
                reward = 0
                done = False


            s_ = np.asarray(self.obs)

            return s_, reward, done

    #def render(self):
        # time.sleep(0.01)
        # self.update()
