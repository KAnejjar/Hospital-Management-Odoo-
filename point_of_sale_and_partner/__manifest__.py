# -*- coding: utf-8 -*-
{
    'name': "*POS Partner* ",
    'summary': "Assurance & Medecin Dans POS",
    'description': "POS & Partner",
    'author': 'KA',
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['point_of_sale'],
    'data': [
        'views/assets.xml',
        'views/pos_config_view.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': ['static/src/xml/*.xml'],
}
