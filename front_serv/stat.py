import os
import json 
t_dict = {}


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
""""""
with open("hydrants.csv", 'r') as g:
   for gh in g.readlines():    
        gh = gh.split('\n')[0].split(';') 
        ls = gh[1].split(":")[-1]
        if ls != "[]":
           #print gh[0], ls, [int(x) for x in ls.strip('][').split(", ")]#.split("/")[-1], gh[1]
           t_dict[gh[0]].append([int(x) for x in ls.strip('][').split(", ")])
        else: 
           t_dict[gh[0]].append([])

#print t_dict
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

  
""""""
