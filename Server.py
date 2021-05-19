import csv
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
            f = open(all_commit_path, "x")
            string = "yay successfully sign up.. what do you want now ? \n"
            string += "create_Repo:RepoName\nsubDir#Repo:nameofsubdir:forwho:pathtosave\nadd_contributer:RepoName:username\n"
            string += "want pull\nwant push\nclient commit\disconnect"
            connection.send(string.encode(ENCODING))
            username = string[1].split(":")[0]

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
                string += "create_Repo:RepoName\nsubDir#Repo:nameofsubdir:forwho:pathtosave\nadd_contributer:RepoName:username\n"
                string += "want pull\nwant push\nclient commit"
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
            contributer = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase", username, string[1],
                                       "contributer")
            contributer += ".txt"
            f = open(contributer, "x")

            with open(contributer, "w") as f:
                f.write(username)
                f.write("\n")

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

        # if "want push" in msg:
        #     string = "Ok send your file name and its content"
        #     connection.send(string.encode(ENCODING))
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
                print("you have access to push")
                content = string[4]
                # read_file = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients", username, file_path)
                # with open(f"{read_file}", "r") as f:
                #     content = f.read()

                write_file = os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', username, file_path)

                with open(write_file, "w") as f:
                    f.write(content)
                string = "push successfully"
                connection.send(string.encode(ENCODING))

            else:
                string = "Sorry you dont have permission -.-"
                connection.send(string.encode(ENCODING))

        if "append_commit" in msg:
            string = str(msg).split("#")
            commit_path = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase", username, string[2],
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

        if "want pull" in msg:
            string = "Ok send which Repo from Who?!"
            connection.send(string.encode(ENCODING))

        if "please pull" in msg:
            splitt = str(msg).split("#")
            which_user = splitt[1]
            which_repo = splitt[2]
            if os.path.exists(
                    os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', which_user, which_repo)):
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
            contributer_path = os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', username, Repo,
                                            "contributer.txt")
            with open(contributer_path, "a") as f:
                f.write(cont_name)
                f.write("\n")
            string = "contributter added successfully ;)"
            connection.send(str(string).encode(ENCODING))

        if "want download" in msg:
            string = "Ok send information above..."
            connection.send(str(string).encode(ENCODING))

        if "Go to download" in msg:
            splitt = str(msg).split(":")
            file_name = splitt[1]
            usr = splitt[2]
            Repo_name = splitt[3]
            file_path = splitt[4]
            full_path = os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\UsersDataBase', usr, Repo_name,
                                     file_path, file_name)
            if os.path.exists(full_path):
                with open(f"{os.path.join(full_path)}", "r") as f:
                    content = f.read()

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
