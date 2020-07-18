#-*- coding: utf-8 -*-
#
import os
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector

#
_COLOR = [8,136,19]
dict_to = {}
d_dict = {}
#

def getV(x,y):
    #print x, y
    for i in y:
        x[i-1] = 1.
    return x

def imgs(x):
      cv2.imshow('Rotat', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()

def not0(x):
  if x == 0:
     x+= 10
  if x == 416:
     x-= 10
  return x

def draw_rect(image, y0, x0 ,y1, x1):
                image = cv2.imread(image)
                image = cv2.resize(image, (416, 416))
                #Y
                image[x0:x1, y1-3:y1, :] = _COLOR  # первая !!
                image[x0:x1, y0-3:y0, :] = _COLOR
                #X
                image[x0-3:x0, y0:y1, :] = _COLOR  # первая !!
                image[x1-3:x1, y0:y1, :] = _COLOR 

                imgs(image)
###############################################################
###############################################################
#### ERROR

def func_o(img):
        nonzero = np.argwhere(img>0)

        g = 0
        dk = {}

        def r_func(x,y):
                    for i in y:
                        if i in x:
                               #print ">>>>", x, y
                               y.remove(i)
                               
                               x += y
                               r_func(list(set(x)),y)
                        #if len(x) == len(y)

        for idx, val in enumerate(nonzero):
                #print idx, val
                dk[idx] = [] 
                for index, value in enumerate(np.ndenumerate(img)):
                    if value[1] == 1:
                        #print index, value[0], idx, val, np.sqrt((val[0] - value[0][0]) ** 2 + (val[1] - value[0][1]) ** 2)
                        if np.sqrt((val[0] - value[0][0]) ** 2 + (val[1] - value[0][1]) ** 2) == 0:
                            #print 'NULL', val, value[0], idx, index
                            dk[idx].append(index)
                        if np.sqrt((val[0] - value[0][0]) ** 2 + (val[1] - value[0][1]) ** 2) == 1:
                            #print 'ONE', val, value[0], idx 
                            dk[idx].append(index)
                        if np.sqrt((val[0] - value[0][0]) ** 2 + (val[1] - value[0][1]) ** 2) == 1.4142135623730951:
                            #print 'ONE_1', val, value[0], idx
                            dk[idx].append(index)


        ng = {}
        for i in dk.keys():
            for ii in dk.keys():
               if ii != i: 
                  
                  g = r_func(dk[i], dk[ii])


        return dk


def window_slide(image, put, ans_V):
        blackarr = np.zeros((104, 104), dtype=np.float32)

        stepSize = 104
        (w_width, w_height) = (104, 104) # window size
        arrr = []
        idxAX = 0
        ddict = {}
        NEWc = np.argwhere(ans_V>0)

        # CREATE 16 pad size = 104x104
        for ii, x in enumerate(range(0, image.shape[1], stepSize)):
           for iii,y in enumerate(range(0, image.shape[0], stepSize)):
              idxAX += 1
              ddict[idxAX] = [(x,x + w_width), (y, y + w_height)]

        answ = T4_4.func_o(ans_V)


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


#################################################
# LOGIC #########################################
#################################################

ddict = {}
idxAX = 0
for ii, x in enumerate(range(0, 416, 104)):
   for iii,y in enumerate(range(0, 416, 104)):
       idxAX += 1
       ddict[idxAX] = [(x,x + 104), (y, y + 104)]




with open('motocsv/big_img.csv', 'r') as g:
             for gh in g:
                 gh = gh.split('\n') 
                 gh = gh[0].split(';')
                 namefile = gh[0]

                 #print namefile
                 try:
                         gh = gh[1].split(':')[1]
                         #namefile = 'bicycles4x4/'+namefile+'.jpg'


                         ans_V = np.zeros([16]) # answer in vector
                         convRUC = [int(i) for i in gh.split('/')]
                         ans_V = getV(ans_V, convRUC)
                         d_dict[namefile] = ans_V
                         
                         
                         #print ans_V
                 except IndexError:
                         pass #print gh

#### NEW ########################

class Graph: 
  
    def __init__(self, row, col, g): 
        self.ROW = row 
        self.COL = col 
        self.graph = g 
  
    # A function to check if a given cell  
    # (row, col) can be included in DFS 
    def isSafe(self, i, j, visited): 
        # row number is in range, column number 
        # is in range and value is 1  
        # and not yet visited 
        return (i >= 0 and i < self.ROW and 
                j >= 0 and j < self.COL and 
                not visited[i][j] and self.graph[i][j]) 
              
  
    # A utility function to do DFS for a 2D  
    # boolean matrix. It only considers 
    # the 8 neighbours as adjacent vertices 
    def DFS(self, i, j, visited): 
  
        # These arrays are used to get row and  
        # column numbers of 8 neighbours  
        # of a given cell 
        rowNbr = [-1, -1, -1,  0, 0,  1, 1, 1]; 
        colNbr = [-1,  0,  1, -1, 1, -1, 0, 1]; 
          
        # Mark this cell as visited 
        visited[i][j] = True
  
        # Recur for all connected neighbours 
        for k in range(8): 
            if self.isSafe(i + rowNbr[k], j + colNbr[k], visited): 
                self.DFS(i + rowNbr[k], j + colNbr[k], visited) 
  
  
    # The main function that returns 
    # count of islands in a given boolean 
    # 2D matrix 
    def countIslands(self): 
        # Make a bool array to mark visited cells. 
        # Initially all cells are unvisited 
        visited = [[False for j in range(self.COL)]for i in range(self.ROW)] 
  
        # Initialize count as 0 and travese  
        # through the all cells of 
        # given matrix 
        count = 0
        for i in range(self.ROW): 
            for j in range(self.COL): 
                # If a cell with value 1 is not visited yet,  
                # then new island found 
                if visited[i][j] == False and self.graph[i][j] ==1: 
                    # Visit all cells in this island  
                    # and increment island count 
                    self.DFS(i, j, visited) 
                    count += 1
  
        return count 


#Сначала пройду по колонкам потом строкам
#Найду максимум/минимум в колонках и строках
# без рекурсии не обойтись!
# промежуточный список в который добавлю все позичии строк и колонок
#Создаю финальную рамку учитывать нужно соседей!

def rec(x):
    mls = []
    for ix, i in enumerate(x):
        if int(i) == 1:
           mls.append(ix)
           
    return mls

def m_m(x):
    ls = []
    for i in x.keys():
        ls += x[i]
        #if x[i] != []:
        #   mi, mx = min(sorted(set(x[i]))), max(sorted(set(x[i])))
        #   print mi, mx
    mi, mx = min(sorted(set(ls))), max(sorted(set(ls)))
    return mi, mx

def co_ro(i):
    DC = {}
    for x in range(4): # Временнно
        #print x,"x", i[x]#[y]
        #DC[x] = []
        DC[x] = rec(i[x])
        #for y in range(4): # Временно
          # print i[x][y] 
    mix, mxx = m_m(DC)
    print "END X", mix, mxx
        


    for y in range(4):
        g = [j[y] for j in i]
        #print y, "y", g
        DC[y] = rec(g)
    miy, mxy = m_m(DC)
    print "END Y", miy, mxy

    return mix, mxx, miy, mxy

import random
ls_r = list(range(10,30))


def get_gh(x, namefile):
    print "ANSWER 4x4 SHAPE\n",x
    row = len(x) 
    col = len(x[0]) 
    #print row, col
    mix, mxx, miy, mxy = co_ro(x)    
    xxx = x
    xxx[miy:mxy, mix:mxx] = 1

    x[miy, mix] = 1
    x[mxy, mxx] = 1
    #x[0, 0] = 1
    print "NEW ANSWER\n", x
    print "XXX\n",xxx
    #g = Graph(row, col, x) 
    #print "Number of islands is:"
    #print g.countIslands() 
    answ = func_o(x)

    pk_r = 25 #random.choice(ls_r)

    for u in answ.keys():
       if answ[u] != []:
                 answ[u] = sorted(set(answ[u]))
                 mi, mx = min(sorted(set(answ[u]))), max(sorted(set(answ[u])))

                 Mx = mx+1 #max(put)
                 Mi = mi+1 #min(put)
                                        #print mi, mx, Mi, Mx 
                 c1 = ddict[Mi]#[0]
                 c2 = ddict[Mx]#[1]
                 x0 = not0(c1[0][0]) 
                 y0 = not0(c1[1][0]) 
                 x1 = not0(c2[0][1]) 
                 y1 = not0(c2[1][1])


                 #------------------
                 
                 #x0 = not0(abs(c1[0][0]+pk_r))
                 #y0 = not0(abs(c1[1][0]+pk_r))
                 #x1 = not0(abs(c2[0][1]-pk_r))
                 #y1 = not0(abs(c2[1][1]-pk_r))
                 #------------------
    

    draw_rect(namefile, y0, x0 ,y1, x1)


#################################


#with open('ERROR.txt', 'r') as g:
with open('tr0M.txt', 'r') as g:
             #idx = 0
             g = g.readlines()
             for idx, gh in enumerate(g):
                 gh = gh.split('\n')[0].split('/')[-1].split('.')[0]
                 
                 namefile = 'motos4x4/'+gh+'.jpg'
                 #
                 dict_to[gh] = []

                 try:
                         ghh = 'Labels/'+gh+'.txt'
                         print idx, ghh
                         P = open(ghh, 'r')
                         P = P.read().split('\n')[0]
                         coord = P.split(' ')[1:]

                         #print "ERRROR FILE",int(coord[0]), int(coord[1]), int(coord[2]), int(coord[3])
                         #x0 = not0(int(coord[0])) 
                         #y0 = not0(int(coord[1])) 
                         #x1 = not0(int(coord[2])) 
                         #y1 = not0(int(coord[3]))
                         #dict_to[gh].append(list([y0, x0 ,y1, x1]))


                         ans_V = d_dict[gh]
                         ans_V = np.reshape(ans_V,(4,4))

                         answ = func_o(ans_V)

                         """
                         for u in answ.keys():
                             if answ[u] != []:
                                #print sorted(set(answ[u])) #answ[u]
                                #mi, mx = min(sorted(set(answ[u]))), max(sorted(set(answ[u])))
                                answ[u] = sorted(set(answ[u]))

                                mi, mx = min(sorted(set(answ[u]))), max(sorted(set(answ[u])))
                                #print mi, mx  

                                Mx = mx+1 #max(put)
                                Mi = mi+1 #min(put)
                                #print mi, mx, Mi, Mx 
                                c1 = ddict[Mi]#[0]
                                c2 = ddict[Mx]#[1]

                                x0 = not0(c1[0][0]) 
                                y0 = not0(c1[1][0]) 
                                x1 = not0(c2[0][1]) 
                                y1 = not0(c2[1][1])
                         """
                         #print "ANSWER 4x4 SHAPE\n",ans_V
                         #AAA = np.zeros(16)
                         #AAA = np.reshape(AAA,(4,4))
                         #AAA[1,1]=1
                         #AAA[2,2]=1
                         #print "AAA\n",AAA 
                         get_gh(ans_V,namefile) 
                         #---->get_gh(AAA)
                         #print "ANSWER COORD's main_1_1", y0, x0 ,y1, x1
                         #print "ANSWER one or two", answ
                         #draw_rect(namefile, y0, x0 ,y1, x1)
                         print "########## END ###########"

                 except IOError:
                         #idx+=1
                         #print gh, idx 
                         dict_to[gh].append(list([0, 0, 0, 0]))


                 except KeyError:
                         pass




           
