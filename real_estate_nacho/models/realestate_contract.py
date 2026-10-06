from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RealEstateContract(models.Model):
    _name = "realestate.contract"
    _description = "Contract"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", copy=False)
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
    
    start_date = fields.Date(string="Start Date", default=fields.Date.today)

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
        default='draft',
        tracking=True
    )

    duration_days = fields.Integer(string="Duration (Days)", 
        compute="_compute_duration_days",
        store=True)

    days_to_end = fields.Integer(string="Days to End", 
        compute="_compute_days_to_end")
    
    days_in_progress = fields.Integer(string="Days in Progress", 
        compute="_compute_days_in_progress")

    has_deposit = fields.Boolean(string="Has Deposit", compute="_compute_has_deposit", store=True)

    _name_uniq = models.Constraint(
        "unique(name)",
        "The contract name must be unique."
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
           if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('realestate.contract')
        res = super().create(vals_list)
        # res. lo que sea
        return res

    def _compute_days_in_progress(self):
        for record in self:
            if record.start_date and record.state == 'progress':
                record.days_in_progress = (fields.Date.today() - record.start_date).days
            else:
                record.days_in_progress = 0

    @api.depends('deposit')
    def _compute_has_deposit(self):
        for record in self:
            record.has_deposit = record.deposit > 0

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

    def _cron_finish_contracts(self):
        contracts = self.env['realestate.contract'].search(
            [('end_date', '<', fields.Date.today()),
             ('state', '=', 'progress')])
        contracts.write({'state': 'done'})

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError("Start Date cannot be after End Date.")

    @api.onchange('property_id')
    def _onchange_property_id(self):
        if self.property_id:
            self.rent = self.property_id.price