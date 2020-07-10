# -*- coding:utf-8 -*-
#!/usr/bin/env python

from __future__ import print_function

import tensorflow as tf
import cv2
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

GAME = 'bird' # the name of the game being played for log files \ название игры, в которую играют для файлов журнала
ACTIONS = 2 # number of valid actions \ количество действительных действий
GAMMA = 0.99 # decay rate of past observations \ скорость распада прошлых наблюдений
OBSERVE = 100000. # timesteps to observe before training \ временные шаги, чтобы наблюдать перед тренировкой
EXPLORE = 2000000. # frames over which to anneal epsilon \ кадры для отжига эпсилон
FINAL_EPSILON = 0.0001 # final value of epsilon \ окончательное значение эпсилона
INITIAL_EPSILON = 0.0001 # starting value of epsilon \ начальная стоимость эпсилона
REPLAY_MEMORY = 1000#50000 # number of previous transitions to remember \ количество предыдущих переходов для запоминания
BATCH = 16#32 # size of minibatch \ размер мини-партии 16#
FRAME_PER_ACTION = 1
"""
1 подаю по одному кадргу разрезанную картинку не готовую!!!
2 каждая разрезанная картинка это действие 
3 для обновления градиента использую созданную партию из порезанных ?
4 терминал true когда 1
"""

def imgs(x):
      cv2.imshow('Rotat', np.array(x, dtype=np.uint8))
      cv2.waitKey(0)
      cv2.destroyAllWindows()

def get(i):
        idxAX = 0
        list = []
        for ii, x in enumerate(range(0, 416, 104)):
           for iii,y in enumerate(range(0, 416, 104)):
              idxAX += 1

              #i[idxAX] = [(x,x + 104), (y, y + 104)]
              list.append(i[x:x + 104,y:y + 104,:])

        return tf.stack(list)


traindict = {}
def getV(x,y):
    #print x, y
    for i in y:
        x[i-1] = 1.
    return x

def readdata():
            lists = ["data/taxi4x4/big_img.csv", "data/bicycles4x4/big_img.csv"]
            for jk in lists:
                clas = jk.split("/")[1]
                print (clas)
                files = open(jk, 'r').readlines()
                for igh, gh in enumerate(files[:]):
                          gh = gh.split('\n') 
                          gh = gh[0].split(';')
                          namefile = 'data/'+clas+'/img/'+gh[0]+'.jpg'
                          if gh[1] != 'no_matching_images':
                                  convRUC = [int(i) for i in gh[1].split(':')[1].split('/')]
                                  ans_V = np.zeros([16]) # answer in vector
                                  ans_V = getV(ans_V, convRUC)
                                  traindict[namefile] = ans_V


def get_batch(k):
                     image = cv2.imread(k) 
                     resize_image = cv2.resize(image, (416, 416))
                     resize_label = np.reshape(np.array(traindict[k]), [16, 1])
                     #return draw_boxes(resize_image), resize_label
                     return resize_image, resize_label


def draw_boxes(image):

        h_z = 416 / 4
        image[0:, h_z:(h_z+5), :] = 255
        image[0:, (h_z*2):((h_z*2)+5), :] = 255
        image[0:, (h_z*3):((h_z*3)+5), :] = 255
        image[0:, (h_z*4):((h_z*4)+5), :] = 255
        # w line
        #      x          y
        image[h_z:(h_z+5), 0:, :] = 255
        image[(h_z*2):((h_z*2)+5), 0:, :] = 255
        image[(h_z*3):((h_z*3)+5), 0:, :] = 255
        image[(h_z*4):((h_z*4)+5), 0:, :] = 255

        return image

def window_slide(image):
        image = draw_boxes(image)
        #imgs(image)
        stepSize = 104
        (w_width, w_height) = (104, 104) # window size
        #arrr = []
        idxAX = 0
        fps16 = []
        for ii, x in enumerate(range(0, image.shape[1], stepSize)):
            for iii, y in enumerate(range(0, image.shape[0], stepSize)):
                      #if int(ans_V[idxAX]) == 1:
                              #fps16.append(image[x:x + w_width, y:y + w_height, :]*.255)
               arrnp = np.copy(image) #np.zeros(shape=(416,416,3), dtype=np.uint8)                    
               arrnp[x:x + w_width, y:y + w_height, :] = image[x:x + w_width, y:y + w_height, :]*.255
               fps16.append(arrnp)
               idxAX += 1
        return fps16

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 0.01)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.01, shape = shape)
    return tf.Variable(initial)

def conv2d(x, W, stride):
    return tf.nn.conv2d(x, W, strides = [1, stride, stride, 1], padding = "SAME")

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = "SAME")

