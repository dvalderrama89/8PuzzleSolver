import time
import sys
from heapq import *
from copy import deepcopy

#vars
start = time.clock()
array = []
f = -1
g = 1
h = -1
message = ""
heap = []
goalState = ['1', '2', '3', '4', '5', '6', '7', '8', 'X']
runningSolution = ""
end = 0
coordinates = {0:(0,0), 1:(1,0), 2:(2,0),
               3:(0,1), 4:(1,1), 5:(2,1),
               6:(0,2), 7:(1,2), 8:(2,2)}

##################
#Class Definitions
##################
class Node:
    def __init__(self, val, val2):
        self.l_child = None
        self.r_child = None
        self.u_child = None
        self.d_child = None
        self.parent = None

        self.isRoot = False
        self.f = val
        self.state = val2
        self.direction = None
        self.index = None
        self.lastExpanded = None


#######################################
#Function Definitions
#######################################
graph = []
#Inserts into the graph list for each child, then keeps track
#of the index of the child with the lowest F value and pops that to choose which node to expand
#After graph_insert is called, the index of the node will be set, which then needs to be coupled with the
#F value into a tuple and stored in the heap
def graph_insert(root, node):
    if root is None:
        root = node
        graph.insert(0,root)
        root.index = graph.index(root)
        heappush(heap, (root.f, root.index))
    else:
        if node.direction == 'l':
          if root.l_child == None:
            index = graph.index(root) + 1
            graph.insert(2*index, node)
            node.index = graph.index(node)
            root.l_child = node
            node.parent = root
            heappush(heap, (node.f, node.index))
        elif node.direction == 'r':
          if root.r_child == None:
            index = graph.index(root)
            graph.insert(2*index+1, node)
            node.index = graph.index(node)
            root.r_child = node
            node.parent = root
            heappush(heap, (node.f, node.index))
        elif node.direction == 'u':
          if root.u_child == None:
            index = graph.index(root) + 1
            graph.insert(2*index+2, node)
            node.index = graph.index(node)
            root.u_child = node
            node.parent = root
            heappush(heap, (node.f, node.index))
        elif node.direction == 'd':
          if root.d_child == None:
            index = graph.index(root)
            graph.insert(2*index+3, node)
            node.index = graph.index(node)
            root.d_child = node
            node.parent = root
            heappush(heap, (node.f, node.index))
    #endif
#end def

path = []
def print_reverse_path(node):
  if not node:
    #reached the end of the parent chain
    path.reverse()
    s = ""
    for direction in path:
      if direction:
        s += direction
    print s
    return
  path.append(node.direction)
  print_reverse_path(node.parent)

#end def

#manhattan distance
def estimateGoal(array):
  total = 0
  for i in '12345678X':
    x1, y1 = coordinates[array.index(i)]
    x2, y2 = coordinates[goalState.index(i)]
    total += abs(x1-x2) + abs(y1-y2)
  return total
#enddef

def moveUp(node):
  array = deepcopy(node.state)
  pos = array.index('X')
  if pos > 2:
    newPos = pos-3
    array[newPos], array[pos] = array[pos], array[newPos]

  n = Node(estimateGoal(array), array)
  n.direction = 'u'
  return n
#enddef

def moveDown(node):
  array = deepcopy(node.state)
  pos = array.index('X')
  if pos < 6:
    newPos = pos+3
    array[newPos], array[pos] = array[pos], array[newPos]

  n = Node(estimateGoal(array), array)
  n.direction = 'd'
  return n
#enddef

def moveLeft(node):
  array = deepcopy(node.state)
  pos = array.index('X')
  if pos % 3 > 0:
    newPos = pos-1
    array[newPos], array[pos] = array[pos], array[newPos]

  n = Node(estimateGoal(array), array)
  n.direction = 'l'
  return n
#enddef

def moveRight(node):
  array = deepcopy(node.state)
  pos = array.index('X')
  if pos % 3 < 2:
    newPos = pos+1
    array[newPos], array[pos] = array[pos], array[newPos]

  n = Node(estimateGoal(array), array)
  n.direction = 'r'
  return n
#enddef

#pushes the F value and node index to the heap for later comparison
def expandNode(node):
  #check the node's F value with that F value of the heap's root
  if not heap:
    graph_insert(None, node)
    #heappush(heap, (node.f, node.index))
    expandNode(node)

  #try a 'quasi' iterative deepening
  if node.f == heap[0][0] and len(heap) != 1:
    #expand both starting with heap node first
    expandNode(graph[heappop(heap)[1]])
    expandNode(node)
  elif node.f <= heap[0][0] or len(heap) == 1:
    left = moveLeft(node)
    right = moveRight(node)
    up = moveUp(node)
    down = moveDown(node)
    if left.state != node.state and node.direction != 'r':
      graph_insert(node, left)
    if right.state != node.state and node.direction != 'l':
      graph_insert(node, right)
    if up.state != node.state and node.direction != 'd':
      graph_insert(node, up)
    if down.state != node.state and node.direction != 'u':
      graph_insert(node, down)
  elif heap[0][0] == 0:
    return
  else:
    temp = heappop(heap)
    newNode = graph[temp[1]]
    expandNode(newNode)
#end def

#####################################
#MAIN
#####################################
#Piped input
for line in sys.stdin:
    array += line.split()

h = estimateGoal(array)
node = Node(h, array)
if h == 0:
  elapsed = time.clock()
  end = elapsed-start
  print end, "seconds"
  sys.exit()
expandNode(node)

#check to see if the top of the heap is the goal state F value
while heap[0][0] != 0:
  #if it isn't, then expand again by first popping off the heap to obtain the index of the
  #node that we want to expand, retrieve that node from the graph then use it
  n = heappop(heap)
  expandNode(graph[n[1]])
  #after expanding, the heap should once again have the lowest values at the root and if one is 0
  #then we're done and need to find the solution path

  #calc endclock
  elapsed = time.clock()
  end = elapsed-start
  #exit after 1800seconds = 30 minutes
  if end >= 1800:
    t = heappop(heap)
    print_reverse_path(graph[t[1]])
    print end, "seconds"
    sys.exit()
#endwhile

#answer found so pop it from heap and obtain the graph position then pass it to the path function
n2 = heappop(heap)
print_reverse_path(graph[n2[1]])
print end, "seconds"
######################################
