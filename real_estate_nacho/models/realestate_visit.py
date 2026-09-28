from odoo import api, fields, models

class RealEstateVisit(models.Model):
    _name = "realestate.visit"
    _description = "Visit"
    _rec_name = "property_id"

    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
        required=True,
    )
    date = fields.Datetime(string="Visit Date", default=fields.Datetime.now)

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Visitor",
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
    )
    phone = fields.Char(string="Phone")
    personal_email = fields.Char(string="Personal Email")
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

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.phone = self.partner_id.phone
            self.personal_email = self.partner_id.email

    def action_schedule(self):
        self.state = "scheduled"
        #self.write({'state': 'scheduled'})

    def action_done(self):
        self.state = "done"
    
    def action_cancel(self):
        self.state = "canceled"
    
    def action_draft(self):
        self.state = "draft"

    def _cron_finish_visits(self):
        visits = self.search([
            ('state', '=', 'scheduled'),
            ('date', '<', fields.Datetime.now()),
        ])
        visits.write({'state': 'done'})