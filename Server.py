import csv
import datetime
import shutil
import socket
import threading
import os

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

    username = ""
    connection.send(string.encode(ENCODING))
    connected = True
    while connected:
        message_len = int(connection.recv(MESSAGE_LEN_SIZE).decode(ENCODING))
        msg = connection.recv(message_len).decode(ENCODING)
        print("message recieve {}".format(msg))

        if msg == "disconnect":
            connection.send("Byee..hope to see you again".encode(ENCODING))
            connected = False
        if msg == "sign up":
            string = "choose your user pass and send like==>lets Go#username:password"
            connection.send(string.encode(ENCODING))

        if "lets Go" in msg:
            string = str(msg).split("#")
            parent_dir = "C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase"
            new_user(string[1].split(":")[0], string[1].split(":")[1])
            create_dir(string[1].split(":")[0], parent_dir)
            # create file for all commits of this user
            all_commit_path = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase",
                                           string[1].split(":")[0], "all_commit.txt")
            username = string[1].split(":")[0]
            f = open(all_commit_path, "x")
            f.close()
            string = "yay successfully sign up.. what do you want now ? \n"
            string += "create_Repo:RepoName:pborpv\nsubDir#Repo:nameofsubdir:forwho:pathtosave\nadd_contributer:RepoName:username:Repofor\n"
            string += "want pull:Repo:forwho\nwant push:Repo:Repofor\nwant download\nclient commit\nif synch:Reponame:owner\ndisconnect"
            connection.send(string.encode(ENCODING))

            print(";;;;"+str(username))

        if msg == "sign in":
            string = "Enter your user pass like this : log in#user:pass"
            connection.send(string.encode(ENCODING))

        if "log in" in msg:
            string = str(msg).split("#")
            username = string[1].split(":")[0]

            flag = old_user(string[1].split(":")[0], string[1].split(":")[1])
            print("here")
            if flag == True:
                string = "Successfully log in...what do you want now ?\n"
                string += "create_Repo:RepoName:pborpv\nsubDir#Repo:nameofsubdir:forwho:pathtosave\nadd_contributer:RepoName:username:Repofor\n"
                string += "want pull:Repo:forwho\nwant push:Repo:Repofor\nwant download\nclient commitif synch:Reponame:owner\ndisconnect"
                connection.send(string.encode(ENCODING))


            else:
                string = "log in failed:( type sign in and try again.."
                connection.send(string.encode(ENCODING))

        if "create_Repo" in msg:
            string = str(msg).split(":")

            print(username)
            parent_dir = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase", username)
            create_dir(string[1], parent_dir)
            # a file that store commits about this repo
            repo_commit = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase", username, string[1],
                                       "commits")
            repo_commit += ".txt"
            f = open(repo_commit, "x")
            f.close()
            contributer = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase", username, string[1],
                                       "contributer")
            contributer += ".txt"


            f = open(contributer, "x")
            f.close()
            if str(string[2]) == "private":
                with open(contributer, "w") as f:
                    string = "private"
                    f.write(string)
                    f.write("\n")
                    f.close()
            elif str(string[2]) == "public":
                with open(contributer, "w") as f:
                    string = "public"
                    f.write(string)
                    f.write("\n")
                    f.close()


            with open(contributer, "a") as f:
                string="owner:"+str(username)
                f.write(string)
                f.write("\n")
                f.close()

            string = "Repository Created Successfully what do you want now ? "
            connection.send(string.encode(ENCODING))

        if "subDir" in msg:

            string = str(msg).split("#")
            Repo = string[1].split(":")[0]
            subdir = string[1].split(":")[1]
            for_who = string[1].split(":")[2]
            path = string[1].split(":")[3]
            contributers = os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', for_who, Repo,
                                        "contributer.txt")
            file = open(contributers)
            if (username in file.read()):
                parent_dir = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase",path)
                create_dir(subdir, parent_dir)
                string = "sub directory in {} created..so now? ".format(Repo)
                connection.send(string.encode(ENCODING))
            else:
                string = "you dont have permission to create subdir -.-"
                connection.send(string.encode(ENCODING))
            file.close()

        if "want push" in msg:
            string = str(msg).split(":")
            print(string)
            Repo=string[1]
            for_who=string[2]
            if os.path.exists(os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', for_who, Repo)):
                contributers = os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', for_who, Repo,
                                            "contributer.txt")
                file = open(contributers)
                if (username in file.read()):
                    string = "You have access to push ;)"
                    connection.send(string.encode(ENCODING))
                    for root, dirs, files in os.walk(os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', for_who, Repo)):

                        for name in files:
                            if name!="commits.txt" and name!="contributer.txt":
                             os.remove(os.path.join(root, name))
                        for dir in dirs:
                            shutil.rmtree(os.path.join(root, dir))

                else:
                    string = "Sorry you dont have permission -.- you can try push in your git server if you want"
                    connection.send(string.encode(ENCODING))
            else:
                string="this Repo doesnt exist...first create it then try to push"
                connection.send(string.encode(ENCODING))





        if msg == "ok":
            string = "Ok I wait for you"
            connection.send(string.encode(ENCODING))

        if "Go to Push" in msg:

            string = str(msg).split("#")
            file_path = string[1]
            Repo_name = string[2]
            for_who = string[3]
            contributers = os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', for_who, Repo_name,
                                        "contributer.txt")
            file = open(contributers)
            if (username in file.read()):
                string = "You have access to push ;)"
                file.close()
                connection.send(string.encode(ENCODING))

                string = str(msg).split("#")
                content = string[4]
                print(content)
                print(";;;;;;;")
                # read_file = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients", username, file_path)
                # with open(f"{read_file}", "r") as f:
                #     content = f.read()

                write_file = os.path.join(file_path)
                print(write_file)
                print("===========")

                with open(write_file, "w") as f:
                    f.write(content)
                    f.close()
                string = "push successfully"
                connection.send(string.encode(ENCODING))

            else:
                string = "Sorry you dont have permission -.- you can try push in your git server if you want"
                connection.send(string.encode(ENCODING))
            file.close()

        if "append_commit" in msg:
            string = str(msg).split("#")
            commit_path = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase", for_who, string[2],
                                       "commits.txt")
            file_object = open(commit_path, 'a')

            file_object.write(string[1])

            file_object.close()
            all_commit_path = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase", username,
                                           "all_commit.txt")
            file_object = open(all_commit_path, 'a')

            file_object.write(string[1])

            file_object.close()
            string = "commits add to server successfully"
            connection.send(string.encode(ENCODING))
            file_object.close()

        if "want pull" in msg:
            string=str(msg).split(":")
            contributer_path = os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', string[2], string[1],"contributer.txt")
            file = open(contributer_path)
            print(file.read())
            file.close()
            file = open(contributer_path)
            if "private" in file.read():
                file.close()
                file = open(contributer_path)
                if username in file.read():
                    file.close()
                    string="this Repo is private but you have access to pull"
                    connection.send(string.encode(ENCODING))
                else:
                    file.close()
                    string="this Repo is private and you have not access to pull"
                    connection.send(string.encode(ENCODING))
            file.close()
            file = open(contributer_path)
            if "public" in file.read():

                file.close()
                string="This Repo is public..Be free to pull"
                connection.send(string.encode(ENCODING))



        if "please pull" in msg:
            splitt = str(msg).split("#")
            which_user = splitt[1]
            which_repo = splitt[2]
            print(os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', which_user, which_repo))
            if os.path.exists(os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', which_user, which_repo)):
                repo_path = os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', which_user,
                                         which_repo)
                connection.send(str(repo_path).encode(ENCODING))
            else:
                string = "what you want nothing found...try again"
                connection.send(str(string).encode(ENCODING))

        if "add_contributer" in msg:
            splitt = str(msg).split(":")
            Repo = splitt[1]
            cont_name = splitt[2]
            contributer_path = os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', splitt[3], Repo,
                                            "contributer.txt")
            file=open(contributer_path)
            if username in file.read():
                file.close()

                with open(contributer_path, "a") as f:
                    string="contributer:"+str(cont_name)
                    f.write(string)
                    f.write("\n")
                    f.close()

                string = "contributter added successfully ;)"
                connection.send(str(string).encode(ENCODING))
            else:
                string = "you dont have access to add contributer -.-"
                connection.send(str(string).encode(ENCODING))
        if "check synch" in msg:
            splitt=str(msg).split("#")
            Repo=splitt[1]
            last_time=splitt[2]
            for_who=splitt[3]
            commit_path=os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase",for_who,Repo,"commits.txt")
            if os.path.exists(commit_path):
                if last_time!="empty":
                    date_time_str_local = str(last_time)
                    print(date_time_str_local)

                    # date_time_obj_local = datetime.datetime.strptime(date_time_str_local, '%Y-%m-%d %H:%M:%S.%f')
                    myFormat = "%Y-%m-%d %H:%M:%S"
                    date_time_obj_local=date_time_str_local.strip(myFormat)

                    times=[]
                    if os.stat(commit_path).st_size != 0:
                        with open(f"{commit_path}", "r") as f:
                            content = f.read()
                            f.close()
                        commits = str(content).split("----------")

                        for i in commits:
                            temp = str(i).split("&&")
                            if temp[0] != "\n":

                                str(temp[4]).replace("\n", "")
                                if temp[2] == Repo:
                                    last_time = temp[4]
                                    times.append(last_time)

                        date_time_str_server = str(times[len(times)-1])
                        date_time_obj_server = date_time_str_server.strip(myFormat)
                        if date_time_obj_local>date_time_obj_server :
                            string="Server is not update please push in order to server be updated"
                            connection.send(str(string).encode(ENCODING))
                        elif date_time_obj_local==date_time_obj_server:
                            string="all server and you synchroned"
                            connection.send(str(string).encode(ENCODING))
                        elif date_time_obj_local<date_time_obj_server:
                            string="Server is update but you are not...type want pull to be updated"
                            connection.send(str(string).encode(ENCODING))
                    else:
                        string = "Server is not update please push in order to server be updated"
                        connection.send(str(string).encode(ENCODING))

                else:
                    if os.stat(commit_path).st_size == 0:
                        string = "all server and you synchroned"
                        connection.send(str(string).encode(ENCODING))
                    else:
                        string = "Server is update but you are not...type want pull to be updated"
                        connection.send(str(string).encode(ENCODING))
            else:
                string = "what you want nothing found...try again"
                connection.send(str(string).encode(ENCODING))














        if "want download" in msg:
            string=str(msg).split(":")

            contributer_path = os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', string[2],
                                            string[1], "contributer.txt")
            file = open(contributer_path)
            print(file.read())
            file.close()
            file = open(contributer_path)
            if "private" in file.read():
                file.close()
                file = open(contributer_path)
                if username in file.read():
                    file.close()
                    string = "this Repo is private but you have access to download"
                    connection.send(string.encode(ENCODING))
                else:
                    file.close()
                    string = "this Repo is private and you have not access to download"
                    connection.send(string.encode(ENCODING))
            file.close()
            file = open(contributer_path)
            if "public" in file.read():
                file.close()
                string = "This Repo is public..Be free to download"
                connection.send(string.encode(ENCODING))

        if "Go to download" in msg:
            splitt = str(msg).split(":")
            file_name = splitt[1]
            usr = splitt[2]
            Repo_name = splitt[3]
            file_path = splitt[4]
            full_path = os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', usr,file_path)
            if os.path.exists(full_path):
                with open(f"{os.path.join(full_path)}", "r") as f:
                    content = f.read()
                    f.close()

                connection.send(str(content).encode(ENCODING))
            else:
                string = "what you want nothing found...try again"
                connection.send(str(string).encode(ENCODING))

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


def new_user(userName, password):
    field_names = ['username', 'password']

    dict = {'username': userName, 'password': password}

    with open('user-pass.csv', 'a') as f_object:
        dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)

        dictwriter_object.writerow(dict)

        f_object.close()


def old_user(userName, password):
    with open('user-pass.csv', newline="") as file:
        readData = [row for row in csv.DictReader(file)]

    size = len(readData)
    for i in range(size):
        user = readData[i]['username']
        pas = readData[i]['password']
        if userName == user and pas == password:
            return True

    return False


if __name__ == '__main__':
    main()
