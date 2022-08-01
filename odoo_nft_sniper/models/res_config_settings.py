# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    etherscan_api_key = fields.Char(config_parameter='nft_sniper.etherscan_key', string="Etherscan API Key")
