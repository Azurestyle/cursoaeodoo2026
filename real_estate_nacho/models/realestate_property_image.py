from odoo import models, fields

class RealestatePropertyImage(models.Model):
    _name = "realestate.property.image"
    _description = "Property Image"

    def _default_name(self):
        return "Imagen "

    name = fields.Char(string="Name", default=_default_name())
    sequence = fields.Integer(string="Sequence", default=10)
    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
        ondelete="cascade",
    )
    image = fields.Binary(string="Image")