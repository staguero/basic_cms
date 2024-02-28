from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta
import re

class Patient(models.Model):
    _name = 'clinic.patient'
    _description = 'Gestión de Pacientes'
    name = fields.Char(string='Nombre', required=True, copy=False)
    last_name = fields.Char(string='Apellido', required=True)
    document_type = fields.Selection([('dni', 'Documento Nacional de Identidad'), ('psp', 'Pasaporte'), ('ce', 'Cédula Extranjera')], string='Tipo de Documento', required=True)
    document_number = fields.Integer(string='Número de Documento', required=True,help="Sin puntos ni comas")
    birth_date = fields.Date(string='Fecha de Nacimiento', required=True, help="Fecha de Nacimiento del Paciente")
    gender = fields.Selection(
        string='Género',
        selection=[('male', 'Masculino'), ('female', 'Femenino'), ('other', 'Otro')],
        help="Espeficique el género del paciente",default='female')
    age = fields.Integer(string='Edad', compute='_compute_age', store=True, readonly=True)
    address = fields.Char(string='Dirección')
    city = fields.Char(string='Ciudad')
    postal_code = fields.Char(string='Código Postal') #could change Integer
    phone = fields.Char(string='Teléfono')            #could be Integer
    active = fields.Boolean(string='Vive', default=True)
    # Many2one: Médico de cabecera
    primary_doctor_id = fields.Many2one('clinic.doctor', string='Médico de Cabecera')

    # Many2many: Médicos que lo han revisado
    doctors_ids = fields.Many2many('clinic.doctor', string='Médicos que lo han Revisado')

    # One2many: Diagnósticos
    diagnosis_ids = fields.One2many('clinic.medical.diagnosis', 'patient_id', string='Diagnósticos', readonly=True)

    # Many2many: Acompañantes
    companions_ids = fields.One2many('clinic.accompanist', 'patients_id', string='Acompañantes', readonly=True)

    display_name = fields.Char(string='Nombre a Mostrar', compute='_compute_display_name', store=True)

    states_ids = fields.Many2many('clinic.states', 'patient_state_rel',compute='_compute_states_ids' , string="Estado", store=True, readonly=True, copy=False, help="Estado del paciente")

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                born = record.birth_date
                rd=relativedelta(today, born)
                if (today.month) == (born.month) & (today.day) >= (born.day):
                    record.age = rd.years + 1
                else:
                    record.age = rd.years
            else:
                record.age = 0


    @api.depends('diagnosis_ids', 'diagnosis_ids.states_id')
    def _compute_states_ids(self):
        for rec in self:
            estados=rec.diagnosis_ids.mapped('states_id.id')
            rec.states_ids=[(6, 0, estados)]

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'{rec.last_name} {rec.name}'

    @api.model
    def _create_patient(self, vals):
        """
        This function creates a new patient record based on the provided data (vals).

        :param: A dictionary containing patient information with keys matching the model fields.
        :return: record (Patient): The newly created patient record.
        :use case: patient = self.env['clinic.patient']._create_patient({
                                                                            'name': 'John',
                                                                            'last_name': 'Doe',
                                                                            'document_type': 'dni',
                                                                            'document_number': 12345678,
                                                                            'birth_date': '1990-01-01',
                                                                            # Optional fields
                                                                            'address': '123 Main Street',
                                                                            'phone': '123-456-7890',
                                                                        })
        """
        # Check mandatory fields are present
        required_fields = ['name', 'last_name', 'document_type',
                           'document_number', 'birth_date']
        missing_fields = [field for field in required_fields if field not in vals]
        if missing_fields:
            raise ValueError(f"Missing required data: {', '.join(missing_fields)}")
        # Create record using super() with provided values
        return self.create(vals)
    
    # Constraints and SQL Constraints
    _sql_constraints = [
        ('unique_document_number', 'unique(document_type, document_number)', 'El número de documento debe ser único para cada paciente.'),
    ]
    @api.constrains('phone')
    def _check_phone_format(self):
        for record in self:
            if record.phone:
                if not re.match(r'^[0-9\s\-\+\(\)]+$', record.phone):
                    raise ValidationError("Formato de número de teléfono inválido. Por favor, utilice solo números, espacios, guiones, paréntesis y signos de suma.")



