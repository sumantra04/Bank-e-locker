import tkinter as tk
from turtle import width
from PIL import ImageTk, Image
# from ctypes.wintypes import HWND
from distutils.cmd import Command
from cgitb import text
from turtle import width
import datetime as dt
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2
from subprocess import call
from subprocess import Popen, PIPE
import pygame
from tkinter import ttk
from pygame import mixer
# import wmi
import pyrebase
import tempfile
from time import strftime
# import RPi.GPIO as GPIO
import time
import bcrypt

firebaseConfig = {
    "apiKey": "AIzaSyAOVWu6ZKBef__T1BtjkSSaIKgzUBUpVWc",
    "authDomain": "fir-realtimedbdemo-55058.firebaseapp.com",
    "projectId": "fir-realtimedbdemo-55058",
    "databaseURL": "https://fir-realtimedbdemo-55058-default-rtdb.firebaseio.com/",
    "storageBucket": "fir-realtimedbdemo-55058.appspot.com",
    "messagingSenderId": "953731241353",
    "appId": "1:953731241353:web:85853ee4932219b2973d58",
    "measurementId": "G-XHGVSY3P57"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

spawnFlag = -1
checkFlag = 1
size = 0
flag = 2
train = 4
cpflag = 0
rsflag = 0
CP = -1
newPass = ''
accNo = ''
flash_delay = 800  # msec between colour change
flash_colours = ('aqua', '#150523')  # Two colours to swap between
dataReq = {}  # data fetched from server to check for login
dataRes = {}  # data fetched from the server at the time of login
mixer.init()  # initialising the mixer


def change_pass():
    chngkey = tk.Toplevel()
    chngkey.title("My Keypad")
    chngkey.geometry("800x480")
    chngkey.overrideredirect(1)
    print('change password triggered')
    print('spawnFlag= ',spawnFlag,'\n checkFlag= ',checkFlag)
    chngkey.configure(background="#150523")
    # keypad.overrideredirect(1)
    pin = tk.StringVar()

    chngkey.update()
    my_label = tk.Label(chngkey, text="Enter Account Number", font=("Orbitron", 13, "bold"), fg="aqua", bg="#150523")
    my_label.place(x=300, y=10)
    calcDisplay = tk.Entry(chngkey, textvariable=pin, relief=tk.GROOVE, justify="center", bd=0, bg="#150523",
                           fg="white", font=("Poppins Medium", 25,), show="*")
    calcDisplay.place(x=250, y=40, width=320, height=50)

    def action(number):
        current = calcDisplay.get()
        calcDisplay.delete(0, tk.END)
        calcDisplay.insert(0, str(current) + str(number))

    def actionClear():
        calcDisplay.delete(0, tk.END)

    def actionEnter():
        global rsflag, accNo, newPass
        if rsflag == 0:
            rsflag += 1
            print(rsflag)
            accNo = calcDisplay.get()  # user input account number
            my_label.configure(text="Enter New  Passkey")
        elif rsflag == 1:
            newPass = calcDisplay.get()
            print(rsflag)
            if (spawnFlag == 1 and checkFlag == 1):
                dbRef = db.child('MANAGER')
            elif (spawnFlag == 0 and checkFlag == 0):
                dbRef = db.child('USER')
            print(dbRef)
            d = dict((dbRef.get()).val())
            uKeys = list(d)
            print(uKeys)
            vals = d.values()
            print(vals)
            index = 0
            for item in vals:
                m = list(item.values())
                m[0] = bytes(m[0], 'utf-8')
                if bcrypt.hashpw(accNo.encode("utf-8"), m[0]) == m[0]:
                    break
                index += 1
            key = uKeys[index]
            newPass = str(bcrypt.hashpw(newPass.encode("utf-8"), bcrypt.gensalt()))[2:-1]
            if (spawnFlag == 1 and checkFlag == 1):
                db.child('MANAGER').child(key).update({'Password': newPass})
            elif (spawnFlag == 0 and checkFlag == 0):
                db.child('USER').child(key).update({'Password': newPass})
            # dbRef.child(key).update({'Password': newPass})
            my_label.configure(text="Passkey changed succesfully")
        actionClear()

        ################################################## ROW -> 1 ###############################################################

    btn1 = tk.Button(chngkey, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="1", command=lambda: action(1))
    # btn1.grid(row=1,column=0)
    btn1.place(x=300, y=100, width=60, height=60)
    btn2 = tk.Button(chngkey, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="2", command=lambda: action(2))
    # btn2.grid(row=1,column=1)
    btn2.place(x=380, y=100, width=60, height=60)
    btn3 = tk.Button(chngkey, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="3", command=lambda: action(3))
    # btn3.grid(row=1,column=2)
    btn3.place(x=460, y=100, width=60, height=60)

    ################################################## ROW -> 2 ###############################################################

    btn4 = tk.Button(chngkey, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="4", command=lambda: action(4))
    # btn4.grid(row=2,column=0)
    btn4.place(x=300, y=180, width=60, height=60)
    btn5 = tk.Button(chngkey, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="5", command=lambda: action(5))
    # btn5.grid(row=2,column=1)
    btn5.place(x=380, y=180, width=60, height=60)
    btn6 = tk.Button(chngkey, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="6", command=lambda: action(6))
    # btn6.grid(row=2,column=2)
    btn6.place(x=460, y=180, width=60, height=60)

    ################################################## ROW -> 3 ###############################################################

    btn7 = tk.Button(chngkey, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="7", command=lambda: action(7))
    # btn7.grid(row=3,column=0)
    btn7.place(x=300, y=260, width=60, height=60)
    btn8 = tk.Button(chngkey, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="8", command=lambda: action(8))
    # btn8.grid(row=3,column=1)
    btn8.place(x=380, y=260, width=60, height=60)
    btn9 = tk.Button(chngkey, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="9", command=lambda: action(9))
    # btn9.grid(row=3,column=2)
    btn9.place(x=460, y=260, width=60, height=60)

    ################################################## ROW -> 4 ###############################################################

    btnC = tk.Button(chngkey, padx=20, pady=10, font=("Digital Numbers", 18, "bold"), bg="#210c29", bd=1, fg="white",
                     text="C", command=lambda: actionClear())
    # btnC.grid(row=4,column=0)
    btnC.place(x=300, y=340, width=60, height=60)
    btn0 = tk.Button(chngkey, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="0", command=lambda: action(0))
    # btn0.grid(row=4,column=1)
    btn0.place(x=380, y=340, width=60, height=60)
    btnE = tk.Button(chngkey, padx=20, pady=10, font=("Digital Numbers", 18, "bold"), bg="#210c29", bd=1, fg="white",
                     text="E", command=lambda: actionEnter())
    # btnE.grid(row=4,column=2)
    btnE.place(x=460, y=340, width=60, height=60)
    dwnld = tk.PhotoImage(file="back.png")
    btn_back = tk.Button(chngkey, image=dwnld, borderwidth=0, relief=tk.SOLID, command=chngkey.destroy)
    btn_back.place(x=50, y=380, height=55, width=100)
    done = tk.Button(chngkey, relief=tk.GROOVE, text="DONE", borderwidth=0, fg="black", bg="white",
                     font=("Orbitron", 15, "bold"), command=finger_process)
    done.place(x=630, y=380)
    chngkey.mainloop()


def set_brightness(val):
    brightness = int(val) * 100  # percentage [0-100] For changing thee screen
    c = wmi.WMI(namespace='wmi')
    methods = c.WmiMonitorBrightnessMethods()[0]
    methods.WmiSetBrightness(brightness, 0)


# Coding the background music
def play_music():
    pygame.mixer.music.load("Sholay.mp3")
    pygame.mixer.music.play(-1)


def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)


