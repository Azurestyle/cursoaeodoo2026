from odoo import models, fields


class RealestatePartnerWizard(models.TransientModel):
    _name = "realestate.partner.wizard"
    _description = "Wizard to manage real estate partners"


    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    street = fields.Char(string="Street")
    city = fields.Char(string="City")
    category_id = fields.Many2many(
        comodel_name="res.partner.category",
        string="Categories"
    )

    def action_create_partner(self):
        self.ensure_one()
        partner = self.env['res.partner'].create({
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'street': self.street,
            'city': self.city,
            'category_id': [(6, 0, self.category_id.ids)],
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Contact',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'res_id': partner.id,
        }