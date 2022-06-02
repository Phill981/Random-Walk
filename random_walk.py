from random import randint
import pandas as pd
import matplotlib.pyplot as plt

class RandomWalk:
    def __init__(self, file_path :str, runs :int, prediction=0) ->None:
        self.file = file_path
        self.prediction = prediction
        self.runs = runs
        self.final_price = 0
        self.read_file()
        self.dates = [i + 1 for i in range(len(self.prices) + self.prediction)]
        self.simulations = []

    def read_file(self)->None:
        """Reads the '.csv' file you donwloaded from Yahoo finance"""
        df = pd.read_csv(self.file)
        self.prices = df["Close"].to_list()
        
        self.avg_up = 0
        self.avg_down = 0

        for i in range(len(self.prices) - 1):
            if self.prices[i + 1] > self.prices[i]:
                self.avg_up += (self.prices[i + 1] - self.prices[i])
            else:
                self.avg_down += (self.prices[i + 1] - self.prices[i])
        self.avg_up /= len(self.prices)
        self.avg_down /= len(self.prices)
        
    def walk(self)->None:
        """Runs the simulation with the runs given at the begining and starts a 
        prediction of n days also writen in the class parameters"""
        for i in range(self.runs): 
            self.origin = self.prices[0]
            #print(self.origin)
            simulation = []
            for j in range(len(self.prices) + self.prediction):
                flip = randint(0, 1)
                if flip == 1:
                    self.origin += self.avg_up
                else:
                    self.origin += self.avg_down
                simulation += [self.origin]
            self.simulations.append(simulation)
            self.final_price += self.origin
        self.final_price /= self.runs

        if self.prediction == 0:
            pass
        else:
            for _ in range(self.prediction):
                self.prices += [self.prices[-1]]
        
    
    def plot(self)->None:
        """Plots all the random walks that were simulated"""
        for sim in self.simulations:
            plt.plot(self.dates, sim)
        plt.plot(self.dates, self.prices)
        plt.grid(True)
        plt.show()
