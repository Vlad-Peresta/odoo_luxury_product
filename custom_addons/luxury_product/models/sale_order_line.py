from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = ["sale.order.line"]

    x_is_luxury_product = fields.Boolean(related="product_template_id.x_is_luxury_product")