def shutDown():
    call('sudo poweroff', shell=tk.TRUE)


def reboot():
    reboot_statement = "sudo shutdown -r -f now"
    popen_args = reboot_statement.split(" ")
    Popen(popen_args, stdout=PIPE, stderr=PIPE)


def settings_page():
    settings = tk.Toplevel()
    settings.title("Smart Locker UI")
    settings.geometry("800x480")
    settings.overrideredirect(1)
    settings.configure(bg="#150523")
    shut = tk.PhotoImage(file="shutdown.png")
    dwnd4 = tk.PhotoImage(file="back.png")
    # scan = tk.PhotoImage(file="scan.png")
    btn1 = tk.Button(settings, command=settings.destroy, relief=tk.GROOVE, image=dwnd4, borderwidth=0)
    # btn_scan = tk.Button(root,command=root.destroy,relief=tk.GROOVE,image=scan,borderwidth=0)
    btn1.place(x=30, y=390, )
    btn_shut = tk.Button(settings, text="SHUTDOWN", borderwidth=0, bg="white", fg="black",
                         font=("Orbitron", 15, "bold"), command=shutDown, relief=tk.GROOVE, image=shut)
    btn_shut.place(x=100, y=100, height=95, width=218)
    # btn_bio.grid(row=2, column=0)

    restart = tk.PhotoImage(file="restart.png")
    btn_reboot = tk.Button(settings, text="REBOOT", borderwidth=0, bg="white", fg="black",
                           font=("Orbitron", 15, "bold"), command=reboot, relief=tk.GROOVE, image=restart)
    btn_reboot.place(x=480, y=100, height=95, width=218)
    # btn_manage.grid(row=2, column=1)

    Volume_text = tk.Label(settings, text="ADJUST VOLUME", bg="#150523", fg="aqua", font=("Orbitron", 15, "bold"))
    Volume_text.place(x=480, y=250)

    Volume_scale = tk.Scale(settings, from_=100, to=0, orient=tk.VERTICAL, bg="#150523", fg="aqua",
                            font=("Orbitron", 11, "bold"), borderwidth=0, relief=tk.GROOVE, command=set_vol)
    Volume_scale.place(x=560, y=300)

    Brightness_text = tk.Label(settings, text="ADJUST BRIGHTNESS", bg="#150523", fg="aqua",
                               font=("Orbitron", 15, "bold"))
    Brightness_text.place(x=70, y=250)

    Brightness_scale = tk.Scale(settings, from_=100, to=0, orient=tk.VERTICAL, bg="#150523", fg="aqua",
                                font=("Orbitron", 11, "bold"), borderwidth=0, relief=tk.GROOVE, command=set_brightness)
    Brightness_scale.place(x=180, y=300)
    play_music()

    settings.mainloop()


def manager_check():
    global spawnFlag, checkFlag
    spawnFlag = 1
    checkFlag = 1
    mDB = (db.child('MANAGER').get()).val()
    # print(size)
    if (mDB):
        finger_process()
    else:
        manager_screen()


