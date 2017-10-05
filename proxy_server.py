"""
This program implements a web proxy server that acts as an itermediary between for
requests from client seeking resources from other servers.
Proxy server should support GET method and implement caching.

Author: Aditya Dubal
Language: Python 2.7
"""

from socket import *

# Create a server socket, bind it to a port and start listening
tcpSerPort = 8084

# AF_INET is socket family and SOCK_STREAM is socket type for TCP
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# bind method binds host address to socket
tcpSerSock.bind(('', 8084))

# listen method sets up and start TCP listener
tcpSerSock.listen(1)

# following loop will create a thread per client request connection
while True:
    print 'Ready to serve'
    # Establish the connection
    tcpCliSock, address = tcpSerSock.accept()
    print 'Received connection from:', address

    # Get Message
    message = tcpCliSock.recv(2048)
    length_input = len(message)
    print 'Bytes received:', length_input

    # Extract the filename from the given message
    print message.split()[1]
    filename = message.split()[1].partition("/")[2]
    fileExist = "false"
    file_to_use = "/" + filename

    # Check whether the file exists in the cache
    try:
        # Opening data stream from HTML
        file_read = open(file_to_use[1:], "r")

        # Reading HTML page
        output_data = file_read.read()

        length_output = len(output_data)
        fileExist = "true"
        print 'File Exists!'

        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        tcpCliSock.send("Content-Type:text/html\r\n")

        # Send the content of the requested file to the client
        for i in range(0, len(output_data)):
            tcpCliSock.send(output_data[i])
        print 'Bytes send:', length_output

        # Error handling for file not found in cache
    except IOError:
        print 'File Exist: ', fileExist
        if fileExist == "false":
            # Create a socket on the proxy server
            print 'Creating socket on proxy server'
            mainServerSock = socket(AF_INET, SOCK_STREAM)

            # Extract host name
            host_name = filename.replace("www.", "", 1)
            print 'Host Name: ', host_name

            try:
                # Connect to the socket to port 80
                mainServerSock.connect((host_name, 80))
                print 'Socket connected to port 80 of the host'

                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                file_obj = mainServerSock.makefile('r', 0)
                file_obj.write("GET " + "http://" + filename + " HTTP/1.0\n\n")

                # Read the response into buffer
                buff = file_obj.readlines()

                # Create a new file in the cache for the requested file. Also send the response in the buffer to client
                # socket and the corresponding file in the cache
                tmpFile = open("./" + filename, "wb")
                for i in range(0, len(buff)):
                    tmpFile.write(buff[i])
                    tcpCliSock.send(buff[i])

            except IOError:  # Triggered if user requests bad link
                tcpCliSock.send("404 Not Found")  # Send response message for file not found

    # Close the socket and the server sockets
    tcpCliSock.close()
    tcpSerSock.close()
