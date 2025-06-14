# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

LOAN_STATE = [
    ('draft', 'Borrador'),
    ('approved', 'Aprobado'),
    ('paid', 'Pagado'),
    ('cancelled', 'Cancelado')
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
        # store=True,
        help="Porcentaje del total que representan las líneas del préstamo")
    interest_rate = fields.Float(
        string='Porcentaje de interés (%)',
        help='Porcentaje de interés aplicado al monto del préstamo')
    interest_amount = fields.Monetary(
        string='Monto del interés',
        compute='_compute_interest',
        # store=True,
        currency_field='currency_id',
        help='Interés calculado sobre el monto del préstamo')
    total_with_interest = fields.Monetary(
        string='Total con interés',
        compute='_compute_interest',
        # store=True,
        currency_field='currency_id',
        help='Suma del monto del préstamo y el interés calculado')
    apply_interest = fields.Boolean(string='Aplicar Intereses', default=False)

    
    @api.depends('amount_loan', 'interest_rate')
    def _compute_interest(self):
        for record in self:
            if record.amount_loan and record.interest_rate:
                record.interest_amount = (record.amount_loan * record.interest_rate) / 100
                record.total_with_interest = record.amount_loan + record.interest_amount
            else:
                record.interest_amount = 0.0
                record.total_with_interest = record.amount_loan or 0.0

    
    def validate_loan(self):
        for record in self:
            record.state = 'approved'

    def payd_loan(self):
        for record in self:
            record.state = 'paid'


    def cancel_loan(self):
        for record in self:
            record.state = 'cancelled'


    def draft_loan(self):
        for record in self:
            record.state = 'draft'

    @api.depends('loan_line.amount', 'amount_total', 'amount_loan', 'interest_rate', 'apply_interest')
    def _compute_percentage_lines(self):
        for record in self:
            if record.amount_loan:  # evita división por cero
                if record.apply_interest:
                    record.percentage_lines = (record.amount_total / record.total_with_interest) * 100
                else:
                    record.percentage_lines = (record.amount_total / record.amount_loan) * 100
            else:
                record.percentage_lines = 0.0

    
    @api.depends('loan_line.amount')
    def _compute_amounts(self):
        for loan in self:
            total = sum(loan.loan_line.mapped('amount'))
            # Determinar el máximo permitido
            max_allowed = loan.total_with_interest if loan.apply_interest else loan.amount_loan

            # Validación: no se puede pasar del monto permitido
            if total > max_allowed:
                raise ValidationError(
                    'La suma de los pagos (%.2f) no puede ser mayor al monto del préstamo (%.2f).' %
                    (total, max_allowed)
                )

            loan.amount_total = total

    
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
