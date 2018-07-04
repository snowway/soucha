# coding=utf-8

import cv2

import cha.utils.feature_extract as ife


def orb_img(img, features_count):
    orb = cv2.ORB_create(features_count)
    orb_key_points, orb_desc = orb.detectAndCompute(img, None)
    orb_signed_img = cv2.drawKeypoints(img, orb_key_points, None)

    return orb_key_points, orb_desc, orb_signed_img


def sift_img(img):
    sift = cv2.xfeatures2d.SIFT_create()
    # sift = cv2.SIFT()
    sift_key_points, sift_desc = sift.detectAndCompute(img, None)
    sift_signed_img = cv2.drawKeypoints(img, sift_key_points, None)

    return sift_key_points, sift_desc, sift_signed_img


def surf_img(img):
    surf = cv2.xfeatures2d.SURF_create()
    surf_key_points, surf_desc = surf.detectAndCompute(img, None)
    surf_signed_img = cv2.drawKeypoints(img, surf_key_points, None)

    return surf_key_points, surf_desc, surf_signed_img


if __name__ == '__main__':
    # jpg = "/Users/philip.du/Documents/Projects/research/tea-recognition/sample_1/1a.JPG"
    # jpg = "/Users/philip.du/Downloads/image1.JPG"
    jpg = "/Users/philip.du/Documents/Projects/research/soucha/app/cha/sample/v1/1a.JPG"

    ## ----  orb --- ##

    gray_img = ife.get_gray_img(jpg)
    key_points, desc, signed_img = orb_img(cv2.resize(gray_img, (128, 128)), 200)
    print("gray# kps: {}, descriptors: {}".format(len(key_points), desc.shape))
    cv2.imwrite("gray_img.orb.signed.jpg", signed_img)

    sobel_img = ife.get_sobel_img(jpg)
    key_points, desc, signed_img = orb_img(cv2.resize(sobel_img, (128, 128)), 200)
    print("sobel# kps: {}, descriptors: {}".format(len(key_points), desc.shape))
    cv2.imwrite("sobel_img.orb.signed.jpg", signed_img)

    canny_img = ife.get_canny_img(jpg)
    key_points, desc, signed_img = orb_img(cv2.resize(canny_img, (128, 128)), 200)
    print("canny# kps: {}, descriptors: {}".format(len(key_points), desc.shape))
    cv2.imwrite("canny_img.orb.signed.jpg", signed_img)

    ## ----  sift --- ##

    gray_img = ife.get_gray_img(jpg)
    key_points, desc, signed_img = sift_img(cv2.resize(gray_img, (128, 128)))
    print("gray# kps: {}, descriptors: {}".format(len(key_points), desc.shape))
    cv2.imwrite("gray_img.signed.jpg", signed_img)

    sobel_img = ife.get_sobel_img(jpg)
    key_points, desc, signed_img = sift_img(cv2.resize(sobel_img, (128, 128)))
    print("sobel# kps: {}, descriptors: {}".format(len(key_points), desc.shape))
    cv2.imwrite("sobel_img.signed.jpg", signed_img)

    canny_img = ife.get_canny_img(jpg)
    key_points, desc, signed_img = sift_img(cv2.resize(canny_img, (128, 128)))
    print("canny# kps: {}, descriptors: {}".format(len(key_points), desc.shape))
    cv2.imwrite("canny_img.signed.jpg", signed_img)

    ## ----  surf --- ##

    gray_img = ife.get_gray_img(jpg)
    key_points, desc, signed_img = surf_img(cv2.resize(gray_img, (128, 128)))
    print("gray# kps: {}, descriptors: {}".format(len(key_points), desc.shape))
    cv2.imwrite("gray_img.surf.signed.jpg", signed_img)

    sobel_img = ife.get_sobel_img(jpg)
    key_points, desc, signed_img = surf_img(cv2.resize(sobel_img, (128, 128)))
    print("sobel# kps: {}, descriptors: {}".format(len(key_points), desc.shape))
    cv2.imwrite("sobel_img.surf.signed.jpg", signed_img)

    canny_img = ife.get_canny_img(jpg)
    key_points, desc, signed_img = surf_img(cv2.resize(canny_img, (128, 128)))
    print("canny# kps: {}, descriptors: {}".format(len(key_points), desc.shape))
    cv2.imwrite("canny_img.surf.signed.jpg", signed_img)
