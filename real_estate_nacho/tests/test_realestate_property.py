from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestRealEstateProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.property = cls.env["realestate.property"].create({
            "name": "Test Property",
            "price": 100000.0,
        })

    def test_action_create_visit(self):
        self.property.action_create_visit()
        visits = self.env["realestate.visit"].search([
            ("property_id", "=", self.property.id),
        ])
        self.assertEqual(len(visits), 1)
        self.assertEqual(visits.user_id, self.property.user_id)
        self.assertTrue(visits.date)

    def test_action_accept_best_offer(self):
        offer_low = self.env["realestate.offer"].create({
            "property_id": self.property.id,
            "amount": 90000.0,
            "state": "sent",
        })
        offer_high = self.env["realestate.offer"].create({
            "property_id": self.property.id,
            "amount": 99000.0,
            "state": "sent",
        })
        offer_draft = self.env["realestate.offer"].create({
            "property_id": self.property.id,
            "amount": 120000.0,
            "state": "draft",
        })
        self.property.action_accept_best_offer()
        self.assertEqual(offer_high.state, "accepted")
        self.assertEqual(offer_low.state, "sent")
        self.assertEqual(offer_draft.state, "draft")
        self.assertFalse(self.property.availability)

    def test_compute_next_visit_date(self):
        Visit = self.env["realestate.visit"]
        Visit.create({
            "property_id": self.property.id,
            "date": "2026-10-07 09:00:00",
            "state": "draft",
        })
        Visit.create({
            "property_id": self.property.id,
            "date": "2026-10-08 09:00:00",
            "state": "canceled",
        })
        Visit.create({
            "property_id": self.property.id,
            "date": "2026-10-10 10:00:00",
            "state": "scheduled",
        })
        Visit.create({
            "property_id": self.property.id,
            "date": "2026-10-12 10:00:00",
            "state": "scheduled",
        })
        self.assertEqual(
            self.property.next_visit_date,
            fields.Datetime.to_datetime("2026-10-10 10:00:00"),
        )
