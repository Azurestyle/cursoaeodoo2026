from odoo import api, fields, models

class RealEstateProperty(models.Model):
    _name = "realestate.property"
    _description = "Property"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    category_id = fields.Many2one(
        comodel_name="realestate.category",
        string="Category",
    )
    price = fields.Float(string="Price")
    reference = fields.Char(string="Reference")
    availability = fields.Boolean(string="Availability", default=True)
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
    )

    stage_id = fields.Many2one(
        comodel_name="realestate.property.stage",
        string="Stage",
        group_expand="_read_group_stage_ids"
    )

    color = fields.Integer(string="Color")
    image_ids = fields.One2many(
        comodel_name="realestate.property.image",
        inverse_name="property_id",
        string="Images"
    )
    visit_ids = fields.One2many(
        comodel_name="realestate.visit",
        inverse_name="property_id",
        string="Visits"
    )
    incident_ids = fields.One2many(
        comodel_name="realestate.property.incident",
        inverse_name="property_id",
        string="Incidents"
    )
    offer_ids = fields.One2many(
        comodel_name="realestate.offer",
        inverse_name="property_id",
        string="Offers"
    )
    next_visit_date = fields.Datetime(
        string="Next Visit",
        compute="_compute_next_visit_date",
        store=True
    )

    def action_reserve(self):
        self.availability = False
    
    def _read_group_stage_ids(self, stages, domain):
        return self.env['realestate.property.stage'].search([], order='sequence')

    @api.depends('visit_ids.date', 'visit_ids.state')
    def _compute_next_visit_date(self):
        for record in self:
            scheduled_visits = record.visit_ids.filtered(
                lambda visit: visit.state == 'scheduled' and visit.date
            )
            visit_dates = scheduled_visits.mapped('date')
            record.next_visit_date = min(visit_dates) if visit_dates else False
    
    def action_create_visit(self):
        vals = {
            'property_id': self.id,
            'date': fields.Datetime.now(),
            'user_id': self.user_id.id
        }
        self.env['realestate.visit'].create(vals)
    
    def action_accept_best_offer(self):
        best_offer = self.env['realestate.offer'].search([('property_id', '=', self.id),('state', '=', 'sent')], order='amount desc', limit=1)
        if best_offer:
            best_offer.action_accept()

    def action_delete_refused_offers(self):
        refused_offers = self.env['realestate.offer'].search([('property_id', '=', self.id),('state', '=', 'refused')])
        refused_offers.unlink()

    def action_create_offer(self):
        vals = {
            'property_id': self.id,
            'amount': self.price,
        }
        offer = self.env['realestate.offer'].create(vals)
        offer.action_send()

    def action_cancel_pending_visits(self):
        pending_visits = self.env['realestate.visit'].search([
            ('property_id', '=', self.id),
            ('state', 'in', ['draft', 'scheduled']),
        ])
        pending_visits.write({'state': 'canceled'})