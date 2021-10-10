from flask import Flask
from flask import render_template
from flask import request, jsonify
from gpiozero import CPUTemperature
import picar_4wd as fc

'''Implementation of keystroke API using url params'''

app = Flask(__name__)

power_val = 50

@app.route('/<keystroke>', methods=["GET"])
def index(keystroke):
    cpu_temp = CPUTemperature()
    temp = cpu_temp.temperature
    direction = "None"
    if keystroke == '87':
        print("Moving forward")
        fc.forward(power_val)
        direction = "Forward"
    elif keystroke == '83':
        print("Moving backward")
        fc.backward(power_val)
        direction = "Reverse"
    elif keystroke == '65':
        print("Turning left")
        fc.turn_left(power_val)
        direction = "Left"
    elif keystroke == '68':
        print("Turning right")
        fc.turn_right(power_val)
        direction = "Right"
    elif keystroke == '88':
        print("Stopping vehicle")
        fc.stop()
        direction = "None"
    else:
        print("Enter a valid direction")
        fc.stop()
    data = [temp, direction]
    return jsonify(data)

@app.route('/', methods=["POST"])
def post():
    data = request.get_json()
    print(data['msg'])
    #TODO: Do something with the data on the PI here 
    res = {'status': 'ok'}
    return jsonify(res)


def main():
    count = 0 
    if count < 1:
        host = input("Enter the IP address of your PI or `localhost` for local development: ")
        count += 1
        app.run(host=host, port = 8080, debug=False)

    

if __name__ == '__main__':
    main()