def createNetwork():
    # network weights
    W_conv1 = weight_variable([8, 8, 4, 32])
    b_conv1 = bias_variable([32])

    W_conv2 = weight_variable([4, 4, 32, 64])
    b_conv2 = bias_variable([64])

    W_conv3 = weight_variable([3, 3, 64, 64])
    b_conv3 = bias_variable([64])
    #------
    W_conv4 = weight_variable([1, 1, 64, 128])
    b_conv4 = bias_variable([128])

    W_conv5 = weight_variable([3, 3, 128, 256])
    b_conv5 = bias_variable([256])

    W_conv6 = weight_variable([1, 1, 256, 256])
    b_conv6 = bias_variable([256])

    #-------
    W_fc1 = weight_variable([1024, 512])
    b_fc1 = bias_variable([512])

    W_fc2 = weight_variable([512, ACTIONS])
    b_fc2 = bias_variable([ACTIONS])

    # input layer
    #s = tf.placeholder("float", [None, 104, 104, 4])
    s = tf.placeholder("float", [None, 416, 416, 4])

    # hidden layers
    h_conv1 = tf.nn.relu(conv2d(s, W_conv1, 4) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)
   
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2, 2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    h_conv3 = tf.nn.relu(conv2d(h_pool2, W_conv3, 1) + b_conv3)
    h_pool3 = max_pool_2x2(h_conv3)
    #<-
    h_conv4 = tf.nn.relu(conv2d(h_pool3, W_conv4, 2) + b_conv4)
    h_conv5 = tf.nn.relu(conv2d(h_conv4, W_conv5, 2) + b_conv5)
    h_conv6 = tf.nn.relu(conv2d(h_conv5, W_conv6, 1) + b_conv6)
    #<-
    #h_pool3_flat = tf.reshape(h_pool3, [-1, 256])
    #h_conv3_flat = tf.reshape(h_conv3, [-1, 1600])
    h_conv3_flat = tf.reshape(h_conv6, [-1, 1024])

    h_fc1 = tf.nn.relu(tf.matmul(h_conv3_flat, W_fc1) + b_fc1)

    # readout layer # cnn layer #считывающий слой
    readout = tf.matmul(h_fc1, W_fc2) + b_fc2

    return s, readout, h_fc1

def gameaction(y,x):
        print ("gameaction", "NN>", y, "MY>", x)
        reward = 0.1
        terminal = False
        if y[1] == x:
            reward = 1
            #print ("GOOOD SCORE")
        else:
            terminal = True
            reward = -1  
            #print ("BAD SCORE")
        #print ("gameaction",  y, x, reward, terminal) #y == 1, y, reward, terminal)   
        return reward, terminal


def gameaction2(y, x, y1, x1):
        print ("gameaction", "NOW>", y, x, "OLD>", y1, x1)
        reward = 0.1
        terminal = False
        if y[1] == x and y1[1] == x1:
            reward = 1
            #print ("GOOOD SCORE")
        if y[1] == x:
            #terminal = True
            reward = 0.5  
            #print ("BAD SCORE")
        if y[1] != x:
            reward = -0.5 
        if y[1] != x and y1[1] != x1:
            terminal = True
            reward = -1
        #print ("gameaction",  y, x, reward, terminal) #y == 1, y, reward, terminal)   
        return reward, terminal

def getid():
        list = []
        for ii, x in enumerate(range(0, 416, 104)):
           for iii,y in enumerate(range(0, 416, 104)):

              #i[idxAX] = [(x,x + 104), (y, y + 104)]
              list.append([x,x + 104, y, y + 104])

        return list


def trainNetwork(s, readout, h_fc1, sess):
    # define the cost function
    # s(input), readout(tf.matmul), h_fc1(tf.nn.relu)
    a = tf.placeholder("float", [None, ACTIONS])
    y = tf.placeholder("float", [None])

    ####
    nss = getid()
    saver = tf.train.Saver()
    sess.run(tf.initialize_all_variables())
    checkpoint = tf.train.get_checkpoint_state("saved_networks_1")
    if checkpoint and checkpoint.model_checkpoint_path:
        saver.restore(sess, checkpoint.model_checkpoint_path)
        print("Successfully loaded:", checkpoint.model_checkpoint_path)
    else:
        print("Could not find old network weights")

    for imgh in traindict.keys():
            image = cv2.resize(cv2.imread(imgh), (416, 416))
            im = image
            image = window_slide(image)
            ans_ls = []
            
            for ig in image:
                a_t = np.zeros([ACTIONS])
                s_t = np.append(ig[:, :, :2], ig[:, :, :2], axis=2)
                answ = sess.run(readout,feed_dict={s : [s_t]})
                action_index = np.argmax(answ)
                #a_t[action_index] = 1
                #print (action_index, answ)
                ans_ls.append(action_index)
                #imgs(s_t)
            for idx, q in enumerate(ans_ls):
                if q == 1:
                   im[nss[idx][0]:nss[idx][1], nss[idx][2]:nss[idx][3], :] *= 255
            print (ans_ls)    
            imgs(im)    
            #print (ans_ls)   
            #answ = sess.run(readout,feed_dict={s : [s_t]})
            #print (answ)
            #imgs(image[1])
    

def playGame():
    #print "DATA LOAD"
    readdata()
    sess = tf.InteractiveSession()
    s, readout, h_fc1 = createNetwork()
    trainNetwork(s, readout, h_fc1, sess)

def main():
    playGame()

if __name__ == "__main__":
    main()
