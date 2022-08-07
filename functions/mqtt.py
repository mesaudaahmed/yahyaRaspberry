import json
from functions.database import *
import paho.mqtt.client as mqtt
import time
class mqtt_esp(mqtt.Client):
    def __init__(self,mqtt_username,mqtt_password,mqtt_topic,mqtt_broker_ip,mqtt_port:int):
        super().__init__()
        self.mqtt_topic=mqtt_topic
        self.mqtt_username=mqtt_username
        self.mqtt_password=mqtt_password
        self.mqtt_broker_ip=mqtt_broker_ip
        self.mqtt_port=mqtt_port
        self.payload=""
    # Set the username and password for the MQTT client
    def instance(self):
        # Don't forget to change the variables for the MQTT broker!
        self.username_pw_set(self.mqtt_username,self.mqtt_password)
    # These functions handle what happens when the MQTT client connects
    # # to the broker, and what happens then the topic receives a message
    def on_connect(self,client, userdata, flags, rc):
        #rc is the error code returned when connecting to the broker
        print ("Connected!", str(rc))
        # Once the client has connected to the broker, subscribe to the topic
        self.subscribe(self.mqtt_topic)
        self.subscribe("connection")#subscribe to a topic to determinate device state
    def on_message(self,client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
        print("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
        self.payload = json.loads(msg.payload)
        print("topic: "+ msg.topic)
        print("topic: "+str(self.payload))
        # self.publish()
        # update the data for eat_state and device work availabilty and update days 
        if msg.topic=="connection":
            #update all esp state on esp table as 0 to to tell the user the state off device is ready for recive tags 
            print(self.payload["state"])
            with sqlite3.connect("clientData.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE EspData set RelayState = 0 where device = ?",(self.payload["deviceID"],))
                con.commit()
        elif msg.topic=="outTopic":
            #get all setting data and store it inside dictonnary
            setting_dic=getSetting("setting")
            #same way for tag data 
            data_dic=getData("EspData",self.payload["tagID"])
            #get the days parametre for tag id 
            days=int(data_dic["Days"])
            #get the savetime parametre for tag id 
            savetime=data_dic["saveTime"]
            #compare it and decide an action to reconfigure relay timer as default configurations
            if int(daysPassed(savetime))>=days:
                with sqlite3.connect("clientData.db") as con:
                    cur = con.cursor()
                    clientes =[(self.payload["deviceID"],setting_dic["R1time"],setting_dic["R2time"],setting_dic["R3time"],str(self.payload["tagID"]))]
                    cur.executemany ( " UPDATE EspData set device =?, R1time=? ,R2time=? ,R3time=?,days=0 where tag=?" , clientes)
                    con.commit()
                    print("table updated for days equal 0")
            else:
                payload=data_dic["R1time"]+"#"+data_dic["R2time"]+"#"+data_dic["R3time"]
                self.publish(self.payload["deviceID"]+"/GroupA",payload)
                #update eatstate update eat time
            print("days passed",int(daysPassed(savetime)))
            print("device: "+str(self.payload["deviceID"]))
            print("tag: "+str(self.payload["tagID"]))
        # chech if days is equale zero then update all relay timer value

        # check if tag is saved on EspData table 
            #if tag is saved
                # check the reload time 
                    # if reload time is True and RElay state is True and days more than 0 then
                        # self.publish() the payload to topic device/setRelays from data base
                    # if reload time is True and RElay state is True and days less than 0 then
                        # self.publish() the payload to topic device/setRelays from default data
            #if tag is not saved on EspDta then save with the default values from setting table
    def on_publish(self,client,userdata,result):             
        #create function for callback
        print("data published \n")
        pass
    def run_mqtt(self):    
    # Here, we are telling the client which functions are to be run
        # # on connecting, and on receiving a message
        self.on_publish = self.on_publish
        self.on_connect = self.on_connect
        self.on_message = self.on_message
        # Once everything has been set up, we can (finally) connect to the broker
        # # 1883 is the listener port that the MQTT broker is using
        self.connect(self.mqtt_broker_ip, 1883)
        # Once we have told the client to connect, let the client object run itself 
        self.loop_start()
        print(self.payload)
    def mqstop(self):
        self.loop_stop()
# mq=mqtt_esp("dell","talib2020","outTopic","localhost",1883)
# mq.instance()
# mq.run_mqtt()
# time.sleep(10)
# mq.mqstop()
