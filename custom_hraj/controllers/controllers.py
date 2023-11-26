# -*- coding: utf-8 -*-
# from odoo import http


# class CustomHraj(http.Controller):
#     @http.route('/custom_hraj/custom_hraj', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_hraj/custom_hraj/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_hraj.listing', {
#             'root': '/custom_hraj/custom_hraj',
#             'objects': http.request.env['custom_hraj.custom_hraj'].search([]),
#         })

#     @http.route('/custom_hraj/custom_hraj/objects/<model("custom_hraj.custom_hraj"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_hraj.object', {
#             'object': obj
#         })
