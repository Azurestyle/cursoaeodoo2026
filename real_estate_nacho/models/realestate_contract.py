from odoo import models, fields

class RealEstateContract(models.Model):
    _name = "realestate.contract"
    _description = "Contract"

    name = fields.Char(string="Name")
    contract_type = fields.Selection(
        selection=[
            ('sale', 'Sale'),
            ('rent', 'Rent'),
        ],
        string="Contract Type",
        default='rent'
    )
    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
    )

    start_date = fields.Date(string="Start Date")

    end_date = fields.Date(string="End Date")

    rent = fields.Float(string="Rent")
    deposit = fields.Float(string="Deposit")

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('progress', 'Progress'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string="State",
        default='draft'
    )

    def action_draft(self):
        self.state = 'draft'

    def action_progress(self):
        self.state = 'progress'

    def action_done(self):
        self.state = 'done'

    def action_cancelled(self):
        self.state = 'cancelled'
