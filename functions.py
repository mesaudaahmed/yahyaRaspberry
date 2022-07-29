#import date time for checking save time tag
from datetime import datetime,timedelta
from tkinter import EXCEPTION
import paho.mqtt.publish as publish
#import datrabase librarey
import sqlite3
import paho.mqtt.client as mqtt
#start connection with database 
conn=sqlite3.connect("clientData.db")
cursor=conn.cursor() 
client = mqtt.Client()
#return how long time the tag is in database
def savetime(firstTime):
    # firstTime = '16/03/22 16:15:19'
    first_time = datetime.strptime(firstTime, '%Y-%m-%d %H:%M:%S.%f')
    later_time = datetime.now()
    difference = later_time - first_time
    timedelta(0, 8, 562000)
    day_to_sec = 24 * 60 * 60
    tup=divmod(difference.days * day_to_sec + difference.seconds, 60)
    return int(tup[0]+tup[1]/60)
# Pfunction to illustrate the addition
# of time onto the datetime object
def reloadtime(time,min):
    savetime = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    new_time=savetime+timedelta(minutes=min)
    return new_time


def rowCounter():
        with sqlite3.connect("clientData.db") as conn:
            cursor=conn.cursor()
            query="SELECT * FROM EspData"
            return len(cursor.execute(query).fetchall())

def updatedata(device:str, tag:int,save_time,reload_time,relay_state:str,eat_state,R1_time:str,R2_time:str,R3_time:str,days:int):
    try:
        clientes =[(device, tag,save_time,reload_time,relay_state,eat_state,R1_time,R2_time,R3_time,days,tag)]
        cursor.executemany ( " UPDATE EspData set device=? , tag=? ,saveTime=? ,ReloadTime=? ,RelayState=? ,EatState=? ,R1time=? ,R2time=? ,R3time=? ,Days=? where tag = ?" , clientes )
        conn.commit()
        print("data updated ..")
        print(searchTag(tag))
        return True
    except EXCEPTION as e:
        print(e)
        return False
def insertdata(device:str, tag:int,save_time,reload_time,relay_state:str,eat_state,R1_time:str,R2_time:str,R3_time:str,days:int):
    cursor.execute ( """ CREATE TABLE IF NOT EXISTS EspData (
                           ID INTEGER PRIMARY KEY,
                           device TEXT,
                           tag INTEGER ,
                           saveTime timestamp,
                           ReloadTime timestamp,
                           RelayState TEXT,
                           EatState TEXT,
                           R1time TEXT,
                           R2time TEXT,
                           R3time TEXT,
                           Days INTEGER) """ )
    clientes =[(device, tag,save_time,reload_time,relay_state,eat_state,R1_time,R2_time,R3_time,days)]
    cursor.executemany ( " INSERT INTO EspData ( device , tag ,saveTime ,ReloadTime ,RelayState,EatState,R1time,R2time ,R3time,Days) VALUES ( ? , ? , ?, ?, ?, ?, ?, ?, ?, ?  ) " , clientes )
    #tableSize=CUR_Test.execute( "SELECT COUNT(*) FROM EspData")
    #print(tableSize)
    conn.commit()
    print("data inserted ..")
    cursor.execute( " SELECT * FROM EspData " )
    print(cursor.fetchall()[rowCounter()-1])
    # cou.close()
    #conn.close()
def deleteTag(tag:str):
    try:
        sql_delete_query = "DELETE FROM EspData WHERE tag = ?"
        cursor.execute(sql_delete_query,(tag,))
        conn.commit()
        return True
    except sqlite3.OperationalError as e:
        print(e)
        return False

def searchTag(Tag):
    Tag=Tag
    TagState=False
    sqlitequery="SELECT * FROM EspData WHERE tag =?"
    cursor.execute(sqlitequery,(Tag,))
    if (len(cursor.fetchall())) >0:
        cursor.execute(sqlitequery,(Tag,))
        TagRow=cursor.fetchall()
        TagState=True
        return TagState,TagRow
    else:
        TagState=False
        TagRow=[]
        return TagState,TagRow
# ionsert data into setting table for one time 
def insertSetting(mqtt_username:str, mqtt_password:str,mqtt_topic:str,mqtt_broker_ip:str,mqtt_port,R1_time:str,R2_time:str,R3_time:str):
    cursor.execute ( """ CREATE TABLE IF NOT EXISTS setting (
                           default_setting TEXT,
                           mqtt_username TEXT,
                           mqtt_password TEXT,
                           mqtt_topic TEXT,
                           mqtt_broker_ip TEXT,
                           mqtt_port TEXT,
                           R1time TEXT,
                           R2time TEXT,
                           R3time TEXT) """ )
    clientes =[("default_setting",mqtt_username, mqtt_password,mqtt_topic,mqtt_broker_ip,mqtt_port,R1_time,R2_time,R3_time)]
    cursor.executemany ( " INSERT INTO setting ( default_setting, mqtt_username , mqtt_password ,mqtt_topic ,mqtt_broker_ip ,mqtt_port, R1time,R2time ,R3time) VALUES ( ? ,? , ? , ?, ?, ?, ?, ?, ? ) " , clientes )
    #tableSize=CUR_Test.execute( "SELECT COUNT(*) FROM EspData")
    #print(tableSize)
    conn.commit()
    cursor.execute( " SELECT * FROM setting " )
    print(cursor.fetchall()[0])
    # cou.close()
    #conn.close()
#update data of a parametre where is in setting table and update his value 
def updateSetting(where:str,value:str):
    data=[(value,"default_setting")]
    query="UPDATE setting set "+where+" = ? where default_setting = ?"
    cursor.executemany (query,data )
    conn.commit()
    cursor.execute( " SELECT * FROM setting " )
    print(cursor.fetchall()[0])
#retrun data setting into dictonnary 
def getSetting(table:str):
    d={}
    selector1=cursor.execute( " SELECT * FROM "+table+"" )
    selector=selector1.fetchall()[0]
    for index,row in enumerate(cursor.description) :
        d[row[0]]=selector[index]
    return d
# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    print ("Connected!", str(rc))
    
def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    print("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
    #client.publish('device1/relay1', '1')

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass
# data=searchTag("1017")
# updateSetting("mqtt_port","1883")
# insertSetting("dell","talib2020","outTopic","localhost","1883","10#20","10#20","10#20")

# cursor.execute( "DROP TABLE IF EXISTS setting;" )
# print(cursor.fetchall()[0])

# updatedata("esp08",1000,datetime.now(),70,"0","0","50#40","25#40","30#40",10)
# print(reloadtime("2022-07-22 18:07:54.138015",60))
# print(deleteTag("585858"))



