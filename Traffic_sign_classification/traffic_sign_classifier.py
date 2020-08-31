
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pylab
from collections import Counter
import cv2
from sklearn.utils import shuffle
from keras.optimizers import Adam


# read the data set
def load_data():

    training_file = '/.../traffic-signs-data/train.p'
    validation_file = '/.../traffic-signs-data/valid.p'
    testing_file = '/.../traffic-signs-data/test.p'

    with open(training_file, mode='rb') as f:
        train = pickle.load(f)
    with open(validation_file, mode='rb') as f:
        valid = pickle.load(f)
    with open(testing_file, mode='rb') as f:
        test = pickle.load(f)

    X_train, y_train = train['features'], train['labels']
    X_valid, y_valid = valid['features'], valid['labels']
    X_test, y_test = test['features'], test['labels']

    X_train, y_train = shuffle(X_train, y_train)

    return X_train, y_train, X_valid, y_valid, X_test, y_test


# TODO: visualize the data
def output_datasize(X_train, y_train, X_valid, X_test):

    # TODO: Number of training examples
    n_train = len(X_train)

    # TODO: Number of validation examples
    n_validation = len(X_valid)

    # TODO: Number of testing examples.
    n_test = len(X_test)

    # TODO: What's the shape of an traffic sign image?
    image_shape = X_train[0].shape

    # TODO: How many unique classes/labels there are in the dataset.
    n_classes = len(np.unique(y_train))

    print("Number of training examples =", n_train)
    print("Number of testing examples =", n_test)
    print("Number of validing examples =", n_validation)
    print("Image data shape =", image_shape)
    print("Number of classes =", n_classes)

'''
def display_images():
    i = np.random.randint(len(X_valid))
    image = X_valid[i]
    print(i)
    plt.figure()
    plt.imshow(image,cmap = 'gray')
    pylab.show()
'''


# TODO: visualize the data set and draw histogram
def visualization_dataset(y_valid, y_test, y_train):

    sign_count = Counter(y_train)
    n_classes = len(np.unique(y_train))

    xval = np.array(range(n_classes))
    yval = [sign_count[i] for i in xval]
    plt.figure(figsize=(10, 8))
    plt.bar(xval, yval)
    plt.xticks([0.5 + i for i in range(n_classes)], list(range(n_classes)))
    plt.xlabel('classes')
    plt.ylabel('number of occurence')
    plt.title('class distribution of training set')
    plt.show()

    sign_count_valid = Counter(y_valid)
    xval = np.array(range(n_classes))
    yval = [sign_count_valid[i] for i in xval]
    plt.figure(figsize=(10, 8))
    plt.bar(xval, yval)
    plt.xticks([0.5 + i for i in range(n_classes)], list(range(n_classes)))
    plt.xlabel('classes')
    plt.ylabel('number of occurence')
    plt.title('class distribution of validation set')
    plt.show()

    sign_count_test = Counter(y_test)
    xval = np.array(range(n_classes))
    yval = [sign_count_test[i] for i in xval]
    plt.figure(figsize=(10, 8))
    plt.bar(xval, yval)
    plt.xticks([0.5 + i for i in range(n_classes)], list(range(n_classes)))
    plt.xlabel('classes')
    plt.ylabel('number of occurence')
    plt.title('class distribution of test set')
    plt.show()


# TODO: normalization
def normalization_dataset(image):

    min_pixl = image.min()
    max_pixl = image.max()
    image = (image - min_pixl) / (max_pixl - min_pixl)
    return image


# TODO: convert RGB images to gray scale images
def graytransform(image):
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return image_gray


# TODO: preprocess the images
def image_process(dataset):
    ret = []
    for image in dataset:
        image_gray = graytransform(image)
        image_norm = normalization_dataset(image_gray)
        ret.append(image_norm)
    ret = np.array(ret)
    return ret


# TODO: making one-hot code
def one_hot(x):
    ret=np.zeros((len(x),n_classes))
    for i,label in enumerate(x):
        ret[i][label] = 1
    return ret


# TODO: establish the structure of LeNet and train the model on training set
def model_fit(X_train, y_train):
    from keras.models import Sequential
    from keras.layers import Flatten, Dense, Dropout
    from keras.layers.convolutional import Conv2D, MaxPooling2D

    model = Sequential()

    model.add(Conv2D(filters=16, kernel_size= 5, strides=(1, 1), input_shape=(32, 32, 1), padding='valid',
                     data_format='channels_last', activation='relu', kernel_initializer='uniform'))
    model.add(Dropout(0.5))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(filters=16, kernel_size=(3, 3), strides=(1, 1), padding='same',
                     data_format='channels_last', activation='relu', kernel_initializer='uniform'))
    model.add(Dropout(0.5))
    model.add(MaxPooling2D((2, 2)))

    model.add(Flatten())

    model.add(Dense(128, activation = 'relu'))
    model.add(Dense(84, activation = 'relu'))
    model.add(Dense(n_classes, activation = 'softmax'))

    model.summary()
    adam = Adam(lr = 0.0015)
    model.compile(loss = 'mse', optimizer = adam, metrics=['accuracy'])
    model.fit(X_train, y_train, batch_size = 64, validation_split = 0.2, epochs = 50, verbose = 1)
    return model


# TODO: calculate the classification accuracy on the validation set
def model_evaluate():
    y_pred = []
    sum = 0
    for image in X_valid:
        image = image.reshape(1,32,32,1)
        pred = model.predict(image)
        pred = np.array(pred)
        index = np.argmax(pred)
        y_pred.append(index)
    for i in range(len(X_valid)):
        if y_pred[i] == y_valid[i]:
            sum += 1
    print(sum)
    acc = sum/len(X_valid)
    return acc


# TODO: implementation
if __name__ == '__main__':
    X_train, y_train, X_valid, y_valid, X_test, y_test = load_data()
    # output_datasize(X_train, y_train, X_valid, X_test)
    n_classes = len(np.unique(y_train))
    # visualization_dataset(y_valid, y_test, y_train)
    X_train = image_process(X_train)
    X_valid = image_process(X_valid)
    X_test = image_process(X_test)
    # display_images()
    y_train_oh = one_hot(y_train)
    y_valid_oh = one_hot(y_valid)
    y_test_oh = one_hot(y_test)
    X_train = X_train.reshape(len(X_train), 32, 32, 1)
    X_valid = X_valid.reshape(len(X_valid), 32, 32, 1)
    X_test = X_test.reshape(len(X_test), 32, 32, 1)
    model = model_fit(X_train, y_train_oh)
    acc = model_evaluate()
    print(acc)
    model.save("model.h5")

