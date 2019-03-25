from threading import *
import socket
import sys
import datetime
import pymysql.cursors

from PyQt5.QtWidgets import *#QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGridLayout, QLineEdit, QMessageBox, QTreeView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QPixmap, QImage, QIcon
from PyQt5.QtCore import pyqtSlot, Qt
#from urllib.request import Request, urlopen


##Sending message
class Talk(Thread):
    def run(self):
        while 1:
            msg = input(str(">> "))
            msg = msg.encode()
            s.send(msg)
            
##Receiving message
class Listen(Thread):
    def run(self):
        incoming_msg = None
        while not incoming_msg == "Terminate program":
            incoming_msg = s.recv(65535)
            incoming_msg = incoming_msg.decode()
            print(incoming_msg)

            if incoming_msg == "Terminate program":
                print("Other user has terminated the program. Goodbye!")
                exit_cmd = "Terminate program"
                exit_cmd = exit_cmd.encode()
                s.send(exit_cmd)
                sys.exit(0)


s = socket.socket()
#The client puts their username.
#The database tracks who the sender and who the recipient of each
#message is by their usernames.
uname = input(str("Enter your username (3-20 chars). DON'T FORGET IT! "))

#Connects to server 
host = input(str("please enter the hostname of the server: "))
port = 8080
s.connect((host,port))

#sends username 
uname = uname.encode()
s.send(uname)


print("\nConnected to chat server. Welcome,", uname.decode())
print("To terminate your connection, type \"Terminate program\"")


talk = Talk()
listen = Listen()

listen.start()
talk.start()

    



