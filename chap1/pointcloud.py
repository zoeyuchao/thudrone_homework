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
    R = np.zeros((3,3))
    R[0][0] = 1 - 2*q[2]*q[2] - 2*q[3]*q[3]
    R[0][1] = 2*q[1]*q[2] + 2*q[0]*q[3]
    R[0][2] = 2*q[1]*q[3] - 2*q[0]*q[2] 
    R[1][0] = 2*q[1]*q[2] - 2*q[0]*q[3]
    R[1][1] = 1 - 2*q[1]*q[1] - 2*q[3]*q[3]
    R[1][2] = 2*q[2]*q[3] + 2*q[0]*q[1]
    R[2][0] = 2*q[1]*q[3] + 2*q[0]*q[2]
    R[2][1] = 2*q[2]*q[3] - 2*q[0]*q[1]
    R[2][2] = 1 - 2*q[1]*q[1] - 2*q[2]*q[2]
    return R

def R2q(R):
    '''
    功能：旋转矩阵转四元数
    输入：R 3x3的旋转矩阵
    返回值：q 1x4的四元数向量，实部在前，虚部在后
    其中输入和返回值都用numpy结构
    '''
    # Code here
    pass

def R2T(R, t):
    '''
    功能：旋转矩阵转变换矩阵
    输入：R 3x3的旋转矩阵 t 3维的平移向量
    返回值：T 4x4的变换矩阵
    其中输入和返回值都用numpy结构
    '''
    # Code here
    T = np.zeros((4,4))
    T[0:3, 0:3] = R
    T[0:3, 3] = t
    T[3][3] = 1
    return T

def T2R(T):
    '''
    功能：变换矩阵转旋转矩阵
    输入：T 4x4的变换矩阵
    返回值：R 3x3的旋转矩阵
    其中输入和返回值都用numpy结构
    '''
    # Code here
    pass


if __name__ == '__main__':
    # 实验二：坐标转换
    colorImgs = []     # 保存RGB图的列表
    depthImgs = []     # 保存深度图的列表
    poses = []         # 保存相机的外参，即转换后的变换矩阵       
    
    # 读取文件，将外参保存在列表中
    with open("./pose.txt", "r") as file:
        lines = file.readlines()
        for i in range(5):
            poses.append(map(float, lines[i].strip().split()))
   
    
    for i in range(5):
        # 利用opencv读取RGB和深度图，按顺序保存在colorImgs和depthImgs中
        # Code here
        b = cv2.imread("./color/" + str(i+1) + ".png")
        colorImgs.append(b)
        a = cv2.imread("./depth/" + str(i+1) + ".pgm", -1)
        depthImgs.append(a)

        # 将poses列表中的单元转成变换矩阵T储存
        # Code here
        tmp = q2R(np.array([poses[i][6], poses[i][3], poses[i][4], poses[i][5]]))
        tmp = R2T(tmp.T, np.array([poses[i][0], poses[i][1], poses[i][2]]))    # 转置
        poses[i] = tmp

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
        color = colorImgs[i]
        depth = depthImgs[i]
        T = poses[i]
        rows = depth.shape[0]
        cols = depth.shape[1]
        for v in range(rows):
            for u in range(cols):
                d = depth[v][u]
                # d=0，即没检测到点，跳过
                if (d == 0):
                    continue

                # 将像素坐标转换成相机坐标
                # Code here
                point = np.zeros(4)
                point[3] = 1
                point[2] = d/depthScale 
                point[0] = (u-cx)*point[2]/fx
                point[1] = (v-cy)*point[2]/fy 

                # 利用变换矩阵T，将相机坐标转换成世界坐标
                # Code here
                pointWorld = np.dot(T, point)
                
                # 将世界坐标添加到cloudWorld中
                # Code here    
                cloudWorld.append(pointWorld[0:3].tolist()+[color[v][u][2],color[v][u][1],color[v][u][0]])

    # ROS相关操作，将点云信息发布出去
    rospy.init_node('pointcloud', anonymous=True)
    pub_cloud = rospy.Publisher("/points", PointCloud2)
    while not rospy.is_shutdown():
        pcloud = PointCloud2()
        # make point cloud
        fields = [PointField('x', 0, PointField.FLOAT32, 1),
                PointField('y', 4, PointField.FLOAT32, 1),
                PointField('z', 8, PointField.FLOAT32, 1),
                PointField('r', 12, PointField.FLOAT32, 1),
                PointField('g', 16, PointField.FLOAT32, 1),
                PointField('b', 20, PointField.FLOAT32, 1)]
        pcloud = point_cloud2.create_cloud(pcloud.header, fields, cloudWorld)
        # pcloud = point_cloud2.create_cloud_xyz32(pcloud.header, cloudWorld)
        pcloud.header.frame_id = "/map"
        pub_cloud.publish(pcloud)
        rospy.sleep(1.0)
    


            