from odoo import http
from odoo.http import request


class Main(http.Controller):

    @http.route('/loan/list', type='http', auth='public', website=True)
    def loan_form_list(self, **kw):
        loans = request.env['partner.loan'].sudo().search([])

        return request.render('mod_bank_loan.partner_loan_list', {
            'loans': loans,
        })


    @http.route('/loan/new', type='http', auth='public', website=True)
    def loan_form(self, **kw):
        partners = request.env['res.partner'].sudo().search([])
        currencies = request.env['res.currency'].sudo().search([])

        return request.render('mod_bank_loan.partner_loan_form', {
            'partners': partners,
            'currencies': currencies
        })

    
    @http.route('/loan/submit', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def loan_submit(self, **post):
        try:
            request.env['partner.loan'].sudo().create({
                'partner_id': int(post.get('partner_id')),
                'date_loan': post.get('date_loan'),
                'amount_loan': float(post.get('amount_loan') or 0.0),
                'firts_date_payment': post.get('firts_date_payment'),
                'currency_id': int(post.get('currency_id')) if post.get('currency_id') else False,
                'note': post.get('note'),
                'interest_rate': float(post.get('interest_rate') or 0.0),
                'apply_interest': post.get('apply_interest') == 'on'
            })

            return request.redirect('/loan/thank-you')

        except Exception as e:
            return f"<h3>Error al crear el préstamo: {str(e)}</h3>"


    @http.route(['/loan/thank-you'], type='http', auth='public', website=True)
    def loan_thank_you(self, **kwargs):
        return request.render('mod_bank_loan.partner_loan_thank_you')