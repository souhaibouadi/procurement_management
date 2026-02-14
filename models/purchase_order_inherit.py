# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    procurement_procedure_id = fields.Many2one(
        'procurement.procedure', string="Linked Procurement Procedure")
