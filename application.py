############################# version 2 ###################################

import sys
#this project was created for yahya to manage his own farme
#sqlite library was imported for saving the values tags for the cheeps
#the time library to manage wich time the tage is in reading 
from datetime import datetime
import sqlite3
import time
import paho.mqtt.client as mqtt
import json

conn =sqlite3.connect('clientData.db')
cursor=conn.cursor()

def check_time():
    #get the current date
    current_time=datetime.now()
    #get the current time by minutes
    current_time_minute=current_time.hour*60+current_time.minute
    #cursor.execute(sqlitequery,(tag,))
    cursor.execute("SELECT * FROM EspData ")
    for row in cursor.execute("SELECT * FROM EspData "):
        if current_time_minute-int(row[2])<0 :
            print("time < 0")
            cursor.execute("UPDATE EspData set saveTime = 0 where tageId = ?",(row[1],))
            conn.commit()
        elif current_time_minute-int(row[2])>12 :
            print("time > 12")
            cursor.execute("UPDATE EspData set RelayState = 0 where tageId = ?",(row[1],))
            conn.commit()
    #connUpdate.close()
def check_timeB():
    #get the current date
    current_time=datetime.now()
    #get the current time by minutes
    current_time_minute=current_time.hour*60+current_time.minute
    #cursor.execute(sqlitequery,(tag,))
    # cursor.execute("SELECT * FROM EspData ")
    for row in cursor.execute("SELECT * FROM GroupB "):
        if current_time_minute-int(row[2])<0 :
            print("time < 0")
            cursor.execute("UPDATE GroupB set saveTime = 0 where tageId = ?",(row[1],))
            conn.commit()
        if current_time_minute-int(row[2])>10 :
            print("time > 12")
            cursor.execute("UPDATE GroupB set RelayState = 0 where tageId = ?",(row[1],))
            conn.commit()
        if current_time_minute-int(row[2])>240 :
            print("time > 4h")
            cursor.execute("UPDATE GroupB set eatState = 1 where tageId = ?",(row[1],))
            cursor.execute("UPDATE GroupB set saveTime = ? where tageId = ?",(current_time_minute,row[1],))
            conn.commit()
        for row1 in cursor.execute("SELECT * FROM EspData "):
            if row[1]==row1[1]:
                sql_delete_query = "DELETE FROM EspData WHERE tageId = ?"
                cursor.execute(sql_delete_query,(row[1],))
  
    #connUpdate.close()
def insertdata(deviceId, tageId):
    #get the current date
    current_time=datetime.now()
    #get the current time by minutes
    current_time_minute=current_time.hour*60+current_time.minute
    print("the current tme is : "+str(current_time_minute))
    #start the connection with database 
    #fucos on the database it self 
    #creat a table into our database with three fields tag id and device wich is esp32 and the time 
    cursor.execute ( """ CREATE TABLE IF NOT EXISTS EspData (
                           device TEXT,
                           tageId INTEGER ,
                           saveTime TEXT,
                           RelayState TEXT) """ )
    clientes =[ (deviceId,tageId ,current_time_minute,"1")]
    cursor.executemany ( " INSERT INTO EspData ( device ,tageId , saveTime ,RelayState) VALUES ( ? , ? , ?, ?  ) " , clientes )
    #tableSize=CUR_Test.execute( "SELECT COUNT(*) FROM EspData")
    #print(tableSize)
    conn.commit()
    print("data inserted ..")
    cursor.execute( " SELECT * FROM EspData " )
    print( cursor.fetchall())
    #conn.close()
def insertdataB(deviceId, tageId):
    #get the current date
    current_time=datetime.now()
    #get the current time by minutes
    current_time_minute=current_time.hour*60+current_time.minute
    print("the current tme is : "+str(current_time_minute))
    #start the connection with database 
    #fucos on the database it self 
    #creat a table into our database with three fields tag id and device wich is esp32 and the time 
    cursor.execute ( """ CREATE TABLE IF NOT EXISTS GroupB (
                           device TEXT,
                           tageId INTEGER ,
                           saveTime TEXT,
                           eatState INTEGER,
                           RelayState TEXT) """ )
    clientes =[ (deviceId,tageId,current_time_minute,0,"1")]
    cursor.executemany ( " INSERT INTO EspData ( device ,tageId , saveTime ,eatState,RelayState) VALUES ( ? , ? ,?, ?, ?  ) " , clientes )
    #tableSize=CUR_Test.execute( "SELECT COUNT(*) FROM EspData")
    #print(tableSize)
    conn.commit()
    print("data inserted ..")
    cursor.execute( " SELECT * FROM GroupB " )
    print( cursor.fetchall())
    #conn.close()

