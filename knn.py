"""
KNN 特征匹配
用 KNN 算法匹配两张图的特征点
"""
import cv2
import numpy as np


def knn_match(des1, des2, ratio=0.75):
    """
    KNN 特征匹配
    
    参数：
        des1: 第一张图的描述子
        des2: 第二张图的描述子
        ratio: 比值测试阈值
    
    返回：
        good_matches: 好的匹配点对
    """
    # 1. 创建 BFMatcher
    bf = cv2.BFMatcher()
    
    # 2. KNN 匹配（每个点找 2 个最近邻）
    matches = bf.knnMatch(des1, des2, k=2)
    
    # 3. 比值测试
    good_matches = []
    for m, n in matches:
        if m.distance < ratio * n.distance:
            good_matches.append(m)
    
    return good_matches


if __name__ == "__main__":
    # 测试
    img1 = cv2.imread("data/img1.jpg")
    img2 = cv2.imread("data/img2.jpg")
    
    if img1 is None or img2 is None:
        print("❌ 找不到图片，请把 img1.jpg 和 img2.jpg 放到 data/ 目录")
        exit()
    
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    
    matches = knn_match(des1, des2)
    print(f"✅ 匹配到 {len(matches)} 对点")