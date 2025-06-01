# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class PartnerLoanLine(models.Model):
    _name = 'partner.loan.line'
    _description = 'Líneas de préstamos'

    name = fields.Char('Name', default='Pago')
    payment_date = fields.Date('Día de Pago')
    amount = fields.Float('Monto')
    loan_id = fields.Many2one(
        comodel_name='partner.loan',
        string='Préstamo',
        required=True, 
        ondelete='cascade', 
        index=True, 
        copy=False)