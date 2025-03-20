# -*- coding: utf-8 -*-
{
    'name': "Invoice Qty Adjust",
    'summary': "Adjust invoice line quantities based on a desired total amount.",
    'description': """
    This module enables users to specify a desired total invoice amount (including tax) 
    and automatically adjusts the quantities of each invoice line so that the pre-tax total 
    is equally distributed among them.
        """,
    'author': "Ahmed Reda",
    'website': "https://www.linkedin.com/in/ahmed-reda301/",
    'category': 'Accounting',
    'version': '0.1',
    'depends': ['base','account'],
    'data': [
        'views/account_move_view.xml',
        'views/menu.xml'
    ],
}

