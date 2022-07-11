# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class RawBlock(models.Model):

    _name = "nft_sniper.raw_block"
    _description = "Raw Block"

    name = fields.Char('Name', required=True)
