""""
Execute on the remote virtual machine client
"""
import bluetooth
import argparse
import json


def write_file(car_telemetry: str, telemetry_file_name: str):
    with open(telemetry_file_name, "w") as file_handle:
        file_handle.write(json.dumps(car_telemetry))


def main():
    host = args.host
    port = args.port
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((host, port))
    while True:
        text = input("Enter f=forward b=back r=right l=left s=stop q=quit : ")
        if text == "q":
            break
        sock.send(text)
        car_telemetry = sock.recv(1024).decode()
        print(f"writing telemetry received from car: {car_telemetry}\n")
        write_file(car_telemetry, args.telemetry_file)
    sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        type=str,
        required=False,
        help="bluetooth address",
        default="B8:27:EB:FD:5D:88",
    )
    parser.add_argument(
        "--port", type=int, required=False, help="bluetooth address", default=1
    )
    parser.add_argument(
        "--telemetry-file",
        type=str,
        required=False,
        help="filename to write to disk",
        default="car-telemetry.json",
    )
    args = parser.parse_args()
    main()
