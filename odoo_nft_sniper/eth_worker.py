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

# https://eth.ppmessage.com
# https://mainnet.eth.cloud.ava.do
# https://main-rpc.linkpool.io
# https://eth-mainnet.token.im
_PROVIDER_URL = "https://main-rpc.linkpool.io"

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
            await asyncio.sleep(14)
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
        w3 = Web3(Web3.HTTPProvider(_PROVIDER_URL))
        w3.provider.request_counter = itertools.count(start=1)
        self.web3 = w3
        return

    async def get_latest_block(self):
        return self.web3.eth.get_block("latest", False)

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

            if not block:
                continue

            self.latest_block = block

            self._save_block_to_db(block)
        return

    def get_sync_block_numbers(self):
        try:
            block = self.web3.eth.get_block("latest", False)
            #_logger.info(block)
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

    def _save_block_to_db(self, block):
        _logger.info(block)
        _block_sql = self._insert_sql("raw_block", block, {}, ["transactions", "uncles"])
        with self.db_connection.cursor() as cr:
            cr.execute(_block_sql)
            _block_id = cr.fetchone()
        _transactions = block.transactions
        for _transaction in _transactions:
            self._save_transaction_to_db(_block_id[0], _transaction)
        return

    def _save_transaction_to_db(self, block_id, transaction):
        _logger.info("block id %d", block_id)
        _logger.info(transaction)
        _sql = self._insert_sql("raw_transaction", transaction,
                                {"raw_transaction_block_id": block_id},
                                ["accessList"])
        with self.db_connection.cursor() as cr:
            cr.execute(_sql)
        return

    def _insert_sql(self, table_name, attrs, others={}, ignores=[]):
        _sql = "INSERT INTO %s %s VALUES %s RETURNING id;"
        _names = []
        _values = []
        _hash_names = ["hash", "logsBloom", "mixHash", "nonce", "parentHash", "receiptsRoot", "sha3Uncles", "stateRoot", "transactionsRoot", "blockHash", "r", "s", "extraData"]
        for k, v in attrs.items():
            if k in ignores:
                continue
            _logger.info(k)
            if k in _hash_names:
                v = self.web3.toHex(v)

            _names.append(table_name + "_" + self._camel_to_snake(k))
            _logger.info(v)
            _values.append(str(v))

        for k, v in others.items():
            _names.append(k)
            _values.append(str(v))

        _logger.info(_names)
        _logger.info(_values)
        _sql = _sql % ("nft_sniper_"+table_name,
                       str(tuple(_names)).replace("'",""),
                       str(tuple(_values)))
        
        return _sql

    def _camel_to_snake(self, s):
        return re.sub("([A-Z])", "_\\1", s).lower().lstrip("_")
