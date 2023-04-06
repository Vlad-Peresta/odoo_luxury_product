from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = ["product.template"]

    x_is_luxury_product = fields.Boolean(
        string="Is luxury product?",
        compute="_compute_x_is_luxury_product",
    )

    def _compute_x_is_luxury_product(self):
        luxury_product_ids = self.filtered(
            lambda template: template.attribute_line_ids.filtered(
                lambda attribute_line: attribute_line.attribute_id.name == "Tag"
            )
            and template.attribute_line_ids.value_ids.filtered(
                lambda value: value.name == "Luxury"
            )
        )
        luxury_product_ids.x_is_luxury_product = True
        (self - luxury_product_ids).x_is_luxury_product = False
