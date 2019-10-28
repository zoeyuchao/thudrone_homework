clear;
clc;
close all
%%
startPosition = [3 1];%Initial point
goalPosition = [14 12];%End point

% Map initialization, 15 for obstacles, 0 for free space
map = zeros(15,15);%It's the simplest demo
%load('map_test.mat');%use this map to check your A* algorithm

[mapRow, mapCol] = size(map);

if map(startPosition(1), startPosition(2))
    error('Parameters Error! in startPosition');
elseif map(goalPosition(1), goalPosition(2))
    error('Parameters Error! in goalPoaition');
end

%%
% Variables in the two structures can be changed, but 'closeList' need
% to be saved as results and please reserve 'row', & 'col' & 'f'.
% Here, 'row' and 'col' are index numbers of the nodes' row and the coloum,
% 'f' caculates the distance
% 'comefrom' is an index of its parent nodes

closeList = struct('row', 0, 'col', 0,'f',0,'comefrom',0);%The set has been estimated
closeListLength = 0;
openList = struct('row', 0, 'col', 0, 'f',0,'comefrom',0);%The set to be estimated
openListLength = 0;

%%
%Search algorithm
direction = [1,1;-1,-1];%Scanning direction
openList(1).row = startPosition(1);
openList(1).col = startPosition(2);
openListLength = openListLength + 1;
openList(1).f  = 0;

while true
     f =openList(1).f;
    nodePosition = 1;%
    for i = 1:openListLength
        if f > openList(i).f
            f = openList(i).f;
            nodePosition = i;
        end
    end
    
    % Put the nearest node into the close list
    closeListLength = closeListLength + 1;
    closeList(closeListLength) = openList(nodePosition);
    if closeList(closeListLength).row == goalPosition(1) && closeList(closeListLength).col == goalPosition(2)
        break;
    end
    

    for i = 1:size(direction,1)
        newPosition = [closeList(closeListLength).row, closeList(closeListLength).col] + direction(i, :);
        if (all(newPosition > 0) && newPosition(1) <= mapRow  && newPosition(2) <=...
                mapCol  && map(newPosition(1), newPosition(2)) ~= 15)% Exclusion of obstacles
            flag = false;
            for j = 1:closeListLength
                if closeList(j).row == newPosition(1) && closeList(j).col == newPosition(2)
                    flag = true;
                    break;
                end
            end
            
            if flag
                continue;
            end
            openList(openListLength).row = newPosition(1);
            openList(openListLength).col = newPosition(2);
            openList(openListLength).comefrom = closeListLength;
            openList(openListLength).f = heuristic_estimate_demo(newPosition, goalPosition);
        end

    end
end
%%
%Show the results
map(startPosition(1), startPosition(2)) = 15;
map(goalPosition(1), goalPosition(2)) = 30;
figflag = closeListLength;
path  = [];
while true
     if(closeList(figflag).row == startPosition(1) && closeList(figflag).col == startPosition(2))
         break;
     end
      path = [[closeList(figflag).row,closeList(figflag).col];path ];
      figflag = closeList(figflag).comefrom ;

end
for k = 2:size(path,1)
    if(closeList(k).row == goalPosition(1) && closeList(k).col == goalPosition(2))
        break;
    end

    map(closeList(k).row, closeList(k).col) = 20;
    pcolor(map)
    pause(0.3);
end
%%
save('result_yourstudentID','path','closeList');