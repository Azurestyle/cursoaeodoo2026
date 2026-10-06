from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestRealEstateOffer(TransactionCase):

    def test_check_amount(self):
        with self.assertRaises(ValidationError):
            self.env["realestate.offer"].create({
                "amount": -1.0,
            })
