from multiprocessing import Process, Queue
import asyncio
import socket
import re
from Copper.Server import server
import time


async def task(s,r):
    while r.empty():
        await asyncio.sleep(1)
    asyncio.get_event_loop().call_soon_threadsafe(asyncio.get_event_loop().stop)


async def my_server(s,r):
    stopper = asyncio.create_task(task(s,r))
    srv = asyncio.create_task(server('127.0.0.1', '8080'))
    s.put([True])
    await stopper 
    await srv

bad_request_matcher = re.compile('HTTP/1[.]1[ ]400[ ]Bad[ ]Request')
ok_request_matcher = re.compile('HTTP/1[.]1[ ]200[ ]Ok')


class TestVerbs:
    @staticmethod
    def start_server(s,r):
        loop = asyncio.run(my_server(s,r))

    @staticmethod
    def send_request(method, path):
        s = socket.socket()
        s.connect(('127.0.0.1', 8080))
        s.send(bytes('%s %s\r\n\r\n' % (method, path), 'utf-8'))
        buffer = s.recv(4000)
        s.close()
        return buffer

    @staticmethod
    def run_method(m):
        reader = Queue()
        sender = Queue()
        p = Process(target=TestVerbs.start_server, args=(reader, sender))
        try:
            p.start()
            while reader.empty():
                time.sleep(0.05)
            buffer = TestVerbs.send_request(m, "/")
            res = ok_request_matcher.match(bytes.decode(buffer,'utf-8'))
            if res:
                assert(True)
            else:
                assert(False)
        except Exception as err:
            raise err
        finally:
            # always join
            sender.put([True])
            p.join()


    def test_methods(self):
        methods = ["GET","HEAD","POST","PUT","DELETE","CONNECT","OPTIONS","TRACE"]
        for i in methods:
            TestVerbs.run_method(i)

    def test_bad_methods(self):
        reader = Queue()
        sender = Queue()
        p = Process(target=TestVerbs.start_server, args=(reader, sender))
        p.start()
        while reader.empty():
            time.sleep(0.05)
        buffer = TestVerbs.send_request("adsdas", "/")
        print(buffer)
        res = bad_request_matcher.match(bytes.decode(buffer,'utf-8'))
        if res:
            sender.put([True])
            p.join()
            assert(True)
        else:
            sender.put([True])
            p.join()
            assert(False)
