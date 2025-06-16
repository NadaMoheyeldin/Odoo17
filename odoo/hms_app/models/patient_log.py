# patient_log.py
from odoo import models, fields

class HmsPatientLog(models.Model):
    _name = "hms_app.patient.log"
    _description = "Patient State Change Log"

    patient_id = fields.Many2one("hms_app.patient", string="Patient", required=True)
    created_by = fields.Many2one("res.users", string="Created By", default=lambda self: self.env.user)
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    description = fields.Text(string="Description")