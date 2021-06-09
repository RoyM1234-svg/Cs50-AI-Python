from cv2 import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4

def main():
    labels = []
    images = []
    data_dir = 'gtsrb-small'
    for i in range(3):
        for filename in os.listdir(os.path.join(data_dir,str(i))):
            labels.append(i)
            img = cv2.imread(os.path.join(data_dir,str(i),filename))
            resized = cv2.resize(img, (IMG_WIDTH,IMG_HEIGHT))
            # print(resized.shape)
            images.append(resized)
    
    print(len(labels))
    print(len(images))


            
    # img = cv2.imread('\\1\\00000_00000.ppm')
    # resized = cv2.resize(img, (IMG_WIDTH,IMG_HEIGHT))
    # print(resized.shape)
if __name__ == '__main__':
    main()