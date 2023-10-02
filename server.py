#  coding: utf-8  
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        data_str = self.data.decode('utf-8')
        print ("Got a request of: %s\n" % data_str)


        method = data_str.split(' ')[0]
        if method == "GET":
            path = data_str.split(' ')[1]
            
            if ".." in path:
                response = "HTTP/1.1 404 Path Not Found\n\n"
                self.request.sendall(response.encode())
                return

            if not path.endswith("/") and os.path.isdir(os.path.join(directory, path.lstrip('/'))):
                new_path = path+"/"
                redirect_response = "HTTP/1.1 301 Moved to\nLocation: "+new_path+"\n\n"
                self.request.sendall(redirect_response.encode())
                return
            
            content_type = "text/plain"
            if path.endswith(".html"):
                content_type = "text/html"
            elif path.endswith(".css"):
                content_type = "text/css"
            
            path = os.path.join(directory, path.lstrip('/'))#change path
            if path and os.path.isfile(path):
                with open(path, 'rb') as file:
                    content = file.read()
                response = "HTTP/1.1 200 OK\nContent-Type:"+content_type+"\n\n"
                self.request.sendall(response.encode())
                self.request.sendall(content)
            elif path and path.endswith("/"):
                path = os.path.join(path, "index.html")
                if path and os.path.isfile(path):
                    with open(path, 'rb') as file:
                        content = file.read()
                    content_type = "text/html"
                    response = "HTTP/1.1 200 OK\nContent-Type:"+content_type+"\n\n"
                    self.request.sendall(response.encode())
                    self.request.sendall(content) 
                else:
                    response = "HTTP/1.1 404 Path Not Found\n\n"
                    self.request.sendall(response.encode())
            
            else:
                response = "HTTP/1.1 404 Path Not Found\n\n"
                self.request.sendall(response.encode())
        else:
            response = "HTTP/1.1 405 Method Not Allowed\n\n"
            self.request.sendall(response.encode())
        
 


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    directory = "./www"#serve from folder

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()