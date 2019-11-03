# Chapter4_A* algorithm

## 1. 路径规划问题

1. 实现 A* 算法
2. 实现 Dijsktra 算法

## 2. 文件说明

- `Astar_Matlab/`：matlab实现代码(仅demo)
- `Astar_Python/`：python实现代码
  - `Astar_demo.ipynb`：需添加 A* 算法核心部分的demo
  - `Astar_demo.py`：需添加 A* 算法核心部分的demo
  - `map.npy`：地图文件
  - `GUI/`：交互式查看路径规划结果
    - `images/`：图形界面所需图片
    - `showPath_GUI.py`：展示路径规划算法结果
  - `answer/`：参考答案
    - `Astar.py`：完整的 A* 算法
    - `Dijkstra.py`：Dijkstra 算法
    - `heuristic.py`：启发式 BFS 算法
    - `findPath.py`：封装后的路径规划函数，采用 A* 算法

## 3. 运行方法

- 路径规划算法实现

  - 将 `map.npy` 与 `Astar.py`，`Dijkstra.py`，`heuristic.py` 文件放在同一文件夹下

  - 在命令行中切换至该文件夹下，运行

    ```shell
    python Astra.py
    python Dijkstra.py
    python heuristic.py
    ```

- 交互式界面查看

  - 将 `findPath.py` 移至 `GUI/` 文件夹下

  - 在命令行中切换至 `GUI/` 文件夹下，运行

    ```shell
    python showPath_GUI.py
    ```

## 4. 常见问题

1. 课件伪代码中的 `g_score[]`，`f_score[]`，`h_score[]` 并非代表 A* 算法中的 g(),f(),h()！`g_score[position A]` 是 openList 中点 A 对应的存储的 `g` 值，其他同理。
2. 根据设置的距离函数和启发式函数 g 与 h 的不同，搜索路径可能不同，最优路径也可能不同。
3. A*算法能够得到最优解的充分条件为
   1. 搜索树上存在着从起点到终点的最优路径
   2. 问题域是有限的
   3. 所有节点的子节点搜索代价值 > 0
   4. h(n) <= h*(n)，即启发值小于真实值
4. 每次从 openlist 中寻找最小的 f 时，通过 `<=` 和 `<` 得到的搜索顺序是不同的，前者表示偏好后加进来的点，后者表示偏好先加进来的点
5. waiting ...

