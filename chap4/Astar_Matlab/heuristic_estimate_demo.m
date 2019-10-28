function cost = heuristic_estimate_demo(start, goal)
 %Caculation of diagonal distance
 dx = abs(start(1) - goal(1));
 dy = abs(start(2) - goal(2));
 cost = dx + dy+(sqrt(2)-2)*min(dx,dy);  

end

