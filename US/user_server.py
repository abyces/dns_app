import requests
from flask import Flask, request
import socket

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>User Server!</p>"


@app.route("/fibonacci", methods=['GET'])
def fibonacci():
    hostname = request.args.get("hostname")
    fs_port = request.args.get("fs_port")
    number = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")

    if None in [hostname, fs_port, number, as_ip, as_port]:
        return "Bad Request", 400

    message = f"TYPE=A\nNAME={hostname}"
    print(f"US sending query message:  \n --- \n {message} \n --- \n to AS.")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (as_ip, int(as_port)))

    data, addr = sock.recvfrom(1024)
    data = data.decode().split('\n')

    if len(data) != 4:
        return "Bad Request.", 400

    fs_ip = data[2].split('=')[1]
    url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
    r = requests.get(url)

    return number + 'th Fibonacci number is ' + r.text, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
