from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    rental_ok = fields.Boolean(string="Rental")