from odoo import http
from odoo.http import request


class Main(http.Controller):

    @http.route('/loan/new', type='http', auth='public', website=True)
    def loan_form(self, **kw):
        partners = request.env['res.partner'].sudo().search([])
        currencies = request.env['res.currency'].sudo().search([])

        return request.render('mod_bank_loan.partner_loan_form', {
            'partners': partners,
            'currencies': currencies
        })


    # @http.route('/mod_bank_loan/objects', type='http', auth='public')
    # def list(self, **kw):
    #     return http.request.render(
    #         'mod_bank_loan.listing',
    #         {
    #             'root': '/mod_bank_loan',
    #             'objects': http.request.env['main'].search([]),
    #         },
    #     )

    # @http.route('/mod_bank_loan/objects/<model("main"):obj>', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('mod_bank_loan.object', {'object': obj})