import socket
import logging
import templates
from tabulate import tabulate
logging.basicConfig(format="%(asctime)s[x]%(levelname)s[X]%(message)s")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(("0.0.0.0", 80)) #35.222.147.83
server_socket.bind(("localhost", 8000))
server_socket.listen()

table = tabulate(
    tabular_data=[("Egor", 45), ("Pavel", 12), ("Valik", 0)],
    headers=["user", "hours"],
    tablefmt="HTML"
)

views = {
    "/main":b"HTTP/1.1 200 OK\n\n" + templates.main,
    # "/main":b"HTTP/1.1 200 OK\n\nHello main page",
    "/shop":b"HTTP/1.1 200 OK\n\nShop page",
    "/users":("HTTP/1.1 200 OK\n\n" + table).encode("utf-8"),
    "/cho":b"HTTP/1.1 200 OK\n\n" + templates.cho,
}


def get_response(request):
    if request:
        url = request[0].split()
        if len(url) > 1:
            url = url[1]
        else:
            logging.error('url is empty')
            return
        if url == "/favicon.ico":
            logging.error("favicon.ico")
            return
        return views.get(url, b"HTTP/1.1 404 Not found\n\n<h1>404)</h1>")


def sender(client, msg):
    if msg:
        client.sendall(msg)


while True:
    client, addr = server_socket.accept()
    logging.warning("accept client by addr {:}".format(addr))
    # logging.warning(f"accept client by addr {addr}")
    msg = client.recv(4096)
    request = msg.decode("utf-8").split("\n")
    response = get_response(request)
    sender(client, response)
    client.close()
