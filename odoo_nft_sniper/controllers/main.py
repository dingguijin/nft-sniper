# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
import logging
import json

import werkzeug.urls
import werkzeug.utils

from odoo.exceptions import AccessDenied
from odoo import http, api
from odoo import SUPERUSER_ID
from odoo import registry as registry_get

from odoo.addons.web.controllers.main import set_cookie_and_redirect, login_and_redirect

_logger = logging.getLogger(__name__)

class Main(http.Controller):

    @http.route("/nft_sniper/login_with_metamask", type="http", auth="none", methods=["POST"])
    def login_with_metamask(self, **kw):
        _logger.info(">>>>>>>>>>>>>>>>>>>>>>>")
        _logger.info(kw)
        _logger.info(">>>>>>>>>>>>>>>>>>>>>>>")

        _address = kw.get("address")
        _chain_id = kw.get("chain_id") or "0x1"
        _signature = kw.get("signature")
        _registry = registry_get(http.request.env.cr.dbname)
        with _registry.cursor() as cr:
            try:
                _env = api.Environment(cr, SUPERUSER_ID, {})
                _credentials = _env["res.users"].sudo().auth_ethereum_user(_address, _chain_id, _signature)
                cr.commit()
                _resp = login_and_redirect(*_credentials, redirect_url="/web")
                return _resp
            except AccessDenied:
                _logger.info("Metamask: access denied, redirect to main page")
                return http.request.redirect("/web/login", 303)
            except Exception as e:
                _logger.exception("Metamask: %s" % str(e))
        return set_cookie_and_redirect("/web/login")
