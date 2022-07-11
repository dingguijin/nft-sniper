# -*- coding: utf-8 -*-


import logging

from odoo import fields
from odoo import http
from odoo.addons.bus.controllers import main

_logger = logging.getLogger(__name__)

class BusController(main.BusController):

    @http.route('/longpolling/poll', type="json", auth="public")
    def poll(self, channels, last, options=None):
        return super().poll(channels, last, options=options)

    def _poll(self, dbname, channels, last, options):
        channels = list(channels)  # do not alter original list
        if http.request.env.user.has_group('odoo_nft_sniper.group_nft_user'):
            channels.append('block_update')
        return super()._poll(dbname, channels, last, options)

