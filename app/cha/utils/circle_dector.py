# -*- coding:utf8 -*-
import cv2
import numpy as np


class CircleDetector(object):
    def __init__(self, img):
        self.img = img

    def blur(self):
        # 双边滤波函数, 能在保持边界清晰的情况下有效的去除噪音，但比较慢
        blur = cv2.bilateralFilter(self.img, 100, 150, 150)

        # kernel_size = (7, 7)
        # sigma = 0
        # gaussian_blur = cv2.GaussianBlur(gray, kernel_size, sigma)

        # median_blur = cv2.medianBlur(gray, 9)
        # cv2.imwrite("median_blur.png", median_blur)

        return blur

    def edge_blur(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        # 1.先用sobel求边缘
        gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
        soble_img = cv2.subtract(gradX, gradY)
        soble_img = cv2.convertScaleAbs(soble_img)

        # 2.对模糊图像二值化。梯度图像中不大于90的任何像素都设置为0（黑色）。 否则，像素设置为255（白色）
        blurred_img = cv2.blur(soble_img, (9, 9))
        # blurred_img = cv2.bilateralFilter(soble_img, 100, 150, 150)
        _, thresh_img = cv2.threshold(blurred_img, 90, 255, cv2.THRESH_BINARY)
        # return thresh_img

        # 3.有很多黑色的空余，要用白色填充这些空余，使得后面的程序更容易识别昆虫区域，这需要做一些形态学方面的操作。
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        closed_img = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, kernel)

        # 4.还有一些小的白色斑点，这会干扰之后的昆虫轮廓的检测，要把它们去掉。分别执行4次形态学腐蚀与膨胀
        closed_img = cv2.erode(closed_img, None, iterations=4)
        closed_img = cv2.dilate(closed_img, None, iterations=4)

        return closed_img, thresh_img, soble_img

    def detect_by_hough(self, image):
        # blur = self.blur()
        # gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        height, weight = self.img.shape[0:2]

        # blur = cv2.bilateralFilter(img, 30, 150, 150)

        inscribe_radius = min(height, weight)

        accumulator_threshold = 100
        circles = []
        while len(circles) is 0:
            circles = cv2.HoughCircles(image,
                                       method=cv2.HOUGH_GRADIENT,
                                       dp=1,
                                       minDist=inscribe_radius / 2,  # 原点间隔
                                       param1=200,  # canny edge
                                       param2=accumulator_threshold,  # detection step
                                       minRadius=inscribe_radius / 3,
                                       maxRadius=inscribe_radius / 2)

            # print("circles:{}, accumulator_threshold:{} ".format(len(circles[0, :]), accumulator_threshold))

            if circles is None:
                circles = []
                accumulator_threshold = accumulator_threshold - 5
            elif len(circles[0, :]) > 2:
                circles = []
                accumulator_threshold = accumulator_threshold + 5

        return np.uint16(np.around(circles)), image

    def show(self):
        blur_img, thresh_img, _ = self.edge_blur()
        circles, _ = self.detect_by_hough(blur_img)
        for circle in circles[0, :]:
            cv2.circle(self.img, (circle[0], circle[1]), circle[2], (255, 255, 0), 5)

        cv2.imshow("blur_img", blur_img)
        cv2.imshow("circles", self.img)
        cv2.waitKey(0)

    def cut(self):
        blur_img, thresh_img, _ = self.edge_blur()
        circles, _ = self.detect_by_hough(blur_img)
        for circle in circles[0, :]:
            # cropImg_1 = self.img[circle[0] - circle[2]:circle[0] + circle[2],
            #             circle[1] - circle[2]:circle[1] + circle[2]]
            cropImg_2 = self.img[circle[1] - circle[2]:circle[1] + circle[2],
                        circle[0] - circle[2]:circle[0] + circle[2]]

            # cv2.circle(self.img, (circle[0], circle[1]), circle[2], (255, 0, 0), 5)

            # cv2.imwrite("cropImg_1.png", cropImg_1)
            # cv2.imwrite("cropImg_2.png", cropImg_2)

            return cropImg_2

        # cv2.imshow("circles", self.img)
        # cv2.waitKey(0)


if __name__ == '__main__':
    for i in range(1, 7):
        jpg = '/Users/philip.du/Documents/Projects/research/soucha/app/cha/sample/v1/' + str(i) + 'a.JPG'
        print(jpg)
        img = cv2.imread(jpg)
        cropImg = CircleDetector(img).cut()
        cv2.imwrite(jpg + "_inscribe_circle.png", cropImg)
