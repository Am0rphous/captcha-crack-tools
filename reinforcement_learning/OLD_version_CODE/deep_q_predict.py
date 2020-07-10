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
REPLAY_MEMORY = 50000 # number of previous transitions to remember \ количество предыдущих переходов для запоминания
BATCH = 32 # size of minibatch \ размер мини-партии 16#
FRAME_PER_ACTION = 1
"""
1 подаю по одному кадргу разрезанную картинку не готовую!!!
2 каждая разрезанная картинка это действие 
3 для обновления градиента использую созданную партию из порезанных ?
4 терминал true когда 1
"""

def imgs(x):
      #cv2.startWindowThread()
      #cv2.namedWindow("Rotat")
      cv2.imshow('Rotat', np.array(x, dtype=np.uint8))
      #k = cv.waitKey(0)
      #if k == 27:         
      #   cv.destroyAllWindows()
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
            with open("data/taxi4x4/big_img.csv", 'r') as g:
                      g = g.readlines()
                      for igh, gh in enumerate(g[:]):
                          gh = gh.split('\n') 
                          gh = gh[0].split(';')
                          namefile = 'data/taxi4x4/img/'+gh[0]+'.jpg'
                          #print namefile
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

def window_slide(image, ans_V):
        stepSize = 104
        (w_width, w_height) = (104, 104) # window size
        #arrr = []
        #fig, ax = plt.subplots(4, 4)
        idxAX = 0
        fps16 = []
        #arrnp = np.zeros(shape=(416,416,3), dtype=np.uint8) #np.ones((416,416,3)) np.array(x, dtype=np.uint8)dtype=np.float32
        for ii, x in enumerate(range(0, image.shape[1], stepSize)):
           for iii,y in enumerate(range(0, image.shape[0], stepSize)):
        #for x in range(0, 4):
        #    for y in range(0, 4): 
              #window = image[x:x + w_width, y:y + w_height, :]
              #imgs(arrnp[x:x + w_width, y:y + w_height, :])
              #arrr.append(window)
              #ax[ii, iii].imshow(window)
              #ax[ii, iii].set_gid(idxAX)
              
              if int(ans_V[idxAX]) == 1:
                      #print x,y, idxAX# x + w_width, y, y + w_height, image.shape[1] - w_width, stepSize
                      #arrnp[x:x + w_width, y:y + w_height, :] = image[x:x + w_width, y:y + w_height, :]
                      #print arrnp[x:x + w_width, y:y + w_height, :], image[x:x + w_width, y:y + w_height, :]
                      fps16.append(image[x:x + w_width, y:y + w_height, :])
              else:
                      #arrnp[x:x + w_width, y:y + w_height, :] = image[x:x + w_width, y:y + w_height, :]*.255
                      #fps16.append(image[x:x + w_width, y:y + w_height, :]*.255)
                      fps16.append(image[x:x + w_width, y:y + w_height, :])
              idxAX += 1
        #print len(arrr)


        #plt.connect('button_press_event', onclick)
        #plt.show()
        #print "GOO"
        #imgs(arrnp)


        #return arrr
        #return arrnp, fps16 
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

    W_fc1 = weight_variable([3136, 512])
    b_fc1 = bias_variable([512])

    W_fc2 = weight_variable([512, ACTIONS])
    b_fc2 = bias_variable([ACTIONS])

    # input layer
    s = tf.placeholder("float", [None, 104, 104, 4])

    # hidden layers
    h_conv1 = tf.nn.relu(conv2d(s, W_conv1, 4) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)
   
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2, 2) + b_conv2)
    #h_pool2 = max_pool_2x2(h_conv2)

    h_conv3 = tf.nn.relu(conv2d(h_conv2, W_conv3, 1) + b_conv3)
    #h_pool3 = max_pool_2x2(h_conv3)

    #h_pool3_flat = tf.reshape(h_pool3, [-1, 256])
    #h_conv3_flat = tf.reshape(h_conv3, [-1, 1600])
    h_conv3_flat = tf.reshape(h_conv3, [-1, 3136])

    h_fc1 = tf.nn.relu(tf.matmul(h_conv3_flat, W_fc1) + b_fc1)

    # readout layer # cnn layer #считывающий слой
    readout = tf.matmul(h_fc1, W_fc2) + b_fc2

    return s, readout, h_fc1

