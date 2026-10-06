from freezegun import freeze_time

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestRealEstateVisit(TransactionCase):

    def setUp(self):
        super().setUp()
        self.property = self.env["realestate.property"].create({
            "name": "Test Property",
        })

    @freeze_time("2026-10-06 10:00:00")
    def test_cron_finish_visits(self):
        Visit = self.env["realestate.visit"]
        visit_past = Visit.create({
            "property_id": self.property.id,
            "date": "2026-10-05 10:00:00",
            "state": "scheduled",
        })
        visit_future = Visit.create({
            "property_id": self.property.id,
            "date": "2026-10-07 10:00:00",
            "state": "scheduled",
        })
        visit_draft = Visit.create({
            "property_id": self.property.id,
            "date": "2026-10-01 10:00:00",
            "state": "draft",
        })
        Visit._cron_finish_visits()
        self.assertEqual(visit_past.state, "done")
        self.assertEqual(visit_future.state, "scheduled")
        self.assertEqual(visit_draft.state, "draft")
