import asyncio 

from Server import Server

srv = Server()
srv.host = "0.0.0.0"
srv.port = "8080"
srv.run()
