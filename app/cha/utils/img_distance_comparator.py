# coding=utf-8

import cv2
# import imagehash
import numpy
# import scipy

import cha.utils.feature_extract as fe


class ImgHash(object):
    def __init__(self, img):
        self.img = img

    # 平均哈希，对于每个像素输出1，如果该像素是大于或等于平均值，否则为0
    def average_hash(self):
        # find average pixel value; 'pixels' is an array of the pixel values, ranging from 0 (black) to 255 (white)
        pixels = numpy.asarray(self.img)
        avg = pixels.mean()

        # create string of bits
        diff = pixels > avg
        return diff

    # 感知哈希, 融合时空域变化信息, TODO 具体原理待学习
    def perceptual_hash(self, high_freq_factor=4):
        height, weight = self.img.shape[0:2]

        import scipy.fftpack
        pixels = numpy.asarray(self.img)
        dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)
        dct_low_freq = dct[:int(height / high_freq_factor), :int(weight / high_freq_factor)]
        med = numpy.median(dct_low_freq)
        diff = dct_low_freq > med
        return diff

    # 梯度哈希，计算每个像素的差值，并与平均差异的差异进行比较。
    def difference_hash(self):
        pixels = numpy.asarray(self.img)
        # compute differences between columns
        diff = pixels[:, 1:] > pixels[:, :-1]
        return diff

    # 小波Hash, 离散小波变换（DWT) , 变换后低频部分类似于原始信号。
    def wavelet_hash(self, hash_size=8, image_scale=None, mode='haar', remove_max_haar_ll=True):
        if hash_size < 2:
            raise ValueError("Hash size must be greater than or equal to 2")

        import pywt
        if image_scale is not None:
            assert image_scale & (image_scale - 1) == 0, "image_scale is not power of 2"
        else:
            height, weight = self.img.shape[0:2]
            image_natural_scale = 2 ** int(numpy.log2(min(height, weight)))
            image_scale = max(image_natural_scale, hash_size)

        ll_max_level = int(numpy.log2(image_scale))

        level = int(numpy.log2(hash_size))
        assert self.hash_size & (hash_size - 1) == 0, "hash_size is not power of 2"
        assert level <= ll_max_level, "hash_size in a wrong range"
        dwt_level = ll_max_level - level

        image = cv2.resize(self.img, (image_scale, image_scale))
        pixels = numpy.asarray(image) / 255

        # Remove low level frequency LL(max_ll) if @remove_max_haar_ll using haar filter
        if remove_max_haar_ll:
            coeffs = pywt.wavedec2(pixels, 'haar', level=ll_max_level)
            coeffs = list(coeffs)
            coeffs[0] *= 0
            pixels = pywt.waverec2(coeffs, 'haar')

        # Use LL(K) as freq, where K is log2(@hash_size)
        coeffs = pywt.wavedec2(pixels, mode, level=dwt_level)
        dwt_low = coeffs[0]

        # Substract median and compute hash
        med = numpy.median(dwt_low)
        diff = dwt_low > med
        return diff

    def hash_code(self, hash_algorithm):
        if hash_algorithm is "average":
            return self.average_hash()
        elif hash_algorithm is "perceptual":
            return self.perceptual_hash()
        elif hash_algorithm is "difference":
            return self.difference_hash()
        elif hash_algorithm is "wavelet":
            return self.wavelet_hash()


class DistanceCalculator(object):
    # 汉明距离
    hamming = 0

    # 欧式距离
    euclidean = 1

    # 余弦距离
    cosine = 2


filters = {"gray": fe.get_gray_img,
           "sobel": fe.get_sobel_img,
           "laplacian": fe.get_laplacian_img,
           "canny": fe.get_canny_img,
           "fft": fe.get_fast_fourier_img}


