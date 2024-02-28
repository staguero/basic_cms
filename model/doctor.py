from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Doctor(models.Model):
    _name = 'clinic.doctor'
    _description = 'Registro de Médicos'

    name = fields.Char(string='Nombre', required=True)
    last_name = fields.Char(string='Apellido', required=True)
    registration_number = fields.Char(string='Matrícula')
    phone = fields.Char(string='Teléfono') 
    specialties = fields.Selection([
        ('pediatrician', 'Pediatra'),
        ('gynecologist', 'Ginecólogo'),
        ('cardiologist', 'Cardiólogo'),
        ('neurologist', 'Neurólogo'),
        ('dermatologist', 'Dermatólogo'),
        ('oncologist', 'Oncólogo'),
        ('psychiatrist', 'Psiquiatra'),
        ('traumatologist', 'Traumatólogo'),
        ('urologist', 'Urólogo'),
        ('endocrinologist', 'Endocrinólogo'),
        ('gastroenterologist', 'Gastroenterólogo'),
        ('hematologist', 'Hematólogo'),
        ('infectologist', 'Infectólogo'),
        ('nephrologist', 'Nefrólogo'),
        ('pulmonologist', 'Neumonólogo'),
        ('radiologist', 'Radiólogo'),
        ('reumatologist', 'Reumatólogo'),
        ('otorhinolaryngologist', 'Otorrinolaringólogo'),
        ('ophthalmologist', 'Oftalmólogo'),
        ('anesthesiologist', 'Anestesiólogo'),
        ('general_practitioner', 'Médico General'),
        ('surgeon', 'Cirujano'),
        ('other', 'Otro')
    ], string='Especialidad', default='other', required=True)
    
    active = fields.Boolean(string='Activo', default=True)
    # One2many: Pacientes cabecera
    patients_ids = fields.One2many('clinic.patient', 'primary_doctor_id', string='Pacientes Asignados',readonly=True)
    # Many2many: Pacientes revisados
    reviewed_patients_ids = fields.Many2many('clinic.patient', string='Pacientes Revisados', readonly=True)
    # Many2many: Diagnósticos realizados por el doctor
    diagnosis_ids = fields.Many2many('clinic.medical.diagnosis', string='Diagnósticos Realizados', readonly=True)

    display_name = fields.Char(string='Nombre a Mostrar', compute='_compute_display_name', store=True)

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'{rec.last_name} {rec.name}'

    # Constraints and SQL Constraints
    _sql_constraints = [
        ('unique_registration_number', 'unique(registration_number)', 'La matrícula debe ser única para cada médico.'),
    ]

    @api.constrains('phone')
    def _check_phone_format(self):
        for record in self:
             if record.phone:
                if not re.match(r'^[0-9\s\-\+\(\)]+$', record.phone):
                    raise ValidationError("Formato de número de teléfono inválido. Por favor, utilice solo números, espacios, guiones, paréntesis y signos de suma.")

