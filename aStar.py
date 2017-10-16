"""""""""""
This implementation of the A * algorithm is written with help from the "Essentials of the A* Algorithm"
document. The code should be clear if the reader have read the "The Basic A* Algorithm" section, but I
have still tried to comment the code as much as possible.
"""""""""""
import hashlib

#The node class represents a cell on the board.
class Node:
    def __init__(self,row,col,g,h):
        self.state = None
        self.row = row
        self.col = col
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.children = []
        self.parent = None
        self.status = None
    def calcF(self):
        self.f = self.g + self.h
    def manhattanDist(self,target):
        return  abs(self.row - target.row) + abs(self.col - target.col)
    def setState(self):
        self.state = hash(str(self.row) + str(self.col))

#The board class holds all the cells on the board, the root and goal node and the weights of each node type.
class Board:
    def __init__(self,board):
        self.nodes = []
        self.root = None
        self.goal = None
        self.weights = {'w': 100, 'm':50, 'f':10, 'g':5, 'r':1, 'B':0,'A':0,'.':1}
        with open("boards/"+board,'r') as file:
            nodesAppended = False
            while self.goal == None:
                row = col = 0
                file.seek(0)
                for line in file:
                    if not nodesAppended:
                        self.nodes.append([]);
                    for item in line:
                        if item != '\n' and not nodesAppended:
                            self.nodes[row].append(item)
                        if item == "A":
                            self.root = Node(row,col,0,0)
                            self.root.setState()
                        if item == "B" and self.root:
                            self.goal = Node(row,col,0,0)
                            self.root.h = self.root.manhattanDist(self.goal)
                            self.root.calcF()
                            self.goal.setState()
                        col += 1
                    col = 0
                    row += 1
                nodesAppended = True

#Open is a class for the open list so its easier to append and sort the list
class Open:
    def __init__(self,root):
        self.list = []
        self.list.append(root)
        root.status = "Open"
    def pushNode(self,node):
        node.status = "Open"
        self.list.append(node)
        self.list.sort(key=lambda x: x.f,reverse=True)

#get node makes a new node from a cell on the board. In this algorithm it is used to make
#a new neighboring/successing node for a node on the board
def getNode(node,board,neighbors,i,j):
    try:
        if (node.row + i > -1) and (node.col+j > -1):
            if board.nodes[node.row + i][node.col+j] is not '#':
                newNode = Node(node.row+i,node.col+j,node.g,0)
                newNode.h = newNode.manhattanDist(board.goal)
                newNode.calcF()
                newNode.setState()
                return newNode
    except Exception as e:
        pass

#using the getNode function this function will make a node in all 4 directions to the wished node if possible.
#For example if the node is in the top left corner there will only be created 2 nodes, the one to the right, and below
def getNeighbors(node,board):
    neighbors = []
    neighbors.append(getNode(node,board,neighbors,-1,0))
    neighbors.append(getNode(node,board,neighbors,1,0))
    neighbors.append(getNode(node,board,neighbors,0,-1))
    neighbors.append(getNode(node,board,neighbors,0,1))
    neighbors = list(filter(None,neighbors))
    return neighbors

#The attach and eval function takes in two nodes node and X and sets X as the parrent of node and updates node to have the
#correct g,h,and f vaulues corresponding to the new parrent X
def attachAndEval(node,X,board):
    node.parent = X
    node.g = X.g + board.weights[board.nodes[node.row][node.col]]
    node.h = node.manhattanDist(board.goal)
    node.calcF()

#The propagate path improvements function thakes a node as input and updates all it's chldren to have the
#node as parrent withg,h and f values if the path is shorter. A nodes parrent is always the node with the shortest path
#currently found, so this function is used to update the parrent of children if there is a new shorter way found(as the name indicates)
#Notice that this is recursive so it can reach many descendants.
def propagatePathImprovements(node):
    for child in node.children:
        if node.g + node.manhattanDist(child) < child.g:
            child.parent = node
            child.g = node.g + child.manhattanDist(node)
            child.calcF()
            propagatePathImprovements(child)

#since the program is pretty much the exact same as the A* example in the "Essentials of the A* Algorithm" I wont comment much
def main():
    board = Board("board-1-1.txt")
    CLOSED = []
    OPEN = Open(board.root)
    solution = None
    while(not solution):
        if OPEN.list == []:
            break
        X = OPEN.list.pop()
        CLOSED.append(X)
        X.status = "Closed"
        if X.state == board.goal.state:
            solution = X
            break
        #neighbors = successors
        neighbors = getNeighbors(X,board)
        for node in neighbors:
            #if node has previously been created
            for x in CLOSED + OPEN.list:
                if x.state == node.state:
                    node = x
            X.children.append(node)
            if node.status != "Open" and node.status != "Closed":
                attachAndEval(node,X,board)
                OPEN.pushNode(node)
            elif (X.g + X.g + board.weights[board.nodes[node.row][node.col]] )< node.g:
                attachAndEval(node,X,board)
                if node.status == "CLOSED":
                    propagatePathImprovements(node)
    #If we found a solution we first print the cost of the solution wich is the g value of the goal node. Then we back propagate
    #through the parents of the nodes. Since that path is the shortest path, we change the symbol at that nodes position on the
    #board to an 'o' so we can see the path. Then we finaly print the solution.
    if solution:
        print("Found a solution with a path cost of:",solution.g)
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
