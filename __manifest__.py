# -*- coding: utf-8 -*-
{
    'name': 'Module bank loan',
    'version': '1.0',
    'summary': """ Módulo de Préstamos Bancarios """,
    'author': 'Breithner Aquituari',
    'website': '',
    'category': '',
    'depends': ['base', 'mail',],
    "data": [
        "data/ir_sequence_data.xml",
        "security/ir.model.access.csv",
        "views/menu_views.xml",
        "views/partner_loan_line_views.xml",
        "views/partner_loan_views.xml",
        "views/res_partner_views.xml"
    ],
    
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
