from odoo import models, fields


class Company(models.Model):
    _inherit = "res.company"

    x_is_gift_product_applied = fields.Boolean(
        "Apply gift for Luxury product", default=False
    )
