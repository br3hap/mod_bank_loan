# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_loan_count = fields.Integer(compute='_compute_loan_count_count', string='Conteo de Préstamos')


    @api.model
    def _get_loan_domain_count(self):
        return []


    def _compute_loan_count_count(self):
        all_partners = self.with_context(active_test=False).search_fetch(
            [('id', 'child_of', self.ids)],
            ['parent_id'],
        )

        loan_groups = self.env['partner.loan']._read_group(
            domain=expression.AND([self._get_loan_domain_count(), [('partner_id', 'in', all_partners.ids)]]),
            groupby=['partner_id'], aggregates=['__count']
        )
        
        self_ids = set(self._ids)

        self.partner_loan_count = 0
        for partner, count in loan_groups:
            while partner:
                if partner.id in self_ids:
                    partner.partner_loan_count += count
                partner = partner.parent_id



    def action_view_partner_loan(self):
        action = self.env['ir.actions.act_window']._for_xml_id('mod_bank_loan.act_res_partner_2_loan')
        all_child = self.with_context(active_test=False).search([('id', 'child_of', self.ids)])
        action["domain"] = [("partner_id", "in", all_child.ids)]
        return action
