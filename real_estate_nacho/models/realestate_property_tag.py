from odoo import fields, models


class RealEstatePropertyTag(models.Model):
    _name = "realestate.property.tag"
    _description = "Property Tag"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
