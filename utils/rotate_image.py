# import matplotlib as mpl
# mpl.use('Agg')
import matplotlib.pyplot as plt
import cv2
import matplotlib.patches as mpatches
import numpy as np
import json

theta = 45

# with open('images/example1_labels.json') as json_data:
#     d = json.load(json_data)
#     print(d)
#
# bb1 = {}
# for i,j in enumerate(d[0]['annotations']):
#     xs = j['xn'].split(';')
#     ys = j['yn'].split(';')
#     bb1[i] = [(float(xs[0]),float(ys[0])), (float(xs[1]),float(ys[1])),(float(xs[2]),float(ys[2])),(float(xs[3]),float(ys[3]))]
#
# print(bb1)


def rotate_box(bb, cx, cy, h, w):
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
        v = [coord[0],coord[1],1]
        # Perform the actual rotation and return the image
        calculated = np.dot(M,v)
        new_bb[i] = (calculated[0],calculated[1])
    return new_bb


def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # centre
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

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

def test():
    # Original image
    img_orig = cv2.imread('images/cat.jpg')
    # Rotated image
    rotated_img = rotate_bound(img_orig, theta)

    # Plot original image with bounding boxes
    fig, [ax1, ax2] = plt.subplots(nrows=2,ncols=1,figsize=(12, 18))
    plt.tight_layout()
    ax1.imshow(img_orig[...,::-1], aspect='auto')
    ax1.axis('off')
    ax1.add_patch(mpatches.Polygon(bb1[0], lw=3.0, fill=False, color='red'))
    ax1.add_patch(mpatches.Polygon(bb1[1], lw=3.0, fill=False, color='red'))
    ax1.add_patch(mpatches.Polygon(bb1[2], lw=3.0, fill=False, color='green'))

    # Calculate the shape of rotated images
    (heigth, width) = img_orig.shape[:2]
    (cx, cy) = (width // 2, heigth // 2)
    (new_height, new_width) = rotated_img.shape[:2]
    (new_cx, new_cy) = (new_width // 2, new_height // 2)
    print(cx,cy,new_cx,new_cy)

    ## Calculate the new bounding box coordinates
    new_bb = {}
    for i in bb1:
        new_bb[i] = rotate_box(bb1[i], cx, cy, heigth, width)

    ## Plot rotated image and bounding boxes
    ax2.imshow(rotated_img[...,::-1], aspect='auto')
    ax2.axis('off')
    ax2.add_patch(mpatches.Polygon(new_bb[0],lw=3.0, fill=False, color='red'))
    ax2.add_patch(mpatches.Polygon(new_bb[1],lw=3.0, fill=False, color='red'))
    ax2.add_patch(mpatches.Polygon(new_bb[2],lw=3.0, fill=False, color='green'))
    ax2.text(0.,0.,'Rotation by: ' + str(theta), transform=ax1.transAxes,
               horizontalalignment='left', verticalalignment='bottom', fontsize=30)
    name='Output.png'
    plt.savefig(name)
    plt.cla()


def main():
    img_orig = cv2.imread('../image/QT-Moi-1.jpg')
    rotated_img = rotate_bound(img_orig, -10)
    plt.imshow(rotated_img)
    plt.show()




if __name__ == '__main__':
    main()