from socket import *

serverAddress = ("", 50000)

ack = 0
last = 0
doneNum = 0
seqnum = 0
retry = False
done = False

serverSocket = socket(AF_INET, SOCK_DGRAM)   
serverSocket.bind(serverAddress)

print("Ready")

cMessage, cAddr = serverSocket.recvfrom(100)
cMessage = cMessage.decode();
cMessage_list = cMessage.split()

#GET file
if(cMessage_list[0].upper() == "GET"):
    print("Sending", (cMessage_list[1]))
    
    #Open requested file and read
    file = open(cMessage_list[1].encode(),'rb')
    l = file.read(90);
    
    
    while (l):
        
        #increment seqnum if not retrying
        if(not retry):
            seqnum = seqnum +1
        
        #prepare and insert into package
        sSeqnum = str(seqnum) + " "
        doneNum = str(doneNum)
        emptyString = " "
        package = sSeqnum.encode()+ doneNum.encode() + emptyString.encode() + l 
        
        #send to client and receive acknowledgement
        serverSocket.sendto(package, cAddr)
        ACK, cAddr = serverSocket.recvfrom(100)
        
        #Check to see if ack number is correct
        if(seqnum != int(ACK.decode())):
            retry = True
            
        #if it is, keep reading file
        if(not retry):
            l = file.read(80)
            #check to see if end of file
            if(len(l) < 80):
                doneNum = 1
    print('Done Sending')
    file.close()
    
#PUT file
if(cMessage_list[0].upper() == "PUT"):
    with open('put_file', 'wb') as f:
        print("Receiving:", cMessage_list[1])
        while True and not done:
            
            #Retrieve seqNum and done number(0 = not done, 1 = done)
            message, cAddr = serverSocket.recvfrom(100)
            splitMessage = message.decode('utf-8', 'ignore').split()
            seqNum = splitMessage[0]
            doneNum = splitMessage[1]
            
            if(int(doneNum) == 1):
                done = True
         
            #skip over the seqNum & doneNum
            if(int(seqNum) <10 ):
                text = message.decode('utf_8', 'ignore')[4:]
            elif(int(seqNum) >=10 and int(seqNum) <100):
                text = message.decode('utf_8', 'ignore')[5:]
            else:
                text = message.decode('utf_8', 'ignore')[6:]
            
            #Check to see if it's retrying
            if(int(seqNum) != ack):
                ack= ack+1 
                retry = False
            else:
                retry = True
                
            #send ack num
            sACK = str(ack)
            serverSocket.sendto(sACK.encode(), cAddr)
            
            if not message:
                done = True
                break
            #write message to a file if not retrying
            if not retry:
                f.write(text.encode())
    print('Done Receiving')
    f.close()
    
serverSocket.shutdown(SHUT_RDWR)
serverSocket.close()