def manager_screen():
    manager = tk.Toplevel()
    manager.title("My Keypad")
    manager.geometry("800x480")
    manager.overrideredirect(1)
    manager.configure(background="#150523")
    # keypad.overrideredirect(1)
    pin = tk.StringVar()
    manager.update()
    # Bfile="BLUE.gif"
    # Rfile="Red.gif"
    # Gfile="Green.gif"

    # info1 = Image.open(Bfile)
    # info2 = Image.open(Gfile)
    # info3 = Image.open(Rfile)

    # frames1 = info1.n_frames  # gives total number of frames that gif contains
    # frames2 = info2.n_frames
    # frames3 = info3.n_frames

    # # creating list of PhotoImage objects for each frames
    # imB = [tk.PhotoImage(file=Bfile,format=f"gif -index {i}") for i in range(frames1)]
    # imG = [tk.PhotoImage(file=Gfile,format=f"gif -index {i}") for i in range(frames2)]
    # imR = [tk.PhotoImage(file=Rfile,format=f"gif -index {i}") for i in range(frames3)]

    # count = 0
    # anim = None

    # keypad labelling
    my_label = tk.Label(manager, text="Enter Registration Number", font=("Orbitron", 13, "bold"), fg="aqua",
                        bg="#150523")
    my_label.place(x=10, y=10)
    calcDisplay = tk.Entry(manager, textvariable=pin, relief=tk.GROOVE, justify="center", bd=0, bg="#150523",
                           fg="white", font=("Poppins Medium", 25,), show="*")
    calcDisplay.place(x=-15, y=40, width=320, height=50)

    def action(number):
        current = calcDisplay.get()
        calcDisplay.delete(0, tk.END)
        calcDisplay.insert(0, str(current) + str(number))

    def actionClear():
        calcDisplay.delete(0, tk.END)

    def actionEnter():
        global CP, cpflag, dataReq
        tempIn = ''
        if (CP == 0):
            if (cpflag == 0):
                cpflag += 1
                tempIn = calcDisplay.get()
                dataReq.update({"AccountNo": tempIn})
                my_label.configure(text="Enter Locker Number")
                my_label.place(x=40)
            elif (cpflag == 1):
                cpflag += 1
                tempIn = calcDisplay.get()
                dataReq.update({"LockerNo": tempIn})
                my_label.configure(text="Enter Password")
                my_label.place(x=60)
            elif (cpflag == 2):
                cpflag += 1
                tempIn = calcDisplay.get()
                dataReq.update({"Password": tempIn})
                my_label.configure(text="Details Entered Successfully")
                my_label.place(x=10)
        elif (CP == 1):
            if (cpflag == 0):
                cpflag += 1
                tempIn = calcDisplay.get()
                dataReq.update({"Id": tempIn})
                my_label.configure(text="Enter Password")
                my_label.place(x=60)
            elif (cpflag == 1):
                cpflag += 1
                tempIn = calcDisplay.get()
                dataReq.update({"Password": tempIn})
                my_label.configure(text="Details Entered Successfully")
                my_label.place(x=60)
        check = calcDisplay.get()
        actionClear()

    def pushData():
        global CP, uCount, mCount, dataReq
        print(CP)
        if (CP == 0):
            dataReq['AccountNo']= str(bcrypt.hashpw(dataReq['AccountNo'].encode("utf-8"), bcrypt.gensalt()))[2:-1]
            dataReq['Password']= str(bcrypt.hashpw(dataReq['Password'].encode("utf-8"), bcrypt.gensalt()))[2:-1]
            print(dataReq)
            db.child('USER').push(dataReq)
            dataReq = {}
        elif (CP == 1):
            dataReq['Id']= str(bcrypt.hashpw(dataReq['Id'].encode("utf-8"), bcrypt.gensalt()))[2:-1]
            dataReq['Password']= str(bcrypt.hashpw(dataReq['Password'].encode("utf-8"), bcrypt.gensalt()))[2:-1]
            print(dataReq,'M')
            db.child('MANAGER').push(dataReq)
            dataReq = {}

    def remData():
        global CP, dataReq
        if (CP == 0):
            # try:
            #     f = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000)
            #
            #     if ( f.verifyPassword() == False ):
            #         raise ValueError('The given fingerprint sensor password is wrong!')
            #
            # except Exception as e:
            #     print('The fingerprint sensor could not be initialized!')
            #     print('Exception message: ' + str(e))
            #     exit(1)

            d = dict((db.child('USER').get()).val())
            uKeys = list(d)
            match = list(dataReq.values())
            vals = d.values()
            index = 0
            fingerIndex = -1
            for item in vals:
                m = list(item.values())
                m[0] = bytes(m[0], 'utf-8')
                if bcrypt.hashpw(match[0].encode("utf-8"), m[0]) == m[0]:
                    fingerIndex = m[1]
                    break
                index += 1
            key = uKeys[index]
            # print(db.child('USER').child(key))
            db.child('USER').child(key).remove()
            print('user removed')

            try:
                if (f.deleteTemplate(fingerIndex) == True):
                    print('Template deleted!')

            except Exception as e:
                print('Operation failed!')
                print('Exception message: ' + str(e))
                exit(1)

        elif (CP == 1):
            try:
                f = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000)
                f1 = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

                if (f.verifyPassword() == False):
                    raise ValueError('The given fingerprint sensor password is wrong!')

            except Exception as e:
                print('The fingerprint sensor could not be initialized!')
                print('Exception message: ' + str(e))
                exit(1)

            d = dict((db.child('MANAGER').get()).val())
            uKeys = list(d)
            print(uKeys)
            print(dataReq)
            match = list(dataReq.values())
            vals = d.values()
            index = 0
            finger1 = -1
            finger2 = -1
            for item in vals:
                m = list(item.values())
                if (match[0] == m[2]):
                    finger1 = m[0]
                    finger2 = m[1]
                    break
                index += 1
            print(index)
            print(uKeys[index])
            key = uKeys[index]
            db.child('MANAGER').child(key).remove()
            print('manager removed')

            try:
                if (f1.deleteTemplate(finger1) == True and f.deleteTemplate(finger2)):
                    print('Template deleted!')

            except Exception as e:
                print('Operation failed!')
                print('Exception message: ' + str(e))
                exit(1)

    def animation(flag):
        display_label.configure(text="** Waiting For Fingerprint **")
        display_label.place(x=270, y=250)
        # global anim
        if flag == 1:
            # im = imG[count]
            display_label.configure(text="** MATCH FOUND **")
            display_label.place(x=310, y=250)
        elif flag == 0:
            # im = imR[count]
            display_label.configure(text="** NO MATCH FOUND **")
            display_label.place(x=290, y=250)
        elif flag == 2:
            print('hey')
            # im = imB[count]

        # gif_label.configure(image=im)
        # count += 1
        # if count == frames1 | count == frames2 | count == frames3:
        #     count = 0
        # anim = manager.after(20, lambda:animation(count,flag))

    # def stop_animation():
    # manager.after_cancel(anim)

    def fRegister():
        import time
        if (CP == 1):
            f1 = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000)

            try:
                if (f1.verifyPassword() == False):
                    raise ValueError('The given fingerprint sensor password is wrong!')

            except Exception as e:
                print('The fingerprint sensor could not be initialized!')
                print('Exception message: ' + str(e))
                exit(1)

        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if (f.verifyPassword() == False):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            exit(1)

        ## Gets some sensor information
        print('Currently used templates: ' + str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))

        ## Tries to enroll new finger
        try:
            print('Waiting for finger...')

            ## Wait that finger is read
            while (f.readImage() == False):
                pass

            ## Converts read image to characteristics and stores it in charbuffer 1
            f.convertImage(FINGERPRINT_CHARBUFFER1)

            ## Checks if finger is already enrolled
            result = f.searchTemplate()
            positionNumber = result[0]

            if (positionNumber >= 0):
                print('Template already exists at position #' + str(positionNumber))
                exit(0)

            print('Remove finger...')
            time.sleep(2)

            print('Waiting for same finger again...')

            ## Wait that finger is read again
            while (f.readImage() == False):
                pass

            ## Converts read image to characteristics and stores it in charbuffer 2
            f.convertImage(FINGERPRINT_CHARBUFFER2)

            ## Compares the charbuffers
            if (f.compareCharacteristics() == 0):
                raise Exception('Fingers do not match')

            ## Creates a template
            f.createTemplate()

            ## Saves template at new position number

            pN1 = f.storeTemplate()
            dataReq.update({"Finger1": pN1})
            if (CP == 0):
                print('User\'s Finger enrolled successfully!')
            elif (CP == 1):
                f.loadTemplate(pN1, charBufferNumber=FINGERPRINT_CHARBUFFER1)
                pN2 = f1.storeTemplate(f1.getTemplateCount() + 1, charBufferNumber=FINGERPRINT_CHARBUFFER1)
                print('Manager\'s Finger enrolled successfully!')
                dataReq.update({"Finger2": pN2})



        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            exit(1)

    ################################################## ROW -> 1 ###############################################################
    btn1 = tk.Button(manager, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="1", command=lambda: action(1))
    # btn1.grid(row=1,column=0)
    btn1.place(x=30, y=80, width=60, height=60)
    btn2 = tk.Button(manager, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="2", command=lambda: action(2))
    # btn2.grid(row=1,column=1)
    btn2.place(x=115, y=80, width=60, height=60)
    btn3 = tk.Button(manager, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="3", command=lambda: action(3))
    # btn3.grid(row=1,column=2)
    btn3.place(x=200, y=80, width=60, height=60)

    ################################################## ROW -> 2 ###############################################################

    btn4 = tk.Button(manager, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="4", command=lambda: action(4))
    # btn4.grid(row=2,column=0)
    btn4.place(x=30, y=160, width=60, height=60)
    btn5 = tk.Button(manager, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="5", command=lambda: action(5))
    # btn5.grid(row=2,column=1)
    btn5.place(x=115, y=160, width=60, height=60)
    btn6 = tk.Button(manager, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="6", command=lambda: action(6))
    # btn6.grid(row=2,column=2)
    btn6.place(x=200, y=160, width=60, height=60)

    ################################################## ROW -> 3 ###############################################################

    btn7 = tk.Button(manager, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="7", command=lambda: action(7))
    # btn7.grid(row=3,column=0)
    btn7.place(x=30, y=240, width=60, height=60)
    btn8 = tk.Button(manager, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="8", command=lambda: action(8))
    # btn8.grid(row=3,column=1)
    btn8.place(x=115, y=240, width=60, height=60)
    btn9 = tk.Button(manager, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="9", command=lambda: action(9))
    # btn9.grid(row=3,column=2)
    btn9.place(x=200, y=240, width=60, height=60)

    ################################################## ROW -> 4 ###############################################################

    btnC = tk.Button(manager, padx=20, pady=10, font=("Digital Numbers", 18, "bold"), bg="#210c29", bd=1, fg="white",
                     text="C", command=lambda: actionClear())
    # btnC.grid(row=4,column=0)
    btnC.place(x=30, y=320, width=60, height=60)
    btn0 = tk.Button(manager, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                     text="0", command=lambda: action(0))
    # btn0.grid(row=4,column=1)
    btn0.place(x=115, y=320, width=60, height=60)
    btnE = tk.Button(manager, padx=20, pady=10, font=("Digital Numbers", 18, "bold"), bg="#210c29", bd=1, fg="white",
                     text="E", command=lambda: actionEnter())
    # btnE.grid(row=4,column=2)
    btnE.place(x=200, y=320, width=60, height=60)
    back_img = tk.PhotoImage(file="back.png")
    btn_back = tk.Button(manager, image=back_img, borderwidth=0, relief=tk.SOLID, command=manager.destroy)
    btn_back.place(x=30, y=410, height=55, width=100)
    gif_label = tk.Label(manager, image="", bg="#150523")
    gif_label.place(x=300, y=280)
    display_label = tk.Label(manager, text="", font=("Orbitron", 13, "bold"), bg="#150523", fg="aqua", justify="center")
    display_label.place(x=300, y=80)
    iris = tk.PhotoImage(file="IrisButton.png")
    iris_button = tk.Button(manager, font=("Digital Numbers", 18, "bold"), bg="#210c29", image=iris, borderwidth=0,
                            relief=tk.SOLID, )
    iris_button.place(x=550, y=30, height=95, width=218)
    print_finger = tk.PhotoImage(file="fingerprint.png")
    finger_button = tk.Button(manager, font=("Digital Numbers", 18, "bold"), bg="#210c29", image=print_finger,
                              borderwidth=0, relief=tk.SOLID, command=lambda: fRegister())
    finger_button.place(x=550, y=140, height=95, width=218)
    register_button = tk.Button(manager, text="R E G I S T E R", font=("Orbitron", 18, "bold"), bg="#210c29", fg="aqua",
                                borderwidth=2, relief=tk.SOLID, command=lambda: pushData())
    register_button.place(x=550, y=250, height=95, width=218)

    delete_button = tk.Button(manager, text="D E L E T E", font=("Orbitron", 18, "bold"), bg="#210c29", fg="aqua",
                              borderwidth=2, relief=tk.SOLID, command=lambda: remData())
    delete_button.place(x=550, y=370, height=95, width=218)

    def show():
        label.config(text=clicked.get())

    # Dropdown menu options
    options = [
        "USER",
        "MANAGER",
    ]

    # datatype of menu text
    clicked = tk.StringVar()

    # initial menu text
    clicked.set("DROPDOWN")

    def checkPerson(*args):
        global CP, cpflag
        if (clicked.get() == "USER"):
            my_label.configure(text="Enter Account Number")
            my_label.place(x=30)
            CP = 0
            cpflag = 0
        elif (clicked.get() == "MANAGER"):
            my_label.configure(text="Enter ID Number")
            my_label.place(x=70)
            CP = 1
            cpflag = 0

    clicked.trace("w", checkPerson)
    # Create Dropdown menu
    drop = tk.OptionMenu(manager, clicked, *options, )
    drop.configure(bg="#210c29", fg="aqua", font=("Orbitron", 11, "bold"))
    drop.place(y=10, x=330)

    # Create button, it will change label text

    # Create Label
    label = tk.Label(manager, text="")
    label.place()
    manager.mainloop()


