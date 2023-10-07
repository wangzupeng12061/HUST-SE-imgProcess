import cv2

def resize_to_match(reference, target):
    '''将目标图像调整为与参考图像相同的尺寸'''
    return cv2.resize(target, (reference.shape[1], reference.shape[0]), interpolation=cv2.INTER_LINEAR)

# 读取两个图像
img1 = cv2.imread('flower2.jpg')
img2 = cv2.imread('flowerx.png')

# 检查两个图像的尺寸是否相同
if img1.shape != img2.shape:
    if img1.size > img2.size:
        img2 = resize_to_match(img1, img2)
    else:
        img1 = resize_to_match(img2, img1)

# 计算两个图像之间的差异
result = cv2.subtract(img1, img2)

# 显示结果
cv2.imshow('Difference', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
