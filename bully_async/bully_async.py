from threading import Thread
from time import sleep
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer
from queue import Queue, Empty


class Communicator:
    def _thread(self, server, index):
        p = ServerProxy(server)
        p.on_bully(index)

    def communicate_multiple(self, servers, index):
        for s in servers:
            Thread(target=lambda: self._thread(s, index)).start()


class BullyFullImpl:
    def __init__(self, servers, myself, listen_addr):
        self.myself = myself
        self.listen_addr = listen_addr

        self.communicator = Communicator()

        self.bully = Bully(servers, myself, self.communicator.communicate_multiple)

        self.queue = Queue()

        self.flag_stop = False

        self.thread = Thread(target=self._thread)
        self.thread.start()

        self.mess_thread = Thread(target=self.process_messages)
        self.mess_thread.start()
        
        self.tick_thread = Thread(target=self._on_tick_thread)
        self.tick_thread.start()

    def close(self):
        self.flag_stop = True

        #self.server.server_close()
        #self.thread.join()
        #self.tick_thread.join()
        #self.mess_thread.join()

    def _thread(self):
        self.server = SimpleXMLRPCServer(self.listen_addr)
        self.server.register_function(self._on_bully, 'on_bully')
        while not self.flag_stop:
            self.server.handle_request()

    def _on_bully(self, index):
        if index >= 0:
            self.queue.put(index)
            return True

    def process_messages(self):
        try:
            while not self.flag_stop:
                self.bully.on_bully(self.queue.get())
        except Empty:
            pass
        
    def _on_tick_thread(self):
        while not self.flag_stop:
            self.bully.on_tick()
            sleep(1)


class Bully:
    TICKS_BEFORE_BULLYING = 5

    def __init__(self, servers, myself, communicate_multiple):
        assert myself in servers
        self.index = servers.index(myself)
        self.servers = servers[:]
        self.tick_counters = [0] * len(servers)
        self.myself = myself
        self.communicate_multiple = communicate_multiple
        self.is_master = False

    def _am_i_the_chosen(self):
        self.is_master = not any(t <= self.TICKS_BEFORE_BULLYING for t in self.tick_counters[:self.index])
        self.tick_counters = [t + 1 for t in self.tick_counters]

    def _tell_to_shut_up(self):
        self.tick_counter = 0
        if self.index < len(self.servers) - 1:
            self.communicate_multiple(self.servers[self.index + 1:], self.index)

    def on_bully(self, index):
        self.tick_counters[index] = 0
        if index < self.index:
            self.is_master = False
            return False
        return True

    def on_tick(self):
        if self.is_master:
            self._tell_to_shut_up()
        else:
            self._am_i_the_chosen ()