def finger_process():
    def key():
        keypad = tk.Toplevel()
        keypad.title("My Keypad")
        keypad.geometry("800x480")

        keypad.overrideredirect(1)
        keypad.configure(background="#150523")
        # keypad.overrideredirect(1)
        pin = tk.StringVar()

        keypad.update()

        # keypad labelling
        my_label = tk.Label(keypad, text="Enter PIN To Begin", font=("Orbitron", 15, "bold"), fg="aqua", bg="#150523")
        my_label.grid(row=0, column=0)
        my_label.pack(pady=10)
        calcDisplay = tk.Entry(keypad, textvariable=pin, relief=tk.GROOVE, justify="center", bd=0, bg="#150523",
                               fg="white", font=("Poppins Medium", 25,), show="*")
        calcDisplay.place(x=250, y=50, width=320, height=50)

        def action(number):
            current = calcDisplay.get()
            calcDisplay.delete(0, tk.END)
            calcDisplay.insert(0, str(current) + str(number))
            if (len(pin.get()) > 6):
                my_label.config(text="PIN Not More Than 6 Digits")
                pin.set("")

        def actionClear():
            calcDisplay.delete(0, tk.END)

        def doneEnable():
            done["state"] = tk.NORMAL
        def doneDisable():
            done["state"] = tk.DISABLED

        def actionEnter():
            global dataReq, dataRes
            if (spawnFlag == 1 and checkFlag == 1):
                dbRef = db.child('MANAGER')
            elif (spawnFlag == 0 and checkFlag == 1):
                dbRef = db.child('MANAGER')
            elif (spawnFlag == 0 and checkFlag == 0):
                dbRef = db.child('USER')

            d = dict((dbRef.get()).val())
            uKeys = list(d)
            dataReq.update({"Passkey": calcDisplay.get()})
            match = list(dataReq.values())
            vals = d.values()
            index = 0
            for item in vals:
                mK = list(item.keys())
                mV = list(item.values())
                index = mK.index('Password')
                mV[index] = bytes(mV[index], 'utf-8')
                if bcrypt.hashpw(match[0].encode("utf-8"), mV[index]) == mV[index]:
                    dataRes = {mK[i]: mV[i] for i in range(len(mK))}
                    print(dataRes)
                    actionClear()
                    # finger_process.destroy()
                    doneEnable()
                    my_label.config(text="Press Done to Proceed")
                    break
            else:
                my_label.config(text="Invalid PIN")
                pin.set("")
                doneDisable()
            actionClear()

        def Action():
            global train, checkFlag, dataReq

            if (spawnFlag == 1 and checkFlag == 1):
                dataReq = {}
                manager_screen()
                finger.destroy
            elif (spawnFlag == 0 and checkFlag == 1):
                # print('manager\'s authentication required')
                train = 5
                checkFlag = 0
                finger_process()
                finger.geometry("800x480")
            elif (spawnFlag == 0 and checkFlag == 0):
                finger.destroy
                # tempIn = ''
                # for i, j in dataRes.items():
                #     tempIn = bytes(dataRes[i], 'utf-8')
                #     tempIn = str(bcrypt.hashpw(tempIn.encode("utf-8"), bcrypt.gensalt()))[2:-1]
                #     dataReq[i] = tempIn
                index= list(dataRes.keys()).index('LockerNo')
                lockerNo = int(list(dataRes.values())[index])
                GPIO.setmode(GPIO.BOARD)
                GPIO.setwarnings(False)
                GPIO.setup(lockerNo, GPIO.OUT)

                GPIO.output(lockerNo, GPIO.HIGH)
                print('Locker Number ', lockerNo, 'opened')
                time.sleep(5)
                GPIO.output(lockerNo, GPIO.LOW)
                print('Locker Number ', lockerNo, 'closed')

        ################################################## ROW -> 1 ###############################################################
        btn1 = tk.Button(keypad, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                         text="1", command=lambda: action(1))
        # btn1.grid(row=1,column=0)
        btn1.place(x=300, y=100, width=60, height=60)
        btn2 = tk.Button(keypad, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                         text="2", command=lambda: action(2))
        # btn2.grid(row=1,column=1)
        btn2.place(x=380, y=100, width=60, height=60)
        btn3 = tk.Button(keypad, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                         text="3", command=lambda: action(3))
        # btn3.grid(row=1,column=2)
        btn3.place(x=460, y=100, width=60, height=60)

        ################################################## ROW -> 2 ###############################################################

        btn4 = tk.Button(keypad, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                         text="4", command=lambda: action(4))
        # btn4.grid(row=2,column=0)
        btn4.place(x=300, y=180, width=60, height=60)
        btn5 = tk.Button(keypad, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                         text="5", command=lambda: action(5))
        # btn5.grid(row=2,column=1)
        btn5.place(x=380, y=180, width=60, height=60)
        btn6 = tk.Button(keypad, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                         text="6", command=lambda: action(6))
        # btn6.grid(row=2,column=2)
        btn6.place(x=460, y=180, width=60, height=60)

        ################################################## ROW -> 3 ###############################################################

        btn7 = tk.Button(keypad, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                         text="7", command=lambda: action(7))
        # btn7.grid(row=3,column=0)
        btn7.place(x=300, y=260, width=60, height=60)
        btn8 = tk.Button(keypad, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                         text="8", command=lambda: action(8))
        # btn8.grid(row=3,column=1)
        btn8.place(x=380, y=260, width=60, height=60)
        btn9 = tk.Button(keypad, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                         text="9", command=lambda: action(9))
        # btn9.grid(row=3,column=2)
        btn9.place(x=460, y=260, width=60, height=60)

        ################################################## ROW -> 4 ###############################################################

        btnC = tk.Button(keypad, padx=20, pady=10, font=("Digital Numbers", 18, "bold"), bg="#210c29", bd=1, fg="white",
                         text="C", command=lambda: actionClear())
        # btnC.grid(row=4,column=0)
        btnC.place(x=300, y=340, width=60, height=60)
        btn0 = tk.Button(keypad, padx=20, pady=10, font=("Digital Numbers", 18,), bg="#210c29", bd=1, fg="#9DFFFF",
                         text="0", command=lambda: action(0))
        # btn0.grid(row=4,column=1)
        btn0.place(x=380, y=340, width=60, height=60)
        btnE = tk.Button(keypad, padx=20, pady=10, font=("Digital Numbers", 18, "bold"), bg="#210c29", bd=1, fg="white",
                         text="E", command=lambda: actionEnter())
        # btnE.grid(row=4,column=2)
        btnE.place(x=460, y=340, width=60, height=60)
        dwnld = tk.PhotoImage(file="back.png")
        btn_back = tk.Button(keypad, image=dwnld, borderwidth=0, relief=tk.SOLID, command=keypad.destroy)
        btn_back.place(x=50, y=380, height=55, width=100)
        change_passkey = tk.Button(keypad, relief=tk.GROOVE, text="CHANGE PASSKEY", borderwidth=0, fg="aqua",
                                   bg="#150523", font=("Orbitron", 15, "bold"), command=change_pass)
        change_passkey.place(x=290, y=420)
        done = tk.Button(keypad, relief=tk.GROOVE, text="DONE", borderwidth=0, fg="black", bg="white",
                         font=("Orbitron", 15, "bold"), command=Action, state=tk.DISABLED)
        done.place(x=630, y=380)
        keypad.mainloop()

    def open():
        process = tk.Toplevel()

        if (spawnFlag == 1 and checkFlag == 1):
            process.geometry("800x480")
        elif (spawnFlag == 0 and checkFlag == 1):
            process.geometry("800x480")
        elif (spawnFlag == 0 and checkFlag == 0):
            process.geometry("800x480")

        process.overrideredirect(1)
        process.configure(bg="#150523")

        # Bfile="BLUE.gif"
        # Rfile="Red.gif"
        # Gfile="Green.gif"

        # info1 = Image.open(Bfile)
        # info2 = Image.open(Gfile)
        # info3 = Image.open(Rfile)

        # frames1 = info1.n_frames  # gives total number of frames that gif contains
        # frames2 = info2.n_frames
        # frames3 = info3.n_frames

        # # creating list of PhotoImage objects for each frames
        # imB = [tk.PhotoImage(file=Bfile,format=f"gif -index {i}") for i in range(frames1)]
        # imG = [tk.PhotoImage(file=Gfile,format=f"gif -index {i}") for i in range(frames2)]
        # imR = [tk.PhotoImage(file=Rfile,format=f"gif -index {i}") for i in range(frames3)]

        # count = 0
        # anim = None
        def animation(flag):
            display_label.configure(text="*** Waiting For Fingerprint ***")
            display_label.place(x=220, y=80)
            # global anim
            if flag == 1:
                # im = imG[count]
                display_label.configure(text="*** MATCH FOUND ***")
                display_label.place(x=270, y=80)
            elif flag == 0:
                # im = imR[count]
                display_label.configure(text="*** NO MATCH FOUND ***")
                display_label.place(x=240, y=80)
            elif flag == 2:
                # im = imB[count]
                print('hey')

        #     gif_label.configure(image=im)
        #     count += 1
        #     if count == frames1 | count == frames2 | count == frames3:
        #         count = 0
        #     anim = process.after(20, lambda:animation(count,flag))

        # def stop_animation():
        #     process.after_cancel(anim)

        def doneEnable():
            done["state"] = tk.NORMAL

        def Finger_scan():
            portStr = ''
            if (spawnFlag == 1 and checkFlag == 1):
                portStr = '/dev/ttyUSB0'
            elif (spawnFlag == 0 and checkFlag == 1):
                portStr = '/dev/ttyUSB1'
            elif (spawnFlag == 0 and checkFlag == 0):
                portStr = '/dev/ttyUSB0'

            try:
                f = PyFingerprint(portStr, 57600, 0xFFFFFFFF, 0x00000000)

                if (f.verifyPassword() == False):
                    raise ValueError('The given fingerprint sensor password is wrong!')

            except Exception as e:
                print('The fingerprint sensor could not be initialized!')
                print('Exception message: ' + str(e))
                exit(1)

            print('Currently used templates: ' + str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))

            try:
                print('Waiting for finger...')

                ## Wait that finger is read
                while (f.readImage() == False):
                    pass

                ## Converts read image to characteristics and stores it in charbuffer 1
                f.convertImage(0x01)

                ## Searchs template
                result = f.searchTemplate()

                positionNumber = result[0]
                accuracyScore = result[1]

                if (positionNumber == -1):
                    flag = 0
                    print(flag)
                    print('No match found!')
                    animation(flag)


                else:
                    flag = 1
                    print(flag)
                    # animation(count)
                    print('Found template at position #' + str(positionNumber))
                    print('The accuracy score is: ' + str(accuracyScore))
                    doneEnable()
                    animation(flag)

                ## OPTIONAL stuff
                ##

                ## Loads the found template to charbuffer 1
                f.loadTemplate(positionNumber, 0x01)

                ## Downloads the characteristics of template loaded in charbuffer 1
                characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

                ## Hashes characteristics of template
                print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

            except Exception as e:
                print('Operation failed!')
                print('Exception message: ' + str(e))

            # def stop_animation():
            #     root.after_cancel(anim)

        def Action():
            global train, checkFlag
            if (spawnFlag == 1 and checkFlag == 1):
                manager_screen()
                finger.destroy
            elif (spawnFlag == 0 and checkFlag == 1):
                # print('manager\'s authentication required')
                train = 5
                checkFlag = 0
                finger_process()
                finger.geometry("800x480")

            elif (spawnFlag == 0 and checkFlag == 0):
                finger.destroy
                lockerNo = int(list(dataRes.values())[2])
                # GPIO.setmode(GPIO.BOARD)
                # GPIO.setwarnings(False)
                # GPIO.setup(lockerNo,GPIO.OUT)
                #
                # GPIO.output(lockerNo, GPIO.HIGH)
                print('Locker Number ', lockerNo, 'opened')
                time.sleep(5)
                # GPIO.output(lockerNo, GPIO.LOW)
                print('Locker Number ', lockerNo, 'closed')

        gif_label = tk.Label(process, image="", bg="#150523")
        gif_label.place(x=300, y=160)
        heading_label = tk.Label(process, text="FINGERPRINT SCAN", font=("Orbitron", 18, "bold"), bg="#150523",
                                 fg="aqua", justify="center")
        heading_label.place(x=250, y=30)
        display_label = tk.Label(process, text="** Click On The SCAN Button To Begin **", font=("Orbitron", 15, "bold"),
                                 bg="#150523", fg="aqua", justify="center")
        display_label.place(x=160, y=80)
        dwnd4 = tk.PhotoImage(file="back.png")
        scan = tk.PhotoImage(file="scan.png")
        btn1 = tk.Button(process, command=process.destroy, relief=tk.GROOVE, image=dwnd4, borderwidth=0)
        btn_scan = tk.Button(process, relief=tk.GROOVE, image=scan, borderwidth=0, command=lambda: Finger_scan())
        btn1.place(x=30, y=380, )
        btn_scan.place(x=340, y=370)
        done = tk.Button(process, relief=tk.GROOVE, text="DONE", borderwidth=0, fg="black", bg="white",
                         font=("Orbitron", 15, "bold"), command=Action, state=tk.DISABLED)
        done.place(x=630, y=380)
        process.mainloop()

    finger = tk.Toplevel()
    finger.title("")

    if (spawnFlag == 1 and checkFlag == 1):
        finger.geometry("800x480")
    elif (spawnFlag == 0 and checkFlag == 1):
        finger.geometry("800x480")
    elif (spawnFlag == 0 and checkFlag == 0):
        finger.geometry("800x480")

    finger.overrideredirect(1)
    finger.configure(bg="#150523")
    back_img = tk.PhotoImage(file="back.png")
    fingerprint_img = tk.PhotoImage(file="fingerprint.png")
    passkey_img = tk.PhotoImage(file="passkey.png")

    btn = tk.Button(finger, image=fingerprint_img, borderwidth=0, relief=tk.SOLID, command=open)
    btn.place(x=150, y=190, height=95, width=218)
    # btn_bio.grid(row=2, column=0)

    btn1 = tk.Button(finger, image=passkey_img, borderwidth=0, relief=tk.SOLID, command=key)
    btn1.place(x=400, y=190, height=95, width=218)
    # btn_manage.grid(row=2, column=1)
    btn_back = tk.Button(finger, image=back_img, borderwidth=0, relief=tk.GROOVE, command=finger.destroy)
    btn_back.place(x=30, y=380, )
    # ok = tk.Button(finger, relief=tk.GROOVE,text="DONE",borderwidth=0,fg="black",bg="white",font=("Orbitron", 15, "bold"),command=finger.destroy)
    # ok.place(x=630,y=380)
    finger.mainloop()


