# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_loan_count = fields.Integer(compute='_compute_loan_count_count', string='Conteo de Préstamos')
