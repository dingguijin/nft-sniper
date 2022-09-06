# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields
from odoo.tests.common import TransactionCase, HttpCase, tagged, Form

from odoo.addons.odoo_nft_sniper.models.eth_function import EthFunction

import time
import base64

@tagged('-standard', 'fuzzy')
class TestFuzzy(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_fuzzy(self):
        print(EthFunction().fuzzy_freemint_sighash())
        print("-------------------------")
        return
        
