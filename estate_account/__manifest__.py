# -*- coding: utf-8 -*-
{
    'name': 'Estate Account',
    
    'summary': 'Estate Account Invoice System',
    
    'description': """
        This module contains common features of Property Account Invoice
    """,
    
    'author': 'Busy Bee Company',
    'website': 'www.busybee.com',
    
    #Categories can be used to filter modules in modules listing
    'category': 'Invoice',
    
    'version': '1.0.0',
    
    #Any modules required for this module to work correctly
    'depends': ['base',
                'estate_management',
                'account',
            ],
    
    #Always loaded
    'data': [],
    
    #Only load during demonstration mode
    'demo':[
        'demo.xml',
    ],
    
    'auto_install': True,
    'license': 'LGPL-3',
}