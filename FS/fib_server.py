from flask import Flask, request
import socket

app = Flask(__name__)

HOSTNAME = ""
IP = ""
PORT = "9090"
AS_IP = ""
AS_PORT = "" # 53533


@app.route("/")
def hello_world():
    return "<p>Fibonacci Server!</p>"


@app.route("/register", methods=['PUT'])
def register():
    global HOSTNAME, IP, AS_IP, AS_PORT

    content = request.json

    HOSTNAME = content["hostname"]
    IP = content["ip"]
    AS_IP = content["as_ip"]
    AS_PORT = content["as_port"]

    message = f"TYPE=A\nNAME={HOSTNAME}\nVALUE={IP}\nTTL=10"
    print(f"FS sending UDP: \n --- \n {message} \n --- \n to AS (ip:{AS_IP}, port:{AS_PORT}).")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (AS_IP, int(AS_PORT)))

    data, addr = sock.recvfrom(1024)
    data = data.decode()

    if data == '400':
        return 'DNS Registration Failed.', 400

    return "Register Succeeded.", 201


@app.route("/fibonacci", methods=['GET'])
def fibonacci():
    number = request.args.get("number")
    if not number.isdigit():
        return "Bad Request.", 400

    number = int(number)
    if number < 2:
        return str(number), 200

    a, b, fib_num = 0, 1, 0
    for i in range(2, number + 1):
        fib_num = a + b
        a = b
        b = fib_num

    return str(fib_num), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
