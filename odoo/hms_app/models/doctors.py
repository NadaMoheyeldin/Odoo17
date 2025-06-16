from odoo import models, fields, api

class HmsDoctor(models.Model):
    _name = "hms_app.doctors"
    _description = "Hospital Doctor"

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    image = fields.Image(string="Image", max_width=1920, max_height=1920)
    image_small = fields.Image("Small Photo", related="image", max_width=128, max_height=128, store=True)

    department_id = fields.Many2one("hms_app.department", string="Department")

    # Computed name field
    name = fields.Char(string="Doctor Name", compute="_compute_name", store=True)

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for doctor in self:
            doctor.name = f"{doctor.first_name} {doctor.last_name}"