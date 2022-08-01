# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields
from odoo.tests.common import TransactionCase, HttpCase, tagged, Form

#from odoo.addons.nft_sniper.models import raw_verified_contract

import time
import base64
from lxml import etree


class TestDownload(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_download(self):
        print("-------------------------")
        return
        
