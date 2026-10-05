from odoo import models, fields


class RealestateOwner(models.Model):
    _name = "realestate.owner"
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one("res.partner", required=True, ondelete="cascade")