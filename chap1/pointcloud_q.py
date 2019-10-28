#!/usr/bin/env python
import numpy as np
import cv2
import rospy
from sensor_msgs.msg import PointCloud2, PointField
from sensor_msgs import point_cloud2
import pdb

# 实验一：三维空间刚体运动的描述方式   请同学们自行学习numpy的用法，利用numpy的向量、矩阵操作完成以下函数
def q2R(q): 
    '''
    功能：四元数转旋转矩阵
    输入：q 1x4的四元数向量，实部在前，虚部在后
    返回值：R 3x3的旋转矩阵
    其中输入和返回值都用numpy结构
    '''
    # Code here

def R2q(R):
    '''
    功能：旋转矩阵转四元数
    输入：R 3x3的旋转矩阵
    返回值：q 1x4的四元数向量，实部在前，虚部在后
    其中输入和返回值都用numpy结构
    '''
    # Code here

def R2T(R, t):
    '''
    功能：旋转矩阵转变换矩阵
    输入：R 3x3的旋转矩阵 t 3维的平移向量
    返回值：T 4x4的变换矩阵
    其中输入和返回值都用numpy结构
    '''
    # Code here

def T2R(T):
    '''
    功能：变换矩阵转旋转矩阵
    输入：T 4x4的变换矩阵
    返回值：R 3x3的旋转矩阵
    其中输入和返回值都用numpy结构
    '''
    # Code here


if __name__ == '__main__':
    # 实验二：坐标转换
    colorImgs = []     # 保存RGB图的列表
    depthImgs = []     # 保存深度图的列表
    poses = []         # 保存相机的外参，即转换后的变换矩阵       
    
    # 读取文件，将外参保存在列表中
    # Code here
   
    
    for i in range(5):
        # 利用opencv读取RGB和深度图，按顺序保存在colorImgs和depthImgs中
        # Code here
        

        # 将poses列表中的单元转成变换矩阵T储存
        # Code here


    # 计算点云并拼接
    # 相机内参
    cx = 325.5
    cy = 253.5
    fx = 518.0
    fy = 519.0
    depthScale = 1000.0

    # 新建一个列表，保存所有点的世界坐标
    cloudWorld = []

    for i in range(5):
        print("processing image " + str(i+1))
        # Code here

                # 将像素坐标转换成相机坐标
                # Code here


                # 利用变换矩阵T，将相机坐标转换成世界坐标
                # Code here

                
                # 将世界坐标添加到cloudWorld中
                # Code here    


    # ROS相关操作，将点云信息发布出去
    rospy.init_node('test', anonymous=True)
    pub_cloud = rospy.Publisher("/points", PointCloud2)
    while not rospy.is_shutdown():
        pcloud = PointCloud2()
        # make point cloud
        # Code here
        
        pcloud.header.frame_id = "/map"
        pub_cloud.publish(pcloud)
        rospy.sleep(1.0)
    


            