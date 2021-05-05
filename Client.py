import socket
PORT=7447
MESSAGE_LEN_SIZE=1024
ENCODING ='utf-8'

def main():
    addrss = socket.gethostbyname(socket.gethostname())
    Host_info = ("192.168.131.1", PORT)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(Host_info)
    message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
    if message:
     print(message)

    while True:

     Request=input()
     send_msg(s,Request)
     if Request == "disconnect":
         message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
         if message:
             print(message)
         exit()

     if Request=="sign up" :
         message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
         if message:
             print(message)

     if Request == "sign in":
         message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
         if message:
             print(message)

     if "lets Go" in Request:
         message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
         if message:
             print(message)

     if "log in" in Request:
         message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
         if message:
             print(message)

     if "create_Repo" in Request:
         message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
         if message:
             print(message)

     if "subDir" in Request:
         message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
         if message:
             print(message)




def send_msg(client,msg):
  message = msg.encode(ENCODING)
  msg_len= len(message)
  msg_len =str(msg_len).encode(ENCODING)
  msg_len +=b' '*(MESSAGE_LEN_SIZE-len(msg_len))
  client.send(msg_len)
  client.send(message)





if __name__ =='__main__':
  main()