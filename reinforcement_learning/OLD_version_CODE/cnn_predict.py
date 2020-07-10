# -*- coding:utf-8 -*-

import numpy as np
import tensorflow as tf
import os, cv2, glob

def batch_normalization_layer(input_layer, name = None, training = True, norm_decay = 0.99, norm_epsilon = 1e-3):
        batch = tf.layers.batch_normalization(inputs = input_layer, momentum = norm_decay, epsilon = norm_epsilon, center = True, scale = True, training = training, name = name)
        return tf.nn.leaky_relu(batch, alpha = 0.1)


def conv2d_layer(inputs, filters_num, kernel_size, name, use_bias = False, strides = 1):
        conv = tf.layers.conv2d(
            inputs = inputs, filters = filters_num,
            kernel_size = kernel_size, strides = [strides, strides], kernel_initializer = tf.glorot_uniform_initializer(),
            padding = ('SAME' if strides == 1 else 'VALID'), kernel_regularizer = tf.contrib.layers.l2_regularizer(scale = 5e-4), use_bias = use_bias, name = name)
        return conv


def residual_layer(inputs, filters_num, blocks_num, conv_index, training = True, norm_decay = 0.99, norm_epsilon = 1e-3):
        inputs = tf.pad(inputs, paddings=[[0, 0], [1, 0], [1, 0], [0, 0]], mode='CONSTANT')
        layer = conv2d_layer(inputs, filters_num, kernel_size = 3, strides = 2, name = "conv2d_" + str(conv_index))
        layer = batch_normalization_layer(layer, name = "batch_normalization_" + str(conv_index), training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
        conv_index += 1
        for _ in range(blocks_num):
            shortcut = layer
            layer = conv2d_layer(layer, filters_num // 2, kernel_size = 1, strides = 1, name = "conv2d_" + str(conv_index))
            #layer = self.myconvol(layer, conv_index, filters_num // 2, 1, 1)
            layer = batch_normalization_layer(layer, name = "batch_normalization_" + str(conv_index), training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
            conv_index += 1
            layer = conv2d_layer(layer, filters_num, kernel_size = 3, strides = 1, name = "conv2d_" + str(conv_index))
            layer = batch_normalization_layer(layer, name = "batch_normalization_" + str(conv_index), training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
            conv_index += 1
            layer += shortcut
        return layer, conv_index


def cnn(inputs, norm_decay = 0.99, norm_epsilon = 1e-3, training = True, conv_index = 1):
    unSample = inputs
    inputs = conv2d_layer(inputs, filters_num = 16, kernel_size = 3, strides = 1, name = "conv2d_" + str(conv_index))
    route = batch_normalization_layer(inputs, name = "batch_normalization_" + str(conv_index), training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
    conv_index += 1
    #### ROUTE 
    inputs = conv2d_layer(route, filters_num = 32, kernel_size = 1, strides = 1, name = "conv2d_" + str(conv_index))
    inputs = batch_normalization_layer(inputs, name = "batch_normalization_" + str(conv_index), training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
    conv_index += 1
    inputs = conv2d_layer(inputs, filters_num = 64, kernel_size = 3, strides = 2, name = "conv2d_" + str(conv_index))
    inputs = batch_normalization_layer(inputs, name = "batch_normalization_" + str(conv_index), training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
    conv_index += 1
    inputs = conv2d_layer(inputs, filters_num = 256, kernel_size = 1, strides = 2, name = "conv2d_" + str(conv_index))
    inputs = batch_normalization_layer(inputs, name = "batch_normalization_" + str(conv_index), training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
    conv_index += 1
    print inputs.shape


    #### ROUTE 
    route, conv_index = residual_layer(route, conv_index = conv_index, filters_num = 64, blocks_num = 1, training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
    route, conv_index = residual_layer(route, conv_index = conv_index, filters_num = 256, blocks_num = 16, training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
   
    unSample_0 = tf.image.resize_nearest_neighbor(inputs, [1 * tf.shape(inputs)[1], 1 * tf.shape(inputs)[1]], name='upSample_0')
 
    """
    inputS = conv2d_layer(inputs, filters_num = 255, kernel_size = 3, strides = 1, name = "conv_" + str(conv_index))
    inputS = batch_normalization_layer(inputS, name = "deconv_" + str(conv_index), training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
    #conv_index += 1

    unSample2 = inputS#tf.image.resize_nearest_neighbor(inputs, [2 * tf.shape(inputs)[1], 2 * tf.shape(inputs)[1]], name='upSample_0')
    """
    unSample2 = inputs

    route0 = tf.concat([unSample_0, route], axis = -1, name = 'route_0')
    print route0.shape, route.shape, unSample_0.shape
    out = conv2d_layer(route0, filters_num = 256, kernel_size = 3, strides = 2, name = "conv2d_" + str(conv_index))
    out = batch_normalization_layer(out, name = "batch_normalization_" + str(conv_index), training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
    conv_index += 1
    out = conv2d_layer(out, filters_num = 64, kernel_size = 1, strides = 2, name = "conv2d_" + str(conv_index))
    out = batch_normalization_layer(out, name = "batch_normalization_" + str(conv_index), training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
    conv_index += 1
    out = conv2d_layer(out, filters_num = 32, kernel_size = 3, strides = 2, name = "conv2d_" + str(conv_index))
    out = batch_normalization_layer(out, name = "batch_normalization_" + str(conv_index), training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
    conv_index += 1

    out = conv2d_layer(out, filters_num = 16, kernel_size = 1, strides = 2, name = "conv2d_" + str(conv_index))
    out = batch_normalization_layer(out, name = "batch_normalization_" + str(conv_index), training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
    conv_index += 1

    out = conv2d_layer(out, filters_num = 1, kernel_size = 3, strides = 1, name = "conv2d_" + str(conv_index))
    out = batch_normalization_layer(out, name = "batch_normalization_" + str(conv_index), training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
    conv_index += 1

    #out = conv2d_layer(out, filters_num = 16, kernel_size = 1, strides = 2, name = "conv2d_" + str(conv_index))
    #out = batch_normalization_layer(out, name = "batch_normalization_" + str(conv_index), training = training, norm_decay = norm_decay, norm_epsilon = norm_epsilon)
    #conv_index += 1
 
    return out, unSample, unSample2



def get(i):
        idxAX = 0
        list = []
        for ii, x in enumerate(range(0, 416, 104)):
           for iii,y in enumerate(range(0, 416, 104)):
              idxAX += 1

              #i[idxAX] = [(x,x + 104), (y, y + 104)]
              list.append(i[x:x + 104,y:y + 104,:])

        return tf.stack(list)

def imgs(x):
      cv2.imshow('Rotat', np.array(x, dtype=np.uint8))
      cv2.waitKey(0)
      cv2.destroyAllWindows()

def func_loss(model, y):
    cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(labels=y, logits=model)
    loss = tf.reduce_mean(cross_entropy)
    return loss



traindict = {}
def getV(x,y):
    #print x, y
    for i in y:
        x[i-1] = 1.
    return x
def readdata():
            with open("data/taxi4x4/taxi.csv", 'r') as g:
                      g = g.readlines()
                      for igh, gh in enumerate(g[:]):
                          gh = gh.split('\n') 
                          gh = gh[0].split(';')
                          namefile = 'data/taxi4x4/img/'+gh[0]+'.jpg'
                          print namefile
                          if gh[1] != 'no_matching_images':
                                  convRUC = [int(i) for i in gh[1].split(':')[1].split('/')]
                                  ans_V = np.zeros([16]) # answer in vector
                                  ans_V = getV(ans_V, convRUC)
                                  traindict[namefile] = ans_V


def get_batch(k):

             #try:
                     image = cv2.imread(k) 
                     resize_image = cv2.resize(image, (416, 416))
                 
                     #resize_label = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
                     resize_label = np.reshape(np.array(traindict[k]), [16, 1])
                     return resize_image, resize_label
             #except:
                     #pass


#def softmax(x):
#    """Compute softmax values for each sets of scores in x."""
#    e_x = np.exp(x - np.max(x))
#    return e_x / e_x.sum(axis=0) # only difference

def softmax(x):
  return np.exp(x)/np.sum(np.exp(x),axis=0)

def sigmoid(a):
  return 1. / (1. + np.exp(-a))


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

def imcr(i):
        NWLS = []
	if True:
	        im_w, im_h, im_c = i.shape
                w, h = im_w//4, im_h//4
		w_num, h_num = int(im_w/w), int(im_h/h)
                
                num = 0
		for wi in range(0, w_num):
		    for hi in range(0, h_num):
			#box = (wi*w, hi*h, (wi+1)*w, (hi+1)*h)
                        
                        num += 1
                                            
                        #32448.0 = 100%
                        #P = A1 / A2 * 100. 
                        #A1= A2 * P / 100.
                        #GGGG = 32448 * 3 / 100
                        P_R = (np.sum(i[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :]) / 32448) * 100
                        P_R = P_R - 100
                        siZe = i[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :]
                        #print P_R, np.sum(i[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :]), im_w, im_h, im_c, siZe.shape
                        #i[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :] = 1
                        #print int(P_R) #np.sum(i[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :]), i[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :].shape, P_R
                        #if 35 < int(P_R):
                        #if 20 < int(P_R):
                        if 10 < int(P_R): #10
                              NWLS.append(str(num))
                        #if NWLS == []:
                        #      if P_R > 20:
                        #         NWLS.append(str(num))
                        else:
                              pass
        return NWLS, np.array(i)     



x = tf.placeholder(shape = [416, 416, 3], dtype = tf.float32) 
y = tf.placeholder(shape = [16, 1], dtype = tf.float32) 
x1 = get(x)
model, unSampleS, unSampleS2 = cnn(x1)
model = tf.reshape(model, [-1, 1 * 1 * 1])

####->>>THIS
#with tf.variable_scope("one"):
#     

print x.shape, x1.shape, model.shape
print "DATA LOAD"
#readdata()
loss = func_loss(model, y)


global_step = tf.Variable(0, trainable = False)
lr = tf.train.exponential_decay(0.001, global_step, decay_steps = 2000, decay_rate = 0.8)
optimizer = tf.train.AdamOptimizer(learning_rate = lr)
train_op = optimizer.minimize(loss = loss, global_step = global_step)



init = tf.global_variables_initializer() #tf.initialize_all_variables()
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.95)


saver = tf.train.Saver()
with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
     sess.run(init)
     saver.restore(sess, "model_save/model.ckpt-135138")

     #Train
     """
     image = cv2.imread("1349039.jpg") 
     resize_image = cv2.resize(image, (416, 416))
     resize_label = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
     resize_label = np.reshape(np.array(resize_label), [16, 1])
     
     
     for epoh in range(100):

         for step, key in enumerate(traindict.keys()):
             resize_image, resize_label = get_batch(key)
             #print resize_label
             tr_E = sess.run([train_op,loss], feed_dict={x: resize_image, y: resize_label})
             
             if step % 50 == 0:
                  print tr_E[1] 
             if step % 1000 == 0:
                  checkpoint_path = os.path.join("model_save", 'model.ckpt')
                  saver.save(sess, checkpoint_path, global_step = global_step)
         if epoh % 3 == 0:
             checkpoint_path = os.path.join("model_save", 'model.ckpt')
             saver.save(sess, checkpoint_path, global_step = global_step)
     
     """
     #Test
     list_file = glob.glob('data/taxi4x4/img/*')
     for F in list_file[:10]:
             image = cv2.imread(F)#1349000.png, 1346959.jpg, 1346862.jpg, 1346862.jpg 1346822.jpg
             resize_image = cv2.resize(image, (416, 416))
             #imgs(resize_image)
             #correct = tf.argmax(model)
             im, uim, uim2 = sess.run([model, unSampleS, unSampleS2], feed_dict={x: resize_image})
            

             answ = []
             #print softmax(im)
             for ix, h in enumerate(softmax(im)):
                #if h[0] > 0.05:
                if h[0] > 0.046:
                            answ.append(ix+1)
                            print ix+1, sigmoid(h[0])
             print answ, uim.shape, uim2.shape

             ##########
             h_z = 416 / 4
             resize_image[0:, h_z:(h_z+5), :] = 255
             resize_image[0:, (h_z*2):((h_z*2)+5), :] = 255
             resize_image[0:, (h_z*3):((h_z*3)+5), :] = 255
             resize_image[0:, (h_z*4):((h_z*4)+5), :] = 255
             # w line
             #      x          y
             resize_image[h_z:(h_z+5), 0:, :] = 255
             resize_image[(h_z*2):((h_z*2)+5), 0:, :] = 255
             resize_image[(h_z*3):((h_z*3)+5), 0:, :] = 255
             resize_image[(h_z*4):((h_z*4)+5), 0:, :] = 255

             imgs(resize_image)
             ##########
     """"""
     #
     """
             # VISUALIZATION
             imgS = uim[:,:,:,:]
             imgS2 = uim2[:,:,:,:]
             Zeros = np.zeros([imgS2.shape[0], imgS2.shape[1], imgS2.shape[2], imgS2.shape[3]])
             newImg = np.zeros([416, 416])
             newImg2 = np.zeros([416, 416, 3])
             
             #for ixx in range(0, 5):
             for ixx in range(0, imgS.shape[0]):
                         # IMAGES --->
                         im_w, im_h = 416, 416
                         w, h = im_w//4, im_h//4
		         w_num, h_num = int(im_w/w), int(im_h/h)
                         #print w_num, h_num
                         num = 0
                         for wi in range(0, w_num):
		            for hi in range(0, h_num):
			        #box = (wi*w, hi*h, (wi+1)*w, (hi+1)*h)
                                
                                #print imgS[ixx,:,:,:].shape
                                if num+1 in answ:                    
                                  newImg2[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :] = imgS[num,:,:,:]
                                num += 1
                                #print siZe.shape     


                         # KERNAL --->
                         kernal = (imgS2[ixx,:,:,:]+255)*255#128#255
                         step = 0
                         
                         for mX in range(0, 416, 26):
                            for mY in range(0, 416, 26): 
                              newImg[mY:mY+(26), mX:mX+(26)] = kernal[:,:,step]
          
                              step += 1
          
                               
                         imgs(newImg)
             imgs(newImg2)
     """
     #Выбрать все 0 и выбрать все больше 0
     # в 0/3 обьема 
     # посчитать колво с 0 и с 255
     # взять 30 процентов от заполнения и


