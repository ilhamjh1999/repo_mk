# -*- coding: utf-8 -*-
from odoo import http

# class FitsDailyReport/(http.Controller):
#     @http.route('/fits_daily_report//fits_daily_report//', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fits_daily_report//fits_daily_report//objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fits_daily_report/.listing', {
#             'root': '/fits_daily_report//fits_daily_report/',
#             'objects': http.request.env['fits_daily_report/.fits_daily_report/'].search([]),
#         })

#     @http.route('/fits_daily_report//fits_daily_report//objects/<model("fits_daily_report/.fits_daily_report/"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fits_daily_report/.object', {
#             'object': obj
#         })