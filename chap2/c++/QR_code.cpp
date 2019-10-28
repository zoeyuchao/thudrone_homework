#include <iostream>
#include<vector>
#include<cmath>
#include"algorithm"
#include "core/core.hpp"
#include "highgui/highgui.hpp"
#include "imgproc/imgproc.hpp"
#include "zbar.h"
#include "string.h"
#include <iomanip>
using namespace std;
using namespace cv;
using namespace zbar;

int ROWS = 600;
int COLS = 800;
vector<vector<Point>> contours;
vector<Vec4i> hierarchy;

bool IsQrRate(float rate)
{
	//大概比例 不能太严格
	return rate > 0.3 && rate < 1.9;
}


//横向黑白比例判断
bool IsQrColorRateX(cv::Mat& image, int flag)
{
	int nr = image.rows / 2;
	int nc = image.cols * image.channels();

	vector<int> vValueCount;
	vector<uchar> vColor;
	int count = 0;
	uchar lastColor = 0;

	uchar* data = image.ptr<uchar>(nr);
	for (int i = 0; i < nc; i++)
	{
		vColor.push_back(data[i]);
		uchar color = data[i];
		if (color > 0)
			color = 255;

		if (i == 0)
		{
			lastColor = color;
			count++;
		}
		else
		{
			if (lastColor != color)
			{
				vValueCount.push_back(count);
				count = 0;
			}
			count++;
			lastColor = color;
		}
	}

	if (count != 0)
		vValueCount.push_back(count);

	if (vValueCount.size() < 5 || vValueCount.size() >7)
		return false;

	//横向黑白比例1:1:3:1:1
	int index = -1;
	int maxCount = -1;
	for (int i = 0; i < vValueCount.size(); i++)
	{
		if (i == 0)
		{
			index = i;
			maxCount = vValueCount[i];
		}
		else
		{
			if (vValueCount[i] > maxCount)
			{
				index = i;
				maxCount = vValueCount[i];
			}
		}
	}

	//左边 右边 都有两个值，才行
	if (index < 2)
		return false;
	if ((vValueCount.size() - index) < 3)
		return false;

	//黑白比例1:1:3:1:1
	float rate = ((float)maxCount) / 3.00;

	cout << "flag:" << flag << " ";

	float rate2 = vValueCount[index - 2] / rate;
	cout << rate2 << " ";
	if (!IsQrRate(rate2))
		return false;

	rate2 = vValueCount[index - 1] / rate;
	cout << rate2 << " ";
	if (!IsQrRate(rate2))
		return false;

	rate2 = vValueCount[index + 1] / rate;
	cout << rate2 << " ";
	if (!IsQrRate(rate2))
		return false;

	rate2 = vValueCount[index + 2] / rate;
	cout << rate2 << endl;
	if (!IsQrRate(rate2))
		return false;

	return true;
}


//纵向黑白比例判断 省略
bool IsQrColorRateY(cv::Mat& image, int flag) {
	int nc = image.cols / 2;
	int nr = image.rows;

	vector<int> vValueCount;
	int count = 0;
	uchar lastColor = 0;

	for (int i = 0; i < nr; i++)
	{
		uchar* data = image.ptr<uchar>(i, nc);
		uchar color;
		if (data[0] > 0 || data[1] > 0 || data[2] > 0)
			color = 255;
		else
			color = 0;

		if (i == 0)
		{
			lastColor = color;
			count++;
		}
		else
		{
			if (lastColor != color)
			{
				vValueCount.push_back(count);
				count = 0;
			}
			count++;
			lastColor = color;
		}
	}

	if (count != 0)
		vValueCount.push_back(count);

	if (vValueCount.size() < 5 || vValueCount.size() >7)
		return false;

	//横向黑白比例1:1:3:1:1
	int index = -1;
	int maxCount = -1;
	for (int i = 0; i < vValueCount.size(); i++)
	{
		if (i == 0)
		{
			index = i;
			maxCount = vValueCount[i];
		}
		else
		{
			if (vValueCount[i] > maxCount)
			{
				index = i;
				maxCount = vValueCount[i];
			}
		}
	}

	//左边 右边 都有两个值，才行
	if (index < 2)
		return false;
	if ((vValueCount.size() - index) < 3)
		return false;

	//黑白比例1:1:3:1:1
	float rate = ((float)maxCount) / 3.00;

	cout << "flag:" << flag << " ";

	float rate2 = vValueCount[index - 2] / rate;
	cout << rate2 << " ";
	if (!IsQrRate(rate2))
		return false;

	rate2 = vValueCount[index - 1] / rate;
	cout << rate2 << " ";
	if (!IsQrRate(rate2))
		return false;

	rate2 = vValueCount[index + 1] / rate;
	cout << rate2 << " ";
	if (!IsQrRate(rate2))
		return false;

	rate2 = vValueCount[index + 2] / rate;
	cout << rate2 << endl;
	if (!IsQrRate(rate2))
		return false;

	return true;
}


