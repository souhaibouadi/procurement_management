# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementMinutes(models.Model):
    _name = 'procurement.minutes'
    _description = 'Official Minutes (PV)'

    name = fields.Char(string="Reference")
    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    committee_id = fields.Many2one('procurement.committee', string="Committee")
    minutes_type = fields.Selection([
        ('specs_review', 'Specifications Review Minutes'),
        ('envelope_opening', 'Envelope Opening Minutes'),
        ('evaluation', 'Bid Evaluation Minutes'),
        ('committee_session', 'Market Committee Session Minutes'),
        ('provisional_acceptance', 'Provisional Acceptance Minutes'),
        ('final_acceptance', 'Final Acceptance Minutes'),
    ], string="Minutes Type")
    minutes_date = fields.Date(string="Minutes Date", required=True)
    content = fields.Html(string="Minutes Content")
    findings = fields.Text(string="Findings and Recommendations")
    reservations = fields.Text(string="Reservations Issued")
    attendee_ids = fields.Many2many('res.partner', 'procurement_minutes_attendee_rel', string="Attending Members")
    signatory_ids = fields.Many2many('res.partner', 'procurement_minutes_signatory_rel', string="Signatories")
    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")
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
        """Validate the minutes"""
        self.write({'state': 'validated'})

    def action_approve(self):
        """Approve the minutes"""
        self.write({'state': 'approved'})

    def action_cancel(self):
        """Cancel the minutes"""
        self.write({'state': 'cancelled'})
