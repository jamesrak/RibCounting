#include <iostream>
#include "opencv2/opencv.hpp"

using namespace std;
using namespace cv;
Mat vertebrae,output, output2, gray;
Mat detected_edges;
int lowThreshold;
int const max_lowThreshold = 100;
char* window_name = "Ribs Counting";

void CannyThreshold(int, void*)
{
  int ratio = 3;
  int kernel_size = 3;
  // Reduce noise with a kernel 3x3
  blur( output, detected_edges, Size(3,3) );

  // Canny detector
  Canny( detected_edges, detected_edges, lowThreshold, lowThreshold*ratio, kernel_size );

  // Using Canny's output as a mask, we display our result
    //output = Scalar::all(0);

  //src.copyTo( output, detected_edges);
  imshow("Ribs Counting",detected_edges);
 }

int main()
{
    Mat inputImage = imread("../data/sample_image/sample_rib2.jpg");
    if(inputImage.data == NULL){
        cout << "Cannot Read Image File!!!"<<endl;
        exit (-1);
    }
/*
    threshold(inputImage,output,threshold_value, max_BINARY_value,threshold_type);
    Canny(output,output,lowThreshold,lowThreshold*3);
*/

///Thoracic vertebrae detection
int vert_threshold_value = 100;
int vert_max_BINARY_value = 255;
int vert_threshold_type = 1;

    threshold(inputImage,vertebrae,vert_threshold_value, vert_max_BINARY_value, vert_threshold_type);

///Draw Lines of each rib
int threshold_value = 180;
int max_BINARY_value = 255;
int threshold_type = 1;
    //Canny(inputImage,output,lowThreshold,lowThreshold*4);
    threshold(inputImage,output,threshold_val=ue, max_BINARY_value,threshold_type);
    morphologyEx(output, output, MORPH_CLOSE, InputArray kernel)
/*
    namedWindow( window_name, CV_WINDOW_AUTOSIZE );
    createTrackbar( "Min Threshold:", window_name, &lowThreshold, max_lowThreshold, CannyThreshold );
    CannyThreshold(0, 0);
*/


    //Canny(output,output,lowThreshold,lowThreshold*3);
/*
    //HoughLines
    //Canny(inputImage, output, 50, 200, 3);
    vector<Vec2f> lines;
    HoughLines(output,lines,1,CV_PI/180,180);
    cvtColor(output,output,COLOR_GRAY2BGR);
    for(int i=0;i<lines.size();i++){
        float rho = lines[i][0];
        float theta = lines[i][1];
        double a = cos(theta), b = sin(theta);
        double x0 = a*rho, y0 = b*rho;
        Point pt1(cvRound(x0 + 1000*(-b)),
                  cvRound(y0 + 1000*(a)));
        Point pt2(cvRound(x0 - 1000*(-b)),
                  cvRound(y0 - 1000*(a)));
        line( output, pt1 , pt2, Scalar(0,0,255),3,8 );
    }
*/
    imshow("Thoracic Vertebrae",vertebrae);
    imshow("Output",output);
    //imshow("Hough Circles",output2);
    waitKey(0);
}
