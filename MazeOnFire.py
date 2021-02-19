import numpy as np
from collections import deque
import heapq
import random
from copy import deepcopy

class MazeOnFire:

    def __init__(self,dim,p,spread):
        self.dim=dim
        self.p=p
        self.spread=spread
        self.maze=self.generateMaze(dim,p)
        self.directions=((0,1),(1,0),(0,-1),(-1,0))
        self.aCount=0
        self.bfsCount=0

    def generateMaze(self,dim,p):
        maze=[[np.random.choice([0,1],p=[1-p,p]) for i in range(dim)] for j in range(dim)]
        maze[0][0]=0
        maze[dim-1][dim-1]=0
        maze[random.randrange(1,self.dim)][random.randrange(1,self.dim)]=2
        return maze

    def generateHeuristic(self):
        heuristic=[[0 for i in range(self.dim)] for j in range(self.dim)]
        for x in range(self.dim):
            for y in range(self.dim):
                heuristic[x][y]=np.sqrt((self.dim-x-1)**2+(self.dim-y-1)**2)
        return heuristic

    def isSafe(self,x,y):
        if( x>=0 and x<self.dim and y>=0 and y<self.dim and self.maze[x][y]==0):
            return True
        else:
            return False

    def isBounded(self,x,y):
        if(x>=0 and x<self.dim and y>=0 and y<self.dim):
            return True
        else:
            return False

    def isReachable(self,start,end):
        stack=deque()
        stack.append(start)
        visited=[[0 for i in range(self.dim)] for j in range(self.dim)]
        while(len(stack)>0):
            curr=stack.pop()
            visited[curr[0]][curr[1]]=1
            if(curr==end):
                return True
            else:
                for move in self.directions:
                    if(self.isSafe(curr[0]+move[0],curr[1]+move[1]) and visited[curr[0]+move[0]][curr[1]+move[1]]==0):
                        stack.append((curr[0]+move[0],curr[1]+move[1]))
        return False

    def shortestBFS(self):
        start=(0,(0,0))
        goal=(self.dim-1,self.dim-1)
        shortestPath=[]
        if(not self.isReachable(start[1],goal)):
            return shortestPath
        prev=[[(None,None) for i in range(self.dim)] for j in range(self.dim)]
        q=[]
        heapq.heapify(q)
        heapq.heappush(q,start)
        while(len(q)>0):
            curr=heapq.heappop(q)
            if(curr[1]==goal):
                break
            for move in self.directions:
                x=curr[1][0]+move[0]
                y=curr[1][1]+move[1]
                if(self.isSafe(x,y) and prev[x][y]==(None,None) and (x,y)!=(0,0)):
                    heapq.heappush(q,(curr[0]+1,(curr[1][0]+move[0],curr[1][1]+move[1])))
                    self.bfsCount+=1
                    prev[x][y]=curr[1]
        back=goal
        while(back!=start[1]):
            shortestPath.insert(0,back)
            back=prev[back[0]][back[1]]
        shortestPath.insert(0,(0,0))
        return shortestPath

    def shortestA(self):
        goal=(self.dim-1,self.dim-1)
        shortestPath=[]
        if(not self.isReachable((0,0),goal)):
            return shortestPath
        prev=[[(None,None) for i in range(self.dim)] for j in range(self.dim)]
        h=self.generateHeuristic()
        q=[]
        heapq.heapify(q)
        start=(h[0][0],(0,0))
        heapq.heappush(q,start)
        while(len(q)>0):
            curr=heapq.heappop(q)
            if(curr[1]==goal):
                break
            for move in self.directions:
                x=curr[1][0]+move[0]
                y=curr[1][1]+move[1]
                if(self.isSafe(x,y) and prev[x][y]==(None,None) and (x,y)!=(0,0)):
                    heapq.heappush(q,(h[x][y],(curr[1][0]+move[0],curr[1][1]+move[1])))
                    self.aCount+=1
                    prev[x][y]=curr[1]
        back=goal
        while(back!=start[1]):
            shortestPath.insert(0,back)
            back=prev[back[0]][back[1]]
        shortestPath.insert(0,(0,0))
        return shortestPath
        
    def advance_fire(self):
        maze_temp=deepcopy(self.maze)
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
                prob=(1-((1-self.spread)**neighborsOnFire))
                if(random.uniform(0,1)<=prob):
                    self.maze[i][j]=2