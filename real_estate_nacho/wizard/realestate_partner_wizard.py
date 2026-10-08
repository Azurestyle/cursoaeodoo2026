from odoo import fields, models


class RealEstatePartnerWizard(models.TransientModel):
    _name = "realestate.partner.wizard"
    _description = "Contact Wizard"

    name = fields.Char(string="Name", required=True)
    phone = fields.Char(string="Phone", required=True)
    email = fields.Char(string="Email")
    street = fields.Char(string="Street")
    city = fields.Char(string="City")
    zip = fields.Char(string="Zip")
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
    )
    category_id = fields.Many2many(
        comodel_name="res.partner.category",
        string="Tags",
    )

    def action_create_partner(self):
        self.ensure_one()
        partner = self.env["res.partner"].create({
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "street": self.street,
            "city": self.city,
            "zip": self.zip,
            "country_id": self.country_id.id,
            "category_id": [(6, 0, self.category_id.ids)],
        })
        return {
            "type": "ir.actions.act_window",
            "name": "Contact",
            "res_model": "res.partner",
            "res_id": partner.id,
            "view_mode": "form",
            "target": "current",
        }
