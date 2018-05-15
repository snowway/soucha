# -*- coding:utf8 -*-

import sys, glob, os, cv2, numpy
from PIL import Image
from compiler import ast

FILE_TYPES = ('jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG')


# PHASH算法
def phash(imgfile):
    """
    cv2.imread
    flags>0时表示以彩色方式读入图片
    flags=0时表示以灰度图方式读入图片
    flags<0时表示以图片的本来的格式读入图片

    interpolation - 插值方法。共有5种：
    １）INTER_NEAREST - 最近邻插值法
    ２）INTER_LINEAR - 双线性插值法（默认）
    ３）INTER_AREA - 基于局部像素的重采样（resampling using pixel area relation）。
        对于图像抽取（image decimation）来说，这可能是一个更好的方法。但如果是放大图像时，它和最近邻法的效果类似。
    ４）INTER_CUBIC - 基于4x4像素邻域的3次插值法
    ５）INTER_LANCZOS4 - 基于8x8像素邻域的Lanczos插值
    """
    # 加载并调整图片为32x32灰度图片
    img = cv2.imread(imgfile, 0)
    img = cv2.resize(img, (64, 64), interpolation=cv2.INTER_CUBIC)

    # 创建二维列表
    h, w = img.shape[:2]
    vis0 = numpy.zeros((h, w), numpy.float32)
    vis0[:h, :w] = img  # 填充数据

    # 二维Dct变换
    vis1 = cv2.dct(cv2.dct(vis0))
    # cv.SaveImage('a.jpg',cv.fromarray(vis0)) #保存图片
    vis1.resize(32, 32)

    # 把二维list变成一维list
    img_list = ast.flatten(vis1.tolist())

    # 计算均值
    avg = sum(img_list) * 1. / len(img_list)
    # 自然排序, 可以忽略图片的旋转
    data = sorted(map(lambda i: 0 if i < avg else 1, img_list), lambda x, y: x - y)
    # avg_list = [0 if i < avg else 1 for i in img_list]
    return reduce(lambda x, (y, z): x | (z << y), enumerate(data), 0)


# 均值hash算法
def avhash(im):
    # 如果参数已经是Image直接返回, 否则通过Image.open打开
    im = isinstance(im, Image.Image) and im or Image.open(im)
    # 将图片缩小到16x16的尺寸，总共256个像素。这一步的作用是去除图片的细节，只保留结构、明暗等基本信息，摒弃不同尺寸、比例带来的图片差异。
    # 将缩小后的图片，转为256级灰度。也就是说，所有像素点总共只有256种颜色。
    im = im.resize((32, 32), Image.ANTIALIAS).convert('L')
    # 计算灰度平均值
    avg = reduce(lambda x, y: x + y, im.getdata()) / 1024.0
    # 将每个像素的灰度，与平均值进行比较。大于或等于平均值，记为1;小于平均值，记为0
    # 按照自然排序, 保证即使图片旋转, 也能获取类似的hash
    data = sorted(map(lambda i: 0 if i < avg else 1, im.getdata()), lambda x, y: x - y)
    return reduce(lambda x, (y, z): x | (z << y), enumerate(data), 0)


# 计算两个long的汉明距离
def hamming(h1, h2):
    h, d = 0, h1 ^ h2
    while d:
        h += 1
        d &= d - 1
    return h


if __name__ == '__main__':
    if len(sys.argv) <= 1 or len(sys.argv) > 3:
        print "Usage: %s image.jpg [dir]" % sys.argv[0]
    else:
        im, wd = sys.argv[1], '.' if len(sys.argv) < 3 else sys.argv[2]
        # h = avhash(im)
        h = phash(im)

        os.chdir(wd)
        images = []
        for ext in FILE_TYPES:
            images.extend(glob.glob('*.%s' % ext))

        seq = []
        prog = int(len(images) > 50 and sys.stdout.isatty())
        for f in images:
            # seq.append((f, hamming(avhash(f), h)))
            seq.append((f, hamming(phash(f), h)))
            if prog:
                perc = 100. * prog / len(images)
                x = int(2 * perc / 5)
                print '\rCalculating... [' + '#' * x + ' ' * (40 - x) + ']',
                print '%.2f%%' % perc, '(%d/%d)' % (prog, len(images)),
                sys.stdout.flush()
                prog += 1

        if prog: print
        for f, ham in sorted(seq, key=lambda i: i[1]):
            print "%d\t%s" % (ham, f)
