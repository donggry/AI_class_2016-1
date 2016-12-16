# coding=utf-8
import copy
class IDS :
    up=None
    down=None
    right=None
    left=None
    parent=None
    depth=0
    depth_limited=0
    cost=0
    position=[]
    current_node=None
    def initial(self,v1,v2):
        self.position=[v1,v2]
    def Solve_next(self,node,maze,Fringe):
        x=node.position[0]
        y=node.position[1]
        if maze.map[x][y - 1] == 0:
            if x!=node.parent.position[0] or (y-1)!=node.parent.position[1]:
                node.left = IDS()
                node.left.initial(x, (y - 1))
                node.left.parent = node
                Fringe.append(node.left)
        if maze.map[x][y + 1] == 0:
            if x != node.parent.position[0] or (y+1) != node.parent.position[1]:
                node.right = IDS()
                node.right.initial(x, (y + 1))
                node.right.parent = node
                Fringe.append(node.right)
        if maze.map[x - 1][y] == 0:
            if (x-1) != node.parent.position[0] or y != node.parent.position[1]:
                node.up = IDS()
                node.up.initial((x - 1), y)
                node.up.parent = node
                Fringe.append(node.up)

        if maze.map[x + 1][y] == 0:
            if (x + 1) != node.parent.position[0] or y != node.parent.position[1]:
                node.down = IDS()
                node.down.initial((x+1),y)
                node.down.parent = node
                Fringe.append(node.down)

    def Check_goal(self,node,maze,Fringe):
        if node.position==maze.goal:
            return 2
        elif not Fringe:
            return 3
        else:
            return 1
    def Depth_update(self,node,maze):
        original = node
        original.depth = 0

        while 1:
            if node.position == maze.start:
                break
            original.depth += 1
            temp = node.parent
            node = temp
        node=original
    def Path_clear(self,node,maze):
        original=node
        while 1:
            if node.position == maze.start:
                maze.map[node.position[0]][node.position[1]] = 2
                break
            maze.map[node.position[0]][node.position[1]] = 0
            temp = node.parent
            node = temp
        node=original
    def Path_update(self,node,maze):
        original=node
        while 1:
            if node.position == maze.start:
                maze.map[node.position[0]][node.position[1]] = 2
                break
            maze.map[node.position[0]][node.position[1]]=2
            temp=node.parent
            node=temp
        node=original
    def Show_Path(self,node,maze_for_clear):
        show_array=[]
        happy=node.depth
        for i in range(happy+1):
            show_array.append(node)
            node=node.parent
        while 1:
            temp_node=show_array.pop()
            print "Depth :",temp_node.depth
            maze_for_clear.map[temp_node.position[0]][temp_node.position[1]]=2
            for i in range(15):
                print maze_for_clear.map[i]
            if temp_node.position==maze_for_clear.goal:
                break

    def Solve(self, maze) :
        maze_for_clear=[]
        maze_for_clear=copy.deepcopy(maze)
        print "Start Searching by Using IDS"
        self.initial(maze.start[0],maze.start[1])
        self.parent=self
        self.current_node=self
        Fringe=[]
        Fringe.append(self.current_node)

        while 1:
            check=self.Check_goal(self.current_node, maze,Fringe)
            if check== 1:
                if self.current_node.depth != self.depth_limited:
                    self.Solve_next(self.current_node, maze, Fringe)

                self.Path_clear(self.current_node,maze)
                self.current_node = Fringe.pop()
                self.cost+=1
                self.Depth_update(self.current_node,maze)
                self.Path_update(self.current_node,maze)

            elif check== 2:

                break
            elif check==3:
                self.depth_limited+=1
                self.current_node=self
                Fringe.append(self.current_node)

            else:
                print "huuuuuuu"


        self.Show_Path(self.current_node,maze_for_clear)
        print "IDS Real done"
        print "DEPTH is ", self.depth_limited
        print "Cost is ", self.cost

