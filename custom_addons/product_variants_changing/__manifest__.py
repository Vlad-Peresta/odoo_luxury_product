{
    'name': 'Product variants changing',
    'description': '''
        Changing product attributes that have already been used
    ''',
    'author': 'Vladyslav Peresta',
    'license': 'LGPL-3',
    'website': 'https://github.com/Vlad-Peresta',
    'category': 'Sales',
    'version': '0.1.1',
    'depends': ['base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_variants_changing_wizard_views.xml',
    ],
}