//横向和纵向黑白比例判断
bool IsQrColorRate(cv::Mat& image, int flag)
{
	bool x = IsQrColorRateX(image, flag);
	if (!x)
		return false;
	bool y = IsQrColorRateY(image, flag);
	return y;
}

//二维码定位角区域切割
Mat CropImage(Mat& img, RotatedRect& rotatedRect) {
	Point2f points[4];
	rotatedRect.points(points);
	int topLeftIndex = 0;
	double topLeftR = points[0].x*points[0].x + points[0].y*points[0].y;
	for (int i = 1; i<4; i++) {
		double r = points[i].x*points[i].x + points[i].y*points[i].y;
		if (r<topLeftR) {
			topLeftIndex = i;
			topLeftR = r;
		}
	}
	double x1 = points[(topLeftIndex + 1) % 4].x - points[topLeftIndex].x, y1 = points[(topLeftIndex + 1) % 4].y - points[topLeftIndex].y;
	double x2 = points[(topLeftIndex + 3) % 4].x - points[topLeftIndex].x, y2 = points[(topLeftIndex + 3) % 4].y - points[topLeftIndex].y;
	double vX1 = x1, vY1 = y1, vX2 = x2, vY2 = y2;
	int width = (int)sqrt(vX1*vX1 + vY1*vY1), height = (int)sqrt(vX2*vX2 + vY2*vY2);
	if (img.dims == 3) {
		Mat ret(Size(width, height), CV_8UC3);
		for (int j = 0; j<ret.rows; j++) {
			for (int i = 0; i<ret.cols; i++) {
				double kx = (double)i / width, ky = (double)j / height;
				int x = (int)(points[topLeftIndex].x+ kx*vX1 + ky*vX2), y = (int)(points[topLeftIndex].y + kx*vY1 + ky*vY2);
				if (x < 0)x = 0;
				else if (x >= img.cols)x = img.cols - 1;
				if (y < 0)y = 0;
				else if (y >= img.rows)y = img.rows - 1;
				ret.at<Vec3b>(j, i) = img.at<Vec3b>(y, x);
			}
		}
		return ret;
	}
	else {
		Mat ret(Size(width, height), CV_8UC1);
		for (int j = 0; j<ret.rows; j++) {
			for (int i = 0; i<ret.cols; i++) {
				double kx = (double)i / width, ky = (double)j / height;
				int x = (int)(points[topLeftIndex].x + kx*vX1 + ky*vX2), y = (int)(points[topLeftIndex].y + kx*vY1 + ky*vY2);
				if (x < 0)x = 0;
				else if (x >= img.cols)x = img.cols - 1;
				if (y < 0)y = 0;
				else if (y >= img.rows)y = img.rows - 1;
				ret.at<uchar>(j, i) = img.at<uchar>(y, x);
			}
		}
		return ret;
	}
}

