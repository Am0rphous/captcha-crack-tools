import os
import json
import numpy as np
import threading, cv2, os, time, requests, json, base64 
t_dict = {}

"""
with open("hydrantsMore.zip.txt", 'r') as g:
   for gh in g.readlines():    
        gh = gh.split('\n')[0].split(';') 
        key = gh[0].split("/")[-1] 
        ls = gh[1]
        #print ls != "[]", type(ls), ls == "None", ls#, [int(x) for x in gh[1].strip('][').split(', ')]
        t_dict[key] = []
        if ls != "[]" and ls != "None":
              t_dict[key].append([int(x) for x in ls.strip('][').split(', ')])#[gh[1].strip('][').split(', ')]
        else: 
              t_dict[key].append([])

#print t_dict
"""
def imgs(x):
      cv2.imshow('Rotat', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()


def cutimg(name, data, idx,answ, col):
	if True:
		#print (data.shape)
		im_w, im_h, im_c = data.shape
		w, h = im_w//col, im_h//col
		w_num, h_num = int(im_w/w), int(im_h/h)
		num = 0
                try: 
                        #print "post>"
		        for wi in range(0, w_num):
		           for hi in range(0, h_num):
		                num += 1
                                if num in answ:
		                   #imgs(data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
                                   
                                   y = "hydr/"+str(num)+str(idx)+"_"+name
                                   cv2.imwrite(y, data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
                                else:
		                   #imgs(data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
                                   
                                   y = "no_hydr/"+str(num)+str(idx)+"_"+name
                                   cv2.imwrite(y, data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
                                   #btt = data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :].tobytes()
                                   #print btt[:10]
                                   #to_file = open(y,"wb").write(btt)
		                   #cutpart = str(data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :]).encode("base64")
		                #imgs(i[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
		        #print deansw(ans)
                except IndexError: 
                   pass



with open("hydrants_dynamic.csv", 'r') as g:
   for gh in g.readlines():    
        gh = gh.split('\n')[0].split(';') 
        ls = gh[1].split(":")[-1]
        
        if ls != "[]":
           t_dict[gh[0]] = []
           #print gh[0], ls, [int(x) for x in ls.strip('][').split(", ")]#.split("/")[-1], gh[1]
           t_dict[gh[0]].append([int(x) for x in ls.strip('][').split(", ")])
        #else: 
        #   t_dict[gh[0]].append([])

#print t_dict

for ix, gh in enumerate(t_dict.keys()):
   #print gh, t_dict[gh][0]
   iop = cv2.imread("DynamicMoreHydrants/"+gh)
   #imgs(iop)
   PP = cutimg(gh, iop, ix, t_dict[gh][0], 3)


"""
match_dict = {}
match_mor_l_dict = {}
match_mor_v_dict = {}
for gh in t_dict.keys():
  ans_L = t_dict[gh][0]
  ans_V = t_dict[gh][1]
  print ans_L, ans_V
  if ans_L == ans_V:
      match_dict[gh] = [ans_L, ans_V]
  if ans_L > ans_V:
      match_mor_l_dict[gh] = [ans_L, ans_V]
  if ans_L < ans_V:
      match_mor_v_dict[gh] = [ans_L, ans_V]

print "All data: ", len(t_dict.keys()), "ans_L==ans_V: ", len(match_dict.keys()), "ans_L>ans_V: ", len(match_mor_l_dict.keys()),"ans_L<ans_V: ", len(match_mor_v_dict.keys())

  
"""
