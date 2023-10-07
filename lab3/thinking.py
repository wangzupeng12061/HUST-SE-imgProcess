import cv2
import numpy as np

# 全局变量
points_selected = []
window_name = "Select 4 points on the image"

def select_point(event, x, y, flags, param):
    global points_selected, window_name

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        points_selected.append([x, y])

        # 当选择了4个点时进行仿射变换
        if len(points_selected) == 4:
            warp_image()
            cv2.destroyAllWindows()

def warp_image():
    global points_selected

    # 定义目标矩形区域的四个点
    width = 300
    height = 200
    dst = np.array([
        [0, 0],
        [width-1, 0],
        [width-1, height-1],
        [0, height-1],
    ], dtype="float32")

    # 仿射变换
    M = cv2.getPerspectiveTransform(np.array(points_selected, dtype="float32"), dst)
    warped = cv2.warpPerspective(img, M, (width, height))

    cv2.imshow("Warped Image", warped)
    cv2.waitKey(0)

# 读取图像
img = cv2.imread("oooo.png")

cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, select_point)

cv2.imshow(window_name, img)
cv2.waitKey(0)
