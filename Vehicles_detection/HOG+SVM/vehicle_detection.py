import cv2
import matplotlib.pyplot as plt
import pylab
import numpy as np
from sklearn.externals import joblib
from skimage.feature import hog
from moviepy.editor import VideoFileClip


# image normalization
def norm(image):
    maxpixel = image.max()
    minpixel = image.min()
    image = (image - minpixel) / (maxpixel - minpixel)
    return image


# image pre-process
def image_process(image):
    image_gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    image_norm = norm(image_gray)
    return image_norm


# generate all the windows
def generate_windows(image, batch_size, window_size):
    x_max = image.shape[1]
    y_max = image.shape[0]
    x_start = 0
    x_stop = x_start + window_size
    window_list = []
    while x_stop <= x_max:
        y_start = 200
        y_stop = y_start + window_size
        while y_stop <= y_max - 50:
            window = ((x_start, x_stop), (y_start, y_stop))
            window_list.append(window)
            y_start += batch_size
            y_stop = y_start + window_size
        x_start += batch_size
        x_stop = x_start + window_size
    return window_list


# display the windows on the image
def draw_windows(image, windows):
    imcopy = np.copy(image)
    for window in windows:
        cv2.rectangle(imcopy, (window[0][0], window[1][0]), (window[0][1], window[1][1]), (0, 0, 255), 5)
    return imcopy


# detect vehicles on each window
def detection(image, window):
    imcopy = []
    for x in range(window[1][0], window[1][1]):
        for y in range(window[0][0], window[0][1]):
            imcopy.append(image[x][y])
    metric = np.array(imcopy).reshape((window[0][1] - window[0][0]),(window[1][1] - window[1][0]))
    image_size = window[0][1] - window[0][0]
    cell = image_size / 8  # define the size of a cell
    normalised_blocks, hog_image = hog(metric, orientations=9, pixels_per_cell=(cell, cell), cells_per_block=(4, 4), visualize=True)
    model = joblib.load("/.../svm.model")  # load the trained SVM model
    pred = model.predict([normalised_blocks])
    return pred


# draw the heatmap
def add_heat(image, hot_windows):
    mask=np.zeros_like(image[:,:,0])
    for window in hot_windows:
        for i in range(window[0][0], window[0][1]):
            for j in range(window[1][0], window[1][1]):
                mask[j][i] += 1
    return mask


# set a threshold on the heatmap
def apply_threshold(heat, threshold):
    heat[heat<threshold]=0
    return heat


# score each window
def compute_score(box, heatmap):
    sum = 0
    for i in range(box[1][0], box[1][1]):
        for j in range(box[0][0], box[0][1]):
            sum += heatmap[i][j]
    score = sum
    return score


# verify that point p is in the box
def check_point(p, box):
    if p[0] >= box[1][0] and p[0] <= box[1][1] and p[1] >= box[0][0] and p[1] <= box[0][1]:
        result = 1
    else:
        result = 0
    return result


# calculate IoU between boxes
def compute_iou(box1, box2):
    p1 = (box2[1][0], box2[0][0])
    p2 = (box2[1][0], box2[0][1])
    p3 = (box2[1][1], box2[0][0])
    p4 = (box2[1][1], box2[0][1])

    if box1[0] == box2[0] or box1[1] == box2[1]:
        iou = 1
    else:
        s = check_point(p1, box1) + check_point(p2, box1) + check_point(p3, box1) + check_point(p4, box1)

        if s == 0:
            iou = -1
        else:
            iou = 1

    return iou


# preprocess image
def preprocess(img):
    image = image_process(img)
    i = 2
    window_size = i * 64  # define the size of windows
    batch_size =16*2  # define the batch size
    windows= generate_windows(image, batch_size, window_size)
    boxs = []
    for window in windows:
        pred = detection(image, window)
        if pred == 1:
            boxs.append(window)  # output the windows with vehicles

    heatmap = add_heat(img, boxs)  # draw the heatmap
    heatmap = apply_threshold(heatmap, 2)  # set a threshold on the heatmap

    box_selected = []
    while boxs:
        score_list = []
        for i in range(len(boxs)):
            box = boxs[i]
            score = compute_score(box, heatmap)
            score_list.append(score)  # output the score of each box

        # remove the redundant boxes according to the IoU
        c = score_list.index(max(score_list))
        box_selected.append(boxs[c])
        box1 = boxs[c]
        boxs.remove(boxs[c])
        boxs_check = tuple(boxs)
        for i in range(len(boxs_check)):
            box2 = boxs_check[i]
            iou = compute_iou(box1, box2)
            if iou >= 0:
                boxs.remove(box2)
    print(box_selected)  # print the final boxes
    imcopy = draw_windows(img, box_selected)  # display the boxes on the example image
    return imcopy


# code to process image
img = cv2.imread("/.../test.jpg") # load the test image
output_image = preprocess(img)
plt.imshow(output_image)
pylab.show()

# code to process video
output = '/.../test_video_output.mp4'  # define the location of output video
clip1 = VideoFileClip('/.../test_video.mp4')  # define the location of test video
out_clip = clip1.fl_image(preprocess) #NOTE: this function expects color images!!
out_clip.write_videofile(output, audio=False)