from odoo import fields, models


class RealEstatePropertyImage(models.Model):
    _name = "realestate.property.image"
    _description = "Property Image"
    _order = "sequence, id"

    name = fields.Char(string="Name")
    image = fields.Binary(string="Image")
    sequence = fields.Integer(string="Sequence", default=10)
    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
        required=True,
        ondelete="cascade"
    )
