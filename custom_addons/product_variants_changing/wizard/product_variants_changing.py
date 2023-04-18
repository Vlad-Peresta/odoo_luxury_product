from odoo import models, fields, api


class ProductVariantsChanging(models.TransientModel):
    _name = "product.variants.changing"
    _description = "Change attributes of the product"

    def _get_x_attribute_id_domain(self):
        return [
            (
                "id",
                "in",
                self.env["product.template"]
                .browse(self.env.context.get("active_id"))
                .attribute_line_ids.attribute_id.ids,
            )
        ]

    x_allowed_value_ids = fields.Many2many(
        "product.attribute.value", compute="_compute_x_allowed_value"
    )
    x_attribute_id = fields.Many2one(
        "product.attribute",
        string="Product variant",
        required=True,
        domain=_get_x_attribute_id_domain
    )
    x_old_attribute_value_id = fields.Many2one(
        "product.attribute.value",
        string="Old product variant",
        required=True,
        domain="[('id', 'in', x_allowed_value_ids)]"
    )
    x_new_attribute_value_id = fields.Many2one(
        "product.attribute.value",
        string="New product variant",
        required=True,
        domain="[('attribute_id', '=', x_attribute_id), ('id', '!=', x_old_attribute_value_id),]"
    )

    @api.depends("x_attribute_id")
    def _compute_x_allowed_value(self):
        self.x_allowed_value_ids = self.env["product.attribute.value"].search(
            [
                (
                    "id",
                    "in",
                    self.env["product.template"]
                    .browse(self.env.context.get("active_id"))
                    .attribute_line_ids.value_ids.ids,
                ),
                ("attribute_id.id", "=", self.x_attribute_id.id),
            ]
        )

    @api.onchange("x_attribute_id")
    def _onchange_x_old_new_attribute_value_id(self):
        self.x_old_attribute_value_id = False
        self.x_new_attribute_value_id = False

    @api.onchange("x_old_attribute_value_id")
    def _onchange_x_new_attribute_value_id(self):
        self.x_new_attribute_value_id = False

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
                    self.env.context.get("active_id"),
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
                    self.env.context.get("active_id"),
                    self.x_attribute_id.id,
                ),
            )
