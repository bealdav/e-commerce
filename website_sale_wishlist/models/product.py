# -*- coding: utf-8 -*-
# © 2021 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def write(self, vals):
        if "website_published" in vals:
            publ = vals.get("website_published")
            prd = self.env["product.product"].search(
                [("product_tmpl_id", "in", self.ids)]
            )
            if publ:
                items = self.env["wishlist.item"].search(
                    [("product_id", "in", prd.ids), ("active", "=", False)]
                )
            else:
                items = self.env["wishlist.item"].search(
                    [("product_id", "in", prd.ids)]
                )
            items.write({"active": publ})
        return super(ProductTemplate, self).write(vals)
