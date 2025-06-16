from odoo import models, fields

class HmsDepartment(models.Model):
    _name = "hms_app.department"
    _description = "Hospital Department"

    name = fields.Char(string="Department Name", required=True)
    capacity = fields.Integer(string="Capacity")
    is_opened = fields.Boolean(string="Is Opened", default=True)
    patient_ids = fields.One2many("hms_app.patient", "department_id", string="Patients")