def iris_process():
    def popUp():
        display_label.config(text="Waiting For Manager's Authentication...")
        # pushing into the requests section

        RAdata = {'test2': 'UNAUTHORISED'}
        db.child('requests').set(RAdata)
        display_label.place(x=180)

    def flashColour(object, colour_index):
        object.config(foreground=flash_colours[colour_index])
        iris_scan.after(flash_delay, flashColour, object, 1 - colour_index)

    def switch():
        global train, checkFlag
        if (train == 4):
            btn1["state"] = tk.DISABLED
            btn_scan["state"] = tk.DISABLED
            print('manager\'s authentication required')
            while (True):
                if (list(dict(db.child('SUCCESS').get().val()).keys()).__contains__('test2')):
                    train = 5
                    checkFlag = 0
                    finger_process()

        elif (train == 5):  # authentication succeded from fingerprint 2
            btn1["state"] = tk.DISABLED
            btn_scan["state"] = tk.DISABLED
            finger_process.destroy()

    iris_scan = tk.Toplevel()
    iris_scan.title("Smart Locker UI")
    iris_scan.geometry("800x480")
    iris_scan.configure(bg="#150523")
    iris_scan.overrideredirect(1)
    heading_label = tk.Label(iris_scan, text="IRIS SCAN", font=("Orbitron", 18, "bold"), bg="#150523", fg="aqua",
                             justify="center")
    heading_label.place(x=320, y=30)
    display_label = tk.Label(iris_scan, text="** Click On The SCAN Button To Begin **", font=("Orbitron", 15, "bold"),
                             bg="#150523", foreground=flash_colours[0], justify="center")
    display_label.place(x=160, y=80)
    dwnd4 = tk.PhotoImage(file="back.png")
    # scan = tk.PhotoImage(file="scan.png")
    btn1 = tk.Button(iris_scan, command=iris_scan.destroy, relief=tk.GROOVE, image=dwnd4, borderwidth=0)
    # btn_scan = tk.Button(root,command=root.destroy,relief=tk.GROOVE,image=scan,borderwidth=0)
    btn1.place(x=30, y=380, )
    # btn_scan.place(x= 420, y=390)
    scan = tk.PhotoImage(file="scan.png")
    btn_scan = tk.Button(iris_scan, relief=tk.GROOVE, image=scan, borderwidth=0, command=lambda: [popUp(), switch(), ])
    btn_scan.place(x=340, y=370)
    flashColour(display_label, 0)
    iris_scan.mainloop()


