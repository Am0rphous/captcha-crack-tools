#-*- coding: utf-8 -*-
#
import os
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import T4_4

#общее обучение нейронных сетей!

#Развивать архитектуры это одно 1 | cnn, capsul-cnn, rnn(LSTM?GRU) - какой вариативней?
#А спобы обучения и данные другое 2
#Мощночти оборудования 3 | Nvidia видеокарты 
#CTC метод более вариативный, seq2seq точный на одном наборе данных ( нет обобщения происходящего для применения в других примерах )

#Унифицированные нейроны с помощью видеокарты и процессора переключение между специализированными моделями на унифицированной архитектуре!!!
#за счет разности в скорости работы нашего мозга и видеокарты
#мы компенсируем разрыв в количестве нейроннов человека и нынешними мощностями???


#reddit, telegram, yotube, twitter, google - обьедяняют нас в одну большую человеческую нейронну сеть!!!
#Какая частота нашего мозга?http://nerealnost.net/forum/index.php?showtopic=13599
#Ритмы головного мозга — диагностируемые электрические колебания мозга — центрального отдела нервной системы человека, представляющего собой компактное скопление нервных клеток и их отростков. 
#Альфа ритм (α-ритм) — частота колебания варьируется от 8 до 13 Гц. Амплитуда 5-100 мкВ, наибольшая амплитуда проявляется при закрытых глазах и в затемненном помещении. 
#Регистрируется преимущественно в затылочной и теменной областях (зрительных отделах мозга).
# ИЗ вики
#                                *** *** ***
#Регистрируется у 85-95 % здоровых взрослых людей. Альфа-ритм связан с расслабленным состоянием бодрствования, покоя. 
#Альфа-волны возникают тогда, когда мы закрываем глаза и начинаем расслабляться. 
#                                *** *** ***
#Бета-ритм (β-ритм) — частота колебания варьируется от 14 до 40 Гц. Амплитуда колебания обычно до 20 мкВ. В норме он весьма слабо выражен и в большинстве случаев имеет амплитуду 3-7 мкВ.
#Регистрируется в области передних и центральных извилин. Распространяется на задние центральные и лобные извилины. 
#Депрессия бета-ритма. Бета-ритм связан с соматическими, сенсорными и двигательными корковыми механизмами и дает реакцию угасания на двигательную активацию или тактильную симуляцию. 
#При выполнении или даже умственном представлении движения бета-ритм исчезает в зоне соответствующей активности. Повышение бета-ритма — острая реакция на стрессовое воздействие. 
#                                *** *** ***
#Гамма-ритм (γ-ритм) — частота колебания выше 30 Гц, иногда достигает 100 Гц, амплитуда обычно не превышает 15 мкВ. Регистрируется в прецентральной, 
#фронтальной, височной и теменной зонах коры головного мозга.
#Общая характеристика.
#Обычно очень хорошо наблюдается при решении задач, которые требуют максимального сосредоточения внимания.  

#Частоты процессоров и видеокарт
#===============================
#     CPU
# Intel® Xeon® E7-8894 v4
# Количество ядер 24 
# Количество потоков 48 
# Базовая тактовая частота процессора 2,40 GHz
# Максимальная тактовая частота с технологией Turbo Boost 3,40 GHz 
#     GPU
# NVIDIA DGX-1 with Tesla V100
# Tesla V100 | TITAN RTX -> cuda core: 5120 | 4608,  tensor core: 640 | 576 + 72 rt core , 1246 MHz | 1350 MHz, 
# CUDA Cores 40,960
# Tensor Cores 5,120
# Тактовая частота 1000 GHz
# .... этих характеристик хватает что бы понять - если 200 Гц у самого умного человека планеты
# а частота 3,40 Ггц сравним превосходство переведя в гц 3400000000/200 = 17 000 000 в столько раз круче
# Герц (русское обозначение: Гц, международное обозначение: Hz) — единица частоты ... 109 Гц, гигагерц, ГГц, GHz, 10−9 Гц, наногерц, нГц, nHz. 1012 Гц .. 
# Разность в количестве нейронных связей размере
# 130 000 000 000 - человек, пк - 530000000 - в случае с пк я занизил цифры, а с человеком повысил
# Разность - 130 000 000 000/530000000 = 245.283018868 - мало :)))
# вопрос времени когда появиться интелект подобный скайнету и его скорей всего сделают таким
# так как трудно создать хаотичность без участия нашего мозга
# мы не получим скайнет только кто то его целонаправлненно не создаст!!!
# 106 слове в yolo v3, + рекурентные слои - нужно считать
# 600x600x3 - 50x50x100 - среднее - 2x2x1024, 4096, reshape несколько рас и снова в нейронную сеть с этими параметрами 1x1x ... 23x23x мысли нужно проверять!! 
# !!! => 26500000 среднее количество нейроннов в одной сети таких сетей может быть 20 - 530000000
# # https://github.com/Mekire/Conway-User-Interaction/blob/master/life.py
# алгоритм интересный может создать раздражение и мотивацию для сетей?
# caps не используем.

