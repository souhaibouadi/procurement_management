# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Procurement Reference Fields
    procurement_procedure_id = fields.Many2one(
        'procurement.procedure', string="Linked Procurement Procedure")
    procurement_award_id = fields.Many2one(
        'procurement.award', string="Linked Procurement Award")
    procurement_service_order_id = fields.Many2one(
        'procurement.service.order', string="Linked Service Order")
    
    # Contract Information
    procurement_contract_number = fields.Char(string="Contract Number")
    procurement_contract_date = fields.Date(string="Contract Date")
    is_public_procurement = fields.Boolean(
        string="Is Public Procurement", default=False,
        help="Check if this purchase order is part of a public procurement process")
