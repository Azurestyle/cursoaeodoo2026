from odoo import api, fields, models


class RealEstateProperty(models.Model):
    _name = "realestate.property"
    _description = "Property"

    _reference_uniq = models.Constraint(
        "unique(reference)",
        "The property reference must be unique."
    )

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    internal_note = fields.Text(string="Internal Note", company_dependent=True)
    category_id = fields.Many2one(
        comodel_name="realestate.category",
        string="Category",
    )
    tag_ids = fields.Many2many(
        comodel_name="realestate.property.tag",
        relation="realestate_property_realestate_property_tag_rel",
        column1="realestate_property_id",
        column2="realestate_property_tag_id",
        string="Tags",
    )
    price = fields.Monetary(string="Price", currency_field="currency_id")
    reference = fields.Char(string="Reference", copy=False)
    availability = fields.Boolean(string="Availability", default=True)
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        default=lambda self: self.env.user
    )
    agent_id = fields.Many2one(
        comodel_name="realestate.agent",
        string="Agent",
    )
    owner_id = fields.Many2one(
        comodel_name="realestate.owner",
        string="Owner",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id
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
        string="Visits",
        copy=False
    )
    incident_ids = fields.One2many(
        comodel_name="realestate.property.incident",
        inverse_name="property_id",
        string="Incidents",
        copy=False
    )
    offer_ids = fields.One2many(
        comodel_name="realestate.offer",
        inverse_name="property_id",
        string="Offers",
        copy=False
    )
    contract_ids = fields.One2many(
        comodel_name="realestate.contract",
        inverse_name="property_id",
        string="Contracts",
        copy=False
    )
    next_visit_date = fields.Datetime(
        string="Next Visit",
        compute="_compute_next_visit_date",
        store=True
    )
    visit_count = fields.Integer(
        compute="_compute_visit_count"
    )
    incident_count = fields.Integer(
        compute="_compute_incident_count"
    )
    contract_count = fields.Integer(
        compute="_compute_contract_count"
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

    @api.depends('visit_ids')
    def _compute_visit_count(self):
        for record in self:
            record.visit_count = len(record.visit_ids)

    @api.depends('incident_ids')
    def _compute_incident_count(self):
        for record in self:
            record.incident_count = len(record.incident_ids)

    @api.depends('contract_ids')
    def _compute_contract_count(self):
        for record in self:
            record.contract_count = len(record.contract_ids)

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

    def action_open_visits(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visits',
            'res_model': 'realestate.visit',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id},
        }

    def action_open_incidents(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Incidents',
            'res_model': 'realestate.property.incident',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id},
        }

    def action_open_contracts(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Contracts',
            'res_model': 'realestate.contract',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id},
        }
