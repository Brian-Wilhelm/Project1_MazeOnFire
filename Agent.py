from MazeOnFire import MazeOnFire
"""
Agent class is used to represent the process of walking through the maze
in each of the three strategies. It creates a MazeOnFire object to handle all
maze generation and search functions. The class then implements the strategies to
walk through the mazes in the MazeOnFire objects.
"""
class Agent:

    def __init__(self,dim,p,q):
        self.maze=MazeOnFire(dim,p,q)       #Constructor takes dimension, p and q to create MazeOnFire object requiring same parameters
        self.currPos=(0,0)                  #Tracks position of agent
        self.endPos=(dim-1,dim-1)
        self.dim=dim
    """
    Shows the maze.
    """
    def showMaze(self):
        for i in range(self.maze.dim):
            print(self.maze.maze[i])
        print(" ")
    """
    Implementation of strategy 1. Follows shortest path from start to finish and dies if it runs into an on fire node.
    """
    def strategyOne(self):
        path=self.maze.shortestA((0,0),(self.maze.dim-1,self.maze.dim-1),"Euclidean")   #Finds shortest path using A* algorithm according to Euclidean heuristic
        if(len(path)==0):       #A* returns an empty path if there is no path, so path length 0 returns False as strategy
            print("No path from start to finish")
            return False
        for pos in path[1:len(path)-1]:                 #Advance agent along shortest path, ignoring start and end nodes
            self.maze.advance_fire()                    #Advance the fire
            if self.maze.maze[pos[0]][pos[1]]==2:       #If current position of agent is on fire, agent dies, return False
                print("Failure")   
                return False
        print("Success")                                #If loop continues along entire path, and at no point agent stands on fire, agent is safe and returns True
        return True
    """
    Implementation of strategy 2, which updates path after each move/fire advancement to find the next shortest and safe path.
    """
    def strategyTwo(self):
        curr=(0,0)
        end=(self.dim-1,self.dim-1)
        while(True):                                                #Loop will continue until one of the terminating statements executes
            if(not self.maze.isReachable(curr,end)):                #DFS used to determine path existence, if no path, no need to continue strategy
                return "No Path"
            if(curr==end):                                          #Terminating condition when agent reaches end node
                print("Success-Strategy 2")
                return True
            self.maze.advance_fire()                                #Advance fire before recalculating path
            path=self.maze.shortestA(curr,end,"Euclidean")          #Calculate new shortest path from updated position and fire, importance of having start and end inputs in shortestA function
            if(len(path)==0):                                       #If the newly calculated path is empty, indicates no further paths exist to goal, break out of loop
                break
            curr=path[1]                                            #Sets current agent position to next step, indicated by next position in updated path
            ##print(path)
            if(self.maze.maze[curr[0]][curr[1]]==2):                #If agent steps on to fire spot next, agent dies and loop terminates
                break
        ##self.showMaze()
        return False                                                #If loop terminates without first returning True, the strategy fails, as the agent never reaches the end, and either there are no more paths or the agent is on fire
    """
    Strategy 3 makes use of ideas from strategy 2 by updating after each time step.
    To improve on strategy 2, strategy 3 uses a new heuristic which takes into account
    both Euclidean distance and the number of open neighbors around each node. The idea is
    that nodes with more open spaces will allow the agent more possible paths to escape the fire.
    By priortizing this way, a shorter path can be found while also accounting for escape in the future states.
    """
    def strategyThree(self):
        curr=(0,0)
        end=(self.dim-1,self.dim-1)
        while(True):                                            #Loops until a termination is reached similar to strategy 3
            if(not self.maze.isReachable(curr,end)):
                return "No Path"
            if(curr==end):
                print("Success - Strategy 3")
                return True
            self.maze.advance_fire()
            path=self.maze.shortestA(curr,end,"Open")           #Main difference is that it makes use of "Open" heuristic
            if(len(path)==0):
                break
            curr=path[1]
            if(self.maze.maze[curr[0]][curr[1]]==2):            #If agent is on fire, agent dies
                break
        return False                                            #If loop terminates from break statement, the agent either was trapped or caught fire
