from MazeOnFire import MazeOnFire
from Agent import Agent
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import time
"""
Plots class handles all necessary plotting to better analyze search algorithms and strategies.
"""
class Plots:
    def __init__(self):             #Initialize plots, nothing else needed
        self.title="Plot"
    """
    This sets up the different densities to test and keeps track of how many successes
    occur for each obstacle density probability. Makes use of matplotlib to handle plotting.
    """
    def reachingGoal(self):
        densities=[0,.05,.1,.15,.2,.25,.3,.35,.4,.45,.5,.55,.6]
        numberOfSuccess=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(10):                                     #Loops through each of the densities
            for j in range(100):                                #100 mazes tested for each density
                maze=MazeOnFire(100,densities[i],0)             #Create 100x100 maze, no fire used in this case
                if maze.isReachable((0,0),(99,99)):             #DFS determines if path exists, if it does, increment successful path for density in position i
                    numberOfSuccess[i]+=1
        probabilityOfSuccess=[x/100 for x in numberOfSuccess]               #Average successes since 100 total mazes per density
        plt.plot(densities,probabilityOfSuccess,'r-')                       #Rest uses matplotlib to plot density vs. average successes for each density
        plt.ylabel("Probability Goal Can Be Reached From Start")
        plt.xlabel("Obstacle Density p")
        plt.title("Probaility Goal Can Be Reached vs. Obstacle Density for 100x100 Mazes")
        plt.xlim(0,.65)
        plt.ylim(0,1)
        plt.show()
    """
    Compares average number of nodes visited by each BFS and A* at varying densities.
    """
    def bfsVsA(self):
        densities=[0,.05,.1,.15,.2,.25,.3,.35,.4,.45,.5,.55,.6]
        visitedA=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        visitedBFS=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(10):                                     #Loops through each density
            for j in range(100):                                #Generates 100 mazes for each density
                maze=MazeOnFire(100,densities[i],0)             #100x100 maze at density i
                maze.shortestBFS()
                maze.shortestA()
                visitedA[i]+=maze.aCount                        #Node counts are determine in MazeOnFire class, add total count for each maze each time
                visitedBFS[i]+=maze.bfsCount
        avgVisitedA=[x/100 for x in visitedA]                   #Average out nodes by dividing by total mazes (100)
        avgVisitedBFS=[x/100 for x in visitedBFS]
        plt.plot(densities,avgVisitedA,'rD')                    #Creates plot, titles, labels, axes, and legend using matplotlib
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
    """
    Times DFS, should produce close to 60 seconds, 5000x5000 dimension determined through trial and error
    """
    def timeDFS(self):
        maze=MazeOnFire(5000,.3,0)
        start_time=time.time()
        maze.isReachable((0,0),(4999,4999))
        end_time=time.time()
        return end_time-start_time              #Returns time from starting DFS to end
    """
    Time BFS, 3000x3000 maze found by trial and error
    """
    def timeBFS(self):
        maze=MazeOnFire(3000,.3,0)
        start_time=time.time()
        maze.shortestBFS()
        end_time=time.time()
        return end_time-start_time          #Returns time close to 60 seconds at this dimension
    """
    Time A*, 4500x4500 maze found by trial and error
    """
    def timeA(self):
        maze=MazeOnFire(4500,.3,0)
        start_time=time.time()
        try:
            maze.shortestA()
        except:
            return "Goal not reachable"
        end_time=time.time()
        return end_time-start_time      #Returns time close to 60 seconds at this dimension
    """
    Compares strategies 1,2 and 3 for spread rates in increments of .1 from 0 to 1.
    Stores number of successful travels through maze in array. Runs 10 times for each 
    strategy at each spread rate. Discars mazes with no initial path and with no path to initial fire.
    """
    def strategyComparison(self):
        spreads=[0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1]
        successOne=[0,0,0,0,0,0,0,0,0,0,0]
        successTwo=[0,0,0,0,0,0,0,0,0,0,0]
        successThree=[0,0,0,0,0,0,0,0,0,0,0]
        for i in range(len(spreads)):
            runCount=0
            while(runCount<10):                                                                 #Terminates once sufficient mazes have been tested
                strat=Agent(100,.3,spreads[i])
                strat.maze.maze[strat.maze.fireStart[0]][strat.maze.fireStart[1]]=0             #Sets initial fire location to 0, since a 2 would be undiscoverable by DFS in this implementation
                if(not strat.maze.isReachable((0,0),(strat.maze.dim-1,strat.maze.dim-1)) or not strat.maze.isReachable((0,0),(strat.maze.fireStart[0],strat.maze.fireStart[1]))):       #DFS to check if there is a path from start to end, and if there is a path from start to the initial fire location
                    print("Not Reachable")
                    continue                                                                #Continue with another new maze since this maze must be discarded
                strat.maze.maze[strat.maze.fireStart[0]][strat.maze.fireStart[1]]=2         #Set inital fire location back to 2, since it must start on fire
                if(strat.strategyOne()):                                                    #All strategies return True if successful and false if not, so if True, increments successful run
                    successOne[i]+=1
                if(strat.strategyTwo()):
                    successTwo[i]+=1
                if(strat.strategyThree()):
                    successThree[i]+=1
                runCount+=1
        plt.plot(spreads,successOne,'rD')                    #Creates plot, titles, labels, axes, and legend using matplotlib
        plt.plot(spreads,successTwo,'bo')
        plt.plot(spreads,successThree,'gs')
        plt.ylabel("Number of Successful Escapes")
        plt.xlabel("Fire Spread q")
        plt.title("Number of Successful Escapes vs Fire Spread (100x100 Mazes, 20 Attempts Each)")
        plt.xlim(0,1)
        plt.ylim(0,20)
        one_patch=mpatches.Patch(color='red', label='Strategy 1')
        two_patch=mpatches.Patch(color='blue', label='Strategy 2')
        three_patch=mpatches.Patch(color='green', label='Strategy 3')
        plt.legend(handles=[one_patch,two_patch,three_patch])
        plt.show()
    """
    timeS1, timeS2, timeS3 return the times it takes for each strategy to successfully exit the maze.
    For these mazes, using the same one on each strategy, timeS1<timeS2<timeS3.
    """
    def timeS1(self):
        test=Agent(100,.3,.1)
        start_time=time.time()
        try:
            test.strategyOne()
        except:
            return "Goal not reachable"
        end_time=time.time()
        return end_time-start_time

    def timeS2(self):
        test=Agent(100,.3,.1)
        start_time=time.time()
        try:
            test.strategyTwo()
        except:
            return "Goal not reachable"
        end_time=time.time()
        return end_time-start_time

    def timeS3(self):
        test=Agent(100,.3,.1)
        start_time=time.time()
        try:
            test.strategyThree()
        except:
            return "Goal not reachable"
        end_time=time.time()
        return end_time-start_time

Plots().strategyComparison()