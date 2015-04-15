"""
Author: Jonathan Gerrand.
Description: Please run this guy first.
"""

from twisted.internet import reactor, protocol


class PersonalEcho(protocol.Protocol):
    """Here we define Echo as inheriting from the Protocal class"""

    def dataReceived(self, data):
        """This is an overridden method of the protocol class, hence
         we are changing the way it normally behaves--> imposing our own
         protocol here :)"""
        self.transport.write(data + "\n")
        self.transport.write("Hey Dan, I hope that the Lab went alright today!")


def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = PersonalEcho  #Make our generic server an 'Echo' server.
    reactor.listenTCP(8000,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()