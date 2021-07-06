from scipy import ndimage
import cv2
import numpy as np


def rotate_image(image_arr=None, angle=35):
    # rotation angle in degree
    image_to_rotate = cv2.imread("/home/vuong/Downloads/The_HDV_moi/QT-Moi-1.jpg")
    # image_to_rotate = image_arr
    rotated = ndimage.rotate(image_to_rotate, angle)
    # cv2.imwrite("../image/rotate.jpg", rotated)
    while True:
        cv2.imshow("image", rotated)
        key = cv2.waitKey(10) & 0xFF
        if key == ord("q"):
            break


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


if __name__ == '__main__':
    rotate_image()