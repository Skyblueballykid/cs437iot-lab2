from typing import Optional
from fastapi import FastAPI
import socket
import bluetooth

app = FastAPI()

HOST_MAC_ADDRESS = "DC:A6:32:73:03:91"
BT_PORT = 0
BACKLOG = 1
SIZE = 1024

WIFI_HOST = "192.168.0.3"
WIFI_PORT = 65432

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/bluetooth")
def bluetooth_server():
    # Adapted from https://github.com/mccaesar/iot-labs/blob/master/iot-lab-2/frontend_tutorial/bt_server.py
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.bind((HOST_MAC_ADDRESS, BT_PORT))
    s.listen(BACKLOG)
    print("listening on port ", BT_PORT)
    try:
        client, clientInfo = s.accept()
        while 1:   
            print("server recv from: ", clientInfo)
            data = client.recv(SIZE)
            if data:
                print(data)
                client.send(data) # Echo back to client
    except Exception as e: 
        print("Closing socket")
        client.close()
        s.close()

@app.get("/wifi")
def wifi_server():
    # Adapted from https://github.com/mccaesar/iot-labs/blob/master/iot-lab-2/frontend_tutorial/wifi_server.py
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((WIFI_HOST, WIFI_PORT))
        s.listen()

        try:
            while 1:
                client, clientInfo = s.accept()
                print("server recv from: ", clientInfo)
                data = client.recv(1024)      # receive 1024 Bytes of message in binary format
                if data != b"":
                    print(data)     
                    client.sendall(data) # Echo back to client
        except Exception as e: 
            print("Closing socket")
            client.close()
            s.close()    

