from odoo import models, fields


class ProductVariantsChanging(models.TransientModel):
    _name = "product.variants.changing"
    _description = "Change attributes of the product"

    def _get_default_x_active_template_id(self):
        return self.env.context.get("active_id")

    x_attribute_id = fields.Many2one(
        "product.attribute",
        string="Product variant",
    )
    x_old_attribute_value_id = fields.Many2one(
        "product.attribute.value",
        string="Old product variant",
    )
    x_new_attribute_value_id = fields.Many2one(
        "product.attribute.value", string="New product variant"
    )

    x_active_template_id = fields.Char(default=_get_default_x_active_template_id)

    def change_product_attribute(self):
        with self.env.cr.savepoint():
            self.env.cr.execute(
                """
                UPDATE product_attribute_value_product_template_attribute_line_rel AS rel
                SET product_attribute_value_id = %s
                FROM product_template_attribute_line AS attribute_line
                WHERE rel.product_template_attribute_line_id = attribute_line.id AND
                attribute_line.product_tmpl_id = %s AND
                attribute_line.attribute_id = %s AND
                rel.product_attribute_value_id = %s
                """,
                (
                    self.x_new_attribute_value_id.id,
                    self.x_active_template_id,
                    self.x_attribute_id.id,
                    self.x_old_attribute_value_id.id,
                ),
            )

            self.env.cr.execute(
                """
                UPDATE product_template_attribute_value
                SET product_attribute_value_id = %s
                WHERE product_attribute_value_id = %s AND
                product_tmpl_id = %s AND
                attribute_id = %s
                """,
                (
                    self.x_new_attribute_value_id.id,
                    self.x_old_attribute_value_id.id,
                    self.x_active_template_id,
                    self.x_attribute_id.id,
                ),
            )
