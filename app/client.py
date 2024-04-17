import socket
from server import HOST, PORT
import threading


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))


    def run(self):
        threading.Thread(target=self.receiveMessages).start()
        threading.Thread(target=self.sendMessages).start()


    def receiveMessages(self):
        while True:
            serverMsg = self.client.recv(1024).decode("utf-8")
            print(serverMsg)


    def sendMessages(self):
        while True:
            msg = input()
            self.client.send(msg.encode("utf-8"))


if __name__ == "__main__":
    client = Client()
    client.run()