# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json


class ProcurementPortalController(http.Controller):
    
    @http.route('/procurement/procedures', type='http', auth='user', website=True)
    def procurement_procedures(self, **kw):
        """Display list of procurement procedures for portal users."""
        procedures = request.env['procurement.procedure'].sudo().search([
            ('state', 'in', ['published', 'open', 'evaluation', 'awarded'])
        ])
        return request.render('procurement_management.portal_procedures', {
            'procedures': procedures,
        })
    
    @http.route('/procurement/procedure/<int:procedure_id>', type='http', auth='user', website=True)
    def procurement_procedure_detail(self, procedure_id, **kw):
        """Display detail of a procurement procedure."""
        procedure = request.env['procurement.procedure'].sudo().browse(procedure_id)
        if not procedure.exists():
            return request.not_found()
        return request.render('procurement_management.portal_procedure_detail', {
            'procedure': procedure,
        })
    
    @http.route('/procurement/notices', type='http', auth='public', website=True)
    def procurement_notices(self, **kw):
        """Display list of public procurement notices."""
        notices = request.env['procurement.notice'].sudo().search([
            ('state', '=', 'published')
        ])
        return request.render('procurement_management.portal_notices', {
            'notices': notices,
        })


class ProcurementAPIController(http.Controller):
    
    @http.route('/api/procurement/procedures', type='json', auth='user')
    def api_get_procedures(self, **kw):
        """API endpoint to get procurement procedures."""
        procedures = request.env['procurement.procedure'].search_read(
            [],
            ['name', 'reference', 'procedure_type', 'state', 'start_date', 'end_date']
        )
        return {'status': 'success', 'data': procedures}
    
    @http.route('/api/procurement/procedure/<int:procedure_id>', type='json', auth='user')
    def api_get_procedure(self, procedure_id, **kw):
        """API endpoint to get a specific procurement procedure."""
        procedure = request.env['procurement.procedure'].browse(procedure_id)
        if not procedure.exists():
            return {'status': 'error', 'message': 'Procedure not found'}
        return {
            'status': 'success',
            'data': {
                'id': procedure.id,
                'name': procedure.name,
                'reference': procedure.reference,
                'procedure_type': procedure.procedure_type,
                'state': procedure.state,
                'start_date': str(procedure.start_date) if procedure.start_date else None,
                'end_date': str(procedure.end_date) if procedure.end_date else None,
            }
        }
    
    @http.route('/api/procurement/statistics', type='json', auth='user')
    def api_get_statistics(self, **kw):
        """API endpoint to get procurement statistics."""
        Procedure = request.env['procurement.procedure']
        return {
            'status': 'success',
            'data': {
                'total_procedures': Procedure.search_count([]),
                'draft_procedures': Procedure.search_count([('state', '=', 'draft')]),
                'published_procedures': Procedure.search_count([('state', '=', 'published')]),
                'open_procedures': Procedure.search_count([('state', '=', 'open')]),
                'awarded_procedures': Procedure.search_count([('state', '=', 'awarded')]),
            }
        }
