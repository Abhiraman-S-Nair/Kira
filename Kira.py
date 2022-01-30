#Creating Database
def dbcreate():
    mycon=mysql.connect(host="localhost", user="root", passwd = "root")
    mycur=mycon.cursor()
    mycur.execute("show databases")
    v=mycur.fetchall()
    f=0
    for i in v:
        if i[0]=="kira":
            f=1
         
    if f==0:
      mycon=mysql.connect(host="localhost",user="root",passwd="root")
      mycur=mycon.cursor()
      mycur.execute("create database Kira")
      mycon.commit()

      mycon=mysql.connect(host="localhost",user="root",passwd="root", database="Kira")
      mycur=mycon.cursor()
      mycur.execute("create table Diary(Date date, FileName char(20))")
      mycon.commit()

      mycon=mysql.connect(host="localhost",user="root",passwd="root", database="Kira")
      mycur=mycon.cursor()
      mycur.execute("create table Reminder(TaskName char(20), TaskDate datetime, TaskType char(20))")
      mycon.commit()

def cursorKira():
    global mycur, mycon
    mycon=mysql.connect(host="localhost",user="root",passwd="root", database="Kira")
    mycur=mycon.cursor()

def checkTask(N, DT):
    cursorKira()
    mycur.execute("select * from Reminder where TaskName=%s and TaskDate=%s",(N, DT))
    v=mycur.fetchall()
    if len(v)!=0:
        return False
    else:
        return True
        
def reminder(step):
    global N, DT
    global nameTask, datetimeTask
    if step==0:
        choice =0
        while choice !=4:
            print("1. Add Reminder")
            print("2. Edit Reminder")
            print("3. Delete Reminder")
            print("4. Back to Home Screen")
            choice=int(input("Enter your choice\n"))
            if choice in [1,2,3]:
                nameTask=input("Enter Task Name\n")
                dateTask=input("Enter Task Date in 'yyyy-mm-dd' format")
                timeTask= input("Enter Task Time in 'hh:mm:ss' format")
                datetimeTask= dateTask + " " + timeTask
                N, DT = nameTask, datetimeTask
            if choice ==1:
                reminder(1)
            elif choice ==2:
                reminder(2)
            elif choice ==3:
                reminder(3)
            elif choice !=4:
                print("Invalid Choice")
            
    elif step==1:
        if checkTask(nameTask, datetimeTask):
            print("1. Music")
            print("2. Long Vibration")
            print("3. Short Vibration")
            print("4. Notification Only")
            typeTask= int(input("Enter your choice\n"))
            while typeTask not in [1,2,3,4]:
                print("Invalid Choice")
                typeTask= int(input("Enter your choice\n"))
            cursorKira()
            mycur.execute("insert into Reminder values (%s, %s, %s)", (nameTask, datetimeTask, typeTask))
            mycon.commit()
        else:
            if input("Task already exist, Do you want to edit the task? (Yes/No)") == "Yes":
                reminder(2)
    elif step==2:
        if not checkTask(nameTask, datetimeTask):
            print("1. Task Name")
            print("2. Task Date and Time")
            print("3. Reminder Type")
            print("4. Back to Home Screen")
            editchoice=int(input("What do you want to edit?"))
            if editchoice ==1:
                new=input("Enter new Task Name\n")
                cursorKira()
                mycur.execute("update Reminder set TaskName=%s where TaskName=%s and TaskDate=%s",(new, N, DT))
                mycon.commit()
                print("Task Name edited Successfully...")
            elif editchoice ==2:
                newDate= input("Enter Task Date in 'yyyy-mm-dd' format")
                newTime= input("Enter Task Time in 'hh:mm:ss' format")
                newDateTime= newDate + " " + newTime
                cursorKira()
                mycur.execute("update Reminder set TaskDate=%s where TaskName=%s and TaskDate=%s",(newDateTime, N, DT))
                mycon.commit()
                print("Task Date and Time edited Successfully...")
            elif editchoice==3:
                print("1. Music")
                print("2. Long Vibration")
                print("3. Short Vibration")
                print("4. Notification Only")
                newType= int(input("Enter your choice\n"))
                while newType not in [1,2,3,4]:
                    print("Invalid Choice")
                    newType= int(input("Enter your choice\n"))
                cursorKira()
                mycur.execute("update Reminder set TaskType=%s where TaskName=%s and TaskDate=%s",(newType, N, DT))
                mycon.commit()
                print("Task edited Successfully...")
        else:
            if input("Task does not exist, Do you want to add a new task?") == "Yes":
                reminder(1)

    elif step ==3:
        if not checkTask(nameTask, datetimeTask):
            cursorKira()
            mycur.execute("delete from Reminder where TaskName=%s and TaskDate=%s",(N, DT))
            mycon.commit()
        else:
            print("Sorry, task does not exist\n")
            
