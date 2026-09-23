from odoo import models, fields

class RealEstateVisit(models.Model):
    _name = "realestate.visit"
    _description = "Visit"
    _rec_name = "property_id"

    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
        required=True,
    )
    date = fields.Datetime(string="Visit Date")

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Visitor",
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
    )
    phone = fields.Char(string="Phone", related="partner_id.phone", readonly=False, store=True)
    personal_email = fields.Char(string="Personal Email", related="partner_id.email")
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("done", "Done"),
            ("canceled", "Canceled"),
        ],
        string="State",
        default="draft",
        group_expand="_group_expand_state"
    )

    def _group_expand_state(self, states, domain):
        return ["draft", "scheduled", "done", "canceled"]

    def action_schedule(self):
        self.state = "scheduled"
        #self.write({'state': 'scheduled'})

    def action_done(self):
        self.state = "done"
    
    def action_cancel(self):
        self.state = "canceled"
    
    def action_draft(self):
        self.state = "draft"