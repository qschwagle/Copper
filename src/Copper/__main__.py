import asyncio 

from Server import Server
from FileManager import FileManager

srv = Server()
srv.host = "0.0.0.0"
srv.port = "8080"
#srv.service = FileManager()
srv.run()
