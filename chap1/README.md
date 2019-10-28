# Chapter1_pointcloud

- pointcloud_q.py是试题，pointcloud.py是答案。

- 运行方法：

  ```
  python pointcloud.py
  ```

  或者将该文件放到某个ROS的包下，执行：

  ```
  chmod +x pointcloud.py
  rosrun xxx pointcloud.py
  ```

- 然后打开一个终端，执行：

  ```
  roscore
  ```

- 再打开一个终端，执行：

  ```
  rviz
  ```

  在rviz界面选择add按钮，选择PointCloud2数据格式，确定之后在下拉菜单下添加一个/points的话题（自行输入或者下拉菜单选择），然后就可以看到点云了。颜色不对的同学就是rgb通道反了或者数据大小不对，rviz认识的是0-1之间。

