from odoo import models


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    def action_confirm(self):
        if self.env.company.x_is_gift_product_applied:
            gift_product = self.env.ref("luxury_product.gift_product")
            for order in self.filtered(
                lambda order_id: order_id.order_line.filtered(
                    lambda line: line.x_is_luxury_product
                )
            ):
                if gift_product not in order.order_line.mapped("product_id"):
                    order.write(
                        {
                            "order_line": [
                                (
                                    0,
                                    False,
                                    {
                                        "product_id": gift_product.id,
                                        "order_id": order.id,
                                    },
                                )
                            ]
                        }
                    )

        return super().action_confirm()
