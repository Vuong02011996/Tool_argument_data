from scipy import ndimage
import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial import distance
from glob import glob


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
                          thickness=0)
    plt.imshow(image, interpolation='nearest')
    plt.show()


def create_image_from_numpy():
    alpha_img = 100 * np.ones((720, 1280, 1), np.uint8)
    # alpha_img = np.ones((1000, 1000, 3), np.uint8)
    plt.imshow(alpha_img)
    plt.show()


def draw_polygon():
    alpha_img = np.zeros((720, 1280, 1), np.uint8)
    bbox_idx = [0, (503, 466), (672, 446), (692, 507), (523, 527)]
    tu_giac = np.array([bbox_idx[1], bbox_idx[2], bbox_idx[3],
                        bbox_idx[4]], dtype=np.int32)
    # tu_giac = np.array([[[240, 130], [380, 230], [190, 280]]], np.int32)
    tu_giac = tu_giac.reshape((-1, 1, 2))
    alpha_img = cv2.fillPoly(alpha_img, [tu_giac], (255, 255, 255))
    plt.imshow(alpha_img)
    plt.show()


# Rotate image and get new bbox
def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # centre
    (h, w) = image.shape[:2]
    (cX, cY) = (w / 2, h / 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))


def rotate_box(bb, cx, cy, h, w, theta):
    new_bb = list(bb)
    for i,coord in enumerate(bb):
        # opencv calculates standard transformation matrix
        M = cv2.getRotationMatrix2D((cx, cy), theta, 1.0)
        # Grab  the rotation components of the matrix)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cx
        M[1, 2] += (nH / 2) - cy
        # Prepare the vector to be transformed
        v = [coord[0],coord[1], 1]
        # Perform the actual rotation and return the image
        calculated = np.dot(M, v)
        new_bb[i] = (calculated[0], calculated[1])
    return new_bb


def find_distance_two_point(a, b):
    return distance.euclidean(a, b)


def find_bbox_roi_from_bbox_large_image(offset, bbox_large_image):
    """
    :param offset: (x0, y0)
    :param bbox_large_image: [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    :return: new bbox : [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    """
    bbox_roi = []
    for i in range(len(bbox_large_image)):
        bbox_roi.append(np.asarray(bbox_large_image[i]) - np.asarray(offset[0]))

    # bbox_roi[0] = tuple(bbox_roi[0] + 3)
    # bbox_roi[1] = tuple([bbox_roi[1][0] - 3, bbox_roi[1][1] + 3])
    # bbox_roi[2] = tuple(bbox_roi[2] - 3)
    # bbox_roi[3] = tuple([bbox_roi[3][0] + 3, bbox_roi[3][1] - 3])

    return bbox_roi


def show_image_folder():
    list_image = glob("/home/gg-greenlab/Downloads/The_HDV/*")
    for image in list_image:
        image = cv2.imread(image)
        while True:
            cv2.imshow("image", image)
            key = cv2.waitKey(10) & 0xFF
            if key == ord("q"):
                break


def show_bbox_of_image(img, bbox):
    """

    :param img:
    :param bbox: [x1, y1, x2, y2]
    :return:
    """
    cv2.rectangle(img, (bbox[0], bbox[1]),
                  (bbox[2], bbox[3]), (255, 0, 0), 5)
    plt.imshow(img)
    plt.show()


def show_label_select():
    list_files_image = glob("/home/gg-greenlab/Downloads/DataHDV/Nguoideothe_0/*.jpg")
    list_files_label = glob("/home/gg-greenlab/Downloads/DataHDV/Nguoideothe_0/*.txt")
    list_files_image.sort()
    list_files_label.sort()
    for i in range(len(list_files_image)):
        image_file = list_files_image[i]
        label_file = list_files_label[i]
        img = cv2.imread(image_file)
        (H, W) = img.shape[:2]
        print('label_file', label_file)
        with open(label_file) as fr:
            lines = fr.readlines()
            print(lines)
            print(len(lines))
            for line in lines:
                class_id = int(float(line.split(' ')[0]))
                x = int(float(line.split(' ')[1]) * W)
                y = int(float(line.split(' ')[2]) * H)
                w = int(float(line.split(' ')[3]) * W)
                h = int(float(line.split(' ')[4]) * H)
                # x = int(float(line.split(' ')[1]))
                # y = int(float(line.split(' ')[2]))
                # w = int(float(line.split(' ')[3]))
                # h = int(float(line.split(' ')[4]))
                show_bbox_of_image(img, [x - int(w / 2), y - int(h / 2), x + int(w / 2), y + int(h / 2)])

                # crop_img = img[y - int(h / 2):y + int(h / 2), x - int(w / 2):x + int(w / 2)]
                # plt.imshow(img)
                # plt.imshow(crop_img)
                # plt.show()


if __name__ == '__main__':
    show_label_select()