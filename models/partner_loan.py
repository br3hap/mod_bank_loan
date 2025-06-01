# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class PartnerLoan(models.Model):
    _name = 'partner.loan'
    _description = 'Préstamos para los contactos'

    name = fields.Char(
        string='Nombre',
        required=True, copy=False, readonly=False,
        default=lambda self: _('New')
        )
    company_id = fields.Many2one(
        comodel_name='res.company',
        required=True, index=True,
        default=lambda self: self.env.company)
    date_loan = fields.Date(
        string='Fecha de préstamo',
        required=True, copy=False,
        default=fields.Datetime.now
        )
    amount_loan = fields.Float(string='Monto de préstamo')
    firts_date_payment = fields.Date(string='Primera fecha de pago')
    currency_id = fields.Many2one('res.currency', string='Moneda')
    loan_line = fields.One2many(
        comodel_name='partner.loan.line',
        inverse_name='loan_id',
        string='Líneas de préstamo',
        copy=False,
        auto_join=True
    )

    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['date_loan'])
                ) if 'date_loan' in vals else None
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'partner.loan', sequence_date=seq_date) or _("New")

        return super().create(vals_list)
