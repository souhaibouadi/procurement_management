# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementAnalyticalSheet(models.Model):
    _name = 'procurement.analytical.sheet'
    _description = 'Analytical Sheet for Award'

    name = fields.Char(string="Reference", required=True, copy=False, readonly=True, default='New')

    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    committee_session_ref = fields.Char(string="Market Committee Session No.", help="e.g. Committee n06/2025")
    session_date = fields.Date(string="Session Date")
    reference_documents = fields.Text(string="Reference Documents", help="Draft contract, opening minutes, evaluation minutes, estimate, award notice")
    contracting_authority = fields.Char(string="Contracting Authority")
    contractor_partner_id = fields.Many2one('res.partner', string="Contractor Partner")
    contract_subject = fields.Text(string="Contract Subject")
    procurement_method = fields.Text(string="Procurement Method")
    legal_basis = fields.Text(string="Applicable Legal References")
    amount_excl_tax = fields.Float(string="Amount Excl. Tax (DZD)")
    amount_excl_tax_words = fields.Char(string="Amount Excl. Tax in Words")
    amount_incl_tax = fields.Float(string="Amount Incl. Tax (DZD)")
    amount_incl_tax_words = fields.Char(string="Amount Incl. Tax in Words")
    specs_approval_ref = fields.Char(string="Specifications Approval Decision Ref.")
    specs_approval_date = fields.Date(string="Specifications Approval Date")
    publication_journals = fields.Text(string="Publication Journals and Dates")
    preparation_days = fields.Integer(string="Offer Preparation Duration")
    specs_withdrawn_count = fields.Integer(string="Number of Specs Withdrawn")
    envelopes_received_count = fields.Integer(string="Number of Envelopes Received")
    envelopes_detail = fields.Text(string="Envelope Details", help="e.g. Envelope 1: SARL X, Envelope 2: EURL Y...")
    allocated_budget = fields.Float(string="Allocated Budget (DZD)")
    administrative_estimate = fields.Float(string="Administrative Estimate (DZD)")
    preliminary_exam_result = fields.Text(string="Preliminary Examination Result")
    retained_bidders = fields.Text(string="Retained Bidders")
    excluded_bidders = fields.Text(string="Excluded Bidders and Reasons")
    final_ranking = fields.Text(string="Final Ranking")
    provisional_awardee_id = fields.Many2one('procurement.bidder', string="Provisional Awardee")
    notes = fields.Text(string="Notes")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validated', 'Validated'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='draft')

    def action_draft(self):
        """Reset to draft state"""
        self.write({'state': 'draft'})

    def action_validate(self):
        """Validate the analytical sheet"""
        self.write({'state': 'validated'})

    def action_approve(self):
        """Approve the analytical sheet"""
        self.write({'state': 'approved'})

    def action_cancel(self):
        """Cancel the analytical sheet"""
        self.write({'state': 'cancelled'})
