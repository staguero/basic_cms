# -*- coding: utf-8 -*-
{
    'name': 'Sistema de Gestión Clínica Médica',
    'version': '17.0',
    'category': 'Medical',
    'summary': 'Gestión de pacientes, acompañantes y diagnósticos médicos',
    'description': """
        Módulo para la gestión de información en una clínica médica.
    """,
    'author': 'Agüero Santiago',
    'depends': ['base'],
    'data': [
        'views/clinic_general_view.xml',
        'security/ir.model.access.csv',
        'report/patient_template.xml',
        'report/patient_report.xml',
        'data/ejemplo_data.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
    "license":'OPL-1',
}

