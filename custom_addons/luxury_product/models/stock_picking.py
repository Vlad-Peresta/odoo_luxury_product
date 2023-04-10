from odoo import models


class Picking(models.Model):
    _inherit = "stock.picking"

    def _get_vip_tag(self):
        PartnerCategory = self.env["res.partner.category"]
        vip_tag = PartnerCategory.search([("name", "=", "VIP")], limit=1)

        return vip_tag if vip_tag else PartnerCategory.create({"name": "VIP"})

    def button_validate(self):
        for picking in self.filtered(
            lambda picking_id: picking_id._is_to_external_location()
            and "VIP" not in picking_id.partner_id.category_id.mapped("name")
        ):
            if picking.move_ids_without_package.filtered(
                lambda move: move.product_id.product_tmpl_id.x_is_luxury_product
            ):
                picking.partner_id.category_id = [(4, self._get_vip_tag().id)]

        return super().button_validate()
