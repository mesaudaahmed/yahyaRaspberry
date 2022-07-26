#import date time for checking save time tag
from datetime import datetime,timedelta
#import datrabase librarey
import sqlite3

#start connection with database 
conn=sqlite3.connect("clientData.db")
cursor=conn.cursor()
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

# print(savetime("2022-07-22 01:52:14.237601"))
def rowCounter():
        with sqlite3.connect("clientData.db") as conn:
            cursor=conn.cursor()
            query="SELECT * FROM EspData"
            return len(cursor.execute(query).fetchall())

def insertdata(device:str, tag:int,save_time,reload_time,relay_state:str,eat_state,R1_time:str,R2_time:str,R3_time:str,days:int):
    #get the current date
    # current_time=datetime.now()
    # #get the current time by minutes
    # current_time_minute=current_time.hour*60+current_time.minute
    # print("the current tme is : "+str(current_time_minute))
    #start the connection with database 
    #fucos on the database it self 
    #creat a table into our database with three fields tag id and device wich is esp32 and the time 
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
# def searchTag2(Tag):
#     data=[]
#     Tag=Tag
#     TagState=False
#     sqlitequery="SELECT * FROM EspData WHERE tag =?"
#     cursor.execute(sqlitequery,(Tag,))
#     if (len(cursor.fetchall())) >0:
#         cursor.execute(sqlitequery,(Tag,))
#         TagState=True
#         data.append(TagState)
#         TagRow=cursor.fetchall()
#         data.append(TagRow)
#         return data
#     else:
#         TagState=False
#         data.append(TagState)
#         TagRow=[]
#         data.append(TagRow)
#         return data

# return SearchTag(Tag)
data=searchTag("1017")
print(data)
# print(t.TagRow)
# print(t.Tag)

# for i in range(50) : insertdata("esp08",1000+i,datetime.now(),70,"0","0","20#40","25#40","30#40",i)
# print(rowCounter())
# print(reloadtime("2022-07-22 18:07:54.138015",60))
# print(deleteTag("585858"))



