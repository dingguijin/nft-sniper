# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-~ PPMessage.
# Guijin Ding, dingguijin@gmail.com.
# All rights reserved.
#

import aiohttp
import asyncio
import collections
import datetime
import itertools
import json
import logging
import re
import time
import threading
import urllib
import uuid

import odoo

from web3 import Web3

_logger = logging.getLogger(__name__)

class EthWorker():
    def __init__(self, dbname):
        self.dbname = dbname
        self.is_stop = False
        self.db_connection = odoo.sql_db.db_connect(self.dbname)
        self.eth_stream = EthStream(self)
        self.event_queue = collections.deque([])
        return

    async def run_loop(self):
        await asyncio.gather(self._run_command_loop(),
                             self._run_sniffer_loop())
        odoo.sql_db.close_db(self.dbname)
        return

    async def _run_command_loop(self):
        while True:
            if self.is_stop:
                break
            await asyncio.sleep(5)
        return

    async def _run_sniffer_loop(self):
        while True:
            if self.is_stop:
                break
            await self.eth_stream.sync_block()
            await asyncio.sleep(24)
        return

    async def _stop(self):
        self.is_stop = True
        return

    def stop(self):
        asyncio.run(self._stop())


class EthStream():

    def __init__(self, server):
        self.status = "NULL"
        self.server = server
        self.db_connection = server.db_connection
        self.latest_block = None
        w3 = Web3(Web3.HTTPProvider("https://eth.ppmessage.com"))
        w3.provider.request_counter = itertools.count(start=1)
        self.web3 = w3
        return

    async def get_latest_block(self):
        return self.web3.eth.get_block("latest", False)

    async def check_block(self):
        return

    async def save_block(self, block):
        return

    async def sync_block(self):
        numbers = self.get_sync_block_numbers()
        if not numbers:
            return
        _logger.info(numbers)
        for number in numbers:
            try:
                block = self.web3.eth.get_block(number, True)
            except Exception as e:
                _logger.info("Exception %s" % e)
                await asyncio.sleep(1)
                break
            
            if block:
                self.latest_block = block
        return

    def get_sync_block_numbers(self):
        try:
            block = self.web3.eth.get_block("latest", False)
        except Exception as e:
            _logger.info("Exception %s", e)
            return []
        
        if not block:
            return []

        if not self.latest_block:
            return [block.number]

        if block.number == self.latest_block.number:
            return []
        
        return list(range(self.latest_block.number+1, block.number))

            
