import cv2

# 读取图像
image = cv2.imread("Fig6.png")

if image is None:
    print("Error loading image. Check the file path and image integrity.")
    exit()

# 对每个B, G, R通道分别进行均衡化
b, g, r = cv2.split(image)
b_eq = cv2.equalizeHist(b)
g_eq = cv2.equalizeHist(g)
r_eq = cv2.equalizeHist(r)

# 合并均衡化后的通道
equalized_image = cv2.merge([b_eq, g_eq, r_eq])

# 显示原始图像和处理后的图像
cv2.imshow("Original", image)
cv2.imshow("Equalized in BGR", equalized_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
