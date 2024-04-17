import socket, threading
from User import User

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090

class Server:
    def __init__(self):
        self.users = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))


    def registerUser(self, userSocket: socket.socket) -> User:
        userSocket.send("[Server]: What is your username?".encode("utf-8"))
        username = userSocket.recv(1024).decode("utf-8")

        userSocket.send("[Server]: What is your password?".encode("utf-8"))
        password = userSocket.recv(1024).decode("utf-8")

        if username in list(map(lambda user: user.name, self.users)):
            userSocket.send("[Server]: Your password is wrong, moron.".encode("utf-8"))
            userSocket.close()
            return User("", "", userSocket)

        else:
            user = User(username, password, userSocket)
            self.users.append(user)
            print(f"{user.name} joined the Chat!")

            for otherUser in self.users:
                otherUser.socket.send(f"{user.name} joined the Chat!".encode("utf-8"))
            return user


    def receiveMessages(self, user: User):
        while True:
            userMsg = user.socket.recv(1024).decode("utf-8")
            if userMsg[:2] == "--":
                user.socket.send(self.commandHandler(userMsg).encode("utf-8"))
                continue

            print(f"{user.name}: {userMsg}")

            for otherUser in self.users:
                if otherUser is user:
                    continue
                otherUser.socket.send(f"{user.name}: {userMsg}".encode("utf-8"))


    def communicationWithClient(self, userSocket: socket.socket):
        user = self.registerUser(userSocket)
        if user.socket not in list(map(lambda user: user.socket, self.users)):
            return
        
        threading.Thread(target=self.receiveMessages, args=[user]).start()


    def commandHandler(self, msg: str) -> str:
        cmd = msg[2::].lower()

        match cmd:
            case "help":
                return """--list: returns the names of all current users"""
            
            case "list":
                return str(list(map(lambda user: user.name, self.users)))


    def run(self):
        self.server.listen()

        while True:
            communicationSocket, address = self.server.accept()
            threading.Thread(target=self.communicationWithClient(communicationSocket)).start()


if __name__ == "__main__":
    server = Server()
    server.run()