# -*- coding: utf-8 -*-

from odoo.exceptions import AccessDenied

from odoo import api, fields, models, registry, SUPERVISOR_ID, _

class Users(models.Model):

    _inherit = "res.users"

    @classmethod
    def _login(cls, db, login, password, user_agent_env):
        try:
            return super(Users, cls)._login(db, login, password, user_agent_env=user_agent_env)
        except AccessDenied as e:
            with registry(db).cursor() as cr:
                # orginal access denied
                cr.execute("SELECT id FROM res_users WHERE lower(login)=%s", (login,))
                res = cr.fetchone()
                if res:
                    raise e

                # 
                env = api.Environment(cr, SUPERUSER_ID, {})
                EthUser = env['nft_sniper.eth_user']
                signed = EthUser._authenticate(login, password)
                if entry:
                    return EthUser._get_or_create_user(login)
                raise e
        return
    
