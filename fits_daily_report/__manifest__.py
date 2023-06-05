# -*- coding: utf-8 -*-
{
    'name': "fits_daily_report/",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ["project","fits_extend_mk"],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'views/daily_report_view.xml',
        'views/project_view.xml',
        'views/photo_galery_view.xml',
        'views/task_view.xml',
        'report/report_photo_const.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
