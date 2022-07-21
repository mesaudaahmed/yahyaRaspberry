import json
import paho.mqtt.client as mqtt
class mqtt_esp():
    def __init__(self,mqtt_username,mqtt_password,mqtt_topic,mqtt_broker_ip):
        self.mqtt_topic=mqtt_topic
        self.mqtt_username=mqtt_username
        self.mqtt_password=mqtt_password
        self.mqtt_broker_ip=mqtt_broker_ip
    def get_user_name(self):
        return self.mqtt_username
    def get_password(self):
        return self.mqtt_password
    # Set the username and password for the MQTT client
    def instance(self):
        # Don't forget to change the variables for the MQTT broker!
        self.client = mqtt.Client()
        self.client.username_pw_set(self.mqtt_username,self.mqtt_password)
    # These functions handle what happens when the MQTT client connects
    # # to the broker, and what happens then the topic receives a message
    def on_connect(self,client, userdata, flags, rc):
        #rc is the error code returned when connecting to the broker
        print ("Connected!", str(rc))
        # Once the client has connected to the broker, subscribe to the topic
        self.client.subscribe(self.mqtt_topic) 
    def on_message(self,client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
        print("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
        data = json.loads(msg.payload)
    def on_publish(self,client,userdata,result):             
        #create function for callback
        print("data published \n")
        pass
    def run_mqtt(self):    
    # Here, we are telling the client which functions are to be run
        # # on connecting, and on receiving a message
        self.client.on_publish = self.on_publish
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # Once everything has been set up, we can (finally) connect to the broker
        # # 1883 is the listener port that the MQTT broker is using
        self.client.connect(self.mqtt_broker_ip, 1883)
        # Once we have told the client to connect, let the client object run itself 
        self.client.loop_forever()
        print()
        self.client.disconnect()

mq=mqtt_esp("debian","debian","outTopic","192.168.43.143")
mq.instance()
mq.run_mqtt()
