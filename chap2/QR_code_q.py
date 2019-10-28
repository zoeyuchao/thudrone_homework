# -- coding: UTF-8 --
import cv2
from pyzbar.pyzbar import decode
import numpy as np

ROWS = 600
COLS = 600

def IsQrRate(rate):
    # rate 是 np.array
    return np.logical_and(rate>0.15, rate<1.9)

#横向黑白比例判断
def IsQrColorRateX(image, flag):
    # 默认处理的是二值化之后的图
    nr = int(image.shape[0] / 2)
    nc = image.shape[1]
    bar = image[nr,:]
    edge = np.where(bar[:-1]!=bar[1:])[0]
    edge = np.array([-1] + list(edge) + [nc])
    count = edge[1:] - edge[:-1]   # 每个区域的长度
    if len(count)<5:   # 至少有5个区域，考虑到切割图象边界处可能会出现7个区域
        return False
    
    ## 横向黑白比例1:1:3:1:1
    maxCount = np.max(count)
    maxIdx = np.argmax(count)
    if maxIdx<2 or maxIdx>len(count)-3:
        return False
    rate = np.concatenate([count[maxIdx-2:maxIdx],count[maxIdx+1:maxIdx+3]],axis=0).astype(np.float32)/maxCount
    rate = IsQrRate(rate)
    
    return False not in rate

#纵向黑白比例判断
def IsQrColorRateY(image, flag):
    # 默认处理的是二值化之后的图
    nc = int(image.shape[1] / 2)
    nr = image.shape[0]
    bar = image[:,nc]
    edge = np.where(bar[:-1]!=bar[1:])[0]
    edge = np.array([-1] + list(edge) + [nr])
    count = edge[1:] - edge[:-1]   # 每个区域的长度
    if len(count)<5:   # 至少有5个区域，考虑到切割图象边界处可能会出现7个区域
        return False
    ## 纵向黑白比例1:1:3:1:1
    maxCount = np.max(count)
    maxIdx = np.argmax(count)
    if maxIdx<2 or maxIdx>len(count)-3:
        return False
    rate = np.concatenate([count[maxIdx-2:maxIdx],count[maxIdx+1:maxIdx+3]],axis=0).astype(np.float32)/maxCount
    rate = IsQrRate(rate)
    
    return False not in rate

# 判断是横纵两个方向比例
def IsQrColorRate(image, flag):
    x = IsQrColorRateX(image, flag)
    if not x:
        return False
    y = IsQrColorRateY(image, flag)
    return y

# 二维码切割
def CropImage(img, rotatedRect):
    # code here
    
# 判断是否为二维码定位角
def IsQrPoint(contour, img, i):
    rotatedRect = cv2.minAreaRect(contour)
    # 最小大小限定
    if rotatedRect[1][0]<10 or rotatedRect[1][1]<10:
        return False
    # 将二维码从图中抠出来
    imgCrop = CropImage(img, rotatedRect)
    flag = i
    # 黑白比例1:1:3:1:1
    result = IsQrColorRate(imgCrop, flag)
    return result

# 二维码解码
def QrDecode(img):
    # code here

def FindQr(imgSrc):
    qrPoint = []

    # 彩色图转灰度图
    # code here

    # 高斯平滑滤波
    # code here

    # 腐蚀
    # code here
    
    # 二值化
    # code here

    # 查找轮廓
    # code here

    # 筛选定位角：黑色定位角满足父轮廓有两个子轮廓
    parentIdx = -1
    imgSrcClone = np.copy(imgSrc) # 调试用
    for i in range(len(contours)):
        k = i
        ic = 0
        parentIdx = i
        # 计算子轮廓深度
        while hierarchy[0][k][2] != -1:
            k = hierarchy[0][k][2]
            ic = ic + 1

        # 判断是否为定位角
        if ic>=2:
            isQr = IsQrPoint(contours[parentIdx], imgBinary, parentIdx)
            print(parentIdx, isQr)
            if isQr:
                qrPoint.append(contours[parentIdx])

    # 绘制二维码定位角
    for point in qrPoint:
        x,y,w,h = cv2.boundingRect(point)
        cv2.rectangle(imgSrc, (x,y), (x+w,y+h), (255,0,0), thickness=2)

    # 根据相邻三个定位角确定二维码整体位置框
    qrCenter = []
    state = [0]*len(qrPoint)
    qrBox = []
    qrCode = []
    # 计算定位角质心
    for i in range(len(qrPoint)):
        center = np.sum(qrPoint[i], axis=0) / qrPoint[i].shape[0]
        qrCenter.append(center)
    # 判断是否构成一个二维码
    for i in range(len(qrPoint)):
        if state[i]:
            continue
        for j in range(len(qrPoint)):
            if j==i or state[j]:
                continue
            for k in range(len(qrPoint)):
                if k==j or k==i or state[k]:
                    continue
                Dij = np.sum((qrCenter[i]-qrCenter[j])**2).astype(np.float32)
                Dik = np.sum((qrCenter[i]-qrCenter[k])**2).astype(np.float32)
                Djk = np.sum((qrCenter[k]-qrCenter[j])**2).astype(np.float32)
                ratio = Dij / Dik
                ratio1 = (Dij + Dik) / Djk
                if ratio>0.6 and ratio<1.6 and ratio1>0.85 and ratio1<1.15:
                    state[i]=1
                    state[j]=1
                    state[k]=1
                    contour = np.concatenate([qrPoint[i],qrPoint[j],qrPoint[k]], axis=0)
                    rotatedRect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rotatedRect)
                    qrBox.append(np.int0(box))
                    imgTemp = CropImage(imgGray, rotatedRect)
                    # 图像显示裁剪后的二维码
                    # code here
                    # 解码二维码
                    # code here
    # 在原图上画出二维码区域，显示出来
    # code here
    
    return qrCode

    
if __name__ == '__main__':
    # 读入图像
    image = cv2.imread('./imgs/14.jpg')
    # 打印信息
    #code here

    # 处理图像
    qrcode = FindQr(image)
    print("Detected QR Code:")
    print(qrcode)
