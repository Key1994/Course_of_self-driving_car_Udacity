
import cv2
from skimage.feature import hog
import os
import sklearn
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
from sklearn.svm import LinearSVC


# making dataset

def load_image():
    X = []
    Y = []
    # load the images without vehicles and annotate them with label "0"
    file_path1 = "/.../dataset/non-vehicles/GTI"  # file location on your own computer
    for image in os.listdir(file_path1):
        image_path = os.path.join(file_path1, image)
        # extract the HOG feature
        hog_image = HOG(image_path)
        X.append(hog_image)
        Y.append(0)

    # load the images with vehicles and annotate them with label "1"
    file_path2 = "/.../vehicles/GTI_MiddleClose" # file location on your own computer
    for image in os.listdir(file_path2):
        image_path = os.path.join(file_path2, image)
        hog_image = HOG(image_path)
        X.append(hog_image)
        Y.append(1)
    return X, Y


# image normalization
def norm(image):
    maxpixel = image.max()
    minpixel = image.min()
    if maxpixel != minpixel:
        image = (image - minpixel) / (maxpixel - minpixel)
    return image


# image pre-process
def image_process(image):
    image = cv2.imread(image)
    # convert RGB to gray scale
    image_gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    image_norm = norm(image_gray)
    return image_norm


# extract the HOG feature
def HOG(image):
    image = image_process(image)
    # 8*8 pixels per cell, 4*4 cells per block
    normalised_blocks, hog_image = hog(image, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(4, 4),visualize=True)
    return normalised_blocks.flatten()


# split training set and test set as 6:4
X, Y = load_image()
train_data, test_data, train_label, test_label = sklearn.model_selection.train_test_split(X, Y, random_state=1,train_size=0.6,test_size=0.4)
svc = LinearSVC(C=0.001, verbose=True, random_state=0)  # load the linearSVC model
svc.fit(train_data, train_label)  # model train
joblib.dump(svc, "/.../svm.model")  # save the SVM model
model = joblib.load("/Users/zhangzheng/desktop/svm.model")  # load the SVM model
result = []
for i in range(len(test_label)):
    image = test_data[i]
    pred = model.predict(image.reshape(1, -1))
    result.append(pred)
acc = accuracy_score(result, test_label)  # calculate the classification accuracy
print(acc)
