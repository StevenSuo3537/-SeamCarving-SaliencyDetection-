# This Python file uses the following encoding: utf-8
# 该文件是主要算法

# if__name__ == "__main__":
#     pass
import sys
import cv2

from tqdm import trange
import numpy as np

def calc_energy(img):
    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
    (success, saliencyMap) = saliency.computeSaliency(img)
    saliencyMap = (saliencyMap * 255).astype("uint8")
    #cv2.imshow("Image", img)
    #cv2.imshow("Output", saliencyMap)
    #cv2.waitKey(0)

    return saliencyMap

#按列裁剪
def crop_c(img, scale_c):
    r, c, _ = img.shape
    new_c = int(scale_c * c)
    if scale_c <= 1:
        for i in trange(c - new_c):
            img = carve_column(img)
    else:

        img = cv2.resize(img, (c+2*(new_c-c) , r), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite("img.jpg",img)
        for i in trange(new_c-c):
            img = carve_column(img)

    return img
#按行裁剪
def crop_r(img, scale_r):
    img = np.rot90(img, 1, (0, 1))
    img = crop_c(img, scale_r)
    img = np.rot90(img, 3, (0, 1))
    return img

def carve_column(img):
    r, c, _ = img.shape

    M, backtrack = minimum_seam(img)
    mask = np.ones((r, c), dtype=np.bool)

    j = np.argmin(M[-1])
    for i in reversed(range(r)):
        mask[i, j] = False
        j = backtrack[i, j]

    mask = np.stack([mask] * 3, axis=2)
    img = img[mask].reshape((r, c - 1, 3))
    return img

def minimum_seam(img):
    r, c, _ = img.shape
    energy_map = calc_energy(img)
    M = energy_map
    backtrack = np.zeros_like(M, dtype=np.int)

    for i in range(1, r):
        for j in range(0, c):
            # 处理图像的左侧边缘，确保不会索引-1
            if j == 0:
                idx = np.argmin(M[i-1, j:j + 2])
                backtrack[i, j] = idx + j
                min_energy = M[i-1, idx + j]
            else:
                idx = np.argmin(M[i - 1, j - 1:j + 2])
                backtrack[i, j] = idx + j - 1
                min_energy = M[i - 1, idx + j - 1]

            M[i, j] += min_energy

    return M, backtrack

