class Node:
    def __init__(self,row,col,g,h):
        self.row = row
        self.col = col
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.children = []
        self.parent = None
    def calcF(self):
        self.f = self.g + self.h
    def manhattanDist(self,target):
        return  abs(self.row - target.row) + abs(self.col - target.col)

class Board:
    def __init__(self,board):
        self.nodes = []
        self.root = None
        self.goal = None
        self.weights = {'w': 100, 'm':50, 'f':10, 'g':5, 'r':1}
        with open("boards/"+board,'r') as file:
            while self.goal == None:
                row = col = 0
                file.seek(0)
                for line in file:
                    self.nodes.append([]);
                    for item in line:
                        if item != '\n':
                            self.nodes[row].append(item)
                        if item == "A":
                            self.root = Node(row,col,0,0)
                        if item == "B" and self.root:
                            self.goal = Node(row,col,0,0)
                            self.root.h = self.root.manhattanDist(self.goal)
                            self.root.calcF()
                        col += 1
                    col = 0
                    row += 1

class Open:
    def __init__(self,root):
        self.list = []
        self.list.append(root)
    def pushNode(self,node):
        self.list.append(node)
        self.list.sort(key=lambda x: x.f,reverse=True)


def getNode(node,board,neighbors,i,j):
    try:
        if (node.row + i > -1) and (node.col+j > -1):
            if board.nodes[node.row + i][node.col+j] is not '#':
                newNode = Node(node.row+i,node.col+j,node.g,0)
                newNode.g += board.weights[board.nodes[node.row + i][node.col+j]]
                newNode.h = newNode.manhattanDist(board.goal)
                newNode.calcF()
                return newNode
    except Exception as e:
        print("There was no successor there")

def getNeighbors(node,board):
    neighbors = []
    neighbors.append(getNode(node,board,neighbors,-1,0))
    neighbors.append(getNode(node,board,neighbors,1,0))
    neighbors.append(getNode(node,board,neighbors,0,-1))
    neighbors.append(getNode(node,board,neighbors,0,1))
    neighbors = list(filter(None,neighbors))
    return neighbors

def attachAndEval(node,X,board):
    node.parent = X
    node.g = X.g + X.manhattanDist(node)
    node.h = node.manhattanDist(board.goal)
    node.calcF()

def propagatePathImprovements(node):
    for child in node.children:
        if node.g + node.manhattanDist(child) < child.g:
            child.parent = node
            child.g = g.node + child.manhattanDist(node)
            child.calcF()
            propagatePathImprovements(child)

def main():
    print("fds")
    board = Board("board-2-1.txt")
    root  = board.root
    goal = board.goal
    CLOSED = []
    OPEN = Open(root)
    solution = None
    finished = False
    while(not finished):
        if OPEN.list == []:
            finished = True
            pass
        else:
            X = OPEN.list.pop()
            CLOSED.append(X)
            if X.row == goal.row and X.col == goal.col:
                finished = True
                solution = X
                print("found solution")
                break
            neighbors = getNeighbors(X,board)
            for node in neighbors:
                print(node.g,node.h,node.f,node.row,node.col)
                #if node S* has previously been created, and if state(S*) = state(S),then S <- S*
                for x in OPEN.list:
                    if node.row == x.row and node.col ==x.col:
                        node = x
                for x in CLOSED:
                    if node.row == x.row and node.col ==x.col:
                        node = x
                X.children.append(node)
                if node not in OPEN.list and node not in CLOSED:
                    attachAndEval(node,X,board)
                    OPEN.pushNode(node)
                elif (X.g + X.manhattanDist(node)) < node.g:
                    attachAndEval(node,X,board)
                    if node in CLOSED:
                        propagatePathImprovements(node)
        print(".......")
    if solution:
        parentNode = solution.parent
        while parentNode:
            board.nodes[parentNode.row][parentNode.col]= 'o'
            if not parentNode.parent:
                board.nodes[parentNode.row][parentNode.col]= 'A'
            parentNode = parentNode.parent

        for i in board.nodes:
            for k in i:
                print(k,end='')
            print('')
    else:
        print("There was no solution")

if __name__ == "__main__":
    main()
