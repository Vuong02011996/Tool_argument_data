

def scale_bbox(bbox_xyxy, ratio_width, ratio_height):
    x1 = int(bbox_xyxy[1] * ratio_width)
    x2 = int(bbox_xyxy[3] * ratio_width)
    y1 = int(bbox_xyxy[2] * ratio_height)
    y2 = int(bbox_xyxy[4] * ratio_height)
    return [bbox_xyxy[0], x1, y1, x2, y2]