# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# Copyright (C) 2019-Today: Druidoo (<https://www.druidoo.io>)
# @author: La Louve
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api, _
from odoo.exceptions import Warning


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def write(self, vals):
        if "available_in_pos" in vals and not vals["available_in_pos"]:
            self.check_pos_session_running()
        return super(ProductTemplate, self).write(vals)

    @api.multi
    def check_pos_session_running(self):
        pos_sessions = self.env["pos.session"].search(
            [("state", "in", ["opening_control", "opened"])]
        )
        if pos_sessions:
            raise Warning(_(
                "You cannot untick Available in the Point of Sale "
                "When POS Session are running.\n"
                "IDs: %s") % pos_sessions.ids)
        return True
