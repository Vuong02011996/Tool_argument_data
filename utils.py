import cv2
img = cv2.imread('/home/vuong/Downloads/Nguoideothe_1.jpg')

all_point = []


def shape_selection(event, x, y, flags, param):
    # grab references to the global variables
    global ref_point, crop

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        # print('ref_point1', ref_point)

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        ref_point.append((x, y))
        print('ref_point2', ref_point)
        all_point.append(ref_point)
        # draw a rectangle around the region of interest
        # cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.line(image, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow("image", image)


def main():
    global image
    # load the image, clone it, and setup the mouse callback function

    frame_ori = img

    image = cv2.resize(frame_ori, (1280, 720))
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", shape_selection)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # press 'r' to reset the window
        if key == ord("r"):
            image = clone.copy()

        # if the 'c' key is pressed, break from the loop
        elif key == ord("q"):
            print('all_point:', all_point)
            break

    # close all open windows
    cv2.destroyAllWindows()


def paste_small_image_to_large_image_cv2():
    large_image = cv2.imread('/home/vuong/Downloads/Nguoideothe_1.jpg')
    large_image = cv2.resize(large_image, (1280, 720))
    small_image = cv2.imread("/home/vuong/Downloads/The_HDV_moi/QT-Moi-20.jpg")
    # large_image[from_row(y1):to_row(y2)y from_col(x1):to_col(x2)] = small_image
    width_small = 685-558
    height_small = 613 - 510
    small_image = cv2.resize(small_image, (width_small, height_small))
    # small_image = cv2.addWeighted(large_image[510:613, 558:685], 0.1, small_image, 0.1, 0)
    large_image[510:613, 558:685] = small_image
    while True:
        cv2.imshow("image", large_image)
        key = cv2.waitKey(10) & 0xFF
        if key == ord("q"):
            break


if __name__ == '__main__':
    # main()
    paste_small_image_to_large_image_cv2()