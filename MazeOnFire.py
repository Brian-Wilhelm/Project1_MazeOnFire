import numpy as np
from collections import deque
import heapq

class MazeOnFire:

    def __init__(self):
        self.maze=[[]]
        self.dim=0
        self.p=0
        self.directions=((0,1),(1,0),(0,-1),(-1,0))

    def generateMaze(self,dim,p):
        self.maze=[[np.random.choice([0,1],p=[1-p,p]) for i in range(dim)] for j in range(dim)]
        self.maze[0][0]=0
        self.maze[dim-1][dim-1]=0
        self.dim=dim
        self.p=p
        return self.maze

    def isSafe(self,x,y):
        if( x>=0 and x<self.dim and y>=0 and y<self.dim and self.maze[x][y]==0):
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
                    prev[x][y]=curr[1]
        back=goal
        while(back!=start[1]):
            shortestPath.insert(0,back)
            back=prev[back[0]][back[1]]
        shortestPath.insert(0,(0,0))
        return shortestPath
        

test=MazeOnFire()
test.generateMaze(20,.3)
print(len(test.shortestBFS()))
for i in range(test.dim):
    print(test.maze[i])