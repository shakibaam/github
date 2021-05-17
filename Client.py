import os
import socket

PORT = 7447
MESSAGE_LEN_SIZE = 1024
ENCODING = 'utf-8'
NAME = ""
# lets Go#username:password  sign up
# log in#user:pass  sign in
# create_Repo:RepoName
# subDir#Repo:DirectoryInRepo
#add_contributer:RepoName:username


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
        send_msg(s, Request)
        if Request == "disconnect":
            message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
            if message:
                print(message)
            exit()

        if Request == "sign up":
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

        if "want push" in Request:
            message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
            if message:
                print(message)

            big_string = ""
            file_name = input("Enter file name")
            big_string += "Go to Push#"
            big_string += str(file_name)
            big_string += '%'
            file_path_local = input("Enter file path local")
            in_which_user=input("who is Repo for?...(notice you can push if you are contributer)")
            Repo = input("Enter which Repo")
            big_string += Repo
            big_string+="@"
            big_string+=in_which_user

            with open(f"{file_path_local}", "r") as f:
                content = f.read()

            big_string += "&"
            big_string += str(content)
            print(big_string)
            big_string += "$"
            commit = input("Enter commit message")
            big_string += commit
            send_msg(s, big_string)
            message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
            if message:
                print(message)
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
            if  "nothing found" in Repo_address:
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

                        with open(os.path.join(root1, file), "w") as f:
                            f.write(content)
                print("pull successfully =))")

        if "add_contributer" in Request:
            message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
            if message:
                print(message)

        if "want download" in Request:
            message = (s.recv(MESSAGE_LEN_SIZE)).decode(ENCODING)
            if message:
                print(message)


















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
