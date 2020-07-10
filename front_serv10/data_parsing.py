import os

class DATA(object):
        def __init__(self):
            self.file = {}
            self.csv = "";
            
        def parseCSV(self):
              with open(self.csv, 'r') as g:
                             for gh in g.readlines():
                                         gh = gh.split('\n')[0].split(';') 
                                         try:
                                              list = self.file[gh[0]]
                                              if gh[1] != 'no_matching_images':
                                                  convRUC = [int(i) for i in gh[1].split(':')[1].split('/')]
                                                  list.append(convRUC)
                                                  self.file[gh[0]] = list
                                              else:
                                                  list.append([])
                                                  self.file[gh[0]] = list
                                         except KeyError:
                                              pass

        def parseIMG(self, dir_name, tp):
                path = "data/"+dir_name
                print ("PARSING",path)
                valid_images = [".jpg",".png"]
                for r, d, f in os.walk(path):
                    for ix, file in enumerate(f):
                        if valid_images[0] in file or valid_images[1] in file:
                          if int(tp) == 4:
                                   self.file[file.split(".")[0]] = [os.path.join(r, file)]
                          else:         
                                   self.file[os.path.join(r, file)] = [os.path.join(r, file)]
                        if ".csv" in file:
                           self.csv = os.path.join(r, file)
