from odoo import models, fields, api

class RealEstateProperty(models.Model):
    _name = "realestate.property"
    _description = "Property"

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    category_id = fields.Many2one(
        comodel_name="realestate.category",
        string="Category",
    )
    price = fields.Monetary(string="Price", currency_field='currency_id')
    reference = fields.Char(string="Reference", copy=False)
    availability = fields.Boolean(string="Availability", default=True)
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        default=lambda self: self.env.user.id
    )
    agent_id = fields.Many2one(
        comodel_name="realestate.agent",
        string="Agent"
    )
    owner_id = fields.Many2one(
        comodel_name="realestate.owner",
        string="Owner"
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id.id
    )
    
    stage_id = fields.Many2one(
        comodel_name="realestate.property.stage",
        string="Stage",
        group_expand="_read_group_stage_ids"
    )

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
    contract_ids = fields.One2many(
        comodel_name="realestate.contract",
        inverse_name="property_id",
        string="Contracts"
    )
    tag_ids = fields.Many2many(
        comodel_name="realestate.property.tag",
        relation="realestate_property_tag_rel",
        column1="realestate_property_id",
        column2="realestate_property_tag_id",
        string="Tags"
    )

    internal_note = fields.Text(string="Internal Note", company_dependent=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company.id
    )

    next_visit_date = fields.Datetime(string="Next Visit Date", compute="_compute_next_visit_date", inverse="_inverse_next_visit_date", store=True)
    color = fields.Integer(string="Color")
    visit_count = fields.Integer(string="Visit Count", compute="_compute_visit_count")
    incident_count = fields.Integer(string="Incident Count", compute="_compute_incident_count")
    contract_count = fields.Integer(string="Contract Count", compute="_compute_contract_count")

    _reference_uniq = models.Constraint(
        "unique(reference)",
        "The property reference must be unique."
    )

    def _inverse_next_visit_date(self):
        for record in self:
            if record.next_visit_date:
                scheduled_visits = record.visit_ids.filtered(lambda visit: visit.state == 'scheduled')
                if scheduled_visits:
                    scheduled_visits[0].date = record.next_visit_date
                   
    def _compute_contract_count(self):
        for record in self:
            record.contract_count = len(record.contract_ids)

    def _compute_visit_count(self):
        for record in self:
            # visit_ids = len(self.env['realestate.visit'].search([('property_id', '=', record.id)]))
            # visit_ids = self.env['realestate.visit'].search_count([('property_id', '=', record.id)])
            record.visit_count = len(record.visit_ids)
    def _compute_incident_count(self):
        for record in self:
            record.incident_count = len(record.incident_ids)

    def action_reserve(self):
        self.availability = False
    
    def _read_group_stage_ids(self, stages, domain):
        return self.env['realestate.property.stage'].search([], order='sequence')
    
    def action_create_visit(self):
        import pdb;pdb.set_trace()
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

    @api.depends('visit_ids.date', 'visit_ids.state')
    def _compute_next_visit_date(self):
        for record in self:
            # next_visit = self.env['realestate.visit'].search([
            #     ('property_id', '=', record.id),
            #     ('state', '=', 'scheduled')], order='date asc', limit=1)
            # record.next_visit_date = next_visit.date if next_visit else False
            scheduled_visits = record.visit_ids.filtered(lambda visit: visit.state =='scheduled' and visit.date)
            visit_dates = scheduled_visits.mapped('date')
            record.next_visit_date = min(visit_dates) if visit_dates else False

    def action_cancel_pending_visits(self):
        pending_visits = self.env['realestate.visit'].search([('property_id', '=', self.id),('state', 'in', ['draft','scheduled'])])
        pending_visits.unlink()

    def action_open_visits(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Visits',
            'res_model': 'realestate.visit',
            'view_mode': 'kanban,list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id}
        }
        return action

    def action_open_incidents(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Incidents',
            'res_model': 'realestate.property.incident',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id}
        }

    def action_open_contracts(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Contracts',
            'res_model': 'realestate.contract',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id}
        }
    # def action_print_property(self):
    #     return self.env.ref('real_estate_nacho.action_report_realestate_property').report_action(self.ids)