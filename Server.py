import csv
import socket
import threading
import os
#lets Go#username:password  sign up
#log in#user:pass  sign in
#create_Repo:RepoName
#subDir#Repo:DirectoryInRepo


PORT = 7447
MESSAGE_LEN_SIZE = 1024
ENCODING = 'utf-8'


def main():
    addrss = socket.gethostbyname(socket.gethostname())
    Host_info = ("192.168.131.1", PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(Host_info)
    print("server start...")
    start(s)


def start(server):
    server.listen()
    while True:
        connection, addrss = server.accept()
        t = threading.Thread(target=handle_client, args=(connection, addrss))
        t.start()


def handle_client(connection, addrss):
    print("new connection from {}".format(addrss))
    string = "Hello Welcome To github..  :)\n sign in or sign up?"
    username=""
    connection.send(string.encode(ENCODING))
    connected = True
    while connected:
        message_len = int(connection.recv(MESSAGE_LEN_SIZE).decode(ENCODING))
        msg = connection.recv(message_len).decode(ENCODING)
        print("message recieve {}".format(msg))

        if msg == "disconnect":
            connection.send("Byee..hope to see you again".encode(ENCODING))
            connected = False
        if msg=="sign up":
            string ="choose your user pass and send like==>lets Go#username:password"
            connection.send(string.encode(ENCODING))

        if "lets Go" in msg:
            string=str(msg).split("#")
            parent_dir="C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase"
            new_user(string[1].split(":")[0],string[1].split(":")[1])
            create_dir(string[1].split(":")[0], parent_dir)
            string = "yay successfully sign up.. what do you want now ? "
            connection.send(string.encode(ENCODING))
            username=string[1].split(":")[0]

        if msg =="sign in":
            string ="Enter your user pass like this : log in#user:pass"
            connection.send(string.encode(ENCODING))

        if "log in" in msg:
            string = str(msg).split("#")
            username=string[1].split(":")[0]

            flag=old_user(string[1].split(":")[0], string[1].split(":")[1])
            print("here")
            if flag==True:
                string = "Successfully log in...what do you want now ?"
                connection.send(string.encode(ENCODING))


            else:
                string = "log in failed:( type sign in and try again.."
                connection.send(string.encode(ENCODING))

        if "create_Repo" in msg:
            string = str(msg).split(":")
            print(username)
            parent_dir=os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase", username,)
            create_dir(string[1], parent_dir)
            string = "Repository Created Successfully what do you want now ? "
            connection.send(string.encode(ENCODING))

        if "subDir" in msg:
            string = str(msg).split("#")
            Repo=string[1].split(":")[0]
            subdir=string[1].split(":")[1]
            parent_dir = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase", username, Repo)
            create_dir(subdir,parent_dir)
            string = "sub directory in {} created..so now? ".format(Repo)
            connection.send(string.encode(ENCODING))


    connection.close()


def create_dir(dir_name, paren_path):
    directory = dir_name
    path = os.path.join(paren_path, directory)

    os.mkdir(path)
    print("Directory '% s' created" % directory)


def send_msg(server, msg):
    message = msg.encode(ENCODING)
    msg_len = len(message)
    msg_len = str(msg_len).encode(ENCODING)
    msg_len += b' ' * (MESSAGE_LEN_SIZE - len(msg_len))
    server.send(msg_len)
    server.send(message)




def new_user(userName,password):

    field_names = ['username', 'password']

    dict = {'username':userName, 'password': password}

    with open('user-pass.csv', 'a') as f_object:

        dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)

        dictwriter_object.writerow(dict)

        f_object.close()




def old_user(userName,password):
    with open('user-pass.csv', newline="") as file:
        readData = [row for row in csv.DictReader(file)]

    size = len(readData)
    for i in range(size):
        user = readData[i]['username']
        pas  = readData[i]['password']
        if userName == user and pas==password:
            return True


    return False
if __name__ == '__main__':
    main()
