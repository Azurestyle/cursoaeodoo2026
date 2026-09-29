from odoo import models, fields
from datetime import timedelta


class RealEstatePropertyScheduleVisits(models.TransientModel):
    _name = "realestate.property.schedule.visits"
    _description = "Schedule Property Visits"

    start_date = fields.Datetime(string="Start Date", required=True)
    end_date = fields.Datetime(string="End Date", required=True)

    def action_create_visits(self):
        vals_list = []
        current_date = self.start_date
        property = self.env['realestate.property'].browse(self.env.context.get('active_id'))
        while current_date <= self.end_date:
            vals_list.append({
                'property_id': property.id,
                'date': current_date,
                'user_id': property.user_id.id,
                'state': 'scheduled',
            })
            current_date += timedelta(days=1)
        visits = self.env['realestate.visit'].create(vals_list)

        return {

            'type': 'ir.actions.act_window',
            'name': 'Scheduled Visits',
            'res_model': 'realestate.visit',
            'view_mode': 'list,form',
            'domain': [('id', 'in', visits.ids)],
        }
        