from socket import *

serverAddress = ("", 50000)
ack = 0
last = 0
done = False
seqnum = 0

serverSocket = socket(AF_INET, SOCK_DGRAM)   
serverSocket.bind(serverAddress)

print("Ready")

cMessage, cAddr = serverSocket.recvfrom(100)     # Establish connection with client.
cMessage = cMessage.decode();
cMessage_list = cMessage.split()

if(cMessage_list[0].upper() == "GET" and not done):
    print("Sending ", (cMessage_list[1]))
    file = open(cMessage_list[1].encode(),'rb')
    l = file.read(90);
    
    while (l):
        seqnum = seqnum +1
        package = str(seqnum).encode()+ str(done).encode()+ l 
        serverSocket.sendto(package, cAddr)
        ACK, cAddr = serverSocket.recvfrom(100)
        print("ACK:", (ACK.decode()))
        l = file.read(90)
    file.close()
    
if(cMessage_list[0].upper() == "PUT" and not done):
    with open('put_file', 'wb') as f:
        print("Recieving:", cMessage_list[1])
        while True:
            message, cAddr = serverSocket.recvfrom(100)
            ack= ack+1 
            sACK = str(ack)
            serverSocket.sendto(sACK.encode(), cAddr)
            if not message:
                done = True
                break
            #write message to a file
            f.write(message)
    f.close()
    
    
serverSocket.shutdown(SHUT_RDWR)
serverSocket.close()
print('Done sending')