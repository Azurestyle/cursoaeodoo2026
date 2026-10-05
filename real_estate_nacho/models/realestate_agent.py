from odoo import fields, models


class RealEstateAgent(models.Model):
    _name = "realestate.agent"
    _description = "Agent"
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Contact",
        required=True,
        ondelete="cascade",
    )
    commission_pct = fields.Float(string="Commission (%)")
