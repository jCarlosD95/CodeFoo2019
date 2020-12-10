from threading import *
import socket
import sys
import datetime
import pymysql.cursors


#Prevents escaping of characters in sent text
def esc(self):
        self = self.translate(str.maketrans({"-":  r"\-",
                                          "]":  r"\]",
                                          "\\": r"\\",
                                          "^":  r"\^",
                                          "$":  r"\$",
                                          "*":  r"\*",
                                          ".":  r"\.",
                                          "'":  r"`@@`",
                                          "\"": r"@``@",}))
        return self
#WHY ARE THERE 2 formatInput functions????
def formatInput(self):
    ret = ""
    #esc = escapeString(re.escape)
    for i in self:
        ret += str("('"+i[0]+"', '"
               +i[1]+"', '"
               +esc(i[2])+"', '"
               +i[3]+"'),\n")


    ret = list(ret)
    ret[-2] = ';'
    ret = "".join(ret)
    

    return ret
def formatInput(self):
    ret = ""
    #esc = escapeString(re.escape)
    for i in self:
        ret += str("('"+esc(i[0])+"', '"
               +esc(i[1])+"', '"
               +esc(i[2])+"', '"
               +esc(i[3])+"'),\n")


    ret = list(ret)
    ret[-2] = ';'
    ret = "".join(ret)
    

    return ret
        
    
#This class creates objects representing a connection to 1 client
class ClientListen(Thread):
    def __init__(self, socket, host, port):
        Thread.__init__(self)
        self.s = socket
        self.h = host
        self.p = port

        #stores history of messages sent by client
        self.history = []
        
        #Connect to client
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()
        self.uname = self.conn.recv(20)
        self.uname = self.uname.decode()


        #These 2 store partner client's info
        self.conn2 = None       
        self.addr2 = None
        self.uname2 = None

        print(self.uname +" Has connected to the server and is now online...")

    def set_partner(self, partner):
        self.conn2, self.addr2, self.uname2 = partner

    def get_info(self):
        return (self.conn, self.addr, self.uname)  

    def run(self):
        while 1:

            ##Receiving message
            incoming_msg = self.conn.recv(65535)
            incoming_msg = incoming_msg.decode()
            sent = str(datetime.datetime.now())[0:19]

            ##Sending message to recipient
            to_recipient = str('\n'+ self.uname +": "+ incoming_msg)
            to_recipient = to_recipient.encode()
            self.conn2.send(to_recipient)

            if incoming_msg == "Terminate program":
                return
            else:
                self.history.append((self.uname, self.uname2, incoming_msg, sent))

###Setting Up Chat Server
s = socket.socket()
host = socket.gethostname()


print("server will start on host: " + host)
print("\nserver is waiting for incoming connections\n")

port = 8080
s.bind((host,port))

print("\nserver bound to host and port successfully")

#Create the threads for each client
t1 = ClientListen(s, host, port)
t2 = ClientListen(s, host, port)



#Allow each thread to access the other thread's client
t1.set_partner(t2.get_info())
t2.set_partner(t1.get_info())

#The message history is stored here to be sent to db



#Run the threads
t1.start()
t2.start()

t1.join()
t2.join()

#Put message history into one string
history = t1.history + t2.history
history = formatInput(history)

#Establishing DB connection
connection = pymysql.connect(host = 'sql3.freemysqlhosting.net',
                             user = 'sql3284782',
                             port = 3306,
                             password = '1LunvIqLVb',
                             db = 'sql3284782',
                             cursorclass=pymysql.cursors.DictCursor)


try:
    with connection.cursor() as cursor:
        sql = "INSERT INTO messages(`sender`, `recipient`, `text`, `sent`) "
        sql += ("VALUES " + history)
        print(sql)
        cursor.execute(sql)
        connection.commit()

finally:
    connection.close()




    

    
     
