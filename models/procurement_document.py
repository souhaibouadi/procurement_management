# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementDocument(models.Model):
    _name = 'procurement.document'
    _description = 'Procurement Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']

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
    date = fields.Date(string="Date", default=fields.Date.context_today)
    document_date = fields.Date(string="Document Date")
    
    # Partner and tracking fields
    partner_id = fields.Many2one('res.partner', string="Partner")
    is_required = fields.Boolean(string="Required", default=False)
    is_received = fields.Boolean(string="Received", default=False)
    received_date = fields.Date(string="Received Date")
    
    # File attachments
    attachment_ids = fields.Many2many('ir.attachment', string="File Attachments")
    description = fields.Text(string="Description")
    notes = fields.Text(string="Notes")
    
    # Verification fields
    verified_by = fields.Many2one('res.users', string="Verified By")
    verification_date = fields.Date(string="Verification Date")
    is_valid = fields.Boolean(string="Valid", default=False)
    expiry_date = fields.Date(string="Expiry Date")
    verification_notes = fields.Text(string="Verification Notes")
