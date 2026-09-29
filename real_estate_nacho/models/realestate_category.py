from odoo import models, fields

class RealEstateCategory(models.Model):
    _name = "realestate.category"
    _description = "Real Estate Category"

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")