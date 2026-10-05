from odoo import models, fields

class RealEstateAgent(models.Model):
    _name = "realestate.agent"
    _description = "Agent"
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=True, ondelete="cascade")
    commission = fields.Float(string="Commission (%)")
    