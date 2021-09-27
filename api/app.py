from flask import Flask
from flask import render_template
from flask import request, jsonify
from gpiozero import CPUTemperature
# import picar_4wd as fc
# import sys
# import tty
# import termios
# import asyncio

'''Implementation of keystroke API using url params'''

app = Flask(__name__)

power_val = 100

@app.route('/<keystroke>', methods=["GET"])
def index(keystroke):
    cpu_temp = CPUTemperature()
    if keystroke == '87':
        fc.forward(power_val)
    elif keystroke == '83':
        fc.backward(power_val)
    elif keystroke == '65':
        fc.turn_left(power_val)
    elif keystroke == '68':
        fc.turn_right(power_val)
    else:
        print("Enter a valid direction")
        fc.stop()

    return (keystroke, cpu_temp.temperature)

def main():
    app.run(host='192.168.0.3', port = 8080, debug=True)

if __name__ == '__main__':
    main()
