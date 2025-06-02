# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

LOAN_STATE = [
    ('draft', "Borrador"),
    ('done', "Préstamo"),
    ('cancel', "Cancelado"),
]


class PartnerLoan(models.Model):
    _name = 'partner.loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Préstamos para los contactos'

    name = fields.Char(
        string='Nombre',
        required=True, copy=False, readonly=False,
        default=lambda self: _('New')
        )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Cliente",
        required=True, change_default=True, index=True,
        tracking=1
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
    amount_total = fields.Monetary(string="Total", store=True, compute='_compute_amounts', tracking=4)
    note = fields.Html(string="Términos y condiciones")
    state = fields.Selection(
        selection=LOAN_STATE,
        string="Estado",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')
    percentage_lines = fields.Float(
        string='Porcentaje pagado',
        compute='_compute_percentage_lines',
        store=True,
        help="Porcentaje del total que representan las líneas del préstamo")


    @api.depends('loan_line.amount', 'amount_total', 'amount_loan')
    def _compute_percentage_lines(self):
        for record in self:
            if record.amount_loan:  # evita división por cero
                record.percentage_lines = (record.amount_total / record.amount_loan) * 100
            else:
                record.percentage_lines = 0.0
        # for record in self:
        #     record.percentage_lines = (record.amount_total / record.amount_loan) * 100
    
    

    
    @api.depends('loan_line.amount')
    def _compute_amounts(self):
        for loan in self:
            loan.amount_total = sum(loan.loan_line.mapped('amount'))

    
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
