clear;
clc;
close all
%%
startPosition = [3 1];%Initial point
goalPosition = [14 12];%End point

%Map initialization, 15 for obstacles, 0 for free space
load('map_test.mat');
[mapRow, mapCol] = size(map);

if map(startPosition(1), startPosition(2))
    error('Parameters Error! in startPosition');
elseif map(goalPosition(1), goalPosition(2))
    error('Parameters Error! in goalPoaition');
end

%%

closeList = struct('row', 0, 'col', 0,'order',0,'comefrom',0);
closeListLength = 0;
openList = struct('row', 0, 'col', 0, 'order',0,'comefrom',0);
openListLength = 0;
closeList(1).row = startPosition(1);
closeList(1).col = startPosition(2);

%%
%Search algorithm
direction = [0,1;0,-1;1,0;-1,0;1,1;1,-1;-1,1;-1,-1];%Scanning direction

for i=1:mapRow
    for j=1:mapCol
        openListLength = openListLength+1;
        openList(openListLength).row = i;
        openList(openListLength).col = j;
        openList(openListLength).order = Inf;
        if openList(openListLength).row == startPosition(1) && openList(openListLength).col == startPosition(2)
            openList(openListLength).order = 0;
        end
    end
end

kflag = 1;
iflag = 1;
while true
    orderflag =openList(1).order;
    nodePosition = 1;%记录
    for i = 1:openListLength
        if openList(i).order <= orderflag
            
            orderflag = openList(i).order;
            nodePosition = i;
        end
    end
    closeListLength = closeListLength + 1;
    closeList(closeListLength) = openList(nodePosition);
    openList(nodePosition).order = openListLength+1;
    
    if closeList(closeListLength ).row == goalPosition(1) && closeList(closeListLength ).col == goalPosition(2)
        break;
    end
    
    
    for i = 1:size(direction,1)
        newPosition = [closeList(closeListLength).row, closeList(closeListLength).col] + direction(i, :);
        
        cflag = false;
        for j = 1:closeListLength
            if closeList(j).row == newPosition(1) && closeList(j).col == newPosition(2)
                cflag = true;
                break;
            end
        end
        
        if cflag
            continue;
        end
        
        if (all(newPosition > 0) && newPosition(1) < mapRow  && newPosition(2) < mapCol  && map(newPosition(1), newPosition(2)) ~= 15)
            
            for mn = 1:openListLength
                if openList(mn).row == newPosition(1)  &&      openList(mn).col == newPosition(2)
                    if openList(mn).order > openListLength+1
                        openList(mn).comefrom = closeListLength;
                        
                        if(openList(mn).row -closeList(closeListLength).row + openList(mn).col -closeList(closeListLength).col == 1)
                            openList(mn).order = closeList(closeListLength).order+1;
                        else
                            openList(mn).order = closeList(closeListLength).order+1.14;
                        end
 
                    end
                end
            end
        end
        
    end
    
end

%%
%结果可视化显示
map(startPosition(1), startPosition(2)) = 30;
map(goalPosition(1), goalPosition(2)) = 30;
iflag = closeListLength;


path  = [];
while true
    if(closeList(iflag).row == startPosition(1) && closeList(iflag).col == startPosition(2))
        break;
    end
    path = [path;[closeList(iflag).row,closeList(iflag).col] ];
    iflag =closeList(iflag).comefrom;
    
end



while true
    if(closeList(iflag).row == goalPosition(1) && closeList(iflag).col == goalPosition(2))
        break;
    end
    iflag =iflag +1;
    %iflag = iflag -1;
    if(closeList(iflag).row ~= goalPosition(1)|| closeList(iflag).col ~= goalPosition(2))
        map(closeList(iflag).row, closeList(iflag).col) = 10;
    end
    pcolor(map)
    pause(0.3);
end

for i = size(path,1):-1:2
    
    map(path(i,1), path(i,2)) = 25;
    
    pcolor(map)
    pause(0.3);
    
end