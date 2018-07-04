# coding=utf-8
import os
import numpy
import imagehash
import PIL.Image as Image


def calculate_distance(source, target, distance_calculator="hamming"):
    from scipy.spatial import distance
    if distance_calculator is "hamming":
        return distance.hamming(source, target)
    elif distance_calculator is "euclidean":
        # return numpy.linalg.norm(a - b)
        return distance.euclidean(source, target)
    elif distance_calculator is "cosine":
        return distance.cosine(source, target)
    else:
        return 0


class ComparableImage(object):
    def __init__(self, img_path):
        self.img = Image.open(img_path)

    def distance(self, to_img, hash_algorithm="perceptual", distance_calculator="hamming"):
        from_hash_code = self.hash_code(hash_algorithm)
        to_hash_code = to_img.hash_code(hash_algorithm)

        rows = from_hash_code.shape[0]
        result = []

        for i in range(0, rows):
            result.append((calculate_distance(from_hash_code[i, :], to_hash_code[i, :], distance_calculator)))

        return result

    def hash_code(self, hash_algorithm="perceptual"):
        height = self.img.height
        width = self.img.width

        # 平均哈希，对于二位矩阵每个对应值, 如果该像素是大于或等于平均值输出1，否则为0
        if hash_algorithm is "average":
            hash_size = min(height, width, 64)
            return imagehash.average_hash(self.img, hash_size).hash.astype(int)

        # 感知哈希, 二位dct变换后取低频部分, 对应二维矩阵取值大于或等于中位值为1，否则为0
        elif hash_algorithm is "perceptual":
            hash_size = int(min(height, width, 64) / 4)
            return imagehash.phash(self.img, hash_size, 4).hash.astype(int)

        # 梯度哈希，计算每个像素的差值，并与平均差异的差异进行比较。
        elif hash_algorithm is "difference":
            hash_size = min(height, width, 64)
            return imagehash.dhash(self.img, hash_size).hash.astype(int)

        # 小波Hash, 离散小波变换（DWT) , 变换后低频部分类似于原始信号。
        elif hash_algorithm is "wavelet":
            hash_size = min(height, width, 64)
            return imagehash.whash(self.img, hash_size).hash.astype(int)


if __name__ == '__main__':
    root = os.getcwd().replace("/app/cha/utils", "")
    print("####", root)

    sample_root = root + "/app/cha/sample/v2/"
    origin_img = ComparableImage(root + "/app/cha/sample/v2/001_1.jpg.sobel.png")

    files = os.listdir(sample_root)

    distance_list_1 = []
    distance_list_2 = []
    distance_list_3 = []
    distance_list_4 = []

    for file in files:
        name, ext = os.path.splitext(file)
        print(name, ext)
        if not os.path.isdir(file) and (ext == ".png"):
            target_img = ComparableImage(sample_root + file)
            distance = origin_img.distance(target_img, hash_algorithm="average", distance_calculator="hamming")

            # print(file,
            #       numpy.asarray(distance).sum(),
            #       numpy.var(distance, ddof=1),
            #       numpy.asarray(distance).mean(),
            #       numpy.median(distance))

            distance_list_1.append((numpy.asarray(distance).sum(), file))
            distance_list_2.append((numpy.var(distance, ddof=1), file))
            distance_list_3.append((numpy.asarray(distance).mean(), file))
            distance_list_4.append((numpy.median(distance), file))

    print(sorted(distance_list_1))
    print(sorted(distance_list_2))
    print(sorted(distance_list_3))
    print(sorted(distance_list_4))
