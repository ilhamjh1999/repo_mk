# -*- coding: utf-8 -*-
from odoo import http

# class FitsExtendMk(http.Controller):
#     @http.route('/fits_extend_mk/fits_extend_mk/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fits_extend_mk/fits_extend_mk/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fits_extend_mk.listing', {
#             'root': '/fits_extend_mk/fits_extend_mk',
#             'objects': http.request.env['fits_extend_mk.fits_extend_mk'].search([]),
#         })

#     @http.route('/fits_extend_mk/fits_extend_mk/objects/<model("fits_extend_mk.fits_extend_mk"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fits_extend_mk.object', {
#             'object': obj
#         })