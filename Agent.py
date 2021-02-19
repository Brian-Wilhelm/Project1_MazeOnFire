from MazeOnFire import MazeOnFire

class Agent:

    def __init__(self,dim,p,q):
        self.maze=MazeOnFire(dim,p,q)
        self.currPos=(0,0)
        self.endPos=(dim-1,dim-1)
        
    def showMaze(self):
        for i in range(self.maze.dim):
            print(self.maze.maze[i])
        print(" ")

    def strategyOne(self):
        path=self.maze.shortestA()
        if(len(path)==0):
            print("No path from start to finish")
            self.showMaze()
        for pos in path:
            if pos==self.endPos:
                print("Success")
            elif self.maze.maze[pos[0]][pos[1]]==2:
                print("Failure")
                break
            self.showMaze()
            self.maze.advance_fire()