import RPi.GPIO as GPIO 
from variables import *
import armdevices as armdevices
from timekeeper import *
from collections import OrderedDict #python dictionary does not retain order
import logcreator as logcreator
import blocktext as blocktext
from pushbulletnotify import Pushbullet_devices
import threading
import serverside as serverside


#PYTHON GPIO 
#GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
#GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
#GPIO.setup(11, GPIO.IN)
#GPIO.output(7,True) ## Turn on GPIO pin 7
#GPIO.add_event_detect(23, GPIO.RISING, callback=menu, bouncetime=300)


#auto generated variables
applianceslist = []
pin_assignment = OrderedDict() #  7:'Lights',11:'TV',... pin no is an integer!
status = "STATUS UPDATE: "
listen_to_on_off = False 
    
def header():
    print "==============t.H.O.U.S.E=============="
    blocktext.logo_2()

    print "Local current time :", gettimenow(reloadtimedate())
    logcreator.startnewloggerthread("Program has started", True)


def initialize_board(pins,inputs_to_use):
    GPIO.setmode(GPIO.BOARD)
    
    print gettimenow(reloadtimedate()), "%s"%(status),"Initializing GPIO board..."
    
    for each_pin in pins:
        GPIO.setup(each_pin, GPIO.OUT) 
        GPIO.output(each_pin,False) ## Turn off all GPIO pins
        print gettimenow(reloadtimedate()), "%s"%(status)+"Pin "+str(each_pin)+" is ready as GPIO outPUT!"
        
    for each_inputpin in inputs_to_use:
        GPIO.setup(each_inputpin, GPIO.IN)
        print gettimenow(reloadtimedate()), "%s"%(status)+"Pin "+str(each_inputpin)+" is ready as GPIO inPUT!"
    
    print gettimenow(reloadtimedate()), "%s ALL APPLIANCES ACTIVATED" %(status)
    
    for each_appliance in appliances:
        applianceslist.append(each_appliance)
        print str(each_appliance)+": "+str(appliances[each_appliance]) #eg. TV: OFF
        
        
    #Assigns each pin to each appliance
    indexno=0
    for eachpin in pins_to_use:
        pin_assignment.update({eachpin:list_appliance_name(indexno)})
        indexno+=1 #to add in exception handling for mismatch of no of pins and appliances
        
    
    print gettimenow(reloadtimedate()), "%s"%(status)+"GPIO is initialized"
    
    #returns the individual name of the appliance using individual index location
def list_appliance_name(indexno): 
    return applianceslist[indexno] #applianceno is the list index
    
    
    
    
    #will return individual appliance's name from individual pin
def list_name_from_pin(pin):
    return pin_assignment[int(pin)] 
	
	#RETUNS individual PIN number from individual appliance name
def list_pin_from_name(appliancename):
	for eachpin in pin_assignment:
		if pin_assignment[eachpin]==str(appliancename):
			return eachpin
			#to add in exception

	#will return on or off
def list_status(appliancename):
    return appliances[appliancename] 
	
def appliancetoarm():
	return appliances_to_arm
	
def inputstouse():
	return inputs_to_use
    
#resets all GPIO and exits
def cleanup():
	print gettimenow(reloadtimedate()), "%s GPIO has been reset\nProgram is exiting now.." %(status)
	GPIO.cleanup()

    
    
	
	
    #switch on_off using appliance name
def switch_on_off(appliancename):
    if appliances[str(appliancename)]=="OFF": #off to on
        GPIO.output(list_pin_from_name(appliancename),True)
        appliances[appliancename]="ON"
        print gettimenow(reloadtimedate()), "%s"%(status)+str(appliancename)+" [Pin: "+str(list_pin_from_name(appliancename))+"] is switched ON!"
        
    elif appliances[str(appliancename)]=="ON": #on to off
        GPIO.output(list_pin_from_name(appliancename),False)
        appliances[appliancename]="OFF"
        print gettimenow(reloadtimedate()), "%s"%(status)+str(appliancename)+" [Pin: "+str(list_pin_from_name(appliancename))+"] is switched OFF!"

    else:
        print gettimenow(reloadtimedate()), "Error: Cannot operate the switch."


		
		

def collect_menu_choice():
    global at_main_menu
    global at_arm_menu
    global at_switch_menu
    global at_timed_task_menu
    at_main_menu = True
    at_switch_menu = False
    at_arm_menu = False
    at_timed_task_menu = False
	
    print "==============MAIN MENU=============="
    print "[1] Switch ON/OFF appliance"
    print "[2] ARM a running appliance"
    print "[3] Set a TIMED task"
    print "[7] Check PushBullet Devices"
    print "[8] Check PIN Functions"
    print "[9] EXIT"
	
    while at_main_menu==True and at_switch_menu==False and at_arm_menu==False:
        menu_choice=raw_input("Choose your option number:")
        
            #switch on and off menu
        if str(menu_choice) == '1': 
			at_main_menu = False
			at_switch_menu = True
            
			while at_switch_menu == True:
				switch_on_off(collect_valid_pin_number())	
		

            #arm appliance menu
        elif str(menu_choice) == '2': 
            at_main_menu = False
            at_arm_menu = True
            
            while at_arm_menu == True:
                armdevices.arm_menu()
                
        elif str(menu_choice) == '3':
            at_main_menu = False
            at_timed_task_menu = True
            
            while at_timed_task_menu == True:
                timedtask_menu()
                
        elif str(menu_choice) == '7':
            pushbulletdevice_query = Pushbullet_devices(api_key)
            pushbulletdevice_query.print_deviceinformation()
                
        elif str(menu_choice) == '8':
            func = GPIO.gpio_function(7) #CHECKS THE FUNCTION OF THE PIN
            print func
       
        elif str(menu_choice) == '9':
            cleanup()
            initialiseserver.stop_listening()
            logcreator.startnewloggerthread("Program has ended. GPIO reset", True)
            exit()
            
        else:
			print "%s Invalid option no. Try again!" %(status)
			collect_menu_choice()
	


	
	
	#collects only a valid pin number as integer and return appliance name
def collect_valid_pin_number():
    at_switch_menu=True

    print "==============Switch MENU=============="
    print "[Pin Assigned] & [Appliance]"
    for eachsinglepin in pin_assignment: #7:'Lights' (int & string)
        print str(eachsinglepin),str(pin_assignment[eachsinglepin])

		
    while at_switch_menu==True:
        print "Enter 99 to return to MAIN MENU"
        pin_no_to_switch=raw_input("Please type in the pin number to operate:: ")
		
        if not pin_no_to_switch.isalpha():
        
            if int(pin_no_to_switch) in pin_assignment:
                at_switch_menu = False
                return str(pin_assignment[int(pin_no_to_switch)])
			
            elif int(pin_no_to_switch)==99:
                at_switch_menu = False
                at_main_menu = True
                collect_menu_choice()
        
            else:
                print gettimenow(reloadtimedate()), "%s The pin [%d] is not in use!! Try again!!!" %(status,int(pin_no_to_switch))
                
        else:
            print gettimenow(reloadtimedate()), "%s NOT A NUMBER!" %(status)
		
		
		

	#MAIN SEQUENCE
def mainsequence():
    header()
    
    #initialise server before board
    global initialiseserver
    initialiseserver = serverside.ListeningServer()
    servicesidethread = threading.Thread(target=initialiseserver.start_listening, args=[])
    servicesidethread.start()
    
    initialize_board(pins_to_use,inputs_to_use)
    collect_menu_choice()

    

mainthread = threading.Thread(target=mainsequence, args=[])
mainthread.start()


