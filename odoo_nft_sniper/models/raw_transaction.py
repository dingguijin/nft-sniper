# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class RawTransaction(models.Model):

    _name = "nft_sniper.raw_transaction"
    _description = "Raw Transaction"

    name = fields.Char('Name', required=True)