#def gameaction(y):
#        reward = 0.1
#        terminal = False

        # check for score
#        playerMidPos = self.playerx + PLAYER_WIDTH / 2
#        for pipe in self.upperPipes:
#            pipeMidPos = pipe['x'] + PIPE_WIDTH / 2
#            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
#                self.score += 1
                #SOUNDS['point'].play()
#                reward = 1
#        if y == 1:
#            reward = 1
#        if y != 1:
#            terminal = True
#            reward = -1     


#        if isCrash:
            #SOUNDS['hit'].play()
            #SOUNDS['die'].play()
#            terminal = True
#            reward = -1
#    return reward, terminal

"""
def gameaction(y):
        print ("gameaction", y)
        reward = 0.1
        terminal = False
        if y == 1:
            reward = 1
        if y != 1:
            terminal = True
            reward = -1  
        print ("gameaction", y == 1, reward, terminal)   
        return reward, terminal
"""
def gameaction(y,x):
        print ("gameaction", y, x)
        reward = 0.1
        terminal = False
        if y[1] == x:
            reward = 1
            print ("GOOOD SCORE")
        else:
            terminal = True
            reward = -1  
            print ("BAD SCORE")
        #print ("gameaction",  y, x, reward, terminal) #y == 1, y, reward, terminal)   
        return reward, terminal


def trainNetwork(s, readout, h_fc1, sess):
    # define the cost function
    # s(input), readout(tf.matmul), h_fc1(tf.nn.relu)
    a = tf.placeholder("float", [None, ACTIONS])
    y = tf.placeholder("float", [None])
    readout_action = tf.reduce_sum(tf.multiply(readout, a), reduction_indices=1) #действие считывания - поэлементно умножаем readout и a - сумма по оси 1
    cost = tf.reduce_mean(tf.square(y - readout_action))
    train_step = tf.train.AdamOptimizer(1e-6).minimize(cost)

    # open up a game state to communicate with emulator \ открыть игровое состояние для связи с эмулятором
    #game_state = game.GameState()

    # store the previous observations in replay memory \ сохранить предыдущие наблюдения в памяти воспроизведения
    #D = deque()
    random.shuffle(traindict.keys())

    # printing
    a_file = open("logs_" + GAME + "/readout.txt", 'w')
    h_file = open("logs_" + GAME + "/hidden.txt", 'w')

    # saving and loading networks
    saver = tf.train.Saver()
    sess.run(tf.initialize_all_variables())
    
    checkpoint = tf.train.get_checkpoint_state("saved_networks")
    if checkpoint and checkpoint.model_checkpoint_path:
        saver.restore(sess, checkpoint.model_checkpoint_path)
        print("Successfully loaded:", checkpoint.model_checkpoint_path)
    else:
        print("Could not find old network weights")

    epsilon = INITIAL_EPSILON
    t = 0
    while "flappy bird" != "angry bird":
         random.shuffle(traindict.keys())
         for step, key in enumerate(traindict.keys()):
             resize_image, resize_label = get_batch(key)
             imgs(resize_image)
             resize_fps16 = window_slide(resize_image, resize_label)
             print ("NEW GAME")
             for ix, ops in enumerate(resize_fps16):
                x_t = cv2.cvtColor(cv2.resize(np.array(ops, dtype=np.uint8), (104, 104)), cv2.COLOR_BGR2GRAY)
                #s_t = np.stack((x_t*128, x_t*255, x_t*33, x_t*66), axis=2)
                s_t = np.stack((ops[:,:,0], ops[:,:,1], ops[:,:,2], x_t), axis=2)
                #s_t
                readout_t = readout.eval(feed_dict={s : [s_t]})[0]
                #print (resize_label[ix], readout_t)
                #imgs(ops)  
                #a_t = np.zeros([ACTIONS])
                print ("AT",readout_t, np.argmax(readout_t), s_t.shape)
                imgs(s_t)



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
