import numpy as np
import cv2

def imgs(x):
      cv2.imshow('Rotat', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()

def getV(x,y):
    #print x, y
    for i in y:
        x[i-1] = 1.
    return x
    
def func_o(img):
        nonzero = np.argwhere(img>0)
        g = 0
        dk = {}
        def r_func(x,y):
                    for i in y:
                        if i in x:
                               y.remove(i)
                               x += y
                               r_func(list(set(x)),y)

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

        #print "DDDKk",dk

        ng = {}
        for i in dk.keys():
            for ii in dk.keys():
               if ii != i: 
                  
                  g = r_func(dk[i], dk[ii])
                  #print i, g
                  #if g is not None:
                  #   ng[i] = g

        return dk
        
def not0(x):
  if x == 0:
     x+= 10
  if x == 416:
     x-= 10
  return x
  
def window_slide():
        blackarr = np.zeros((104, 104), dtype=np.float32)
        stepSize = 104
        (w_width, w_height) = (104, 104) # window size
        idxAX = 0
        #distances = np.sqrt((nonzero[:,0] - TARGET[0]) ** 2 + (nonzero[:,1] - TARGET[1]) ** 2)
        # CREATE 16 pad size = 104x104
        for ii, x in enumerate(range(0, 416, stepSize)):
           for iii,y in enumerate(range(0, 416, stepSize)):
              idxAX += 1
              ddict[idxAX] = [(x,x + w_width), (y, y + w_height)]
ddict = {}   
dict_to = {}    
window_slide()     
image = np.ones(shape=(416, 416, 3), dtype=np.float32)
def func_1():
                    answ = [1,5,6,7,16]#[1,2,10]
                    ans_V = np.zeros([16]) # answer in vector
                    convRUC = [int(i) for i in answ]
                    ans_V = getV(ans_V, convRUC)
                    ans_V = np.reshape(ans_V,(4,4))
                    answ = func_o(ans_V)
                    
                    dict_to["GH"] = []
                    for u in answ.keys():
                             if answ[u] != []:
                                #print sorted(set(answ[u])) #answ[u]
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
                                #if dict_to[u] is type(list()): 
                                #dict_to[u].append(list(x0,y0,x1,y1))
                                #else:
                                #self.dict_to[u] = list([x0,y0,x1,y1])
                                # 
                                dict_to["GH"].append(list([y0, x0 ,y1,x1]))
                                image[x0:x1,y0:y1,:] = 0
#print ("Start")
func_1()
print (dict_to)
imgs(image)
