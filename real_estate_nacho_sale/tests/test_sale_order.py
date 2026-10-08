from odoo.tests import common


class TestSaleOrder(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({
            "name": "Test Customer",
        })
        self.rental_product = self.env["product.product"].create({
            "name": "Rental Product",
            "list_price": 1200.0,
            "is_rental": True,
        })
        self.other_product = self.env["product.product"].create({
            "name": "Other Product",
            "list_price": 300.0,
        })
        self.rental_order = self.env["sale.order"].create({
            "partner_id": self.partner.id,
            "order_line": [(0, 0, {
                "product_id": self.rental_product.id,
                "product_uom_qty": 1.0,
                "price_unit": 1200.0,
            })],
        })
        self.other_order = self.env["sale.order"].create({
            "partner_id": self.partner.id,
            "order_line": [(0, 0, {
                "product_id": self.other_product.id,
                "product_uom_qty": 1.0,
                "price_unit": 300.0,
            })],
        })

    def test_action_confirm_creates_contract(self):
        self.rental_order.action_confirm()
        self.assertTrue(self.rental_order.contract_id)
        self.assertEqual(self.rental_order.contract_id.partner_id, self.partner)
        self.assertEqual(self.rental_order.contract_id.product_id, self.rental_product)
        self.assertEqual(self.rental_order.contract_id.contract_type, "rent")
        self.assertEqual(self.rental_order.contract_id.rent, 1200.0)

    def test_action_confirm_without_rental_product(self):
        self.other_order.action_confirm()
        self.assertFalse(self.other_order.contract_id)