def chekIfTagExists(deviceId,tag):
    try:
        #get the current date
        current_t=datetime.now()
        #get the current time by minutes
        current_t_minute=current_t.hour*60+current_t.minute
        cursor.execute(" CREATE TABLE IF NOT EXISTS EspData ( device TEXT,tageId INTEGER , saveTime TEXT,RelayState TEXT) ")
        print("start cheking if the tage [%s] is exists", tag)
        sqlitequery="SELECT tageId FROM EspData WHERE tageId =?"
        cursor.execute(sqlitequery,(tag,))
        data=cursor.fetchall()
        if len(data)==0:
            print('no tageid named %s'%tag)
            print('check ESP State')
            cursor.execute("SELECT * FROM EspData ")
            ok=0
            ok2=0
            for row in cursor.execute("SELECT * FROM EspData "):
                if row[0]==deviceId and row[3]=="1":
                    ok=ok+1
            for row in cursor.execute("SELECT * FROM GroupB "):
                if row[0]==deviceId and row[4]=="1":
                    ok2=ok2+1
            if ok==0 and ok2 ==0:
                print('start creating record for Tag : %s'%tag)
                insertdata(deviceId,tag)
                #publish data win the id is in recording
                relayoneTopic=deviceId+"/relay1"
                ret= client.publish(relayoneTopic,"1")
                print(" Relays start %s "%tag)
            else :
                print("esp buzy")
            
        else:
            print('tageid : %s already exists'%tag)
            #rowsQuerySelect="SELECT device ,tageId , saveTime ,Relay1 FROM EspData "
            # rowsQueryDelete="DELETE tageId FROM EspData WHERE tageId =?"
            #DB_cur.execute(rowsQuerySelect)
            sqlitequery="SELECT tageId FROM EspData WHERE tageId =?"
            #cursor.execute(sqlitequery,(tag,))
            cursor.execute("SELECT * FROM EspData ")
            for row in cursor.execute("SELECT * FROM EspData "):
                if current_t_minute-int(row[2])<0 :
                    cursor.execute("UPDATE EspData set saveTime = 0 where tageId = ?",(row[1],))
                    conn.commit()
                elif current_t_minute-int(row[2])>12 :
                    cursor.execute("UPDATE EspData set RelayState = 0 where tageId = ?",(row[1],))
                    conn.commit() 
    except sqlite3.Error as error:
        print("Failed to check %s"%tag,"if exist in table EspData",error)
def chekIfTagExistsB(deviceId,tag):
    try:
        relayoneTopic=deviceId+"/relay2"
        #get the current date
        current_t=datetime.now()
        #get the current time by minutes
        current_t_minute=current_t.hour*60+current_t.minute
        cursor.execute(" CREATE TABLE IF NOT EXISTS GroupB ( device TEXT,tageId INTEGER , saveTime TEXT,eatState,RelayState TEXT) ")
        print("check if "+ str(tag) +" exist")
        sqlitequery="SELECT tageId FROM GroupB WHERE tageId =?"
        cursor.execute(sqlitequery,(tag,))
        data=cursor.fetchall()
        if len(data)==0:
            print(' tag in Group A '+ str(tag))
            chekIfTagExists(deviceId,tag)
            showInRow()
        else:
            print(' tag in Group B')
            ok=0
            ok2=0
            for row in cursor.execute("SELECT * FROM GroupB "):
                if row[0]==deviceId and row[4]=="1":
                    ok=ok+1
            for row in cursor.execute("SELECT * FROM EspData "):
                if row[0]==deviceId and row[3]=="1":
                    ok2=ok2+1
            sqlitequery="SELECT * FROM GroupB WHERE tageId =?"
            cursor.execute(sqlitequery,(tag,))
            row=cursor.fetchone()
            if row[0]=="0" and ok==0 and ok2 ==0:
                cursor.execute("UPDATE GroupB set device = ? where tageId = ?",(deviceId,tag,))
                cursor.execute("UPDATE GroupB set saveTime = ? where tageId = ?",(current_t_minute,tag,))
                cursor.execute("UPDATE GroupB set eatState = ? where tageId = ?",(0,tag,))
                cursor.execute("UPDATE GroupB set RelayState = ? where tageId = ?",("1",tag,))
                client.publish(relayoneTopic,"1")
            if row[3] == "1" and ok==0 and ok2 ==0:
                cursor.execute("UPDATE GroupB set eatState = ? where tageId = ?",(0,tag,))
                cursor.execute("UPDATE GroupB set RelayState = ? where tageId = ?",("1",tag,))
                client.publish(relayoneTopic,"1")
                cursor.execute("UPDATE GroupB set saveTime = ? where tageId = ?",(current_t_minute,tag,))
                # cursor.executemany ( " INSERT INTO EspData ( device ,tageId , saveTime ,eatState,RelayState) VALUES ( ? , ? ,?, ?, ?  ) " , clientes )
                #publish data win the id is in recording
    except sqlite3.Error as error:
        print("Failed to check %s"%tag,"if exist in table GroupB",error)
