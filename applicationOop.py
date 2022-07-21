from msilib.schema import tables
import sys
#this project was created for yahya to manage his own farme
#sqlite library was imported for saving the values tags for the cheeps
#the time library to manage wich time the tage is in reading 
from datetime import datetime
import sqlite3
import time
import paho.mqtt.client as mqtt
import json
def get_savetime(firstTime):
    print(firstTime)
    first_time = datetime.datetime.strptime(str(firstTime), '%Y-%m-%d %H:%M:%S.%f')
    later_time = datetime.datetime.now()
    difference = later_time - first_time
    datetime.timedelta(0, 8, 562000)
    seconds_in_day = 24 * 60 * 60
    tup=divmod(difference.days * seconds_in_day + difference.seconds, 60)
    return int(tup[0]+tup[1]/60)

def CreateTables():
    try:
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        # doo somthing with your data
        cursor.execute ( """ CREATE TABLE IF NOT EXISTS GroupA (
                              Device TEXT,
                              Tag INTEGER ,
                              SaveTime timestamp) """ )
        cursor.execute ( """ CREATE TABLE IF NOT EXISTS GroupB (
                              Device TEXT,
                              Tag INTEGER ,
                              SaveTime timestamp) """ )
        cursor.execute ( """ CREATE TABLE IF NOT EXISTS GroupC (
                              Device TEXT,
                              Tag INTEGER ,
                              SaveTime timestamp) """ )
        cursor.execute ( """ CREATE TABLE IF NOT EXISTS GroupD (
                              Device TEXT,
                              Tag INTEGER ,
                              SaveTime timestamp) """ )
        cursor.execute ( """ CREATE TABLE IF NOT EXISTS ESP (
                              Device TEXT,
                              state BOOL) """ )
        cursor.close()
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")
def Time_checker(device,tag):
    tables = ["GroupA", "GroupB", "GroupC","GroupD"]
    try:
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        for table in tables :
            for row in cursor.execute("SELECT * FROM "+ table +" WHERE Tag =?",(tag,)):
                if get_savetime(row[2])>240 :
                    print("time > 4h")
                    cursor.execute("UPDATE" + table+ "set saveTime = ? where tageId = ?",(datetime.datetime.now(),tag,))
                    #publish to device with group
                    relayoneTopic=device+"/"+table
                    client.publish(relayoneTopic,"1")
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")

"""
Python MQTT Subscription client
Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
Written for my Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
"""

# Don't forget to change the variables for the MQTT broker!
mqtt_username = "debian"
mqtt_password = "debian"
mqtt_topic = "outTopic"
mqtt_broker_ip = "192.168.43.143"

client = mqtt.Client()
# Set the username and password for the MQTT client
client.username_pw_set(mqtt_username, mqtt_password)

# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    print ("Connected!", str(rc))
    
    # Once the client has connected to the broker, subscribe to the topic
    client.subscribe(mqtt_topic)
def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    print("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
    #client.publish('device1/relay1', '1')
    data = json.loads(msg.payload)
    CreateTables()
    Time_checker(str(data['deviceID']),data['tagID'])

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass
# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
client.on_publish = on_publish
client.on_connect = on_connect
client.on_message = on_message
# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
client.connect(mqtt_broker_ip, 1883)

# Once we have told the client to connect, let the client object run itself
while True :
    print("programme started")
    client.loop_forever()
    print("scrip stoped lite's run it aagin ")

client.disconnect()









