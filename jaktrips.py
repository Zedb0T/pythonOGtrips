import time
import random
import socket
import os
import struct
import subprocess
import time
import sys
import random
from dotenv import load_dotenv
from os.path import exists

#Set the working directory
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(os.path.realpath(sys.executable))
elif __file__:
    application_path = os.path.dirname(__file__)

#out\build\Release\bin\gk -v -- -boot -fakeiso -debug

#paths
PATHTOGOALC = application_path + "\goalc.exe"
PATHTOGK = application_path +"\gk.exe -v -- -boot -fakesiso -debug"

#
#Function definitions
#
def sendForm(form):
    header = struct.pack('<II', len(form), 10)
    clientSocket.sendall(header + form.encode())
    print("Sent: " + form)
    return

#Launch REPL, connect bot, and mi

#This splits the Gk commands into args for gk.exe
GKCOMMANDLINElist = PATHTOGK.split()

#Close Gk and goalc if they were open.
print("If it errors below that is O.K.")
subprocess.Popen("""taskkill /F /IM gk.exe""",shell=True)
subprocess.Popen("""taskkill /F /IM goalc.exe""",shell=True)
time.sleep(3)

#Open a fresh GK and goalc then wait a bit before trying to connect via socket
print("opening " + PATHTOGK)
print("opening " + PATHTOGOALC)
GK_WIN = subprocess.Popen(GKCOMMANDLINElist)
GOALC_WIN = subprocess.Popen([PATHTOGOALC])
time.sleep(3)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
clientSocket.connect(("127.0.0.1", 8181))
time.sleep(1)
data = clientSocket.recv(1024)
print(data.decode())

#Int block these comamnds are sent on startup
sendForm("(lt)")
sendForm("(mi)")
sendForm("(send-event *target* 'get-pickup (pickup-type eco-red) 5.0)")
sendForm("(dotimes (i 1) (sound-play-by-name (static-sound-name \"cell-prize\") (new-sound-id) 1024 0 0 (sound-group sfx) #t))")
sendForm("(set! *cheat-mode* #f)")
sendForm("(set! *debug-segment* #f)")
#End Int block

startingTime = time.time()
timerTrigger = 60 * .25
chanceToTrigger = 90

while True:
    #need to track the current time, and the elasped time
    currentTime = time.time()
    elapsedTime = currentTime - startingTime

    #if the amount of elapsed time is enough to trigger, then do an action
    if elapsedTime >= timerTrigger:
        print("Time has triggered! Starting event now")
        
        if chanceToTrigger >= random.randint(0, 100):
            print("Probably check passed! we will run the event")
            #Do stuff here
            sendForm("(go-process *target* target-load-wait)")
        else:
            print("Probablilty check did not pass, we will not run this time.")
            #Dont Do stuff here
        #reset startingTime to be whatever the current time is
        print("Event should be finished now, restoring startingTime")
        print("")
        startingTime = currentTime




