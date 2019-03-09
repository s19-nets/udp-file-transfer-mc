from socket import *

serverAddress = ('localhost', 50000)

ack = 0 
last = 0
doneNum = 0
seqnum = 0
done = False
retry = False

#Get user input
input = input("What would you like to do?")
input_list = input.split()

#Create socket and send user input
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.sendto(input.encode(), serverAddress)

#GET file
if(input_list[0].upper() == "GET"):
    with open('get_file', 'wb') as f:
        print("Receiving:", input_list[1])
        while True and not done:
            
            #Retrieve seqNum and done number (0 = not done, 1 = done)
            message, serverAddrPort = clientSocket.recvfrom(1000)
            splitMessage = message.decode('utf_8', 'ignore').split()
            seqNum = splitMessage[0]
            doneNum =  splitMessage[1]
            
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
            clientSocket.sendto(sACK.encode(), serverAddress)
            
            if not message:
                done = True
                break
            #write message to a file if not retrying
            if not retry:
                f.write(text.encode())
    print('Done Receiving')
    f.close()
    
#PUT file
if(input_list[0].upper() == "PUT"):
    print("Sending", (input_list[1]))
    
    #Open requested file 
    file = open(input_list[1].encode(),'rb')
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
        clientSocket.sendto(package, serverAddress)
        ACK, cAddr = clientSocket.recvfrom(100)
        
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