//判断是否是二维码定位角
bool IsQrPoint(vector<Point>& contour, Mat& img, int i)
{
	//最小大小限定
	RotatedRect rotatedRect = minAreaRect(contour);
	if (rotatedRect.size.height < 10 || rotatedRect.size.width < 10)
		return false;

	//将二维码从整个图上抠出来
	cv::Mat cropImg = CropImage(img, rotatedRect);
	int flag = i++;

	//横向黑白比例1:1:3:1:1
	bool result = IsQrColorRate(cropImg, flag);
	return result;
}


//二维码解码
void RecogQr(Mat& image, string& qrcode) {
	ImageScanner scanner;
	scanner.set_config(ZBAR_NONE, ZBAR_CFG_ENABLE, 1);
	int width = image.cols;
	int height = image.rows;
	uchar *raw = (uchar *)image.data;
	Image imageZbar(width, height, "Y800", raw, width * height);
	scanner.scan(imageZbar); //扫描条码    
	Image::SymbolIterator symbol = imageZbar.symbol_begin();
	qrcode = symbol->get_data();
}


//找出图片中所有二维码，用定位框标出并识别
void FindQrPoint(Mat& srcImg, vector<vector<Point>>& qrPoint)
{
	//彩色图转灰度图
	Mat src_gray, src_Gaussian;
	Mat imageSobelX, imageSobelY, imageSobelOut;
	cvtColor(srcImg, src_gray, CV_BGR2GRAY);
	namedWindow("src_gray", 0);
	cvResizeWindow("src_gray", COLS, ROWS);
	imshow("src_gray", src_gray);

	//高斯平滑滤波
	GaussianBlur(src_gray, src_Gaussian, Size(3, 3), 0);
	namedWindow("Gaussian_filtering", 0);
	cvResizeWindow("Gaussian_filtering", COLS, ROWS);
	imshow("Gaussian_filtering", src_Gaussian);
	imageSobelOut = src_Gaussian.clone();
	
	//开运算,消除亮度较高的细小区域,先腐蚀后膨胀（腐蚀，消除局部反光影响）  
	Mat  element1=getStructuringElement(0,Size(3,3));    
	erode(imageSobelOut, imageSobelOut, element1);
	namedWindow("腐蚀", 0);
	cvResizeWindow("腐蚀", COLS, ROWS);
	imshow("腐蚀",imageSobelOut);     
	
	//二值化
	Mat threshold_output;
	threshold(imageSobelOut, threshold_output, 0, 255, THRESH_BINARY | THRESH_OTSU);
	Mat threshold_output_copy = threshold_output.clone();
	namedWindow("Threshold_output", 0);
	cvResizeWindow("Threshold_output", COLS, ROWS);
	imshow("Threshold_output", threshold_output);

	//调用查找轮廓函数
	findContours(threshold_output, contours, hierarchy, CV_RETR_TREE, CHAIN_APPROX_NONE, Point(0, 0));

	Mat srcImg_copy = srcImg.clone();
	for (int i = 0; i < contours.size(); i++)
	{
		Rect rect = boundingRect((Mat)contours[i]);
		float c = (float)rect.width / rect.height;
		rectangle(srcImg_copy, rect, Scalar(255), 2);
	}
	namedWindow("contours", 0);
	cvResizeWindow("contours", COLS, ROWS);
	imshow("contours", srcImg_copy);


	//通过黑色定位角作为父轮廓，有两个子轮廓的特点，筛选出三个定位角
	int parentIdx = -1;

	for (int i = 0; i < contours.size(); i++)
	{
		int k = i;
		int ic = 0;
		while (hierarchy[k][2] != -1) {
			if (ic == 0)
				parentIdx = i;
			k = hierarchy[k][2];
			ic++;
		}


		//有两个子轮廓才是二维码的顶点
		if (ic >= 2)
		{
			cout << parentIdx << endl;
			bool isQr = IsQrPoint(contours[parentIdx], threshold_output_copy, parentIdx);

			//保存找到的三个黑色定位角
			if (isQr)
				qrPoint.push_back(contours[parentIdx]);

			parentIdx = -1;
		}
	}
	//绘制二维码定位角
	for (int i = 0; i < qrPoint.size(); i++)
	{
		Rect rect = boundingRect((Mat)qrPoint[i]);
		rectangle(srcImg, rect, Scalar(255), 2);
	}


	//根据相邻三个定位角确定二维码整体位置框，并对二维码进行解码
	vector<Point> qrCenter;					//各个定位角的中心
	vector<int> state(qrPoint.size(),0);	//状态变量，记录该定位角是否属于某个完整二维码（只有三个定位角同时出现才认为是一个完整的二维码）
	vector<vector<Point>> qrBox;			//保存所有二维码整体位置框
	vector<string> qrCode;					//保存所有二维码解码结果
	for (int i = 0; i < qrPoint.size(); i++)
	{
		Point tmp = qrPoint[i][0];
		for (int m = 1; m < qrPoint[i].size(); m++)
			tmp += qrPoint[i][m];
		tmp = tmp / (int)qrPoint[i].size();
		qrCenter.push_back(tmp);
	}
	for (int i = 0; i < qrPoint.size(); i++) {
		if (state[i] == 1) continue;
		for (int j = 0; j < qrPoint.size(); j++) {
			if (j == i || state[j] == 1) continue;
			for (int k = 0; k < qrPoint.size(); k++) {
				if (k == j || k == i || state[k] == 1)continue;
				float Dij, Dik, Djk;	//根据三个定位角构成等腰直角三角形性质，判断哪几个定位角对应一个二维码
				Dij = (qrCenter[i].x - qrCenter[j].x)*(qrCenter[i].x - qrCenter[j].x) + (qrCenter[i].y - qrCenter[j].y)*(qrCenter[i].y - qrCenter[j].y);
				Dik = (qrCenter[i].x - qrCenter[k].x)*(qrCenter[i].x - qrCenter[k].x) + (qrCenter[i].y - qrCenter[k].y)*(qrCenter[i].y - qrCenter[k].y);
				Djk = (qrCenter[k].x - qrCenter[j].x)*(qrCenter[k].x - qrCenter[j].x) + (qrCenter[k].y - qrCenter[j].y)*(qrCenter[k].y - qrCenter[j].y);
				float ratio = Dij / Dik;
				float ratio1 = (Dij + Dik) / Djk;
				if (ratio > 0.6 && ratio<1.6 && ratio1>0.85 && ratio1 < 1.15) {
					state[i] = 1;
					state[j] = 1;
					state[k] = 1;
					vector<Point> contour;
					contour.insert(contour.end(), qrPoint[i].begin(), qrPoint[i].end());
					contour.insert(contour.end(), qrPoint[j].begin(), qrPoint[j].end());
					contour.insert(contour.end(), qrPoint[k].begin(), qrPoint[k].end());
					RotatedRect rotatedRect = minAreaRect(contour);
					Point2f points[4];
					rotatedRect.points(points);
					vector<Point> box;
					for (int m = 0; m < 4; m++)
						box.push_back(points[m]);
					qrBox.push_back(box);		//二维码定位框
					Mat img_tmp;
					string qrcode_tmp;
					img_tmp = CropImage(src_gray, rotatedRect);
					RecogQr(img_tmp, qrcode_tmp);
					qrCode.push_back(qrcode_tmp);
					cout << "QR code: " << qrcode_tmp << endl;	//二维码解码字符串
				}
			}
		}
	}
	drawContours(srcImg, qrBox, -1, Scalar(0, 0, 255), 2);
	imwrite("QRimage.png", srcImg);
	namedWindow("QRimage", 0);
	cvResizeWindow("QRimage", COLS,ROWS);
	imshow("QRimage", srcImg);

}


int main(int argc, char *argv[])
{
	Mat image;
	vector<vector<Point>> qrPoint;

	image = imread("im_test/raw/14.jpg", 1);

	int width = image.cols;
	int height = image.rows;
	cout << width << " X " << height << endl;
	namedWindow("原图像", 0);
	cvResizeWindow("原图像", COLS, ROWS);
	imshow("原图像", image);

	FindQrPoint(image, qrPoint);

	waitKey();

	return 0;
}
