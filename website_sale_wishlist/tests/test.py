# -*- coding: utf-8 -*-
# © 2021 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import SavepointCase


class Test(SavepointCase):
    def setUp(self):
        super(Test, self).setUp()
        self.prd = self.env.ref("product.product_product_5b")

    def test_whishlist_item_unpublished(self):
        wishlist = self.feed_wishlist_item()
        item = self.env["wishlist.item"].search(
            [
                ("wishlist_id", "=", wishlist.id),
                ("product_id", "=", self.prd.id),
                "|",
                ("active", "=", True),
                ("active", "=", False),
            ],
            limit=1,
        )
        assert item.active is True
        self.prd.write({"website_published": False})
        assert item.active is False
        self.prd.write({"website_published": True})
        assert item.active is True

    def feed_wishlist_item(self):
        user = self.env["res.users"].create(
            {
                "name": "wishlist_user",
                "login": "wishlist_user",
                "groups_id": [(4, self.env.ref("base.group_portal").id)],
            }
        )
        wishl = self.env["wishlist"].create({"user_id": user.id})
        self.env["wishlist.item"].create(
            {
                "wishlist_id": wishl.id,
                "product_id": self.prd.id,
            }
        )
        return wishl
