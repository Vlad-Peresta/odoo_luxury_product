from odoo import models, fields


class Picking(models.Model):
    _inherit = "stock.picking"

    vip_tag = fields.Char(compute="_compute_vip_tag")

    def _compute_vip_tag(self):
        PartnerCategory = self.env["res.partner.category"]
        for picking in self:
            picking.vip_tag = PartnerCategory.search(
                [("name", "=", "VIP")], limit=1
            ).name

    def _get_vip_tag(self):
        PartnerCategory = self.env["res.partner.category"]
        vip_tag = PartnerCategory.search([("name", "=", "VIP")], limit=1)

        if vip_tag.exists():
            return vip_tag
        return PartnerCategory.create({"name": "VIP"})

    def button_validate(self):
        for picking in self:
            if (
                picking._is_to_external_location()
                and "VIP" not in picking.partner_id.category_id
            ):
                for move in picking.move_ids_without_package:
                    if move.product_id.product_tmpl_id.is_luxury_product:
                        picking.partner_id.category_id = [(4, self._get_vip_tag().id)]

        return super().button_validate()
