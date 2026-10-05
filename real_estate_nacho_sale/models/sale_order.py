from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    contract_id = fields.Many2one(
        comodel_name="realestate.contract",
        string="Contract",
    )
