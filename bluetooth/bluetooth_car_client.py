""""
Execute on the remote virtual machine client
"""
import bluetooth

# Bluetooth address of the raspberry pi on the car
host = "B8:27:EB:FD:5D:88"
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((host, port))
while True:
    text = input("Enter command for car:")
    if text == "quit":
        break
    sock.send(text)

    data = sock.recv(1024)
    print("from car: ", data)
sock.close()
