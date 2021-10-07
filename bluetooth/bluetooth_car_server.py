import bluetooth
import picar_4wd as fc
from gpiozero import CPUTemperature


class CarTelemetry:
    def __init__(self, speed, distance_traveled, direction, temp):
        self.speed = speed
        self.distance_traveled = distance_traveled
        self.direction = direction
        self.temp = temp

    def __rep__(self):
        return str(self.__dict__)


hostMACAddress = "B8:27:EB:FD:5D:88"
backlog = 1
size = 1024
port = 0
power_val = 50


def move(direction):
    cpu_temp = CPUTemperature()
    temp = cpu_temp.temperature
    car_telemetry = CarTelemetry(
        speed=power_val,
        distance_traveled=0,
        direction="Not a valid direction",
        temp=temp,
    )
    if direction == "f":
        fc.forward(power_val)
        car_telemetry.direction = "Moving forward"
    elif direction == "b":
        fc.backward(power_val)
        car_telemetry.direction = "Moving backward"
    elif direction == "l":
        fc.turn_left(power_val)
        car_telemetry.direction = "Turning left"
    elif direction == "r":
        fc.turn_right(power_val)
        car_telemetry.direction = "Turning right"
    elif direction == "s":
        fc.stop()
        car_telemetry.direction = "stopping the car"
    else:
        fc.stop()
        car_telemetry.direction = "Not a valid direction"
    return car_telemetry


print("***starting bluetooth server waiting for command from client***")
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
try:
    client, clientInfo = s.accept()
    while True:
        data = client.recv(size)
        print(f"server recv from: {clientInfo} -> {data}")
        if data:
            res = move(data.decode())
            client.send(res.__rep__())
except Exception as Error:
    print(Error)
    print("Closing socket")
    client.close()
    s.close()
