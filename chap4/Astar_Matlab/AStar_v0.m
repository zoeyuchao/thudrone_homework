clear;
clc;
close all
%%
startPosition = [3 1];%Initial point
goalPosition = [14 12];%End point

% Map initialization, 15 for obstacles, 0 for free space
%map = zeros(15,15);%It's the simpleset demo
load('map_test.mat');%use this map to check your A* algorithm

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
% 'g' & 'h' & 'f' caculate g(n),h(n)&f(n),respectively
% 'comefrom' is an index of its parent nodes

closeList = struct('row', 0, 'col', 0, 'g', 0, 'h', 0,'f',0,'comefrom',0);  
closeListLength = 0;
openList = struct('row', 0, 'col', 0, 'g', 0, 'h', 0,'f',0,'comefrom',0);
openListLength = 0;

direction = [0,1;0,-1;1,0;-1,0;1,1;1,-1;-1,1;-1,-1];% Diagonal distance is allowed

%%
% Search algorithm, which need to be completed by you

while true %Other termination conditions are also allowed

    if true
    break;
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
%Save the results
save('result_yourstudentID','path','closeList');