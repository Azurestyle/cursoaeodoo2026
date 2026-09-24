from odoo import models, fields

class RealestatePropertyIncident(models.Model):
    _name = "realestate.property.incident"
    _description = "Property Incident"

    sequence = fields.Integer(string="Sequence", default=10)
    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
        ondelete="cascade"
    )
    date = fields.Datetime(string="Date")
    priority = fields.Selection(
        selection=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'),('very_high', 'Very High')],
        string="Priority",
        default='medium'
    )

    state = fields.Selection(
        selection=[('draft', 'Draft'), ('in_progress', 'In Progress'), ('done', 'Done'), ('canceled', 'Canceled')],
        string="State",
        default='draft'
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User"
    )