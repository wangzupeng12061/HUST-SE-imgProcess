import cv2
import numpy as np

def rgb_to_hsi(rgb_image):
    # 将图像从0-255范围转换到0-1范围
    rgb_image = rgb_image.astype(float) / 255

    r, g, b = rgb_image[:, :, 0], rgb_image[:, :, 1], rgb_image[:, :, 2]

    numerator = 0.5 * ((r - g) + (r - b))
    denominator = np.sqrt((r - g) ** 2 + (r - b) * (g - b))
    theta = np.arccos(numerator / (denominator + 1e-6))
    h = np.where(b > g, 2 * np.pi - theta, theta)

    min_channel = np.min(rgb_image, axis=2)
    sum_channel = np.sum(rgb_image, axis=2)
    s = 1 - (3 * min_channel / (sum_channel + 1e-6))
    s[sum_channel == 0] = 0  # 当亮度为0时，饱和度为0

    i = sum_channel / 3.0

    return np.stack([h, s, i], axis=2)

def hsi_to_rgb(hsi_image):
    h, s, i = hsi_image[:, :, 0], hsi_image[:, :, 1], hsi_image[:, :, 2]

    r = np.zeros(h.shape)
    g = np.zeros(h.shape)
    b = np.zeros(h.shape)

    # 分三种情况处理
    cond1 = h < 2 * np.pi / 3
    b[cond1] = i[cond1] * (1 - s[cond1])
    r[cond1] = i[cond1] * (1 + s[cond1] * np.cos(h[cond1]) / np.cos(np.pi / 3 - h[cond1]))
    g[cond1] = 3 * i[cond1] - (r[cond1] + b[cond1])

    cond2 = (h >= 2 * np.pi / 3) & (h < 4 * np.pi / 3)
    h[cond2] = h[cond2] - 2 * np.pi / 3
    r[cond2] = i[cond2] * (1 - s[cond2])
    g[cond2] = i[cond2] * (1 + s[cond2] * np.cos(h[cond2]) / np.cos(np.pi / 3 - h[cond2]))
    b[cond2] = 3 * i[cond2] - (r[cond2] + g[cond2])

    cond3 = h >= 4 * np.pi / 3
    h[cond3] = h[cond3] - 4 * np.pi / 3
    g[cond3] = i[cond3] * (1 - s[cond3])
    b[cond3] = i[cond3] * (1 + s[cond3] * np.cos(h[cond3]) / np.cos(np.pi / 3 - h[cond3]))
    r[cond3] = 3 * i[cond3] - (g[cond3] + b[cond3])

    return np.stack([r, g, b], axis=2) * 255

# 读取图像
image = cv2.imread("Fig6.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# RGB -> HSI
hsi_image = rgb_to_hsi(image)

# 对亮度分量I进行直方图均衡化
hsi_image[:, :, 2] = cv2.equalizeHist((hsi_image[:, :, 2] * 255).astype(np.uint8)) / 255.0

# HSI -> RGB
result_image = hsi_to_rgb(hsi_image).astype(np.uint8)
result_image_bgr = cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)

# 显示原始图像和处理后的图像
cv2.imshow("Original", image)
cv2.imshow("Equalized in HSI", result_image_bgr)

cv2.waitKey(0)  # 等待用户按键
cv2.destroyAllWindows()  # 关闭所有窗口