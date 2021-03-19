# -*- coding: utf-8 -*-
# sys here is used for the system messages.
import sys
import socket,ssl
import threading

# This function is used make the DNSOverTLS queries.
def dnsOverTLSQuery(data):
    try:
        # Connection info. 
        # TODO: This is not flexible yet.
        hostname = '1.1.1.1'
        port = '853'

        # Adding super powers (TLS) to the socket be able to hide 
        # sensitive data : )
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
                # We can set some socket properties here.
                sslsock.settimeout(10)
                sslsock.sendall(data)
                # RFC7830 (padding)
                response = sslsock.recv(8192)
        return response
    except:
        sys.stderr.write("Couldn't make a query")
        return None
    finally:
        sslsock.close()

class MultiThreadTCPServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        # Create a TCP/IP socket.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # We can reutilize the session for more active clients.
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket.
        self.sock.bind((self.host, self.port))

    def listen(self):
        # Lets listen and start the game. : )
        self.sock.listen(5)
        while True:
            # When a client connect...
            client, address = self.sock.accept()
            # We set the timeout for inactivity.
            client.settimeout(45)
            # And start exclusive thread for it.
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        # The buffer size don't need to be too big for DNS.
        # A small but enough buffer size will make this faster.
        # For sure, some kernel parameters would help with this too.
        # I couldn't sniff to analyse the best value here. :( This number is a 
        # reasonable decision based in experience with network buffers.
        buffer_size = 2048
        while True:
            try:
                data = client.recv(buffer_size)
                if data:
                    # We don't need to spend time recreating queries.
                    # Just forward over TLS.
                    response = dnsOverTLSQuery(data)
                    # With the same logic, just forward the answer.
                    client.sendall(response)
                else:
                    raise Exception('Client disconnected or no DNS answer.')
            except:
                sys.stderr.write("Couldn't serve a TCP client. : (")
                return False
            finally:
                client.close()

if __name__ == '__main__':
    while True:
        print('Starting DNSOverTLS in and waiting...')
        MultiThreadTCPServer('',53).listen()