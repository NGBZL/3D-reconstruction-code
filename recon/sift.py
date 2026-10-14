"""
SIFT 特征提取
用 OpenCV 的 SIFT 提取图像特征点和描述子
"""
import cv2
import numpy as np


def extract_sift(image, max_features=1000):
    """
    提取 SIFT 特征点和描述子
    
    参数：
        image: 输入图像（BGR 或灰度）
        max_features: 最多提取多少个特征点
    
    返回：
        keypoints: 特征点列表
        descriptors: 描述子矩阵 (N, 128)
    """
    # 1. 转灰度（如果不是灰度图）
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # 2. 创建 SIFT 检测器
    sift = cv2.SIFT_create(nfeatures=max_features)
    
    # 3. 检测特征点 + 计算描述子
    keypoints, descriptors = sift.detectAndCompute(gray, None)
    
    return keypoints, descriptors


def draw_keypoints(image, keypoints, output_path=None):
    """
    在图像上画出特征点
    
    参数：
        image: 输入图像
        keypoints: 特征点列表
        output_path: 输出路径（可选）
    
    返回：
        result: 画了特征点的图像
    """
    # 用 OpenCV 自带的函数画
    result = cv2.drawKeypoints(
        image,
        keypoints,
        None,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )
    
    # 保存（可选）
    if output_path:
        cv2.imwrite(output_path, result)
        print(f"✅ 已保存到 {output_path}")
    
    return result


if __name__ == "__main__":
    # 测试
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python sift.py <图片路径>")
        print("示例: python sift.py data/img1.jpg")
        sys.exit(1)
    
    # 1. 读图
    img_path = sys.argv[1]
    img = cv2.imread(img_path)
    
    if img is None:
        print(f"❌ 找不到图片: {img_path}")
        sys.exit(1)
    
    print(f"✅ 图片尺寸: {img.shape}")
    
    # 2. 提取 SIFT
    kp, des = extract_sift(img, max_features=1000)
    
    print(f"✅ 提取到 {len(kp)} 个特征点")
    print(f"✅ 描述子形状: {des.shape}")
    print(f"✅ 描述子维度: {des.shape[1]} 维")
    
    # 3. 可视化
    result = draw_keypoints(img, kp, output_path="sift_result.jpg")
    
    # 4. 显示
    cv2.imshow("SIFT Features", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()