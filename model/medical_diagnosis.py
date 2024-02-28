from odoo import models, fields, api


class MedicalDiagnosis(models.Model):
    _name = 'clinic.medical.diagnosis'
    _description = 'Gestión de Diagnósticos Médicos'

    diagnosis_code = fields.Selection([
        ('cystic_fibrosis', 'Fibrosis Quística'),
        ('asthma', 'Asma'),
        ('diabetes_type1', 'Diabetes Tipo 1'),
        ('diabetes_type2', 'Diabetes Tipo 2'),
        ('hypertension', 'Hipertensión'),
        ('hyperlipidemia', 'Hiperlipidemia'),
        ('arthritis', 'Artritis'),
        ('migraine', 'Migraña'),
        ('depression', 'Depresión'),
        ('anxiety', 'Ansiedad'),
        ('obesity', 'Obesidad'),
        ('allergies', 'Alergias'),
        ('bronchitis', 'Bronquitis'),
        ('pneumonia', 'Neumonía'),
        ('gastroenteritis', 'Gastroenteritis'),
        ('ulcer', 'Úlcera'),
        ('gastritis', 'Gastritis'),
        ('kidney_stones', 'Cálculos Renales'),
        ('urinary_tract_infection', 'Infección del Tracto Urinario'),
        ('appendicitis', 'Apendicitis'),
        ('other', 'Otro')
    ], string='Diagnóstico', default='other', required=True)
    diagnosis_date = fields.Date(string='Fecha del Diagnóstico')
    doctor_id = fields.Many2one('clinic.doctor', string='Médico')
    patient_id = fields.Many2one('clinic.patient', string='Paciente')
    states_id = fields.Many2one('clinic.states', string='Estado de Avance', readonly=True)
    
    @api.model
    def _get_list(self,diagnostico):
        """
        Get a list of patient names associated with the given diagnosis.

        :param diagnosis: The diagnosis type to search for
        :return: List of patient names
        :use case: lista=self.env['clinic.medical.diagnosis']._get_list('migraine')
        :if .id then: lista=self.env['clinic.patient'].browse(self.env['clinic.medical.diagnosis']._get_list('migraine')).mapped('display_name')
        """
        diagnosticos= self.search([('diagnosis_code','=',diagnostico)])
        return diagnosticos.mapped('patient_id.display_name')if diagnosticos else []
    
    @api.model
    def set_state(self, state):
        for rec in self:
            target_state = self.env['clinic.states'].search([('name', '=', state)], limit=1)
            if not target_state:
                target_state = self.env['clinic.states'].create({'name': state})
            rec.states_id = target_state.id
        return True
    
    def set_state_curado(self):
        self.set_state('Curado')
    def set_state_diagnosticado(self):
        self.set_state('Diagnosticado')
    def set_state_ingresado(self):
        self.set_state('Ingresado')
    def set_state_internado(self):
        self.set_state('Internado')
    def set_state_tratamiento(self):
        self.set_state('Tratamiento')
    
    @api.model
    def _create_diagnosis(self, vals):
        """
        This function creates a new diagnosis record based on the provided data (vals).

        :param vals: A dictionary containing diagnosis information.
                    It should include 'diagnosis_code', 'diagnosis_date', 'doctor_id',
                    'document_type', and 'document_number'.
        :return: record (MedicalDiagnosis): The newly created diagnosis record.
        :use case: diagnosis = self.env['clinic.medical.diagnosis']._create_diagnosis({
                                                                                        'diagnosis_code': 'asthma',
                                                                                        'diagnosis_date': '2024-02-26',
                                                                                        'doctor_id': 1,
                                                                                        'document_type': 'dni',
                                                                                        'document_number': 798456,
                                                                                    })
        """
        # Check mandatory fields are present
        required_fields = ['diagnosis_code', 'diagnosis_date', 'doctor_id', 'document_type', 'document_number']
        missing_fields = [field for field in required_fields if field not in vals]
        if missing_fields:
            raise ValueError(f"Missing required data: {', '.join(missing_fields)}")
        
        # Find patient based on document type and number
        patient = self.env['clinic.patient'].search([('document_type', '=', vals['document_type']),
                                                    ('document_number', '=', vals['document_number'])], limit=1)
        if not patient:
            raise ValueError("Patient not found with the provided document type and number.")
        
        # Add patient to the vals dictionary
        vals['patient_id'] = patient.id
        
        # Remove 'document_type' and 'document_number' from vals
        vals.pop('document_type', None)
        vals.pop('document_number', None)
        
        # Create diagnosis record using patient's ID
        return self.create(vals)

