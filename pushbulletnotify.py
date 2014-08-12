from PUSHbulletnotifications.pushbullet import PushBullet
from PUSHbulletnotifications.pushbullet import Device
import threading
from variables import api_key

#collects all the ids of all the devices linked to the account
devices_id = []


class Pushbullet_devices(object):
    
    def __init__(self, api_key):
    
        #imports the PushBullet API class
        global pb
        pb = PushBullet(api_key)
        self.pb = pb
        
        #extraction of device ids from the device readbacks
        for devicedata in self.pb._devices:
            #print devicedata
            positionofcomma = str(devicedata).index(',')
            extracted_deviceidno_original = str(devicedata)[(positionofcomma+2):]
            extracted_deviceidno = extracted_deviceidno_original.replace(')', "")
            devices_id.append(extracted_deviceidno)
        
        
        
    def printdevices(self):
        print self.pb.devices
        #eg. index 0 will be [Device('v1AKK5CDIVoP3iYjKDhVNHihZQjY4yYDEvujwirvOODWm', 5629499534213120)] 
        
    
    def getdevicebyid(self, deviceid):
        phone = self.pb[int(deviceid)] 
        #phone = pb.get(12345)
        
        self.phone = phone
        
        
    def createnewdevice(self):
        #this doesn't make a network request
        newdevice = Device(api_key, device_id)
        
    
    def print_deviceinformation(self):
    
        print "There are ", len(devices_id), " devices connected."
        
        counter = 1
        
        for eachdeviceid in devices_id:
            
        
            print "--------------DEVICE ", counter, "--------------"
            self.getdevicebyid(eachdeviceid)
            print "OWNER: ", self.phone.owner 
            print "MODEL: ", self.phone.model
            print "MANUFACTURER: ", self.phone.manufacturer
            print "ANDROID VERSION: ", self.phone.android_version
            print "APP VERSION: ", self.phone.app_version

            counter+=1
            
            
      
    
      
      #pushes notifications to all devices!
class Pushbullet_notifications(Pushbullet_devices):

        
    def push_textnote(self, text_title, text_body):
    
        for each_deviceid in devices_id:

            self.getdevicebyid(each_deviceid)

            #push = phone.push_note("This is the title", "This is the body")
            push = self.phone.push_note(str(text_title), str(text_body))
            
        
    def push_address(self):
    
        for each_deviceid in devices_id:

            self.getdevicebyid(each_deviceid)
    
            address = " 25 E 85th St, 10028 New York, NY"
            push = self.phone.push_address("home", address)
            
        
    def push_list(self):
    
        for each_deviceid in devices_id:

            self.getdevicebyid(each_deviceid)
    
            to_buy = ["milk", "bread", "cider"]
            push = self.phone.push_list("Shopping list", to_buy)
            
        
    def push_link(self):
    
        for each_deviceid in devices_id:
        
            self.getdevicebyid(each_deviceid)
            
            push = self.phone.push_link("Cool site", "https://github.com")
        
    def pushfile(self):
    
        for each_deviceid in devices_id:

            self.getdevicebyid(each_deviceid)
        
            with open("my_cool_app.apk", "rb") as apk:
                push = self.phone.push_file(apk)
                

    def check_status(self):
        print(push.status_code)
        
        
def bulletpush_thread(title, body):
    test1 = Pushbullet_notifications(api_key)
    test1.push_textnote(str(title), str(body))    
    
    

def initiate_bulletpush_thread(title, body):
    bulletpushthread = threading.Thread(target=bulletpush_thread, args=(title, body,))
    bulletpushthread.start()
    
