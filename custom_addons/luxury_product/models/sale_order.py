from odoo import models


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    def action_confirm(self):
        gift_product = self.env.ref("luxury_product.gift_product")
        luxury_order_line_ids = self.filtered(
            lambda order: order.order_line.filtered(
                lambda line: line.order_id.id == order.id
            )
            and order.order_line.filtered(lambda line: line.is_luxury_product is True)
        )
        params = self.env["ir.config_parameter"].sudo()
        is_gift_product_applied = params.get_param(
            "luxury_product.is_gift_product_applied"
        )

        if is_gift_product_applied and luxury_order_line_ids:
            self.write(
                {
                    "order_line": [
                        (
                            0,
                            False,
                            {
                                "product_id": gift_product.id,
                                "order_id": self.id,
                            },
                        )
                    ]
                }
            )

        return super().action_confirm()
