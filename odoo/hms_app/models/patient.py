from odoo import models, fields, api
from odoo.exceptions import  ValidationError

class HmsPatient(models.Model):
    _name = "hms_app.patient"
    _description = "Hospital Patient"
    _inherit = 'image.mixin'

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    birth_date = fields.Date(string="Birth Date")
    cr_ratio = fields.Float(string="CR Ratio")
    blood_type = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ], string="Blood Type")
    pcr = fields.Boolean(string="PCR Test Done")
    image = fields.Image(string="Image", max_width=1920, max_height=1920)
    image_small = fields.Image("Small Photo", related="image", max_width=128, max_height=128, store=True)
    address = fields.Text(string="Address")
    age = fields.Integer(string="Age")
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string="Status", default='undetermined')


    department_id = fields.Many2one("hms_app.department", string="Department",
                                    domain="[('is_opened', '=', True)]")
    department_capacity = fields.Integer(related="department_id.capacity", string="Department Capacity")

    doctor_ids = fields.Many2many(
        "hms_app.doctors",
        string="Doctors",
        domain="[('department_id', '=', department_id)]",


    )

    # New field for logs
    log_ids = fields.One2many("hms_app.patient.log", "patient_id", string="State Change Logs")

    @api.onchange('age')
    def _onchange_age(self):
        for record in self:
            if record.age < 30:
                record.pcr = True
                return {
                    'value': {},
                    'warning': {
                        'title': "PCR Auto-checked",
                        'message': "PCR has been automatically checked because age is below 30."
                    }
                }

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError("CR Ratio is required when PCR is checked.")

    def write(self, vals):
        if 'state' in vals:
            old_state = dict(self._fields['state'].selection).get(self.state, self.state)
            new_state = dict(self._fields['state'].selection).get(vals['state'], vals['state'])
            description = f"State changed from {old_state} to {new_state}"
            self.env["hms_app.patient.log"].create({
                'patient_id': self.id,
                'description': description
            })
        return super(HmsPatient, self).write(vals)

    @api.onchange('department_id')
    def _onchange_department(self):
        if self.department_id:
            # Clear doctors when department changes
            self.doctor_ids = False
            return {
                'warning': {
                    'title': "Notice",
                    'message': "You can now select doctors for this department"
                }
            }