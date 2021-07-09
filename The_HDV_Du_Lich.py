import sys
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QApplication,QTabWidget, \
    QWidget, QComboBox, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QFileDialog, QPushButton, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QColor, QPainter, QPen
from PyQt5 import uic
from PyQt5.QtCore import Qt
import cv2
from glob import glob
import os
from utils.dataset import scale_bbox_5_point, scale_bbox_xyxy, scale_bbox_large_image, scale_point_follow_fx_fy, \
    save_yolo_label_file
from utils.image_process import find_three_point, find_angle_from_three_point, rotate_image, rotate_box, rotate_bound, \
    find_distance_two_point, find_bbox_roi_from_bbox_large_image, show_bbox_of_image
import numpy as np
from scipy import ndimage
import time


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        # loading the ui file with uic module
        uic.loadUi('The_HDV_Du_Lich.ui', self)
        # tab
        self.tabWidget = self.findChild(QWidget, "tabWidget")
        # self.MainWindow = self.findChild(QTabWidget, "MainWindow")
        self.tabWidget.setCurrentIndex(0)
        # self.tabWidget.currentChanged.connect(self.onChange)
        # index = self.tabwidget.indexOf(page)

        # label display
        self.label_num_image = self.findChild(QLabel, "label_num_image")
        self.label_num_card = self.findChild(QLabel, "label_num_card")
        self.label_process = self.findChild(QLabel, "label_process")
        self.width_img_org = 0
        self.height_img_org = 0
        self.ratio_width = 0
        self.ratio_height = 0
        self.img_org = None

        self.label_show = self.findChild(QLabel, "label_show")
        print(self.label_show.frameSize())
        self.width_show = 1280
        self.height_show = 720

        self.pix, self.arr_image, self.name_image = self.show_image_to_qlabel('./image/background.jpg')

        # Button load folder
        self.list_image_show = []
        self.pushButton_select_folder_image = self.findChild(QPushButton, "pushButton_select_folder_image")
        self.pushButton_select_folder_image.clicked.connect(self.open_folder_image_show)

        # Button next
        self.pushButton_next = self.findChild(QPushButton, "pushButton_next")
        self.pushButton_next.clicked.connect(self.show_image_next)
        self.idx = 0
        self.bbox_idx = []
        self.bbox_no_rotate = []
        self.points1 = (0, 0)
        self.points2 = (0, 0)
        self.points3 = (0, 0)
        self.angle_rotate_scale = 0

        # Button load folder card
        self.list_card = []
        self.pushButton_select_folder_card = self.findChild(QPushButton, "pushButton_select_folder_card")
        self.pushButton_select_folder_card.clicked.connect(self.open_folder_card)
        self.width_card_in_image = 0
        self.height_card_in_image = 0

        # Select class of card
        self.comboBox_class = self.findChild(QComboBox, "comboBox_class")
        self.comboBox_class.currentTextChanged.connect(self.combo_class_selected)
        self.class_card = None

        # Button ghep the : save bbox and idx image show to folder data need training
        self.pushButton_paster_card = self.findChild(QPushButton, "pushButton_paster_card")
        self.pushButton_paster_card.clicked.connect(self.paster_card_to_image)

        # Button load folder save
        self.folder_save_data = "./Data_HDV"
        self.pushButton_select_folder_save_data = self.findChild(QPushButton, "pushButton_select_folder_save_data")
        self.pushButton_select_folder_save_data.clicked.connect(self.open_folder_save_data)

        # ----------------------------------------------VIEW RESULT----------------------------------------------------
        self.label_show_result = self.findChild(QLabel, "label_show_result")
        self.label_process_result = self.findChild(QLabel, "label_process_result")
        self.label_num_image_result = self.findChild(QLabel, "label_num_image_result")

        self.list_image_result = [glob(x + "/*") for x in glob(self.folder_save_data + "/*")]
        self.list_image_result = sum(self.list_image_result, []) # flatten list of list
        self.idx_result = 0
        if len(self.list_image_result) > 0:
            self.show_image_result_to_qlabel(self.list_image_result[self.idx_result])
            self.label_process_result.setText("{}/{}".format(self.idx_result, len(self.list_image_result)))
        else:
            self.show_image_result_to_qlabel('./image/background.jpg')

        self.pushButton_next_result = self.findChild(QPushButton, "pushButton_next_result")
        self.pushButton_next_result.clicked.connect(self.next_result)

        self.pushButton_select_folder_image_result = self.findChild(QPushButton, "pushButton_select_folder_image_result")
        self.pushButton_select_folder_image_result.clicked.connect(self.select_folder_image_result)

        self.pushButton_back_result = self.findChild(QPushButton, "pushButton_back_result")
        self.pushButton_back_result.clicked.connect(self.back_result)

        # ----------------------------------------------VIEW RESULT----------------------------------------------------

    def show_image_to_qlabel(self, path_image):
        arr_image = cv2.imread(path_image)
        # arr_image = cv2.cvtColor(arr_image, cv2.COLOR_BGR2RGB)
        self.width_img_org = arr_image.shape[1]
        self.height_img_org = arr_image.shape[0]
        self.img_org = arr_image
        self.ratio_width = self.width_img_org / self.width_show
        self.ratio_height = self.height_img_org / self.height_show

        arr_image = cv2.resize(arr_image, (self.width_show, self.height_show), interpolation=cv2.INTER_AREA)
        height, width, channel = arr_image.shape
        self.label_show.setFixedWidth(width)
        self.label_show.setFixedHeight(height)
        img = QImage(cv2.cvtColor(arr_image, cv2.COLOR_BGR2RGB), width, height, width * 3, QImage.Format_RGB888)
        pix_map = QPixmap(img).scaled(width, height, Qt.KeepAspectRatio)
        self.label_show.setPixmap(pix_map)
        self.label_show.mousePressEvent = self.get_pixel
        self.label_show.setScaledContents(True)
        self.label_show.show()

        # get name image
        name_image = path_image.split("/")[-1].split(".")[0]
        return pix_map, arr_image, name_image

    def get_pixel(self, event):
        if len(self.bbox_idx[self.idx]) < 5:
            x = event.pos().x()
            y = event.pos().y()

            # check anh hien tai da ve chua neu ve roi thi add them diem thu 2, nguoc lai tao diem dau tien.
            if len(self.bbox_idx[self.idx]) >= 2 and (self.idx == self.bbox_idx[self.idx][0]):
                if len(self.bbox_idx[self.idx]) < 4:
                    self.bbox_idx[self.idx].append((x, y))
                    if len(self.bbox_idx[self.idx]) == 4:
                        bbox_xyxy = self.bbox_idx[self.idx]
                        x_extra = bbox_xyxy[3][0] - bbox_xyxy[2][0]
                        y_extra = bbox_xyxy[2][1] - bbox_xyxy[1][1]
                        x4 = bbox_xyxy[1][0] + x_extra
                        y4 = bbox_xyxy[3][1] - y_extra
                        self.bbox_idx[self.idx].append((x4, y4))

                        self.width_card_in_image = find_distance_two_point(self.bbox_idx[self.idx][1],
                                                                      self.bbox_idx[self.idx][2])
                        self.height_card_in_image = find_distance_two_point(self.bbox_idx[self.idx][3],
                                                                       self.bbox_idx[self.idx][2])
                        if self.width_card_in_image < self.height_card_in_image:
                            self.bbox_idx[self.idx] = [self.idx]
                            self.pix, self.arr_image, self.name_image = self.show_image_to_qlabel(self.list_image_show[self.idx])
                            # self.bbox_idx = list([self.idx])

                        else:
                            self.bbox_no_rotate = [min(bbox_xyxy[1][0], bbox_xyxy[4][0]), min(bbox_xyxy[1][1], bbox_xyxy[2][1]),
                                                   max(bbox_xyxy[2][0], bbox_xyxy[3][0]), max(bbox_xyxy[3][1], bbox_xyxy[4][1])]

                            self.draw_line(bbox_xyxy[1][0], bbox_xyxy[1][1], bbox_xyxy[2][0], bbox_xyxy[2][1])  # |
                            self.draw_line(bbox_xyxy[2][0], bbox_xyxy[2][1], bbox_xyxy[3][0], bbox_xyxy[3][1])  # |_
                            self.draw_line(bbox_xyxy[3][0], bbox_xyxy[3][1], bbox_xyxy[4][0], bbox_xyxy[4][1])  # |_|
                            self.draw_line(bbox_xyxy[4][0], bbox_xyxy[4][1], bbox_xyxy[1][0], bbox_xyxy[1][1])  # |_|

                            # draw line bbox no rotate
                            self.draw_line(self.bbox_no_rotate[0], self.bbox_no_rotate[1], self.bbox_no_rotate[2], self.bbox_no_rotate[1])
                            self.draw_line(self.bbox_no_rotate[2], self.bbox_no_rotate[1], self.bbox_no_rotate[2], self.bbox_no_rotate[3])
                            self.draw_line(self.bbox_no_rotate[2], self.bbox_no_rotate[3], self.bbox_no_rotate[0], self.bbox_no_rotate[3])
                            self.draw_line(self.bbox_no_rotate[0], self.bbox_no_rotate[3], self.bbox_no_rotate[0], self.bbox_no_rotate[1])

                            # find three points
                            self.points2 = self.bbox_idx[self.idx][1]
                            self.points1 = self.bbox_idx[self.idx][2]
                            self.points3 = (self.points2[0] + 100, self.points2[1])
                            # a, b, c = find_three_point(self.bbox_no_rotate, [bbox_xyxy[1][0], bbox_xyxy[1][1],
                            #                                                  bbox_xyxy[4][0], bbox_xyxy[4][1]])
                            self.draw_point(self.points1[0], self.points1[1], color=Qt.blue)  # a xanh duong
                            self.draw_point(self.points1[0], self.points2[1], color=Qt.yellow)  # b vang
                            self.draw_point(self.points3[0], self.points3[1], color=Qt.green)  # c xanh la
                            # self.angle_rotate_scale = find_angle_from_three_point(a, b, c)
                            # a_scale = [a[0] * self.ratio_width, a[1] * self.ratio_height]
                            # b_scale = [b[0] * self.ratio_width, b[1] * self.ratio_height]
                            # c_scale = [c[0] * self.ratio_width, c[1] * self.ratio_height]
                            # self.angle_rotate_scale = find_angle_from_three_point(a_scale, b_scale, c_scale)

            else:
                self.bbox_idx[self.idx].append((x, y))
            self.draw_point(x, y)
        else:
            QMessageBox.warning(self, "Warning",
                                "Image draw enough point")

    def draw_point(self, x, y, color=Qt.red):
        qp = QPainter(self.pix)
        pen = QPen(color, 10)
        qp.setPen(pen)
        qp.drawPoint(x, y)
        qp.end()
        self.label_show.setPixmap(self.pix)

    def draw_line(self, x1, y1, x2, y2):
        qp = QPainter(self.pix)
        pen = QPen(Qt.red, 3)
        qp.setPen(pen)
        qp.drawLine(x1, y1, x2, y2)
        qp.end()
        self.label_show.setPixmap(self.pix)

    def open_folder_image_show(self):
        dir_ = QFileDialog.getExistingDirectory(None, 'Select project folder:', '/home/',
                                                QFileDialog.ShowDirsOnly)
        self.list_image_show = glob(dir_ + "/*")
        self.list_image_show = sorted(self.list_image_show)
        if len(self.list_image_show) == 0:
            QMessageBox.warning(self, "Warning",
                                "Directory is no any image")
            sys.exit(0)
        else:
            self.pix, self.arr_image, self.name_image = self.show_image_to_qlabel(self.list_image_show[self.idx])
            self.label_num_image.setText(str(len(self.list_image_show)) + " ảnh")
            self.label_process.setText("{}/{}".format(self.idx, len(self.list_image_show)))
            self.bbox_idx.append([self.idx])

    def open_folder_card(self):
        dir_ = QFileDialog.getExistingDirectory(None, 'Select project folder:', '/home/',
                                                QFileDialog.ShowDirsOnly)
        self.list_card = glob(dir_ + "/*")
        self.list_card = sorted(self.list_card)
        if len(self.list_card) == 0:
            QMessageBox.warning(self, "Warning",
                                "Directory is no any card")
        else:
            self.label_num_card.setText(str(len(self.list_card)) + " thẻ")
            print(self.list_card)

    def open_folder_save_data(self):
        dir_ = QFileDialog.getExistingDirectory(None, 'Select project folder:', '/home/',
                                                QFileDialog.ShowDirsOnly)
        self.folder_save_data = dir_

    def show_image_next(self):
        # check current image already ghep the
        list_folder_image_saved = [os.path.basename(x) for x in glob(self.folder_save_data + "/*")]
        if self.name_image not in list_folder_image_saved:
            message = QMessageBox.question(self, "Choice Message",
                                           "Current image haven't save yet!"
                                           "If you want to save choice Yes",
                                           QMessageBox.Yes |
                                           QMessageBox.No)
            if message == QMessageBox.Yes:
                self.paste_and_save_image()
            # else:
            #     QMessageBox.information(self, "Information",
            #                             "Current image don't saved")

        self.idx += 1
        self.pix, self.arr_image, self.name_image = self.show_image_to_qlabel(self.list_image_show[self.idx])
        self.label_process.setText("{}/{}".format(self.idx, len(self.list_image_show)))
        self.bbox_idx.append([self.idx])

    def paster_card_to_image(self):
        if len(self.bbox_idx[self.idx]) > 1:
            print(self.bbox_idx)
            if len(self.list_card) > 0:
                self.paste_and_save_image()
        else:
            QMessageBox.warning(self, "Warning",
                                "No bounding box in image to paster card")

    def paste_and_save_image(self):
        # get card in folder , paste to image and save to folder
        path_save_image_combine = self.folder_save_data + '/' + self.name_image
        if not os.path.exists(path_save_image_combine):
            os.mkdir(path_save_image_combine)
        print(path_save_image_combine)

        start_time = time.time()
        for idx in range(len(self.list_card)):
            small_image = cv2.imread(self.list_card[idx])
            large_image = self.img_org
            if len(self.bbox_idx[self.idx]) != 5:
                QMessageBox.warning(self, "Warning",
                                    "No bbox in image")
                sys.exit(0)
            # # rotated image
            # find width , height of card in origin image

            width_card_in_image = self.width_card_in_image * self.ratio_width
            height_card_in_image = self.height_card_in_image * self.ratio_height
            width_card_rotated = small_image.shape[1]
            height_card_rotated = small_image.shape[0]
            fx = width_card_in_image / width_card_rotated
            fy = height_card_in_image / height_card_rotated

            # scale point draw to size origin image
            points1_scale = scale_point_follow_fx_fy(self.points1, self.ratio_width, self.ratio_height)
            points2_scale = scale_point_follow_fx_fy(self.points2, self.ratio_width, self.ratio_height)
            points3_scale = scale_point_follow_fx_fy(self.points3, self.ratio_width, self.ratio_height)
            # scale point to size of card image
            points1_scale = scale_point_follow_fx_fy(points1_scale, fx, fy)
            points2_scale = scale_point_follow_fx_fy(points2_scale, fx, fy)
            points3_scale = scale_point_follow_fx_fy(points3_scale, fx, fy)
            self.angle_rotate_scale = find_angle_from_three_point(points1_scale, points2_scale, points3_scale)

            rotated_img = ndimage.rotate(small_image, angle=self.angle_rotate_scale)
            # # scale bbox no rotate to size image origin
            bbox_no_rotate_org = scale_bbox_xyxy(self.bbox_no_rotate, self.ratio_width, self.ratio_height)
            # # scale card to size of bbox no rotate
            width_bbox_no_rotate_org = bbox_no_rotate_org[2] - bbox_no_rotate_org[0]
            height_bbox_no_rotate_org = bbox_no_rotate_org[3] - bbox_no_rotate_org[1]
            fx1 = width_bbox_no_rotate_org / rotated_img.shape[1]
            fy1 = height_bbox_no_rotate_org / rotated_img.shape[0]
            rotated_small_img = cv2.resize(rotated_img, (width_bbox_no_rotate_org, height_bbox_no_rotate_org), interpolation=cv2.INTER_AREA)
            # Create mask with color black
            alpha_img = np.zeros((height_bbox_no_rotate_org, width_bbox_no_rotate_org), np.uint8)

            # Find bounding box card after rotated
            # # scale bbox in size tool to size origin image
            # box_large_image = scale_bbox_large_image(self.bbox_idx[self.idx][1:], self.ratio_width, self.ratio_height)
            # offset = [(bbox_no_rotate_org[0], bbox_no_rotate_org[1])]
            # # scale bbox in origin image to bbox rotated
            # new_bb = find_bbox_roi_from_bbox_large_image(offset, box_large_image)

            bbox_card_no_rotate = [(0, 0), (width_card_rotated, 0), (width_card_rotated, height_card_rotated), (0, height_card_rotated)]
            (cx, cy) = (width_card_rotated // 2, height_card_rotated // 2)
            new_bb1 = rotate_box(bbox_card_no_rotate, cx, cy, height_card_rotated, width_card_rotated, self.angle_rotate_scale)
            new_bb1 = scale_bbox_large_image(new_bb1, fx1, fy1)
            tu_giac = np.array(new_bb1, dtype=np.int32)
            # fill bounding box card of mask by color white
            alpha_s = cv2.fillPoly(alpha_img, [tu_giac], (255, 255, 255))
            alpha_s = cv2.blur(alpha_s, (3, 3))
            alpha_s = alpha_s.astype(float) / 255.0
            alpha_l = 1.0 - alpha_s
            # plt.imshow(alpha_s)
            # plt.imshow(alpha_l)
            # plt.show()
            # paste image card to bbox no rotate image origin
            roi_img = large_image[bbox_no_rotate_org[1]:bbox_no_rotate_org[3], bbox_no_rotate_org[0]:bbox_no_rotate_org[2]]
            for c in range(0, 3):
                roi_img[:, :, c] = roi_img[:, :, c] * alpha_l + rotated_small_img[:, :, c] * alpha_s

            name_file_save = path_save_image_combine + "/" + self.name_image + "_" + \
                        self.list_card[idx].split("/")[-1].split(".")[0]
            file_save = name_file_save + ".jpg"
            cv2.imwrite(file_save, large_image)

            # write file bounding box
            """
           Each row is class x_center y_center width height format.
           Box coordinates must be in normalized xywh format (from 0 - 1). 
           If your boxes are in pixels, divide x_center and width by image width, and y_center and height by image height.
           """
            x_center = (width_bbox_no_rotate_org / 2) + bbox_no_rotate_org[0]
            y_center = (height_bbox_no_rotate_org / 2) + bbox_no_rotate_org[1]
            w = width_bbox_no_rotate_org
            h = height_bbox_no_rotate_org
            # normalize to 0 - 1
            x_center = x_center / self.width_img_org
            y_center = y_center / self.height_img_org
            w = w / self.width_img_org
            h = h / self.height_img_org

            # show_bbox_of_image(self.img_org, bbox_no_rotate_org)
            save_yolo_label_file(name_file_save, self.class_card, x_center, y_center, w, h)
        print("time ", time.time() - start_time)
        print("Done image id", self.idx)

    def combo_class_selected(self):
        item = self.comboBox_class.currentText()
        if item == "Thẻ HDV":
            self.class_card = 0
        elif item == "Không phải thẻ HDV":
            self.class_card = 1
        else:
            QMessageBox.warning(self, "Warning",
                                "Please select class of card")
    # ----------------------------------------------VIEW RESULT----------------------------------------------------
    """Phan result"""
    def select_folder_image_result(self):
        dir_ = QFileDialog.getExistingDirectory(None, 'Select project folder:', '/home/',
                                                QFileDialog.ShowDirsOnly)
        self.list_image_result = glob(dir_ + "/*")
        self.idx_result = 0
        if len(self.list_image_result) == 0:
            QMessageBox.warning(self, "Warning",
                                "Directory is no any image")
            sys.exit(0)
        else:
            self.show_image_result_to_qlabel(self.list_image_result[self.idx_result])
            self.label_process_result.setText("{}/{}".format(self.idx_result, len(self.list_image_result)))

    def next_result(self):
        if self.idx_result < len(self.list_image_result)-1:
            self.idx_result += 1
            self.show_image_result_to_qlabel(self.list_image_result[self.idx_result])
            self.label_process_result.setText("{}/{}".format(self.idx_result, len(self.list_image_result)))
        else:
            QMessageBox.warning(self, "Warning",
                                "The end image")
            sys.exit(0)

    def back_result(self):
        if self.idx_result > 0:
            self.idx_result -= 1
            self.show_image_result_to_qlabel(self.list_image_result[self.idx_result])
            self.label_process_result.setText("{}/{}".format(self.idx_result, len(self.list_image_result)))

    def show_image_result_to_qlabel(self, path_image):
        arr_image = cv2.imread(path_image)
        # arr_image = cv2.cvtColor(arr_image, cv2.COLOR_BGR2RGB)
        arr_image = cv2.resize(arr_image, (self.width_show, self.height_show), interpolation=cv2.INTER_AREA)
        height, width, channel = arr_image.shape
        self.label_show_result.setFixedWidth(width)
        self.label_show_result.setFixedHeight(height)
        img = QImage(cv2.cvtColor(arr_image, cv2.COLOR_BGR2RGB), width, height, width * 3, QImage.Format_RGB888)
        pix_map = QPixmap(img).scaled(width, height, Qt.KeepAspectRatio)
        self.label_show_result.setPixmap(pix_map)
        self.label_show_result.setScaledContents(True)
        self.label_show_result.show()


app = QApplication([])
window = UI()
window.show()
app.exec_()