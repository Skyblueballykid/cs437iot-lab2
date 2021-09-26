from flask import Flask
from flask import render_template
from flask import request, jsonify
import socket
import bluetooth

# Change these to your specific Mac and IP
MAC = "DC:A6:32:73:03:91"
HOST = "192.168.3.49" # IP address of your Raspberry PI

SOCKET_PORT = 65432 # Port to listen on (non-privileged ports are > 1023)
BT_PORT = 0 # Bluetooth Port
backlog = 1
size = 1024

app = Flask(__name__)
greeting = " "

def greet(name):
    return "Hi " + name + " . Python server sends its regards."

@app.route('/', methods=["GET", "POST"])
def index():
    global greeting

    # recieve message from electron app
    if request.method == "POST":
        json_message = request.get_json()
        print(json_message)
        greeting = greet(json_message)
        return jsonify(server_greet = greeting)        

    return jsonify(server_greet = greeting)

'''Connect over Bluetooth'''
# Adapted from https://github.com/mccaesar/iot-labs/blob/master/iot-lab-2/frontend_tutorial/bt_server.py
def bluetooth():
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.bind((MAC, BT_PORT))
    s.listen(backlog)
    print("listening on port ", BT_PORT)
    try:
        client, clientInfo = s.accept()
        while 1:   
            print("server recv from: ", clientInfo)
            data = client.recv(size)
            if data:
                print(data)
                client.send(data) # Echo back to client
    except Exception: 
        print("Closing socket")
        client.close()
        s.close()

'''Connect with a raw TCP socket'''
# Adapted from: https://github.com/mccaesar/iot-labs/blob/master/iot-lab-2/frontend_tutorial/wifi_server.py
def raw_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, SOCKET_PORT))
        s.listen()

        try:
            while 1:
                client, clientInfo = s.accept()
                print("server recv from: ", clientInfo)
                data = client.recv(1024)      # receive 1024 Bytes of message in binary format
                if data != b"":
                    print(data)     
                    client.sendall(data) # Echo back to client
        except Exception: 
            print("Closing socket")
            client.close()
            s.close()    

def websocket():
    return print("TODO, write websocket server")


def main():
    selection = input("Select how you want to establish the connection: ")
    print("1. HTTP Connection")
    print("2. Bluetooth Connection")
    print("3. Raw TCP Socket Connection")
    print("4. Websocket Connection")

    if selection == 1:
        app.run( host='192.168.0.3', port = 5000, debug=True)
    elif selection == 2:
        bluetooth()
    elif selection == 3:
        raw_socket()
    else: 
        websocket()

if __name__ == '__main__':
    main()
