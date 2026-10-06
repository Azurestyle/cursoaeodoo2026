from odoo.tests import common


class TestRealEstateProperty(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.Property = self.env['realestate.property']
        self.Visit = self.env['realestate.visit']
        self.Offer = self.env['realestate.offer']

        self.property_1 = self.Property.create({
            'name': 'Test Property',
            'price': 100000.0,
        })

        self.visit_1 = self.Visit.create({
            'property_id': self.property_1.id,
            'date': '2026-10-10 10:00:00',
            'state': 'scheduled',
        })
        self.visit_2 = self.Visit.create({
            'property_id': self.property_1.id,
            'date': '2026-10-12 10:00:00',
            'state': 'scheduled',
        })
        self.visit_3 = self.Visit.create({
            'property_id': self.property_1.id,
            'date': '2026-10-08 10:00:00',
            'state': 'draft',
        })

        self.offer_1 = self.Offer.create({
            'property_id': self.property_1.id,
            'amount': 90000.0,
            'state': 'sent',
        })
        self.offer_2 = self.Offer.create({
            'property_id': self.property_1.id,
            'amount': 99000.0,
            'state': 'sent',
        })

    def test_action_create_visit(self):
        self.property_1.action_create_visit()
        self.assertEqual(len(self.property_1.visit_ids), 4)
        self.assertEqual(self.property_1.visit_ids[-1].user_id, self.property_1.user_id)

    def test_action_accept_best_offer(self):
        self.property_1.action_accept_best_offer()
        self.assertEqual(self.offer_2.state, 'accepted')
        self.assertEqual(self.offer_1.state, 'sent')
        self.assertFalse(self.property_1.availability)

    def test_compute_next_visit_date(self):
        self.assertEqual(self.property_1.next_visit_date, self.visit_1.date)