def deleteRecord(tagDublicated):
    try:
        print("Delete record")
        #DELETE FROM mytable WHERE (msg_when <= datetime('now', '-4 days')
        # Deleting single record now
        sql_delete_query = """DELETE FROM EspData WHERE tageId = ?"""
        cursor.execute(sql_delete_query,(tagDublicated,))
        print("Record deleted successfully ")
        print(cursor.fetchall())
        conn.commit()
        #cursor.close()
    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("the sqlite connection is closed")
def deleteRecordB(tagDublicated):
    try:
        print("Delete record")
        #DELETE FROM mytable WHERE (msg_when <= datetime('now', '-4 days')
        # Deleting single record now
        sql_delete_query = """DELETE FROM GroupB WHERE tageId = ?"""
        cursor.execute(sql_delete_query,(tagDublicated,))
        print("Record deleted successfully ")
        print(cursor.fetchall())
        conn.commit()
        #cursor.close()
    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("the sqlite connection is closed")
def showInRow():
    #get the current date
    current_time=datetime.now()
    #get the current time by minutes
    current_time_minute=current_time.hour*60+current_time.minute
    print('sqlite3 connected to show rows')
    rowsQuerySelect="SELECT * FROM EspData "
   # rowsQueryDelete="DELETE tageId FROM EspData WHERE tageId =?"
    cursor.execute(rowsQuerySelect)
    print("the current time is ",current_time_minute)
    for row in cursor.execute(rowsQuerySelect):
        print('ESP :',row[0],' tageID : ',row[1],'save time :',row[2],'RelayState',row[3])
        #print(type(row[0]))
        #print(current_time_minute-int(row[2]))
        #print(type(int(row[2])))
        #for now we able to delete the row evry 3 minutes from saving it
        if (current_time_minute-int(row[2])>240):
            #print('start delet tagid : ',row[1],'from : ',row[0])
            sql_delete_query = "DELETE FROM EspData WHERE tageId = ?"
            cursor.execute(sql_delete_query,(row[1],))
            print("Record ",row[1],"deleted successfully ")
            conn.commit()
            #conn.close()
            #print(CUR.fetchall())
        elif current_time_minute-int(row[2])<0 :
            print("midnight")
            cursor.execute("UPDATE EspData set saveTime = 0 where tageId = ?",(row[1],))
            conn.commit()
            #print("Total number of rows updated :",CUR.total_changes)
        elif current_time_minute-int(row[2])>11 :
            print("RelayState 0")
            print(current_time_minute-int(row[2]))
            cursor.execute("UPDATE EspData set RelayState = 0 where tageId = ?",(row[1],))
            conn.commit()
            #print("Total number of rows updated :",CUR.total_changes)
        else:
            print('not yet for esp: ',row[0],' tagid: ',row[1],' time : ',current_time_minute-int(row[2]),'relayState',row[3])
            #check_time()

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
    # chekIfTagExists(str(data['deviceID']),data['tagID'])
    # showInRow()
    chekIfTagExistsB(str(data['deviceID']),data['tagID'])
    check_timeB()

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





