from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestRealEstateContract(TransactionCase):

    def test_check_dates(self):
        with self.assertRaises(ValidationError):
            self.env["realestate.contract"].create({
                "start_date": "2026-10-10",
                "end_date": "2026-10-05",
            })
