# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementDocument(models.Model):
    _name = 'procurement.document'
    _description = 'Procurement Document'

    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    document_type = fields.Selection([
        ('specs', 'Specifications (Tender Documents)'),
        ('specs_corrected', 'Corrected Specifications'),
        ('specs_approved', 'Approved Specifications'),
        ('admin_estimate', 'Administrative Estimate'),
        ('needs_sheet', 'Needs Sheet'),
        ('proforma', 'Quotation / Pro Forma Invoice'),
        ('consultation_letter', 'Consultation Letter'),
        ('posting_letter', 'Posting Letter'),
        ('transmittal', 'Transmittal Slip'),
        ('purchase_order', 'Purchase Order'),
        ('contract', 'Contract'),
        ('draft_contract', 'Draft Contract'),
        ('approved_contract', 'Approved Contract'),
        ('retention_letter', 'Retention Letter'),
        ('thanks_letter', 'Thank You Letter'),
        ('control_sheet', 'Product/Service Control Sheet'),
        ('receipt_note', 'Receipt Note'),
        ('performance_bond', 'Performance Bond'),
        ('amendment', 'Amendment'),
        ('final_statement', 'General and Final Statement'),
        ('other', 'Other'),
    ], string="Document Type")
    name = fields.Char(string="Document Name")
    document_reference = fields.Char(string="Document Reference", help="e.g. ER08.PR.02.MPR/A1")
    document_date = fields.Date(string="Document Date")
    attachment_ids = fields.Many2many('ir.attachment', string="File Attachments")
    notes = fields.Text(string="Notes")
