# coding=utf-8

import cv2
import os
import cha.utils.feature_extract as fe

if __name__ == '__main__':
    sample_root = os.getcwd()

    files = os.listdir(sample_root)

    distance_list = []
    for file in files:
        if not os.path.isdir(file):
            img_path = sample_root + "/" + file
            print(img_path)
            cv2.imwrite( sample_root + "/" + file + ".gray.png", fe.get_gray_img(img_path))
            cv2.imwrite(sample_root + "/" + file + ".sobel.png", fe.get_sobel_img(img_path))
            cv2.imwrite(sample_root + "/" + file + ".fast_fourier.png", fe.get_fast_fourier_img(img_path))
            cv2.imwrite(sample_root + "/" + file + ".laplacian.png", fe.get_laplacian_img(img_path))
            cv2.imwrite(sample_root + "/" + file + ".canny.png", fe.get_canny_img(img_path))
