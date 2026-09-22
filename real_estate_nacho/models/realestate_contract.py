from odoo import models, fields, api

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

    duration_days = fields.Integer(string="Duration (Days)", 
        compute="_compute_duration_days",
        store=True)

    days_to_end = fields.Integer(string="Days to End", 
        compute="_compute_days_to_end")

    @api.depends('start_date', 'end_date')
    def _compute_duration_days(self):
        for record in self:
            if record.start_date and record.end_date:
                record.duration_days = (record.end_date - record.start_date).days
            else:
                record.duration_days = 0
    
    def _compute_days_to_end(self):
        for record in self:
            if record.end_date:
                record.days_to_end = (record.end_date - fields.Date.today()).days
            else:
                record.days_to_end = 0

    def action_draft(self):
        self.state = 'draft'

    def action_progress(self):
        self.state = 'progress'

    def action_done(self):
        self.state = 'done'

    def action_cancelled(self):
        self.state = 'cancelled'
