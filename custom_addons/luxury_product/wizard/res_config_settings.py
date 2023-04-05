from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    x_is_gift_product_applied = fields.Boolean(
        related="company_id.x_is_gift_product_applied", readonly=False
    )
