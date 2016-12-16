# coding=utf-8
import copy
class ASTAR:
    up = None
    down = None
    right = None
    left = None
    parent=None
    fn=None
    position=[]
    current_x=None
    current_y=None
    path=[]
    cost=0
    depth=0
    current_node=None

    def initial(self,v1,v2):
      self.position=[v1,v2]
      self.fn = self.Cost_Path() + self.Hueristic(v1, v2)
      self.current_x = v1
      self.current_y = v2
      if v1==0 and v2==1:
        self.parent=self
        self.current_node = self

    def __cmp__(self, other):
        return cmp(self.fn, other.fn)

    def Cost_Path(self):
        return self.depth+1

    def Path_update(self,node,maze):
        temp=node
        len=self.path.__len__()
        while 1:
                t=self.path.pop()
                if t.position==maze.start:
                    self.path.append(t)
                    break
                x=t.position[0]
                y=t.position[1]
                maze.map[x][y]=0
        self.depth=0
        while 1:
                if temp.position==maze.start:
                    break
                maze.map[temp.position[0]][temp.position[1]] = 2
                self.depth+=1
                self.path.append(temp)
                temp2=temp.parent
                temp=temp2
        node.depth=self.depth

    def Hueristic(self,v1,v2):
        return 27-v1-v2

    def Solve_next(self,node,maze,Fringe):
            check=0
            x=node.current_x
            y=node.current_y

            if maze.map[x-1][y]==0:
                if (x - 1) != node.parent.position[0] or y != node.parent.position[1]:
                    node.up=ASTAR()
                    node.up.initial((x-1),y)
                    node.up.parent=node
                    Fringe.append(node.up)
                    check =1
            if maze.map[x +1][y] == 0:
                if (x + 1) != node.parent.position[0] or y != node.parent.position[1]:
                    node.down = ASTAR()
                    node.down.initial((x+1),y)
                    node.down.parent =  node
                    Fringe.append( node.down)
                    check=1
            if maze.map[x][y+1] == 0:
                if x != node.parent.position[0] or (y + 1) != node.parent.position[1]:
                    node.right = ASTAR()
                    node.right.initial(x,(y+1))
                    node.right.parent =  node
                    Fringe.append( node.right)
                    check=1
            if maze.map[x][y-1] == 0:
                if x != node.parent.position[0] or (y - 1) != node.parent.position[1]:
                    node.left = ASTAR()
                    node.left.initial(x,(y-1))
                    node.left.parent =  node
                    Fringe.append( node.left)
                    check=1
            if check==0:
                maze.map[ node.position[0]][ node.position[1]]=9
                self.current_node= node.parent
                self.Path_update(self.current_node,maze)
                self.cost += 1

    def Show_path(self,node,maze_for_clear):
        show_array = []
        happy = node.depth

        for i in range(happy + 1):
            show_array.append(node)
            node = node.parent
        while 1:
            temp_node = show_array.pop()
            print "Depth :", temp_node.depth
            maze_for_clear.map[temp_node.position[0]][temp_node.position[1]] = 2
            for i in range(15):
                print maze_for_clear.map[i]
            if temp_node.position == maze_for_clear.goal:
                break


    def Solve(self, maze):
        maze_for_clear=[]
        maze_for_clear = copy.deepcopy(maze)
        print "Start Searching by Using A Star"
        self.initial(maze.start[0],maze.start[1])
        if self.current_node.position==maze.start:
            maze.map[self.current_x][self.current_y] = 2
            self.path.append(self.current_node)
            self.depth=1

        Fringe = []

        while self.current_node.position!=maze.goal:
            self.Solve_next(self.current_node,maze,Fringe)
            next_step = min(Fringe)

            Fringe.remove(min(Fringe))
            self.cost += 1

            self.current_node=next_step
            if self.path.__len__()>=1:
                self.path.append(self.current_node)

            self.Path_update(self.current_node,maze)

        self.depth=0
        self.Show_path(self.current_node,maze_for_clear)
        print "A Star Really done"
        print "Depth is",self.depth
        print "COST is",self.cost