class Comparator(object):

    def __init__(self, target_img, to_compared_img=[]):
        self.images_hash = {}
        self.target_img = target_img
        self.to_compared_img = to_compared_img
        self.to_compared_img.insert(0, target_img)

    def compare(self,
                # 是否需要对图片进行下采样缩小
                sub_sample=(1024, 1024),
                # 是否需要对图片进行滤波
                filter="gray",
                # 图片hash算法
                hash_algorithm="perceptual",
                # 比对算子
                distance_calculator="hamming"):
        self.convert_img(sub_sample, filter)
        self.hash_img(hash_algorithm)

        target_hash = self.images_hash[self.target_img]
        result = {}

        for index, img_path in enumerate(self.to_compared_img):
            distance = self.distance_img(distance_calculator, target_hash, self.images_hash[img_path])
            result[img_path] = distance

        return result

    def convert_img(self, sub_sample, filter):
        self.images = {}
        for index, img_path in enumerate(self.to_compared_img):
            img = cv2.resize(cv2.imread(img_path), sub_sample)
            cv2.imwrite("sub_sample.png", img)
            img = filters.get(filter)("sub_sample.png")
            self.images[img_path] = img

        return self.images

    def hash_img(self, hash_algorithm):

        for key, image in self.images.items():
            if hash_algorithm is "average":
                self.images_hash[key] = ImgHash(image).average_hash()
            elif hash_algorithm is "perceptual":
                self.images_hash[key] = ImgHash(image).perceptual_hash()
            elif hash_algorithm is "difference":
                self.images_hash[key] = ImgHash(image).difference_hash()
            elif hash_algorithm is "wavelet":
                self.images_hash[key] = ImgHash(image).wavelet_hash()

        return self.images_hash

    def distance_img(self, distance_calculator, a, b):
        print("#####", a.data)

        from scipy.spatial import distance
        if distance_calculator is "hamming":
            return distance.hamming(a.data, b.data)
        elif distance_calculator is "euclidean":
            # return numpy.linalg.norm(a - b)
            return distance.euclidean(a.data, b.data)
        elif distance_calculator is "cosine":
            return distance.cosine(a.data, b.data)
        else:
            return 0


if __name__ == '__main__':
    comparator = Comparator("/Users/philip.du/Documents/Projects/research/soucha/app/cha/sample/candidate/1a.png",
                            ["/Users/philip.du/Documents/Projects/research/soucha/app/cha/sample/v1/1a.JPG",
                             "/Users/philip.du/Documents/Projects/research/soucha/app/cha/sample/v1/2a.JPG",
                             "/Users/philip.du/Documents/Projects/research/soucha/app/cha/sample/v1/3a.JPG",
                             "/Users/philip.du/Documents/Projects/research/soucha/app/cha/sample/v1/4a.JPG",
                             "/Users/philip.du/Documents/Projects/research/soucha/app/cha/sample/v1/5a.JPG",
                             "/Users/philip.du/Documents/Projects/research/soucha/app/cha/sample/v1/6a.JPG"])

    # images_hash = comparator.compare(filter="gray", hash_algorithm="perceptual", distance_calculator="hamming")
    # print("filter:{}, hash:{}, distance:{}, result:{}".format("gray", "perceptual", "hamming", images_hash))
    # images_hash = comparator.compare(filter="sobel", hash_algorithm="perceptual", distance_calculator="hamming")
    # print("filter:{}, hash:{}, distance:{}, result:{}".format("sobel", "perceptual", "hamming", images_hash))
    # images_hash = comparator.compare(filter="canny", hash_algorithm="perceptual", distance_calculator="hamming")
    # print("filter:{}, hash:{}, distance:{}, result:{}".format("canny", "perceptual", "hamming", images_hash))
    #
    # images_hash = comparator.compare(filter="gray", hash_algorithm="difference", distance_calculator="hamming")
    # print("filter:{}, hash:{}, distance:{}, result:{}".format("gray", "difference", "hamming", images_hash))
    # images_hash = comparator.compare(filter="sobel", hash_algorithm="difference", distance_calculator="hamming")
    # print("filter:{}, hash:{}, distance:{}, result:{}".format("sobel", "difference", "hamming", images_hash))
    # images_hash = comparator.compare(filter="canny", hash_algorithm="difference", distance_calculator="hamming")
    # print("filter:{}, hash:{}, distance:{}, result:{}".format("canny", "difference", "hamming", images_hash))
    #
    # images_hash = comparator.compare(filter="gray", hash_algorithm="wavelet", distance_calculator="hamming")
    # print("filter:{}, hash:{}, distance:{}, result:{}".format("gray", "wavelet", "hamming", images_hash))
    # images_hash = comparator.compare(filter="sobel", hash_algorithm="wavelet", distance_calculator="hamming")
    # print("filter:{}, hash:{}, distance:{}, result:{}".format("sobel", "wavelet", "hamming", images_hash))
    # images_hash = comparator.compare(filter="canny", hash_algorithm="wavelet", distance_calculator="hamming")
    # print("filter:{}, hash:{}, distance:{}, result:{}".format("canny", "wavelet", "hamming", images_hash))

    # images_hash = comparator.compare(filter="gray", hash_algorithm="wavelet", distance_calculator="euclidean")
    # print("filter:{}, hash:{}, distance:{}, result:{}".format("gray", "wavelet", "euclidean", images_hash))
    # images_hash = comparator.compare(filter="sobel", hash_algorithm="wavelet", distance_calculator="euclidean")
    # print("filter:{}, hash:{}, distance:{}, result:{}".format("sobel", "wavelet", "euclidean", images_hash))
    images_hash = comparator.compare(
        filter="canny",
        hash_algorithm="perceptual",
        distance_calculator="hamming")
    print("filter:{}, hash:{}, distance:{}, result:{}".format("canny", "perceptual", "hamming", images_hash))
