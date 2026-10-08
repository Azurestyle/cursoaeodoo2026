from datetime import timedelta

from odoo import fields, models


class RealEstatePropertyScheduleVisits(models.TransientModel):
    _name = "realestate.property.schedule.visits"
    _description = "Wizard to schedule visits for a property"

    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
        required=True
    )
    start_date = fields.Datetime(
        string="Start Date",
        required=True,
        default=fields.Datetime.now
    )
    end_date = fields.Datetime(
        string="End Date",
        required=True,
        default=fields.Datetime.now
    )

    def action_create_visits(self):
        vals_list = []
        current_date = self.start_date
        while current_date <= self.end_date:
            vals_list.append({
                "property_id": self.property_id.id,
                "date": current_date,
                "user_id": self.property_id.user_id.id,
                "state": "scheduled",
            })
            current_date += timedelta(days=1)
        visits = self.env["realestate.visit"].create(vals_list)
        for visit in visits:
            visit.message_post(
                body=f"Visit scheduled for {self.property_id.display_name}."
            )
        return {
            "type": "ir.actions.act_window",
            "name": "Visits",
            "res_model": "realestate.visit",
            "view_mode": "list,form",
            "domain": [("id", "in", visits.ids)],
            "target": "current",
        }
