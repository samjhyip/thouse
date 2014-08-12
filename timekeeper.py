from variables import *
from datetime import datetime
import pytz
from pytz import timezone
import time
import threading
from collections import OrderedDict
from index import *


#misc
#now = datetime.now()
#print now
#print now.year
#print now.month
#print now.day
#print '%s/%s/%s' % (now.month, now.day, now.year)
#print '%s:%s:%s' % (now.hour, now.minute, now.second) 

#pytz
#for x in timezone: print x  --> to show entire list of timezones.


format = '%d-%m-%Y %H:%M:%S %Z%z'



def reloadtimedate():
    utc = pytz.utc
    utc_dt = utc.localize(datetime.utcfromtimestamp(time.time())) #time.time() = CPU time
   
    #prints out utc time
    #print utc_dt.strftime(format)

    sg_timezone = timezone('Asia/Singapore')
    sg_daytime = sg_timezone.normalize(utc_dt.astimezone(sg_timezone))
    
    return sg_daytime
    

def gettimenow(sg_daytime):

    global timenow
    timenow = sg_daytime.strftime(format) #this is a string
    #print sg_daytime.hour, sg_daytime.minute, sg_daytime.second
    
    return timenow
    
    
def getdate(sg_daytime):

    day = int(sg_daytime.day)
    month = int(sg_daytime.month)
    year = int(sg_daytime.year)
    
    return (day), (month), (year)
    
    
    #in 24 hour time format
def gettimebreakdown():
    
    utc = pytz.utc
    utc_dt = utc.localize(datetime.utcfromtimestamp(time.time())) #time.time() = CPU time
    #prints out utc time
    #print utc_dt.strftime(format)

    sg_timezone = timezone('Asia/Singapore')
    sg_daytime = sg_timezone.normalize(utc_dt.astimezone(sg_timezone))

    return sg_daytime.hour, sg_daytime.minute
    
    
def timedtask_menu():
    pass
    
    
def collecttimeschedule():
    
    print "Welcome to to time scheduler!\nI will help you operate the switch even when you are not around.\nAll you have to do is to give me instructions!\n"
    
    collectpinno = raw_input("Which pin do you want to operate?\n")
    
    if int(collectpinno) in pins_to_use:
        
        isvalidtimetoswitchoncollected = False
        
        while isvalidtimetoswitchoffcollected = False:
            timetoswitchoninput = raw_input("What time do you want the switch to start operating?\n")
                
            if len(str(switchoninput)) == 4:
                isvalidtimetoswitchoncollected = True
                
                applianceswitchoffyesno = raw_input("Is there a time to stop operation?\n")
                    
                    
                    
                if str(applianceswitchoffyesno) == 'y' or str(applianceswitchoffyesno) == 'Y':
                    isvalidtimetoswitchoffcollected = False
                
                    while isvalidtimetoswitchoffcollected == False:
                        timetoswitchoffinput = raw_input("What time do you want the switch to stop operating?\n")
                    
                        if len(str(switchoffinput)) == 4:
                            isvalidtimetoswitchoffcollected = True
                            return collectpinno, timetoswitchoninput, timetoswitchoffinput
                    
                        else:
                            print timetoswitchoffinput, " is not a valid XXXX time input.\nTry again."
         
         
            
                elif str(applianceswitchoffyesno) == 'n' or str(applianceswitchoffyesno) == 'N':
                    timetoswitchoffinput = '9999'
                    return collectpinno, timetoswitchoninput, timetoswitchoffinput
                
            else:
                print timetoswitchoninput, " is not a valid XXXX time input.\nTry again."
                
lists_of_tasks_to_run = OrderedDict()


class Backgroundtasks(object):
    
    def __init__(self, collectpinno, timetoswitchoninput, timetoswitchoffinput):
    
        self.pin_no = collectpinno
        #time is in 4 digit format, subsequently to do splicing of the string
        self.timetoswitchoninput = timetoswitchoninput
        self.timetoswitchoffinput = timetoswitchoffinput
        
        
        
        
    def createnewtask(self):
    
        lists_of_tasks_to_run[str(self.pin_no)] = [str(self.timetoswitchoninput), (self.timetoswitchoffinput)]

        lists_of_tasks_to_run[self.collectpinno] = threading.Thread(target=task_timekeeper, args=(collecttimeschedule(),))
        lists_of_tasks_to_run[self.collectpinno].start()
        
        print 'Task has been started'
        
    
    
    
    
    
    #KEEPS ON RUNNING IN THE BACKGROUND, 1 thread for 1 set of 2 tasks 
    #IF TIME EQUALS TIME TO SWITCH ON, SWITCH ON, PROBABLY WITH A BIT OF A THRESHOLD +-
    def task_timekeeper(self,collectedpinno, timetoswitchon, timetoswitchoff):
        
        switchontask_notover = True
        switchofftask_notover = False
        
        while switchontask_notover is True:
            
            hour_now, minutes_now = gettimebreakdown()
            
            hour_toswitchon = timetoswitchon[0:2]
            minute_toswitchon = timetoswitchon[2:4]
            
            if (int(hour_toswitchon) - int(hour_now) == 0):
            
                if ((int(minutes_now) - int(minute_toswitchon)>=0) and (int(minutes_now) - int(minute_toswitchon)<=1)):
                    
                    switch_on_off(str(list_name_from_pin(int(collectpinno))))
                    switchontask_notover = False
                    print 'TaskName has been started at time. Appliance is switched on'
                    
                    if timetoswitchoff != '9999':
                        switchofftask_notover = True
                
             
        while switchofftask_notover is True:
        
            hour_now, minutes_now = gettimebreakdown()
            
            hour_toswitchoff = timetoswitchoff[0:2]
            minute_toswitchoff = timetoswitchoff[2:4]
            
            if (int(hour_toswitchoff) - int(hour_now) == 0):
            
                if ((int(minutes_now) - int(minute_toswitchoff)>=0) and (int(minutes_now) - int(minute_toswitchoff)<=1)):
                    
                    switch_on_off(str(list_name_from_pin(int(collectpinno))))
                    switchofftask_notover = False
                    print 'TaskName has been started at time. Appliance is switched off'
            
          

    