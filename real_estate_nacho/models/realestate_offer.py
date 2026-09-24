from odoo import models, fields

class RealEstateOffer(models.Model):
    _name = "realestate.offer"
    _description = "Offer"
    _rec_name = "partner_id"

    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
    )
    category_id = fields.Many2one(
        comodel_name="realestate.category",
        string="Category",
        related="property_id.category_id",
        readonly=True
    )

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
    )

    amount = fields.Float(string="Amount")
    date = fields.Datetime(string="Date")
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="State",
        default='draft',
    )
    note = fields.Html(string="Note")

    def action_send(self):
        self.state = 'sent'

    def action_accept(self):
        self.state = 'accepted'
        self.property_id.action_reserve()

    def action_refuse(self):
        self.state = 'refused'

    def action_draft(self):
        self.state = 'draft'

    def action_create_contract(self):
        self.env['realestate.contract'].create({
            'property_id': self.property_id.id,
            'partner_id': self.partner_id.id,
            'contract_type': 'sale',
            'start_date': fields.Date.today(),
        })