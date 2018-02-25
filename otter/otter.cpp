#include "opencv2/imgproc.hpp"
#include "opencv2/highgui.hpp"
#include <math.h>
#include <iostream>

using namespace cv;
using namespace std;

//g++ otter.cpp -o otter `pkg-config --cflags --libs opencv`

const int w = 11/2.0*110;
const int h = 8.5*110;
int levels = 3;

Mat src; Mat src_gray; Mat img; Mat canny_output;
vector<vector<Point> > contours;
vector<Vec4i> hierarchy;
int thresh = 100;
RNG rng(12345);


int main( int argc, char** argv)
{
    src = imread("otter.jpg", 1);
    int height = src.size().height;
    int width = src.size().width;

    cvtColor( src, src_gray, CV_BGR2GRAY );
    //Extract the contours so that

    Canny( src_gray, canny_output, thresh*0.4, thresh*2, 3);
    findContours( canny_output, contours, hierarchy, RETR_TREE, CHAIN_APPROX_SIMPLE);

    Mat dst = Mat::zeros(height, width, CV_8UC3);
    dst = Scalar(255,255,255);
    for(size_t i = 0; i < contours.size(); i++) {
        drawContours(dst, contours, i, Scalar(0,0,0), 2, 8, hierarchy, 0, Point());
    }

    Mat img(height, width*2, CV_8UC3);
    Mat left(img, Rect(0 ,0, width, height));
    src.copyTo(left);
    Mat right(img, Rect(width ,0, width, height));
    dst.copyTo(right);
    namedWindow( "image", 1 );
    imshow( "image", img );

    imwrite("otter_out.jpg", dst);

    waitKey();

    return 0;
}
