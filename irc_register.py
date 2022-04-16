import irctokens
import socket
import os

webircpass = os.getenv("WEBIRC_PASS")

def ircregister(userip, username, password, email="*"):

    d = irctokens.StatefulDecoder()
    e = irctokens.StatefulEncoder()
    s = socket.socket()

    # Here we assume using this only on localhost i.e. loopback
    s.connect(("127.0.0.1", 6667))

    # define the send function
    def _send(line):
        print(f"> {line.format()}")
        e.push(line)
        while e.pending():
            e.pop(s.send(e.pending()))

    # Registering connection
    
    # WEBIRC
    _send(irctokens.build("WEBIRC", [ webircpass, "WebregGateway", userip, userip, "secure"]))

    # Check for "ERROR :Invalid WebIRC password"
    # Should all of this this be under a try except block?
    lines = d.push(s.recv(1024))
    if lines == None:
        print("!disconnected")
        return "disconnected"
    elif lines.command == "ERROR" and lines.params == "Invalid WebIRC password":
        return "WebIRC bad password"
    
    # Inform the server that we support
    # CAP 3.2
    _send(irctokens.build("CAP", ["LS", "302"]))

    # REGISTER can be attempted before-connect if server supports
    # but if the server responds with the corresponding FAIL we
    # need to try again. We can also handle email-required using
    # the same keys. How to access these key-value pairs?
    # reference: https://ircv3.net/specs/extensions/account-registration.html
    
    # NICK and USER
    _send(irctokens.build("USER", ["u", "0", "*", username]))
    _send(irctokens.build("NICK", [username]))

    # go through all cases

    while True:
        for line in lines:
            print(f"< {line.format()}")
            if line.command == "432":
                return "ERR_ERRONEUSNICKNAME"
            elif line.command == "433":
                return "ERR_NICKNAMEINUSE"
            _send(irctokens.build("CAP", ["REQ", "draft/account-registration"]))
            if line.command == "CAP" and ("NAK" in line.params):
                return "CAP_REFUSED"
            elif line.command == "CAP" and ("ACK" in line.params):
                to_send = irctokens.build("CAP", ["END"])
                _send(to_send)
            if line.command == "PING":
                to_send = irctokens.build("PONG", [line.params[0]])
                _send(to_send)
            if line.command == "001":
                # assuming no verif reqd.
                to_send = irctokens.build("REGISTER", ["*", email, password])
                _send(to_send)
            if line.command == "REGISTER" and ("SUCCESS" in line.params):
                to_send = irctokens.build("QUIT")
                _send(to_send)
                return "SUCCESS"
