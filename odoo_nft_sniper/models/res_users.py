# -*- coding: utf-8 -*-

from odoo.exceptions import AccessDenied

from odoo import api, fields, models, registry, _

import logging

_logger = logging.getLogger(__name__)

class Users(models.Model):

    _inherit = "res.users"

    block_chain_address = fields.Char("Block Chain Address")
    block_chain_id = fields.Char("Block Chain Id")
    block_chain_ens = fields.Char("Ens")
    block_chain_balance = fields.Char("Balance")
    
    @classmethod
    def _login(cls, db, login, password, user_agent_env):
        try:
            return super(Users, cls)._login(db, login, password, user_agent_env=user_agent_env)
        except AccessDenied as e:
            with registry(db).cursor() as cr:
                cr.execute("SELECT id FROM res_users WHERE lower(block_chain_address)=%s", (login,))
                res = cr.dictfetchone()
                if not res:
                    raise e
                if not cls._check_signature(login, password):
                    raise e
                return res.get("id")
        return

    @api.model
    def _generate_signup_values(self, chain_id, address, signature):
        _v = {
            "name": address,
            "login": address,
            "email": address,
            "password": signature,
            "active": True,
            "groups_id": [(4, self.env.ref("base.group_user").id)],
            "block_chain_address": address,
            "block_chain_id": chain_id
        }
        return _v
    
    @api.model
    def auth_ethereum_user(self, address, chain_id, signature):
        if not self._check_signature(address, signature):
            raise AccessDenied()        
        user = self.search([("block_chain_address", "=", address),
                            ("block_chain_id", "=", chain_id)])
        if not user:
            _v = self._generate_signup_values(chain_id, address, signature)
            self.signup(_v)
        return (self.env.cr.dbname, address, signature)

    @classmethod
    def _check_signature(cls, address, signature):
        # address signature address string
        # if signature = address.sign(address)
        return True
    
    def _check_credentials(self, password, env):
        try:
            return super(Users, self)._check_credentials(password, env)
        except AccessDenied:
            passwd_allowed = env['interactive'] or not self.env.user._rpc_api_keys_only()
            if passwd_allowed and self.env.user.active:
                if self._check_signature(self.env.user.block_chain_address, password):
                    return
            raise

