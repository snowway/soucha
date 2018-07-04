# coding=utf-8

import cv2
import os
import cha.utils.feature_extract as fe

if __name__ == '__main__':
    sample_root = os.getcwd()

    files = os.listdir(sample_root)

    distance_list = []
    for file in files:
        if not os.path.isdir(file) and file != "transform_v2.py":
            img_path = sample_root + "/" + file

            origin_img = cv2.imread(img_path)
            cv2.imwrite(img_path + ".2048.png", cv2.resize(origin_img, (2048, 2048)))
            cv2.imwrite(img_path + ".1024.png", cv2.resize(origin_img, (1024, 1024)))
            cv2.imwrite(img_path + ".512.png", cv2.resize(origin_img, (512, 512)))

    for file in files:
        if not os.path.isdir(file) and file != "transform_v2.py":
            img_path = sample_root + "/" + file
            print(img_path)

            cv2.imwrite(sample_root + "/" + file + ".gray.png", fe.get_gray_img(img_path))
            cv2.imwrite(sample_root + "/" + file + ".sobel.png", fe.get_sobel_img(img_path))
            # cv2.imwrite(sample_root + "/" + file + ".fast_fourier.png", fe.get_fast_fourier_img(img_path))
            cv2.imwrite(sample_root + "/" + file + ".laplacian.png", fe.get_laplacian_img(img_path))
            cv2.imwrite(sample_root + "/" + file + ".canny.png", fe.get_canny_img(img_path))
