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
    D = deque()
    random.shuffle(traindict.keys())

    # printing
    a_file = open("logs_" + GAME + "/readout.txt", 'w')
    h_file = open("logs_" + GAME + "/hidden.txt", 'w')

    # get the first state by doing nothing and preprocess the image to 80x80x4 \ получить первое состояние, ничего не делая, и предварительно обработать изображение до 80x80x4
    #do_nothing = np.zeros(ACTIONS)
    #do_nothing[0] = 1
    ####
    r_image, r_label = get_batch(traindict.keys()[0])
    r_fps16 = window_slide(r_image, r_label)
    #r_0, terminal = gameaction(r_label[0])
    #x_t = cv2.cvtColor(cv2.resize(np.array(r_fps16[0], dtype=np.uint8), (416, 416)), cv2.COLOR_BGR2GRAY)
    #ret, x_t = cv2.threshold(x_t,1,255,cv2.THRESH_BINARY)
    #s_t = np.stack((x_t, x_t, x_t, x_t), axis=2)
    #s_t = np.stack((x_t, x_t, x_t, x_t), axis=2)
    s_t = np.append(r_fps16[0][:, :, :2], r_fps16[0][:, :, :2], axis=2)
 
    #imgs(s_t)
    print (s_t.shape, r_label[2])
    # saving and loading networks
    saver = tf.train.Saver()
    sess.run(tf.initialize_all_variables())
    
    checkpoint = tf.train.get_checkpoint_state("saved_networks_6")
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
             resize_fps16 = window_slide(resize_image, resize_label)
             print ("NEW GAME")
             #imgs(resize_fps16[0])
             
             for ix, ops in enumerate(resize_fps16):
                #imgs(s_t)
                readout_t = readout.eval(feed_dict={s : [s_t]})[0]
                #print (resize_label[ix], readout_t)
                #imgs(ops)  
                a_t = np.zeros([ACTIONS])
                action_index = 0
                if t % FRAME_PER_ACTION == 0:
                    if random.random() <= epsilon:
                        #print("----------Random Action----------")
                        action_index = random.randrange(ACTIONS)
                        a_t[random.randrange(ACTIONS)] = 1
                    else:
                        action_index = np.argmax(readout_t)
                        #print ("----------Action----------", action_index, "<<<<>>>>", readout_t)
                        a_t[action_index] = 1
                else:
                    #print ("----------Do nothing----------", action_index, "<<<<>>>>", readout_t)
                    a_t[0] = 1 # do nothing
                #print ("AT", a_t, random.randrange(ACTIONS), readout_t, np.argmax(readout_t))
                # scale down epsilon \ уменьшать эпсилон
                if epsilon > FINAL_EPSILON and t > OBSERVE:
                    epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE
   
                #     
                #
                #imgs(ops) 
                #r_t, terminal = gameaction(resize_label[ix])#
                #print (len(D))
                x_t1 = ops
                x_t1 = np.reshape(x_t1, (416, 416, 3))
                s_t1 = np.append(x_t1[:, :, :2], s_t[:, :, :2], axis=2) 
   
                if ix>0:
                        r_t, terminal = gameaction2(a_t, resize_label[ix], D[ix-1][1], resize_label[ix-1]) 
                else:
                        r_t, terminal = gameaction(a_t, resize_label[ix])
                        
                D.append((s_t, a_t, r_t, s_t1, terminal))
                if len(D) > REPLAY_MEMORY:
                        D.popleft()

                #if ix>0: 
                #   print (D[ix][1], D[ix][2], D[ix][4], "NEW == OLD", D[ix-1][1], D[ix-1][2], D[ix-1][4])

                if t > OBSERVE:
                    # sample a minibatch to train on \ образец мини-пакета для обучения на
                    minibatch = random.sample(D, BATCH) 
                    #print ("minibatch", len(minibatch))
                    # get the batch variables
                    s_j_batch = [d[0] for d in minibatch]
                    a_batch = [d[1] for d in minibatch]
                    r_batch = [d[2] for d in minibatch]
                    s_j1_batch = [d[3] for d in minibatch]

                    y_batch = []
                    readout_j1_batch = readout.eval(feed_dict = {s : s_j1_batch})
                    for i in range(0, len(minibatch)):
                        terminal = minibatch[i][4]
                        # if terminal, only equals reward \ если терминал, только равняется вознаграждению
                        if terminal:
                            y_batch.append(r_batch[i])
                        else:
                            y_batch.append(r_batch[i] + GAMMA * np.max(readout_j1_batch[i]))

                    # perform gradient step \ выполнить шаг градиента
                    train_step.run(feed_dict = {
                        y : y_batch,
                        a : a_batch,
                        s : s_j_batch}
                    )

                # update the old values \ обновить старые значения
                s_t = s_t1
                t += 1
                #cv2.imshow('Rotat', np.array(s_t1, dtype=np.uint8))
                cv2.imshow('Rotat', np.array(s_t, dtype=np.uint8))
                #cv2.waitKey(0)
                cv2.waitKey(33)

                #cv2.destroyAllWindows()
                #print ("END")
                # save progress every 10000 iterations
                if t % 10000 == 0:
                    saver.save(sess, 'saved_networks_6/' + GAME + '-dqn', global_step = t)
                #print ("THIS START - 0", t)
                # print info
                state = ""
                if t <= OBSERVE:
                    state = "observe"
                elif t > OBSERVE and t <= OBSERVE + EXPLORE:
                    state = "explore"
                else:
                    state = "train"
             #
             #print (resize_image, resize_labe)
          
             """"""


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
