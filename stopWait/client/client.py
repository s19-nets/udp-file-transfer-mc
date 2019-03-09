from socket import *

serverAddress = ('localhost', 50000)

ack = 0 
last = 0
done = False

input = input("What would you like to do?")
input_list = input.split()

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.sendto(input.encode(), serverAddress)

if(input_list[0].upper() == "GET" and not done):
    with open('get_file', 'wb') as f:
        print("Recieving:", input_list[1])
        while True:
            message, serverAddrPort = clientSocket.recvfrom(100)
            message.decode()
            print("Message: ", message[0])
            ack= ack+1 
            sACK = str(ack)
            clientSocket.sendto(sACK.encode(), serverAddress)
            if not message:
                done = True
                break
            #write message to a file
            f.write(message)
    f.close()
    
if(input_list[0].upper() == "PUT" and not done):
    print("Sending", (input_list[1]))
    file = open(input_list[1].encode(),'rb')
    l = file.read(100);
    
    while (l):
        clientSocket.sendto(l, serverAddress)
        ACK, cAddr = clientSocket.recvfrom(100)
        print("ACK:", (ACK.decode()))
        l = file.read(100)
    file.close()
    
print("DONE")