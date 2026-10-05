from odoo import Command, api, fields, models


class RealEstateContract(models.Model):
    _inherit = "realestate.contract"

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
    )
    order_ids = fields.One2many(
        comodel_name="sale.order",
        inverse_name="contract_id",
        string="Sale Orders",
    )
    order_count = fields.Integer(
        string="Sale Orders Count",
        compute="_compute_order_count",
    )

    @api.depends("order_ids")
    def _compute_order_count(self):
        for record in self:
            record.order_count = len(record.order_ids)

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.rent = self.product_id.list_price

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name"):
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "realestate.contract"
                )
        return super().create(vals_list)

    def action_create_sale_order(self):
        for record in self:
            self.env["sale.order"].create({
                "partner_id": record.partner_id.id,
                "contract_id": record.id,
                "company_id": (record.property_id.company_id or self.env.company).id,
                "order_line": [Command.create({
                    "product_id": record.product_id.id,
                    "product_uom_qty": 1.0,
                    "price_unit": record.rent,
                })],
            })

    def action_view_orders(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Sale Orders",
            "res_model": "sale.order",
            "view_mode": "list,form",
            "domain": [("contract_id", "=", self.id)],
            "context": {"default_contract_id": self.id},
        }

    def action_confirm_and_invoice(self):
        for record in self:
            orders = record.order_ids.filtered(
                lambda order: order.state in ("draft", "sent")
            )
            if not orders:
                continue
            orders.action_confirm()
            orders._create_invoices()

    def action_cancelled(self):
        res = super().action_cancelled()
        self.order_ids.action_cancel()
        return res
