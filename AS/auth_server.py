import json
import socket
import os

# UDP_IP = "127.0.0.1"
# UDP_IP = "172.18.0.1"
UDP_PORT = 53533
FILENAME = "registration.json"  # storing all host in json format

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', UDP_PORT))


def register(data, addr):
    data = data.decode().split('\n')
    response = "400"
    if len(data) == 4:
        # register service
        print("register/ register service")
        new_obj = {}
        for entry in data:
            k, v = entry.split('=')
            new_obj[k] = v

        json_objs = {}

        with open(FILENAME, 'r', encoding='utf-8') as json_file:
            if os.path.getsize(FILENAME) > 0:
                json_objs = json.load(json_file)

        json_objs[new_obj["NAME"]] = new_obj
        with open(FILENAME, 'w') as json_file:
            json.dump(json_objs,
                      json_file,
                      indent=4,
                      separators=(',', ': '))

        response = "200"

    elif len(data) == 2:
        # process DNS query
        print("register/ query DNS")

        hostname = data[1].split('=')[1]

        json_objs = {}
        with open(FILENAME) as json_file:
            json_objs = json.load(json_file)

        if hostname in json_objs:
            target = json_objs[hostname]
            response = f"TYPE={target['TYPE']}\nNAME={target['NAME']}\nVALUE={target['VALUE']}\nTTL={target['TTL']}"

    sock.sendto(response.encode(), addr)


def run_dns_service():
    data, addr = None, None
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(f"received message: {data}")

            register(data, addr)
        except KeyboardInterrupt:
            break
        except:
            if addr:
                sock.sendto("400".encode(), addr)


if __name__ == '__main__':
    if not os.path.exists(FILENAME):
        f = open(FILENAME, 'w')
        f.close()

    run_dns_service()