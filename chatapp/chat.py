from twisted.internet import protocol, reactor

class ChatProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.username = None
    
    def connectionMade(self):
        self.factory.clients.append(self)
    
    def connectionLost(self, reason):
        self.factory.clients.remove(self)
    
    def dataReceived(self, data):
        message = data.decode().strip()
        if self.username is None:
            self.username = message
            self.sendMessage(f"Welcome, {self.username}!")
        else:
            message = f"{self.username}{message}"
            self.sendMessage(message)
    
    def sendMessage(self, message):
        for client in self.factory.clients:
            client.transport.write(message.encode())

class ChatFactory(protocol.Factory):
    def __init__(self):
        self.clients = []
    
    def buildProtocol(self, addr):
        return ChatProtocol(self)

reactor.listenTCP(8000, ChatFactory())
reactor.run()
