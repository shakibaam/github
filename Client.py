import os
import socket
from datetime import datetime

PORT = 7447
MESSAGE_LEN_SIZE = 1024
ENCODING = 'utf-8'
NAME = ""


# lets Go#username:password  sign up
# log in#user:pass  sign in
# create_Repo:RepoName
# subDir#Repo:nameofsubdir:forwho:pathtosave
# add_contributer:RepoName:username_toadd:Repofor


def main():
    global NAME
    NAME = input("we need to know who are you?")
    create_dir(NAME, 'C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients')
    addrss = socket.gethostbyname(socket.gethostname())
    Host_info = ("192.168.131.1", PORT)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(Host_info)
    message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
    if message:
        print(message)

    while True:

        Request = input()
        if "client commit" not in Request:
            send_msg(s, Request)
            if Request == "disconnect":
                message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
                if message:
                    print(message)
                exit()

            if Request == "sign up":
                f = open(os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients",NAME,
                                      "all_commit.txt"), "x")
                f.close()
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
                Repo_name=str(Request).split(":")
                create_dir(Repo_name[1],os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients" , NAME))
                f=open(os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients" , NAME,Repo_name[1],"client_commit.txt"),"x")
                f.close()
                f = open(os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients", NAME, Repo_name[1],
                                      "contributers.txt"), "x")
                f.close()
                with open(os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients", NAME, Repo_name[1],
                                      "contributers.txt"), "a") as f:
                    f.write(NAME)
                    f.write("\n")
                    f.close()
                message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
                if message:
                    print(message)

            if "subDir" in Request:
                message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
                if message:
                    print(message)

            if "want push" in Request:
                Repo=input("Enter which Repo you want push")
                for_who=input("Enter the name of person that Repo for")
                changed_file=[]
                commit_path=os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients",NAME,Repo,"client_commit.txt")
                if os.stat(commit_path).st_size != 0:
                    with open(f"{commit_path}", "r") as f:
                        content = f.read()
                        f.close()
                    commits=str(content).split("----------")

                    for i in commits:
                        temp=str(i).split("&&")
                        if temp[0] != "\n":
                            print(temp)
                            str(temp[4]).replace("\n","")

                            if not temp[3]in changed_file:

                                changed_file.append(temp[3])

                    for file in changed_file:
                        read=os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients",NAME,file)
                        with open(f"{read}", "r") as f:
                            content = f.read()
                            f.close()
                        big_string = ""
                        big_string += "Go to Push#"
                        big_string+=str(file)
                        big_string+="#"
                        big_string+=Repo
                        big_string+="#"
                        big_string+=for_who
                        big_string+="#"
                        big_string+=str(content)
                        send_msg(s, big_string)

                    message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
                    if message:
                        print(message)
                    # sending comments to server
                    with open(f"{commit_path}", "r") as f:
                        content = f.read()
                        f.close()
                    string="append_commit"
                    string+="#"
                    string+=str(content)
                    string+="#"
                    string+=Repo
                    send_msg(s, string)
                    message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
                    if message:
                        print(message)
                    a_file = open(commit_path, "w")
                    a_file.truncate()
                    a_file.close()
                else:
                    print("you dont have any commit...first commit something then push")





                # push_commit=input("Enter push commit")
                # client_commit = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients", NAME, Repo,
                #                              "client_commit.txt")
                # all_commit = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients", NAME, "all_commit.txt")
                # now = datetime.now()
                # string = str(NAME) + "&&" + str(push_commit) + "&&" + str(Repo) + "&&" + str(target_file) + "&&" + str(now)
                # with open(client_commit, "w") as f:
                #     f.write(push_commit)
                #     f.write("\n")
                #     f.write("----------")
                #     f.write("\n")
                #     f.close()
                # with open(all_commit, "w") as f:
                #     f.write(push_commit)
                #     f.write("\n")
                #     f.write("----------")
                #     f.write("\n")
                #     f.close()





                # message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
                # if message:
                #     print(message)
                #
                # big_string = ""
                # file_name = input("Enter file name")
                # big_string += "Go to Push#"
                # big_string += str(file_name)
                # big_string += '%'
                # file_path_local = input("Enter file path local")
                # in_which_user = input("who is Repo for?...(notice you can push if you are contributer)")
                # Repo = input("Enter which Repo")
                # big_string += Repo
                # big_string += "@"
                # big_string += in_which_user
                #
                # with open(f"{file_path_local}", "r") as f:
                #     content = f.read()
                #
                # big_string += "&"
                # big_string += str(content)
                # print(big_string)
                # big_string += "$"
                # commit = input("Enter commit message")
                # big_string += commit
                # send_msg(s, big_string)
                # message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
                # if message:
                #     print(message)
            if Request == "ok":
                message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
                if message:
                    print(message)

            if "want pull" in Request:
                message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
                # print(message)

                pull_string = ""
                pull_string += "please pull#"
                which_user = input("Enter which user you  want?")
                which_repo = input("Enter which repo from {}".format(which_user))
                pull_string += str(which_user)
                pull_string += "#"
                pull_string += str(which_repo)
                send_msg(s, pull_string)
                Repo_address = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
                if "nothing found" in Repo_address:
                    print(Repo_address)

                else:
                    print(Repo_address)
                    create_dir(which_repo, os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients", NAME))
                    pull_path = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients", NAME, which_repo)

                    for root, subdirectories, files in os.walk(Repo_address):
                        root1 = root.replace(Repo_address,
                                             os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients", NAME,
                                                          which_repo))
                        for subdirectory in subdirectories:
                            print(os.path.join(root1, subdirectory))
                            create_dir(subdirectory, root1)
                        for file in files:
                            print(os.path.join(root1, file))

                            with open(f"{os.path.join(root, file)}", "r") as f:
                                content = f.read()
                                f.close()
                            if os.path.basename(os.path.join(root1, file)) != "contributer.txt":
                                with open(os.path.join(root1, file), "w") as f:

                                     f.write(content)
                                     f.close()
                    print("pull successfully =))")

            if "add_contributer" in Request:
                splitt=str(Request).split(":")
                contributer_path = os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients', splitt[3],splitt[1],"contributers.txt")
                file = open(contributer_path)
                if NAME in file.read():
                    file.close()

                    with open(contributer_path, "a") as f:
                        f.write(splitt[2])
                        f.write("\n")
                        f.close()
                message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
                if message:
                    print(message)

            if "want download" in Request:
                message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
                if message:
                    print(message)
                file_name = input("Enter file name you want download")
                from_who = input("Enter user you want download from")
                Repo = input("Enter which Repo?")
                path = input("Enter path in Repo that file exist in")
                download = "Go to download"
                download += ":"
                download += str(file_name)
                download += ":"
                download += from_who
                download += ":"
                download += Repo
                download += ":"
                download += path
                send_msg(s, download)
                msg = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
                if "nothing found" in msg:
                    print(msg)
                else:
                    file1 = open(os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients)", NAME, file_name), "x")
                    with open(file1, "a") as f:
                        f.write(msg)
                        f.close()
                    print("download successfully ;)")

        else:

            Repo=input("Enter Repo name")
            for_who=input("Enter Repo for ?")
            commit=input("Enter your commit message")
            target_file=input("Enter address of file that you change")
            now = datetime.now()
            string=str(NAME)+"&&"+str(commit)+"&&"+str(Repo)+"&&"+str(target_file)+"&&"+str(now)
            client_commit = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients", NAME, Repo,
                                         "client_commit.txt")
            all_commit = os.path.join("C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients", NAME, "all_commit.txt")
            contributer_path = os.path.join('C:\\Users\\Asus\\PycharmProjects\\CN_P2\\Clients',for_who , Repo,"contributers.txt")
            file = open(contributer_path)
            if NAME in file.read():
                file.close()
                with open(client_commit, "a") as f:
                    f.write(string)
                    f.write("\n")
                    f.write("----------")
                    f.write("\n")
                    f.close()
                with open(all_commit, "a") as f:
                    f.write(string)
                    f.write("\n")
                    f.write("----------")
                    f.write("\n")
                    f.close()
                print("commited successfully in clinet commit of {}".format(Repo))
            else:
                file.close()
                print("you dont have permission to commit -.-")



def send_msg(client, msg):
    message = msg.encode(ENCODING)
    msg_len = len(message)
    msg_len = str(msg_len).encode(ENCODING)
    msg_len += b' ' * (MESSAGE_LEN_SIZE - len(msg_len))
    client.send(msg_len)
    client.send(message)


def create_dir(dir_name, paren_path):
    directory = dir_name
    path = os.path.join(paren_path, directory)
    if not os.path.exists(path):
        os.mkdir(path)
        print("Directory '% s' created" % directory)


if __name__ == '__main__':
    main()
