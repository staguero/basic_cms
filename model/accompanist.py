from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
class Accompanist(models.Model):
    _name = 'clinic.accompanist'
    _description = 'Gestión de Acompañantes'

    name = fields.Char(string='Nombre', required=True)
    last_name = fields.Char(string='Apellido', required=True)
    relationship = fields.Selection([
        ('parent', 'Padre/Madre'),
        ('brother', 'Hermano/a'),
        ('friend', 'Amigo/a'),
        ('son', 'Hijo/a'),
        ('other', 'Otro')
    ], string='Parentesco con el paciente', required=True, copy=False)
    phone = fields.Char(string='Teléfono de Contacto')
    # Many2one: Paciente acompañado
    patients_id = fields.Many2one('clinic.patient', string='Pacientes')

    # Constraints and SQL Constraints
    _sql_constraints = [
        ('unique_accompanist_record', 'unique(name, last_name, patients_id)', 'El registro debe ser único para cada acompañante.'),
    ]

    @api.constrains('phone')
    def _check_phone_format(self):
        for record in self:
             if record.phone:
                if not re.match(r'^[0-9\s\-\+\(\)]+$', record.phone):
                    raise ValidationError("Formato de número de teléfono inválido. Por favor, utilice solo números, espacios, guiones, paréntesis y signos de suma.")
