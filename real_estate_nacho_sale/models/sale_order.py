from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    contract_id = fields.Many2one(comodel_name="realestate.contract",
                                  string="Contract")