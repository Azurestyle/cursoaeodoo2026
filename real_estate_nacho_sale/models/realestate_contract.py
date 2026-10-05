from odoo import Command, models, fields, api


class RealEstateContract(models.Model):
    _inherit = "realestate.contract"

    product_id = fields.Many2one(comodel_name="product.product",
                                 string="Product")
    order_ids = fields.One2many(comodel_name="sale.order",
                                inverse_name="contract_id",
                                string="Orders")
    order_count = fields.Integer(string="Order Count", compute="_compute_order_count")

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.rent = self.product_id.list_price

    def _compute_order_count(self):
        for contract in self:
            contract.order_count = len(contract.order_ids)

    def action_view_orders(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Orders",
            "res_model": "sale.order",
            "view_mode": "list,form",
            "domain": [("contract_id", "=", self.id)],
            "context": {"default_contract_id": self.id},
        }

    def action_create_sale_order(self):
        for record in self:

            vals = {
                "partner_id": record.partner_id.id,
                "contract_id": record.id,
                "company_id": record.property_id.company_id.id,
                "order_line": [(0, 0, {
                    "product_id": record.product_id.id,
                    "product_uom_qty": 1.0,
                    "price_unit": record.rent,
                })]
            }
            # vals = {
            #     "partner_id": record.partner_id.id,
            #     "contract_id": record.id,
            #     "order_line": [Command.create({
            #         "product_id": record.product_id.id,
            #         "product_uom_qty": 1.0,
            #         "price_unit": record.rent,
            #     })]
            #             }
            order_id = self.env['sale.order'].create(vals)
            return {
                "type": "ir.actions.act_window",
                "name": "Sale Order",
                "res_model": "sale.order",
                "view_mode": "form",
                "res_id": order_id.id,
            }

    def action_cancelled(self):
        res = super().action_cancelled()
        self.order_ids.action_cancel()
        return res

    def action_confirm_and_invoice(self):
        for record in self:
            orders = record.order_ids.filtered(lambda o: o.state in ("draft"))
            if not orders:
                continue
            orders.action_confirm()
            orders._create_invoices()