#более упорядоченей поэтому производительней
# у нас хаотично появляюься мысли
 


_COLOR = [8,136,19]

def imgs(x):
      cv2.imshow('Rotat', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()

def onkeypress(event):
    global object_list
    global tl_list
    global br_list
    global img
    if event.key == 'q':
        #print(object_list)
        tl_list = []
        br_list = []
        object_list = []
        img = None


def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata

    print 'x = %d, y = %d'%(ix, iy), event.inaxes.get_gid() #inaxes

    global coords
    coords = [ix, iy]

    return coords


def line_select_callback(eclick, erelease):
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))


    #rect = plt.Rectangle( (min(x1,x2),min(y1,y2)), np.abs(x1-x2), np.abs(y1-y2) )
    #ax.add_patch(rect)
    # Так выглядит дарк нет настоящий!
    # В массе для туристов созданные сайты и тор :)))

def not0(x):
  if x == 0:
     x+= 10
  if x == 416:
     x-= 10
  return x


def window_slide(image, put, ans_V):
        blackarr = np.zeros((104, 104), dtype=np.float32)

        stepSize = 104
        (w_width, w_height) = (104, 104) # window size
        arrr = []
        #fig, ax = plt.subplots(4, 4)
        idxAX = 0
        ddict = {}
        NEWc = np.argwhere(ans_V>0)
        #distances = np.sqrt((nonzero[:,0] - TARGET[0]) ** 2 + (nonzero[:,1] - TARGET[1]) ** 2)
        
        #print NEWc

        # CREATE 16 pad size = 104x104
        for ii, x in enumerate(range(0, image.shape[1], stepSize)):
           for iii,y in enumerate(range(0, image.shape[0], stepSize)):

              """
              if ans_V[ii, iii] == 1.0:# or ans_V[ii, iii] > ans_V[ii+1, iii+1]:
                   print ii, iii,'ANSWER', ans_V[ii, iii]
                   #Знаю координаты и знаю что в них ответ!!!
                   
              else:
                   pass
              """
        #for x in range(0, 4):
        #    for y in range(0, 4): 
              idxAX += 1
              
              #print (x,x + w_width), (y, y + w_height)
              #window = image[x:x + w_width, y:y + w_height, :]
              #arrr.append(window)
              
              #
              #if ans_V[ii, iii] == 1:
                      #print NEWc[idxAX-1]
              #        ax[ii, iii].imshow(blackarr)
              #        ax[ii, iii].set_gid(idxAX)
              #else:
              #        ax[ii, iii].imshow(window)
              #        ax[ii, iii].set_gid(idxAX)
              # FOR COORD's ...
              ddict[idxAX] = [(x,x + w_width), (y, y + w_height)]
        #print len(arrr)
        """
        new = fig.get_axes()
        # FROM RUCAPTCHA DATA
        for P in put:
              #print (int(P)-1)
              axexx = new[P-1]
              axexx.imshow(blackarr)
              #print  'SDSDSD', axexx.get_gid(), int(P)
        #fig.connect('button_press_event', onclick)
        """
        #plt.connect('button_press_event', onclick)
        #plt.show()
        #plt.close(fig)
        
        # NEW IMAGE AND COORD's rectangle
        #imgs(image)
        fig0, ax0 = plt.subplots()

        answ = T4_4.func_o(ans_V)
        #print answ

        dict_to = {}
 
        for u in answ.keys():
             if answ[u] != []:
                #print sorted(set(answ[u])) #answ[u]
                mi, mx = min(sorted(set(answ[u]))), max(sorted(set(answ[u])))
                #print mi, mx  

                Mx = mx+1 #max(put)
                Mi = mi+1 #min(put)
                #c0 = ddict[Mi]#[0]
                #c00 = ddict[Mx]#[1]
                print "OUT", ddict[Mi], ddict[Mx], Mi, Mx
                
                c1 = ddict[Mi]#[0]
                c2 = ddict[Mx]#[1]
                if c1[0][0] == c2[0][1] or c1[1][0] == c2[1][1]:
                      cc1, cc2 = min(c1), max(c2)
                      x0 = not0(cc1[0]) 
                      y0 = not0(cc1[1]) 
                      x1 = not0(cc2[0]) 
                      y1 = not0(cc2[1])
                      
                      print cc1[0], cc2[0]#c1[0][0], c1[1][0], c2[0][1], c2[1][1]
                      
                else:
                      x0 = not0(c1[0][0]) 
                      y0 = not0(c1[1][0]) 
                      x1 = not0(c2[0][1]) 
                      y1 = not0(c2[1][1])
                        #if dict_to[u] is type(list()): 
                #dict_to[u].append(list(x0,y0,x1,y1))
                #else:
                dict_to[u] = list([x0,y0,x1,y1])
                #   print u, x0,y0,x1,y1
                 
                #Y
                image[x0:x1, y1-3:y1, :] = _COLOR  # первая !!
                image[x0:x1, y0-3:y0, :] = _COLOR
                #X
                image[x0-3:x0, y0:y1, :] = _COLOR  # первая !!
                image[x1-3:x1, y0:y1, :] = _COLOR       
                
                #c1[0][1], c1[1][1], c2[0][1], c2[1][1]
        plt.imshow(image)
        RS = RectangleSelector(ax0, line_select_callback,
                                       drawtype='box', useblit=False,
                                       button=[1, 1],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)

        """
        RS1 = RectangleSelector(ax0, line_select_callback,
                                               drawtype='box', useblit=False,
                                               button=[1, 1],  # don't use middle button
                                               minspanx=5, minspany=5,
                                               spancoords='pixels',
                                               interactive=True)
        """

        RS.to_draw.set_visible(False)
        #RS1.to_draw.set_visible(True)
        
        RS.extents = (y0,y1, x0,x1)
        #RS1.extents = ((y0+20),(y1+20), x0-10,x1-10)

        fig0.canvas.draw()
        plt.show()
        #return arrr
        #print "@#@WE@#E@", dict_to#, image
        return dict_to, image

