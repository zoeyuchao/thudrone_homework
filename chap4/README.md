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

1. 课件伪代码中的 `g_score[]`，`f_score[]`，`h_score[]` 并非代表 A* 算法中的 $g(\cdot), f(\cdot), h(\cdot)$！`g_score[position A]` 是 openList 中点 A 对应的存储的 `g` 值，其他同理。
2. waiting ...