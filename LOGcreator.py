import timekeeper as timekeeper
import os.path
from variables import *
import threading



class LogWriter(object):

    def __init__(self):
        pass
        


    def openfile(self):
        day, month, year = timekeeper.getdate(timekeeper.reloadtimedate())
        day = str(day)
        month = str(month)
        year = str(year)
        
        if len(day) != 2:
            day = '0' + day
            
        if len(month) != 2:
            month = '0' + month
        
        
        self.day = day
        self.month = month
        self.year = year
        
        self.eightdigitdate = day + month + year #eg 29062014
        
        if os.path.exists(logsfolderpath):
        
            if os.path.isfile(logsfolderpath+str(self.eightdigitdate)+".txt"):
            
                file = open(logsfolderpath+self.eightdigitdate+'.txt', 'a')
              
              
            else:
            
                file = open(logsfolderpath+self.eightdigitdate+".txt", "w")
            
        
        else:
            os.makedirs(logsfolderpath)
            
            
        self.file = file
        
        
    def writethelog(self, contenttowriteineachline):
        self.file.write(str(timekeeper.gettimenow(timekeeper.reloadtimedate())) + ' ' + str(contenttowriteineachline) + '\n')


    def closefile(self):
        self.file.close()

        
    def readfile(self):
        #read_file = open("text.txt", "r")
        self.file.read()
        
       

        

def startnewloggerthread(string_to_log, to_log_or_not_to_log):

    if to_log_or_not_to_log:
    
        print "LOGGING--> " + string_to_log
        
        global logging_thread
        logging_thread = threading.Thread(target=logthis, args=(string_to_log,)) 
        #OR processThread = threading.Thread(target=processLine, args=[dRecieved])
        
        logging_thread.start()
        #logging_thread.join()
        
    else:
        print string_to_log
    
    
def logthis(string_to_log):
    writer = LogWriter()
    writer.openfile()
    writer.writethelog(string_to_log)
    writer.closefile()