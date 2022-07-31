# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{

    'author': 'Guijin Ding',
    'price': 2999,
    'currency': 'EUR',
    'name': 'Nft Sniper',
    'category': 'crypto',
    'summary': 'Nft Sniper provide Nft tools',
    'version': '1.0',
    'description': """
        This module provides a suite of Nft tools to make money.
        """,
    'depends': ['mail', 'contacts'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/login_template.xml',
        'views/views.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'odoo_nft_sniper/static/src/xml/*.xml'
        ],
        'web.assets_backend': [
            'odoo_nft_sniper/static/src/js/contract_list_view.js',
        ],
        'web.assets_frontend': [
        ],
        'web.assets_common': [
            'odoo_nft_sniper/static/lib/js/web3.min.js',
            'odoo_nft_sniper/static/src/js/login_with_metamask.js'
        ],
        'web.tests_assets': [
        ],
        'web.qunit_mobile_suite_tests': [
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'post_load': 'post_load',
    'post_init_hook': 'post_init_hook'
}
