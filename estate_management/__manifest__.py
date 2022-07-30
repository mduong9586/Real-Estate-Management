# -*- coding: utf-8 -*-
{
    'name': 'Estate Management',
    
    'summary': 'Estate Management System',
    
    'description': """
        This module contains common features of Property Management
    """,
    
    'author': 'Busy Bee Company',
    'sequence': 0,
    'website': 'www.busybee.com',
    'application': True,
    
    #Categories can be used to filter modules in modules listing
    'category': 'Management',
    
    'version': '1.0.0',
    
    #Any modules required for this module to work correctly
    'depends': ['base'],
    
    #Always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/room_view.xml',
        'views/room_type_view.xml',
        'views/room_tags_view.xml',
        'views/room_offer_view.xml',
        'views/users_view.xml',
    ],
    
    #Only load during demonstration mode
    'demo':[
        'demo.xml',
    ],
    
    'auto_install': False,
    'license': 'LGPL-3',
}