def biometrics():
    global spawnFlag
    spawnFlag = 0
    iris_button = tk.Toplevel()
    iris_button.geometry("800x480")
    iris_button.overrideredirect(1)
    iris_button.configure(bg="#150523")

    back_img = tk.PhotoImage(file="back.png")
    irisscan_img = tk.PhotoImage(file="IrisButton.png")

    btn_irish = tk.Button(iris_button, image=irisscan_img, borderwidth=0, relief=tk.SOLID, command=iris_process)
    btn_irish.place(x=280, y=190, height=95, width=218)
    btn_back = tk.Button(iris_button, image=back_img, borderwidth=0, relief=tk.GROOVE, command=iris_button.destroy)
    btn_back.place(x=30, y=380)

    iris_button.mainloop()


root = tk.Tk()
root.title("Smart Locker UI")
root.geometry("800x480")
root.overrideredirect(1)
root.configure(bg="#150523")
bio_img = tk.PhotoImage(file="button1.png")
manage_img = tk.PhotoImage(file="button2.png")
setting_img = tk.PhotoImage(file="button3.png")
btn_bio = tk.Button(root, image=bio_img, borderwidth=0, command=biometrics)
btn_bio.place(x=20, y=190, height=95, width=218)
# btn_bio.grid(row=2, column=0)

btn_manage = tk.Button(root, image=manage_img, borderwidth=0, command=manager_check)
btn_manage.place(x=280, y=190, height=95, width=218)
# btn_manage.grid(row=2, column=1)

btn_setting = tk.Button(root, image=setting_img, borderwidth=0, command=settings_page)
btn_setting.place(x=540, y=190, height=95, width=218)


# btn_setting.grid(row=2, column=2)

def time():
    string = strftime('%H:%M:%S %p')
    lbl.config(text=string)
    lbl.after(1000, time)


date = dt.datetime.now()
# Create Label to display the Date
label = tk.Label(root, text=f"{date:%A, %B %d, %Y}", font=("Orbitron", 11), bg="#150523", fg="aqua")
label.place(x=570, y=430)
lbl = tk.Label(root, font=('Orbitron', 11,),
               background='#150523',
               foreground='aqua')
lbl.place(x=670, y=390)
time()

root.mainloop()
