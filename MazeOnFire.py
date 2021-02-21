import numpy as np
from collections import deque
import heapq
import random
from copy import deepcopy
"""
Class MazeOnFire handles maze generation, DFS, BFS, A*
and fire advancement algorithms. The class is initialized
with desired dimensions, obstacle probabiliy p, and spread
probability spread.
"""
class MazeOnFire:

    def __init__(self,dim,p,spread):
        self.dim=dim
        self.p=p
        self.spread=spread
        self.fireStart=[0,0]                        #Used to keep track of initial fire location
        self.maze=self.generateMaze(dim,p)          #Maze represented by 2D matrix
        self.directions=((0,1),(1,0),(0,-1),(-1,0)) #Keeps track of possible directions agent/fire can travel (Right,Down, Up, Left)
        self.aCount=0                               #aCount and bfsCount keep track of nodes visited by each algorithm
        self.bfsCount=0

    """
    generateMaze takes the dimensions and obstacle probability
    and creates the maze. Also generates a random starting location
    for the fire and stores it. 0 spaces represent open or safe spaces,
    1 spaces represent obstacles, and 2 represents fire spaces.
    """
    def generateMaze(self,dim,p):
        maze=[[np.random.choice([0,1],p=[1-p,p]) for i in range(dim)] for j in range(dim)]
        maze[0][0]=0
        maze[dim-1][dim-1]=0
        self.fireStart[0]=random.randrange(1,self.dim)
        self.fireStart[1]=random.randrange(1,self.dim)
        maze[self.fireStart[0]][self.fireStart[1]]=2
        return maze
    """
    Generates the Euclidean heuristic to be used by A* algorithm
    """
    def generateEuclideanHeuristic(self):
        heuristic=[[0 for i in range(self.dim)] for j in range(self.dim)]
        for x in range(self.dim):
            for y in range(self.dim):
                heuristic[x][y]=np.sqrt((self.dim-x-1)**2+(self.dim-y-1)**2)    #Represents Euclidean distance d^2=x^2+y^2
        return heuristic
    """
    Generates heuristic similar to Euclidean, but adds number nonzero neighbors.
    This is part of strategy 3, and aims to take into consideration not only distance,
    but also the open paths from the current position. By prioritizing nodes with more 
    open spaces (and therefore fewer closed spaces) the search can look for nodes with more
    escape paths and therefore a better chance of surviving.
    """
    def generateClosedHeuristic(self):
        heuristic=self.generateEuclideanHeuristic()
        for x in range(self.dim):
            for y in range(self.dim):
                heuristic[x][y]=self.countClosedSpaces(x,y)+heuristic[x][y]
        return heuristic
    """
    Counts number of closed (1,2) spaces next to any given node
    """
    def countClosedSpaces(self,x,y):
        count=0
        for move in self.directions:
            if(self.isBounded(x+move[0],y+move[1]) and self.maze[x+move[0]][y+move[1]]!=0):
                count+=1
        return count
    """
    Determines if position is within bounds of matrix and is an open space
    """
    def isSafe(self,x,y):
        if( x>=0 and x<self.dim and y>=0 and y<self.dim and self.maze[x][y]==0):
            return True
        else:
            return False
    """
    Determines if position is within bounds, but not necessarily open or closed
    """ 
    def isBounded(self,x,y):
        if(x>=0 and x<self.dim and y>=0 and y<self.dim):
            return True
        else:
            return False
    """
    Makes use of DFS, using deque() as a stack to determine if there exists a path between
    start position and end position.
    """
    def isReachable(self,start,end):
        stack=deque()
        stack.append(start)
        visited=[[False for i in range(self.dim)] for j in range(self.dim)]     #Keeps track of visited nodes
        if(start==end):                         #Checks if input start and end are the same, if they are the path is obvious (same node)
            return True
        while(len(stack)>0):                    #If stack is empty and end node has not been discovered, no path exists
            curr=stack.pop()
            visited[curr[0]][curr[1]]=1
            if(curr==end):                      #Current node is goal node, and search can stop, path exists
                return True
            else:
                for move in self.directions:        #Loops through possible directions of travel 
                    if(self.isSafe(curr[0]+move[0],curr[1]+move[1]) and not visited[curr[0]+move[0]][curr[1]+move[1]]):     #In order to continue path, node must be safe and unvisited previously
                        stack.append((curr[0]+move[0],curr[1]+move[1]))
        return False                #If loop terminates without reaching end position, no path exists, return False
    """
    Uses BFS to search all possible nodes. Once the end node is found, search terminates.
    Keeps track of nodes and previous nodes to return list of shortest path.
    """
    def shortestBFS(self):
        start=(0,(0,0))                 #For BFS, only cocerned with searches from (0,0) to goal node
        goal=(self.dim-1,self.dim-1)
        shortestPath=[]
        if(not self.isReachable(start[1],goal)):            #If not path exists from start to finish, terminate and return empty path
            return shortestPath
        prev=[[(None,None) for i in range(self.dim)] for j in range(self.dim)]      #Prev matrix contains position that was used to reach that position, back track through this to determine path
        q=[]            #Heap q used as priority queue implementation for BFS
        heapq.heapify(q)
        heapq.heappush(q,start)
        while(len(q)>0):            #If queue becomes empty before finding goal node, all possible nodes explored and no path is found
            curr=heapq.heappop(q)
            if(curr[1]==goal):      #Termination condition, end found
                break   
            for move in self.directions:        #Looping through possible directions
                x=curr[1][0]+move[0]            #Next x and y positions of nodes to explore
                y=curr[1][1]+move[1]
                if(self.isSafe(x,y) and prev[x][y]==(None,None) and (x,y)!=(0,0)):          #Ensures node is safe, prev=(None,None) represents the node is unvisited, and the start node does not need to be added
                    heapq.heappush(q,(curr[0]+1,(curr[1][0]+move[0],curr[1][1]+move[1])))   #Uniform cost for each path (1), so prioritize order by distance, updating each distance by 1 from previous node
                    self.bfsCount+=1        #Increments count of explored nodes
                    prev[x][y]=curr[1]      #Sets prev of explored node to the node used to reach it
        back=goal                           #Start back tracking at goal
        while(back!=start[1]):              #Back track through prev matrix, adding each node along the way to shortest path
            shortestPath.insert(0,back)
            back=prev[back[0]][back[1]]
        shortestPath.insert(0,(0,0))
        return shortestPath
    """
    Implements A* algorithm, but takes inputs since shortest path needs to be
    found from a different start each step in strategies 2 and 3. Start and goal
    are tuples of (x,y) position and heurisitic is either "Euclidean" or "Open" to
    differentiate between which heuristic to use for strategy 2 and 3 respectively.
    Main difference between this and BFS is the use of the heuristic to order queue elements.
    """
    def shortestA(self,start,goal,heuristic):
        shortestPath=[]
        if(not self.isReachable(start,goal)):
            return shortestPath
        prev=[[(None,None) for i in range(self.dim)] for j in range(self.dim)]          #Again prev tracks nodes to determine path, also used to track visited nodes
        h=[[]]                      #Empty heurisitc, filled with either Euclidean or Open rules
        if(heuristic=="Euclidean"):
            h=self.generateEuclideanHeuristic()
        elif(heuristic=="Open"):
            h=self.generateClosedHeuristic()
        q=[]
        heapq.heapify(q)                        #Makes use of heapq as priority queue, same as min heap
        curr=(h[start[0]][start[1]],start)
        heapq.heappush(q,curr)
        while(len(q)>0):
            curr=heapq.heappop(q)
            if(curr[1]==goal):
                break
            for move in self.directions:
                x=curr[1][0]+move[0]
                y=curr[1][1]+move[1]
                if(self.isSafe(x,y) and prev[x][y]==(None,None) and (x,y)!=(0,0)):              #Same as BFS, but organizes by heuristic and not simply distance so far
                    heapq.heappush(q,(h[x][y],(curr[1][0]+move[0],curr[1][1]+move[1])))
                    self.aCount+=1
                    prev[x][y]=curr[1]
        back=goal                           #Back tracks in similar fashion to BFS
        while(back!=start):
            shortestPath.insert(0,back)
            back=prev[back[0]][back[1]]
        shortestPath.insert(0,start)
        return shortestPath
        
    def advance_fire(self):             #Advances the fire one step
        maze_temp=deepcopy(self.maze)   #Make copy of maze
        for i in range(self.dim):
            for j in range(self.dim):
                neighborsOnFire=0
                if(maze_temp[i][j]==0):
                    for move in self.directions:
                        try:
                            if(maze_temp[i+move[0]][j+move[1]]==2 and self.isBounded(i+move[0],j+move[1])):
                                neighborsOnFire+=1
                        except:
                            pass
                prob=(1-((1-self.spread)**neighborsOnFire))     #Calculate probability node catches fire
                if(random.uniform(0,1)<=prob):
                    self.maze[i][j]=2               #Set node on fire (2)
