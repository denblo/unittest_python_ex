from abc import ABCMeta, abstractmethod

class Bully:
    TICKS_BEFORE_BULLYING = 5

    def __init__(self, servers, myself, communicate_multiple):
        assert myself in servers
        self.index = servers.index(myself)
        self.servers = servers[:]
        self.myself = myself
        self.communicate_multiple = communicate_multiple
        self.tick_counter = 0
        self.is_master = False

    def _am_i_the_chosen(self):
        if self.index != 0:
            if self.communicate_multiple(self.servers[:self.index], self.index):
                self.is_master = False
        self.is_master = True

    def _tell_to_shut_up(self):
        self.tick_counter = 0
        if self.index < len(self.servers) - 1:
            self.communicate_multiple(self.servers[self.index + 1:], self.index)

    def on_bully(self, index):
        if index < self.index:
            self.tick_counter = 0
            self.is_master = False
            return False
        return True

    def on_tick(self):
        if self.is_master:
            self._tell_to_shut_up()
        else:
            self.tick_counter += 1
            if self.tick_counter > self.TICKS_BEFORE_BULLYING:
                self._am_i_the_chosen ()

