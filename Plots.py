from MazeOnFire import MazeOnFire
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import time

class Plots:
    def __init__(self):
        self.title="Plot"
        
    def reachingGoal(self):
        densities=[0,.05,.1,.15,.2,.25,.3,.35,.4,.45,.5,.55,.6]
        numberOfSuccess=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(10):
            for j in range(100):
                maze=MazeOnFire(100,densities[i],0)
                if maze.isReachable((0,0),(99,99)):
                    numberOfSuccess[i]+=1
        probabilityOfSuccess=[x/100 for x in numberOfSuccess]
        plt.plot(densities,probabilityOfSuccess,'r-')
        plt.ylabel("Probability Goal Can Be Reached From Start")
        plt.xlabel("Obstacle Density p")
        plt.title("Probaility Goal Can Be Reached vs. Obstacle Density for 100x100 Mazes")
        plt.xlim(0,.65)
        plt.ylim(0,1)
        plt.show()
    
    def bfsVsA(self):
        densities=[0,.05,.1,.15,.2,.25,.3,.35,.4,.45,.5,.55,.6]
        visitedA=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        visitedBFS=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(10):
            for j in range(100):
                maze=MazeOnFire(100,densities[i],0)
                maze.shortestBFS()
                maze.shortestA()
                visitedA[i]+=maze.aCount
                visitedBFS[i]+=maze.bfsCount
        avgVisitedA=[x/100 for x in visitedA]
        avgVisitedBFS=[x/100 for x in visitedBFS]
        plt.plot(densities,avgVisitedA,'rD')
        plt.plot(densities,avgVisitedBFS,'bo')
        plt.ylabel("Average Nodes Visited")
        plt.xlabel("Obstacle Density p")
        plt.title("Average Nodes Visited vs Obstacle Density (100 Mazes of 100x100)")
        plt.xlim(0,.65)
        plt.ylim(0,10000)
        a_patch=mpatches.Patch(color='red', label='A*')
        bfs_patch=mpatches.Patch(color='blue', label='BFS')
        plt.legend(handles=[a_patch,bfs_patch])
        plt.show()

    def timeDFS(self):
        maze=MazeOnFire(5000,.3,0)
        start_time=time.time()
        maze.isReachable((0,0),(4999,4999))
        end_time=time.time()
        return end_time-start_time
    
    def timeBFS(self):
        maze=MazeOnFire(3000,.3,0)
        start_time=time.time()
        maze.shortestBFS()
        end_time=time.time()
        return end_time-start_time
    
    def timeA(self):
        maze=MazeOnFire(4000,.3,0)
        start_time=time.time()
        maze.shortestA()
        end_time=time.time()
        return end_time-start_time

    

