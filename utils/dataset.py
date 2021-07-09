import cv2
from glob import glob
import matplotlib.pyplot as plt

from utils.image_process import show_bbox_of_image


def scale_bbox_5_point(bbox_xyxy, ratio_width, ratio_height):
    x1 = int(bbox_xyxy[1][0] * ratio_width)
    x2 = int(bbox_xyxy[3][0] * ratio_width)
    y1 = int(bbox_xyxy[1][1] * ratio_height)
    y2 = int(bbox_xyxy[3][1] * ratio_height)
    return [bbox_xyxy[0], x1, y1, x2, y2]


def scale_bbox_large_image(bbox, ratio_width, ratio_height):
    x1 = int(bbox[0][0] * ratio_width) + 3
    y1 = int(bbox[0][1] * ratio_height) + 3
    x2 = int(bbox[1][0] * ratio_width) - 3
    y2 = int(bbox[1][1] * ratio_height) + 3
    x3 = int(bbox[2][0] * ratio_width) - 3
    y3 = int(bbox[2][1] * ratio_height) - 3
    x4 = int(bbox[3][0] * ratio_width) + 3
    y4 = int(bbox[3][1] * ratio_height) - 3
    return [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]


def scale_point_follow_fx_fy(point, ratio_width, ratio_height):
    x1 = int(point[0] * ratio_width)
    y1 = int(point[1] * ratio_height)
    return tuple([x1, y1])


def scale_bbox_xyxy(bbox_xyxy, ratio_width, ratio_height):
    x1 = int(bbox_xyxy[0] * ratio_width)
    x2 = int(bbox_xyxy[2] * ratio_width)
    y1 = int(bbox_xyxy[1] * ratio_height)
    y2 = int(bbox_xyxy[3] * ratio_height)
    return [x1, y1, x2, y2]


def save_yolo_label_file(name_file_save, classes, cx, cy, w, h):
    # write file bounding box
    label_file = name_file_save + ".txt"
    boding_box_label = str(classes) + ' ' + str(cx) + ' ' + str(cy) + ' ' \
                       + str(w) + ' ' + str(h) + '\n'
    with open(label_file, 'w+') as f_label_image_write:
        f_label_image_write.write(boding_box_label)