def getV(x,y):
    #print x, y
    for i in y:
        x[i-1] = 1.
    return x


def func_ld():
        with open('bicycsv/big_img.csv', 'r') as g:
             for gh in g:
                 gh = gh.split('\n') 
                 gh = gh[0].split(';')
                 namefile = gh[0]

                 
                 try:
                         gh = gh[1].split(':')[1]
                         namefile = 'bicycles4x4/'+namefile+'.jpg'

                         iop = cv2.imread(namefile)
                         iop = cv2.resize(iop, (416, 416))
                         ans_V = np.zeros([16]) # answer in vector
                         convRUC = [int(i) for i in gh.split('/')]
                         ans_V = getV(ans_V, convRUC)
                         ans_V = np.reshape(ans_V,(4,4))
                         
                         print ans_V#[ans_V[int(i)]=y for i in gh.split('/')]
                         #[ans_V[int(i)] if ans_V[int(i)] != 1. else 1. for i in gh.split('/')]#[1. for x in ans_V for ]
                         iop = window_slide(iop, convRUC, ans_V)#getline(iop)
                         return iop
                 except IndexError:
                         print gh



if __name__ == '__main__':


        with open('bicycsv/big_img.csv', 'r') as g:
             for gh in g:
                 gh = gh.split('\n') 
                 gh = gh[0].split(';')
                 namefile = gh[0]

                 
                 try:
                         gh = gh[1].split(':')[1]
                         namefile = 'bicycles4x4/'+namefile+'.jpg'

                         iop = cv2.imread(namefile)
                         iop = cv2.resize(iop, (416, 416))
                         ans_V = np.zeros([16]) # answer in vector
                         convRUC = [int(i) for i in gh.split('/')]
                         ans_V = getV(ans_V, convRUC)
                         ans_V = np.reshape(ans_V,(4,4))
                         
                         print ans_V#[ans_V[int(i)]=y for i in gh.split('/')]
                         #[ans_V[int(i)] if ans_V[int(i)] != 1. else 1. for i in gh.split('/')]#[1. for x in ans_V for ]
                         iop = window_slide(iop, convRUC, ans_V)#getline(iop)

                 except IndexError:
                         print gh
