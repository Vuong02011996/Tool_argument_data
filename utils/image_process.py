from scipy import ndimage
import cv2
import numpy as np
from matplotlib import pyplot as plt


def rotate_image(image_arr=None, angle=35):
    # rotation angle in degree
    # image_to_rotate = cv2.imread("/home/vuong/Downloads/The_HDV_moi/QT-Moi-1.jpg")
    image_to_rotate = image_arr
    rotated = ndimage.rotate(image_to_rotate, angle)
    # cv2.imwrite("../image/rotate.jpg", rotated)
    # plt.imshow(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB), interpolation='nearest')
    # plt.show()
    return rotated
    # while True:
    #     cv2.imshow("image", rotated)
    #     key = cv2.waitKey(10) & 0xFF
    #     if key == ord("q"):
    #         break


def find_angle_from_three_point(a, b, c):
    """
    https://manivannan-ai.medium.com/find-the-angle-between-three-points-from-2d-using-python-348c513e2cd
    :param a: [x, y]
    :param b: [x, y]
    :param c: [x, y]
    :return:
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    if c[1] < a[1]:
        return -np.degrees(angle)
    else:
        return np.degrees(angle)


def find_three_point(bbox1, bbox2):
    """

    :param bbox1: [x1, y1, x2, y2]
    :param bbox2: [x1, y1, x1, y2]
    :return:
    """
    x_center = bbox1[0] + int((bbox1[2] - bbox1[0]) / 2)
    y_center = bbox1[1] + int((bbox1[3] - bbox1[1]) / 2)

    b = [x_center, y_center]
    a = [bbox1[0], bbox1[1] + int((bbox1[3] - bbox1[1]) / 2)]
    xc = bbox2[0] + int((bbox2[2] - bbox2[0]) / 2)
    c = [xc, bbox2[1] + int((bbox2[3] - bbox2[1]) / 2)]
    return a, b, c


def test_draw_polygon_image():
    # path
    path = "../image/rotate.jpg"

    # Reading an image in default
    # mode
    image = cv2.imread(path)

    # Polygon corner points coordinates
    pts = np.array([[25, 70], [25, 145],
                    [75, 190], [150, 190],
                    [200, 145], [200, 70],
                    [150, 25], [75, 25]],
                   np.int32)

    pts = pts.reshape((-1, 1, 2))

    isClosed = True

    # Green color in BGR
    color = (0, 255, 0)

    # Line thickness of 8 px
    thickness = 8

    # Using cv2.polylines() method
    # Draw a Green polygon with
    # thickness of 1 px
    image = cv2.polylines(image, [pts],
                          isClosed, color,
                          thickness=-1)
    plt.imshow(image, interpolation='nearest')
    plt.show()


if __name__ == '__main__':
    # rotate_image()
    test_draw_polygon_image()