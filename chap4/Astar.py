import numpy as np
import matplotlib.pyplot as plt

##########################################
########    initialization     ########
##########################################
#mapmap = np.load('map.npy')
mapmap = np.zeros((15,15),dtype=np.int)
print(mapmap.shape)
startPosition = (2, 0)    #Initial point
goalPosition = (13, 11)   #End point
direction = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
#direction = [[0,1],[0,-1],[1,0],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]] #reachable direction
mapRow, mapCol = mapmap.shape;
if mapmap[startPosition[0], startPosition[1]]:
    exit('Parameters Error! in startPosition')
elif mapmap[startPosition[0], startPosition[1]]:
    exit('Parameters Error! in goalPoaition')
    
##########################################
########   heuristic function   ########
##########################################
def cost(startPoistion, goalPosition):
    dx, dy = abs(np.array(startPoistion)-np.array(goalPosition))
    distance = 10*(dx+dy) - 6*min(dx,dy)
    #distance = dx+dy-0.6*min(dx,dy)
    return distance

def g(startPoistion, startCost, goalPosition):
    goalCost = startCost + cost(startPoistion, goalPosition)
    return goalCost

def heuristic(startPosition, goalPosition):
    dx, dy = abs(np.array(startPosition)-np.array(goalPosition))
    distance = 10*(dx+dy) - 6*min(dx,dy)
    return distance

##########################################
########    useful function    ########
##########################################
def isPositionValid(position):
    return position[0]>=0 and position[1]>=0 and position[0]<mapRow \
            and position[1]<mapCol and (mapmap[position[0],position[1]]==0)

def isInCloseList(position, closeList):
    for i in range(len(closeList)):
        if position==closeList[i][0:2]:
            return True
    return False

##########################################
########     A* algorithm     ########
##########################################
# initialize
openList = []
closeList = []

# add the first node
nodePosition = startPosition
gg = g(startPosition, 0, nodePosition)
hh = heuristic(nodePosition, goalPosition)
nodeInfo = (nodePosition[0],nodePosition[1],gg+hh, gg, hh, 0)
openList.append(nodeInfo)

while True:
    # find the closest node in openList 
    if not openList:
        break
    nodeIdx = 0
    fmin = openList[nodeIdx][2]
    for i in range(1,len(openList)):
        if openList[i][2] <= fmin:  #加上=表示偏好于后加进来的点，可以减少搜索次数
            fmin = openList[i][2]
            nodeIdx = i
        
    nodeInfo = openList.pop(nodeIdx)
    nodePosition = nodeInfo[0:2]
    closeList.append(nodeInfo)
    
    if nodePosition == goalPosition:
        break
    
    for i in range(len(direction)):
        nextPosition = tuple(np.array(nodePosition) + np.array(direction[i]))
        if (not isPositionValid(nextPosition)) or isInCloseList(nextPosition, closeList):
            continue
        
        flag = True
        nextg = g(nodePosition,nodeInfo[3],nextPosition);
        nexth = heuristic(nextPosition,goalPosition)
        nextf =  nextg + nexth
        for j in range(len(openList)):
            if tuple(nextPosition)==openList[j][0:2]:
                flag = False
                if nextf < openList[j][2]:
                    openList[j] = (nextPosition[0],nextPosition[1],nextf,nextg,nexth,len(closeList)-1)
                break
        
        if flag:
            nextInfo = (nextPosition[0],nextPosition[1],nextf,nextg,nexth,len(closeList)-1)
            openList.append(nextInfo)
        
##########################################
########    visualization      ########
##########################################
fig, (ax0, ax1) = plt.subplots(1, 2)
fig.suptitle('A* algorithm',fontsize=36)
ax0.set_title('Searching process')
ax1.set_title('Searched path')

mapViz = mapmap.copy()
mapViz[startPosition[0],startPosition[1]] = 30;
mapViz[goalPosition[0], goalPosition[1]] = 30;
for k in range(len(closeList)-1):
    mapViz[closeList[k][0],closeList[k][1]] = 200-closeList[k][2]
    ax0.pcolormesh(mapViz)
    plt.pause(0.1)
    
mapViz = mapmap.copy()
mapViz[startPosition[0],startPosition[1]] = 30;
mapViz[goalPosition[0], goalPosition[1]] = 30;
flag = closeList[-1][0:2] == goalPosition
path = []
nodeIdx = -1
while flag:
    if closeList[nodeIdx][0:2]==startPosition:
        break
    path.append(closeList[nodeIdx][0:2])
    nodeIdx = closeList[nodeIdx][-1]
path.reverse()
for k in range(len(path)-1):
    mapViz[path[k][0],path[k][1]] = 20
    ax1.pcolormesh(mapViz)
    plt.pause(0.1)
    
plt.show()