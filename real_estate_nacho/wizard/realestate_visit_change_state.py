from odoo import fields, models


class RealEstateVisitChangeState(models.TransientModel):
    _name = "realestate.visit.change.state"
    _description = "Wizard to change the state of visits"

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("done", "Done"),
            ("canceled", "Canceled"),
        ],
        string="State",
        required=True,
        default="draft"
    )

    def action_change_state(self):
        visits = self.env["realestate.visit"].browse(
            self.env.context.get("active_ids", [])
        )
        visits.write({"state": self.state})
        return {
            "type": "ir.actions.act_window",
            "name": "Visits",
            "res_model": "realestate.visit",
            "view_mode": "list,form",
            "domain": [("id", "in", visits.ids)],
            "target": "current",
        }
