# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import asyncio
import logging
import time
import threading
import urllib

import odoo
from odoo.service.server import Worker
from odoo.service.server import PreforkServer

from . import eth_worker

_logger = logging.getLogger(__name__)

def db_list():
    if odoo.tools.config['db_name']:
        db_names = odoo.tools.config['db_name'].split(',')
    else:
        db_names = odoo.service.db.list_dbs(True)
    return db_names

def worker():    
    old_process_spawn = PreforkServer.process_spawn
    def process_spawn(self):
        old_process_spawn(self)
        if not hasattr(self, "eth_workers"):
            self.eth_workers = {}
        if not self.eth_workers:
            self.worker_spawn(EthWorker, self.eth_workers)
    PreforkServer.process_spawn = process_spawn

class BaseWorker(Worker):
    def __init__(self, multi):
        super().__init__(multi)
        self.threads = {}  # {db_name: thread}
        self.interval = 1

    def signal_handler(self, sig, frame):
        super().signal_handler(sig, frame)
        
    def start(self):
        super().start()
        if self.multi and self.multi.socket:
            self.multi.socket.close()
        return

    def sleep(self):
        return

    def stop(self):
        super().stop()
        for _thread in self.threads.values():
            _thread.stop()
            _thread.join()

    def process_work(self):
        # this called by run() in while self.alive cycle
        db_names = db_list()
        for dbname in db_names:
            if self.threads.get(dbname, False):
                continue
            _thread = self.get_worker_thread(dbname)
            _thread.start()
            self.threads[dbname] = _thread
        time.sleep(10)
        # process work will be called every timeslice
        # need sleep to release CPU
            
    def get_worker_thread(self, dbname):
        pass

class EthWorker(BaseWorker):
    def get_worker_thread(self, dbname):
        return EthWorkerThread(dbname)

class EthWorkerThread(threading.Thread):
    """
    """

    def stop(self):
        _logger.info("stoping ..... %s", self.name)
        return

    def __init__(self, dbname):
        threading.Thread.__init__(self, name='EthWorkerThread')
        threading.current_thread().dbname = dbname
        self.daemon = True
        self.worker = eth_worker.EthWorker(dbname)

    def run(self):
        _logger.info("%s start.", self.name)
        asyncio.run(self.worker.run_loop())
        _logger.info("%s stopped.", self.name)
        
