MB-DNSOverTLS-Proxy
=========

This is a very simple DNS Proxy written in Python3 when studing DNSOverTLS
in 2019. I didn't updated it since that, but decided to publish it now.

The goal of this app is serve all internal DNS queries using the traditional
(RFC1035) implementation but forwarding these queries over TLS to an external
DNS Server with the DNSOverTLS (RFC7858) capabilities.

It was developed and tested in a Fedora environment, but containerized in
CentOS 8, for a better stability, performance and higher security. Also, due
CentOS has all the Red Hat knowhow for servers and containers in its background
and now is one of the most modern distribution for DevOP in critical environments.

This app was developed in a very short time in my limited free time and, for sure,
a lot of nice and extra features could be added before go to the production
environment. So, sorry if you find some typo or something not so good. :(

The logic is pretty simple, to attend the demand with a simple and fast
solution. The app will:

- Listen on port 53/tcp and expect DNS requests.
- Receive DNS requests from known clients.
- Forward the RAW request to a Cloudflare DNSOverTLS (1.1.1.1:853)
- Get the answer from the DNS server and forward back to the client.

References:
- https://tools.ietf.org/html/rfc7858
- https://tools.ietf.org/html/rfc1035
- https://tools.ietf.org/html/rfc7830
- https://docs.python.org/3/library/socket.html
- https://docs.python.org/3/library/ssl.html
- https://pypi.org/project/dnslib/

Content
------------

This solution comes with three files:

- README.md
  - This one.
- Dockerfile
  - Used to build our image, used to our containers.
- dnsOverTLSProxy.py
  - The code where the magic happens. :)

ToDo
------------

Cache System

- For better efficiency and performance, we need to implement a cache system.
- The cache system should be uniq but easy to be replicated and balanced.
- So, we need to implement using MongoDB or other NoSQL system.
- The cache should be consulted before make a connection with the external server.
- The cache should hold, at least, the hostname, the IP Address, the query timestamp and validity.
- If able to use other servers in the future, the server responsible by the answer should be informed too.

ACL System

- For security, we have to implement a client source validation, to avoid undesired queries.
- This is very simple to do in the APP getting the IP address of the peer from the socket and
  comparing it with a list or range of authorized networks.
- If the client is not authorized, immediately close the socket.

DNS Security

- We never can rely on foreign infrastructures or systems!
- Even loosing some performance, we can consider the use of DNSSEC for these queries.

More Compatibility

- Accept connections in IPv4 and IPv6 simultaneously.
- Accept connections in TCP and UDP simultaneously.

More Scalability

- The function dnsOverTLSQuery() is not yet optimized for busy environments.
- Should be implemented threads here too.
- As the consulted servers trends to be few and always the same, we have to reuse the sessions as much
  as possible to avoid unnecessary TLS handshakes.
  

Requirements
------------

For APP:

- python3 and the following modules:
  - ssl
  - socket
  - sys
  - threading

For Container:

- docker

Docker Variables
--------------

This version is not using variables yet, but we have to do that before thinking
in high scalability. At least these variables should be used:

- DNS_SERVER: IP Address or Hostname of the DNSOverTLS server, like 1.1.1.1.
- DNS_PORT: The RFC7858 permits a port different of 853/tcp since both sides of the connection are aware.
- LISTEN_ADDR: If we intend to bind some specific address to receive the queries.
- LISTEN_PORT: If not defined, we will use 53 to listen.

Dependencies
------------

None. The code was make thinking in the best compatibility.

Dirtying the Hands
----------------

First we need to satisfy the SO requirements:
For Fedora:

- $ sudo dnf install -y python3 docker
- $ sudo systemctl start docker

For RedHat/CentOS:

- $ sudo yum install -y python3 docker
- $ sudo systemctl start docker

Now we have to build our image. So, from the directory where you extracted the files:

- $ sudo docker build -t mb-dnsovertls .

With our new image build, we can use it in our new container, mapping the port 53:

- $ sudo docker run -d -p 53:53 --name dnsTLS mb-dnsovertls

Now we can use any tool to test the app. Follow some examples:

- host -T -t A google.com 127.0.0.1
- host -T -t MX google.com 127.0.0.1
- host -T -t NS google.com 127.0.0.1
- dig @127.0.0.1 +tcp google.com
- dig @127.0.0.1 +tcp MX google.com
- dig @127.0.0.1 +tcp NS google.com

License
-------

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, you can obtain one at http://mozilla.org/MPL/2.0/.

Author Information
------------------

- Marcus Burghardt 
- https://github.com/marcusburghardt/
- https://www.linkedin.com/in/marcusburghardt/
