from odoo import models, fields, api

class States(models.Model):
    _name = 'clinic.states'
    _description = 'Estado de Pacientes'
    name = fields.Char(string='Nombre', copy=False)
    # One2many: Diagnósticos
    diagnosis_ids = fields.One2many('clinic.medical.diagnosis', 'states_id', string='Diagnósticos', readonly=True)
    # Constraints and SQL Constraints
    _sql_constraints = [
        ('unique_state_name', 'unique(name)', 'El nombre del estado debe ser único.'),
    ]
