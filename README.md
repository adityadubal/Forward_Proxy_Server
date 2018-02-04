# Forward_Proxy_Server
## Concept of Forward Proxy Server
A forward proxy provides services to clients or group of clients. A proxy server acts as intermediary for requests from clients seeking resources from other servers. When one of these clients makes a connection  attempt to that file transfer server on Internet, it's requests have to pass through proxy first. So when server responds, it addresses its response to the proxy. Also proxy handle errors whenever a client requests object that is not available.

This proxy server implemented with Caching. HTTP proxy caching enables to store copies of frequently accessed web objects and then serve this information to users on demand. It improves performance and frees up internet bandwidth for other tasks.

## Project Design
1. Create a ServerSocket object to monitor user defined port (e.g. 8080)
2. If client request is received, new thread is created to process request. Also new socket is created for connection with client.
3. ServerSocket object continues monitoring.
4. Parse the request line and headers sent by client.
5. If new request matches past one, the proxy will directly return the cached data. If not go to next step.
6. Send request to real server. HTTP response including requested file will be received at the proxy.
7. Thread reads incoming stream, get the file name and content.
8. Forward content to client.
9. Close the socket.

## Prerequisites
You will need Python version 2.7 or greater to be installed on your system. You can download and install from following link.

https://www.python.org/download/releases/2.7/

## Running the Program
To run this program from windows command prompt, enter the following command:

python proxy_server.py

After this, go to your browser and enter following URL:

http://127.0.0.1:8080/www.wikipedia.org

## Testing of Program
For testing, configure web browser for proxy server. Make sure proxy server is running and now all HTTP requests from browser would be served via proxy.

## Author
Aditya Dubal
