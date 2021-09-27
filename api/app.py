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
    if keystroke == '87':
        print("Moving forward")
        fc.forward(power_val)
    elif keystroke == '83':
        print("Moving backward")
        fc.backward(power_val)
    elif keystroke == '65':
        print("Turning left")
        fc.turn_left(power_val)
    elif keystroke == '68':
        print("Turning right")
        fc.turn_right(power_val)
    else:
        print("Enter a valid direction")
        fc.stop()

    return f'{temp}' 

def main():
    app.run(host='192.168.0.3', port = 8080, debug=True)

if __name__ == '__main__':
    main()
