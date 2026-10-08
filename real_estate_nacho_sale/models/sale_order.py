from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    contract_id = fields.Many2one(
        comodel_name="realestate.contract",
        string="Contract",
    )

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if order.contract_id:
                continue
            rental_line = order.order_line.filtered(
                lambda line: line.product_id.is_rental
            )[:1]
            if not rental_line:
                continue
            contract = self.env["realestate.contract"].create({
                "partner_id": order.partner_id.id,
                "product_id": rental_line.product_id.id,
                "contract_type": "rent",
                "rent": rental_line.price_unit,
            })
            order.contract_id = contract.id
        return res
