from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_gift_product_applied = fields.Boolean(
        "Apply gift for Luxury product", default=False
    )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "luxury_product.is_gift_product_applied", self.is_gift_product_applied
        )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env["ir.config_parameter"].sudo()
        res.update(
            is_gift_product_applied=params.get_param(
                "luxury_product.is_gift_product_applied"
            )
        )
        return res