def checkEntry(D):
    cursorKira()
    mycur.execute("select * from Diary where Date=%s",(D,))
    v=mycur.fetchall()
    if len(v)!=0:
        return False
    else:
        return True
    
def readDiary(D):
    cursorKira()
    mycur.execute("select FileName from Diary where Date=%s",(D,))
    v=mycur.fetchall()
    op=open(v[0][0],"r")
    print(op.read())
    op.close()
    
def appendDiary(D):
    cursorKira()
    mycur.execute("select FileName from Diary where Date=%s",(D,))
    v=mycur.fetchall()
    op=open(v[0][0],"a")
    lineList=[]
    n=int(input("Enter number of lines\n"))
    for i in range(n):
        lineList+=[input("Enter a Line\n")+"\n"]
    op.writelines(lineList)
    op.close()
    
def deleteDiary(D):
    cursorKira()
    mycur.execute("select FileName from Diary where Date=%s",(D,))
    v=mycur.fetchall()
    os.remove(v[0][0])
    cursorKira()
    mycur.execute("delete from Diary where Date=%s",(D,))
    mycon.commit()
    
def Diary(step):
    global date
    choice=0
    if step==0:
        while choice !=5:
            print("1. Write a New Entry")
            print("2. Read an Entry")
            print("3. Edit an Existing Entry")
            print("4. Delete an Entry")
            print("5. Back to Home Screen")
            choice=int(input("Enter your choice\n"))
            if choice in [1,2,3,4]:
                date=input("Enter date in 'yyyy-mm-dd' format")
            if choice==1:
                Diary(1)
            elif choice==2:
                Diary(2)
            elif choice==3:
                Diary(3)
            elif choice==4:
                Diary(4)
            elif choice !=5:
                print("Invalid Choice")
    elif step==1:
        if checkEntry(date):
            fileName=date+".txt"
            op=open(fileName, "w")
            lineList=[]
            n=int(input("Enter number of lines\n"))
            for i in range(n):
                lineList+=[input("Enter a Line\n")+"\n"]
            op.writelines(lineList)
            op.close()
            cursorKira()
            mycur.execute("insert into Diary values (%s, %s)", (date, fileName))
            mycon.commit()
            
        else:
            if input("Entry already exists. Do you want to edit? (Yes/No)") =="Yes":
                Diary(3)
                
    elif step==2:
        if not checkEntry(date):
            readDiary(date)
        else:
            if input("Entry does not exist. Do you want to write a new entry? (Yes/No)") =="Yes":
                Diary(1)

    elif step==3:
        if not checkEntry(date):
            appendDiary(date)
        else:
             if input("Entry does not exist. Do you want to write a new entry? (Yes/No)") =="Yes":
                 Diary(1)

    elif step==4:
        if not checkEntry(date):
            deleteDiary(date)
        else:
            print("Sorry, Entry does not exist\n")
            
#Music Player            
def music_player(emotion):
    try:
        file_name = emotion + ".mp3"
        playsound(file_name)
    except:
        return True

def emotional_support():
    inpt=0
    while inpt !=6:
        print("1.Happy\n2.Sad\n3.Stressed\n4.Creative\n5.Distracted\n6.Back to Home Screen")
        inpt = input("Please enter your choice:")
        try:
            inpt = int(inpt)
            if inpt >= 1 and inpt <= 6:
                if inpt == 1:
                    emotion = "Happy" 
                elif inpt == 2:
                    add_on = str(randint(1,2))
                    emotion = "Sad" + add_on
                elif inpt == 3:
                    emotion = "Stressed" 
                elif inpt == 4:
                    emotion = "Creative" 
                elif inpt == 5:
                    emotion = "Distracted"
                    
                try1=music_player(emotion)
            else:
                new_entry = input("Well then how 'are' you feeling today (in one word)? ")
                file1 = open("Emotions.txt", "w+")
                file1.write(new_entry.title())
                print("I'll make sure to find something to help you next time.")
                optn = input("For now would you like to hear a song from our existing playlist (Y/N)?")
                optn = optn.upper()
                if optn == "Y":
                    print("Please choose from one of the following.")
                    emotional_support()
                else:
                    print("Well then, Good Bye!")
                    exit()
        except ValueError:
            print("Please choose from one of the following.")
            emotional_support()

#Importing Modules    
import mysql.connector as mysql
import os
from playsound import playsound
from random import randint

#Main
dbcreate()
choice=0
while choice !=4:
    print("1. Diary")
    print("2. Reminder")
    print("3. Mood Booster")
    print("4. Exit")
    choice=int(input("Enter your choice\n"))
    if choice==1:
        Diary(0)
    elif choice==2:
        reminder(0)
    elif choice==3:
        print("How are you feeling today?")
        emotional_support()
    elif choice==4:
        break
    else:
        print("Invalid Choice")
