import sys

from PyQt5.QtWidgets import QApplication,QTabWidget, \
    QWidget, QComboBox, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QFileDialog, QPushButton, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QColor, QPainter, QPen
from PyQt5 import uic
from PyQt5.QtCore import Qt
import cv2
from glob import glob
import os
from utils.dataset import scale_bbox
from utils.image_process import find_three_point, find_angle_from_three_point


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
        self.angle_rotate = 0

        # Button load folder card
        self.list_card = []
        self.pushButton_select_folder_card = self.findChild(QPushButton, "pushButton_select_folder_card")
        self.pushButton_select_folder_card.clicked.connect(self.open_folder_card)

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
        print(self.bbox_idx[self.idx])
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

                        # find angle rotate
                        a, b, c = find_three_point(self.bbox_no_rotate, [bbox_xyxy[1][0], bbox_xyxy[1][1],
                                                                         bbox_xyxy[4][0], bbox_xyxy[4][1]])
                        self.angle_rotate = find_angle_from_three_point(a, b, c)
                        print(self.angle_rotate)

            else:
                self.bbox_idx[self.idx].append((x, y))
            self.draw_point(x, y)
        else:
            QMessageBox.warning(self, "Warning",
                                "Image draw enough point")

    def draw_point(self, x, y):
        qp = QPainter(self.pix)
        pen = QPen(Qt.red, 10)
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

            print(self.list_image_show)

    def open_folder_card(self):
        dir_ = QFileDialog.getExistingDirectory(None, 'Select project folder:', '/home/',
                                                QFileDialog.ShowDirsOnly)
        self.list_card = glob(dir_ + "/*")
        self.list_card = sorted(self.list_card)
        if len(self.list_card) == 0:
            QMessageBox.warning(self, "Warning",
                                "Directory is no any card")
            sys.exit(0)
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
        if len(self.bbox_idx[self.idx]) > 0:
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

        for idx in range(len(self.list_card)):
            small_image = cv2.imread(self.list_card[idx])
            if len(self.bbox_idx[self.idx]) != 5:
                QMessageBox.warning(self, "Warning",
                                    "No bbox in image")
                sys.exit(0)
            bbox_xyxy = self.bbox_idx[self.idx]
            bbox_xyxy_org = scale_bbox(bbox_xyxy, self.ratio_width, self. ratio_height)
            width_small = bbox_xyxy_org[3] - bbox_xyxy_org[1]
            height_small = bbox_xyxy_org[4] - bbox_xyxy_org[2]
            small_image = cv2.resize(small_image, (width_small, height_small), interpolation=cv2.INTER_AREA)

            large_image = self.img_org
            large_image[bbox_xyxy_org[2]:bbox_xyxy_org[4], bbox_xyxy_org[1]:bbox_xyxy_org[3]] = small_image
            file_save = path_save_image_combine + "/" + self.name_image + "_" + \
                        self.list_card[idx].split("/")[-1].split(".")[0] + ".jpg"
            cv2.imwrite(file_save, large_image)

            """
            Each row is class x_center y_center width height format.
            Box coordinates must be in normalized xywh format (from 0 - 1). 
            If your boxes are in pixels, divide x_center and width by image width, and y_center and height by image height.
            """
            # while True:
            #     cv2.imshow("image", large_image)
            #     key = cv2.waitKey(10) & 0xFF
            #     if key == ord("q"):
            #         break

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