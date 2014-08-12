import RPi.GPIO as GPIO
import time
from variables import *
import index as index
from timekeeper import *
from logcreator import startnewloggerthread
from pushbulletnotify import initiate_bulletpush_thread


 #Dictionary for auto generated variable for the class
armed_appliances = {}
bounceduration=300 #milliseconds
status = "STATUS UPDATE: "


class ListeningAppliance(object):
    arm_status = False
    wait_status = ""

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin

    def startlistening(self, detect_rise_or_fall):
        
        if (detect_rise_or_fall == 'r' or detect_rise_or_fall == 'R') and self.wait_status == '':
            
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            #Waiting for RISE, PUD_DOWN
            
            self.wait_status = 'RISE'
            
            GPIO.add_event_detect(self.pin, GPIO.RISING, callback = self.armedandwaiting, bouncetime=bounceduration)
                
            if self.arm_status == False:
                self.changearmstatus()
                   
            print gettimenow(reloadtimedate()), "%s %s is ARMED on pin [%d]. Waiting for a rise in voltage (PUD_DOWN)....." %(status, self.name, self.pin)
        
       
        elif (detect_rise_or_fall == 'f' or detect_rise_or_fall == 'F') and self.wait_status == '':
            
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            #Waiting for FALL, PUD_UP
            
            self.wait_status = 'FALL'
            
            GPIO.add_event_detect(self.pin, GPIO.FALLING, callback = self.armedandwaiting, bouncetime=bounceduration)
                
            if self.arm_status == False:
                self.changearmstatus()
                
            print gettimenow(reloadtimedate()), "%s %s is ARMED on pin [%d]. Waiting for a fall in voltage (PUD_UP)....." %(status, self.name, self.pin)
            
        
        elif (detect_rise_or_fall == 'd' or detect_rise_or_fall == 'D') and self.wait_status == '':
                
            self.wait_status = 'DOOR MONITORING MODE'
            self.doorstatus_initialise(self.pin)
            
            if self.arm_status == False:
                self.changearmstatus()
        
        
        else:
            print gettimenow(reloadtimedate()), "%s This pin is already waiting for a " %(status), self.wait_status, "\nDo not repeat the same procedure!!! \nRESET THE PIN BEFORE TRYING AGAIN." 
            arm_menu()
                
                
                
    def doorstatus_initialise(self, channel):
        
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
            #if door is initially opened
        if GPIO.input(channel) == True:
        
            print self.name, " is currently open" 
            GPIO.add_event_detect(self.pin, GPIO.FALLING, callback = self.door_close, bouncetime=10)
           
        
            #if door is initially closed
        elif GPIO.input(channel) == False:
        
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            print self.name, " is currently closed"
            GPIO.add_event_detect(self.pin, GPIO.RISING, callback = self.door_open, bouncetime=0) #this is not a switch bounce.
            
            
            
            
    def door_open(self, placeholder):
        
        if GPIO.input(self.pin) == True: #switch opened
        
            print self.name, " is now opened"
            GPIO.remove_event_detect(self.pin)
        
            #wait for switch to be closed again
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(self.pin, GPIO.FALLING, callback = self.door_close, bouncetime=5) #falling == door is closed
            
            
    def door_close(self,placeholder): #switch closed
    
        if GPIO.input(self.pin) == False:
            print self.name," is now closed"
            GPIO.remove_event_detect(self.pin)
            
            #wait for switch to be open again
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(self.pin, GPIO.RISING, callback = self.door_open, bouncetime=0) #rising == door is opened
        
        
        
    def armedandwaiting(self, channel):
        
        """
        WIRES NOT TOUCHING
        INPUT IS HIGH DUE TO PULL-UP RESISTOR
        GPIO.input(channel) = True
        
        WIRES ARE TOUCHING
        INPUT IS LOW
        and if the wires are touching, then the input is low (connected to ground).
        GPIO.input(channel) = False
        """
        
        
        if str(self.name) == 'doorbellSwitch':
            time.sleep(0.1) 
            
            try:
                
                if not GPIO.input(channel): #only if input is still high after x seconds then execute. perhaps one way to deal with electromagnetic interference
                
                    index.switch_on_off('doorBell')
                    time.sleep(2) #wait for 2 seconds
                    index.switch_on_off('doorBell')
                    
                    #prints and logs
                    startnewloggerthread("%s Doorbell IS pressed. " %(status) + str(self.wait_status) + " on PIN: " + str(self.pin), True)
                    initiate_bulletpush_thread('DoorBell:', "Doorbell IS pressed. " + str(self.wait_status) + " on PIN: " + str(self.pin))
                    
            
            except KeyboardInterrupt:
                print "%s Error in INTERRUPT process" %(status)
                
                
        else:
            
            try:
            
                print "%s DETECTED" %(status), self.wait_status, " on PIN: ", self.pin
                index.switch_on_off('TESTsubject')
                 
            except KeyboardInterrupt:
                print "%s Error in INTERRUPT process" %(status)
                
               
    def changearmstatus(self):
        if self.arm_status == False:
            self.arm_status = True
                
        else:
            self.arm_status = False
            
            
            
    def clearinterrupt(self):
        
        GPIO.remove_event_detect(self.pin)
        self.wait_status = ''
        self.changearmstatus() #from true to false
        print self.pin, " is no LONGER armed."


        
def allocatedevice_to_pin():

    index=0
        #self generated dictionary for the class
    for each_appliance in appliances_to_arm:
    
        #for each_pin in inputs_to_use:
    
        armed_appliances[each_appliance] = ListeningAppliance(each_appliance, inputs_to_use[index])
        index+=1    
        
allocatedevice_to_pin()
            
        
        
def arm_menu():
        
    print "==============ARM MENU==============" 
        
    for each_appliance in armed_appliances:
        print armed_appliances[each_appliance].pin, armed_appliances[each_appliance].name, armed_appliances[each_appliance].arm_status #print armed_appliances['Door'].name
        
    print "Key '88' to reset a specific armed appliance"
            
    pin_to_arm = raw_input("Please type in the pin number to ARM:: \nKey '99' to return to Main Menu\n")

    if str(pin_to_arm) == '88':
    
        pin_to_reset = raw_input("Please type in the pin number to reset: ")
            
        for each_appliance in armed_appliances:
        
            if int(pin_to_reset) == armed_appliances[each_appliance].pin and armed_appliances[each_appliance].wait_status != '':
                armed_appliances[each_appliance].clearinterrupt()
                arm_menu()
                    
            #else:
        print gettimenow(reloadtimedate()), "%s This pin has not been armed!\nThere is no need for a RESET" %(status)
        arm_menu()
    
    elif str(pin_to_arm) == '99':
        index.collect_menu_choice()
        
        
        
    else:
        
        print "To detect a rise, type 'r'.", "\nTo detect a fall, type 'f'.", "\nFor a door or window, type 'd'."
        detect_rise_or_fall = raw_input("r/f/d:: ")
        
        
        for each_appliance in armed_appliances:
        
            if int(pin_to_arm) == armed_appliances[each_appliance].pin:
                armed_appliances[each_appliance].startlistening(detect_rise_or_fall)
            
            
        if int(pin_to_arm) not in inputs_to_use:
            print gettimenow(reloadtimedate()), "%s This pin has not been initialized, Try again" %(status)
            
        arm_menu()