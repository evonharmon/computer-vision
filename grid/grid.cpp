#include "opencv2/imgproc.hpp"
#include "opencv2/highgui.hpp"
#include <math.h>
#include <iostream>

using namespace cv;
using namespace std;

const int w = 600;
const int h = 600;
const int n = 8;

Mat draw_grid(int width, int height, int squares)
{
    Mat img = Mat::zeros(height, width, CV_8UC3);

    Point p1 = Point(0,0);
    Point p2 = Point(0,0);
    Scalar c = Scalar(0,0,0);
    int color = 0;


    for (int i = 0; i < squares; i++) {
      for (int j = 0; j < squares; j++) {
        int x1 = width/squares * i;
        int y1 = height/squares * j;
        int x2 = width/squares * (i+1);
        int y2 = height/squares * (j+1);
        cout << "i,j: " << i << " " << j;
        cout << "   x1,y1: " << x1 << ", " << y1;
        cout << "   x2,y2: " << x2 << ", " << y2;
        cout << "   color: " << color << endl;

        p1 = Point(x1,y1);
        p2 = Point(x2,y2);

        if (color%2 == 0) {
          c = Scalar(255,255,255);
        } else {
          c = Scalar(0,0,0);
        }

        rectangle(img, p1, p2, c, -1, 8);
        color++;
      }
      color++;
    }

    return img;
}

int main( int argc, char** argv)
{
    Mat img = draw_grid(w,h,n);
    //show the faces
    namedWindow( "image", 1 );
    imshow( "image", img );

    waitKey();

    return 0;
}
