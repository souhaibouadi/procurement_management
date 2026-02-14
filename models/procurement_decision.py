# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementDecision(models.Model):
    _name = 'procurement.decision'
    _description = 'Committee Decision'

    name = fields.Char(string="Reference", help="e.g. Decision NXXX/CM/YYYY")
    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    committee_id = fields.Many2one('procurement.committee', string="Committee")
    decision_type = fields.Selection([
        ('specs_approval', 'Specifications Approval'),
        ('contract_approval', 'Contract Approval'),
        ('amendment_approval', 'Amendment Approval'),
        ('award', 'Award'),
        ('closure', 'Closure'),
        ('unsuccessful_declaration', 'Unsuccessful Declaration'),
        ('cancellation', 'Cancellation'),
    ], string="Decision Type")
    legal_references = fields.Text(string="Legal References", help="Considering decree..., Considering law..., Considering ministerial decision...")
    appointment_decision_ref = fields.Char(string="Ministerial Appointment Decision Reference")
    reporter_id = fields.Many2one('res.partner', string="Reporter")
    session_reference = fields.Char(string="Session Reference", help="e.g. n06/2025 of 25/12/2025")
    minutes_reference = fields.Char(string="Minutes Reference")
    decision_body = fields.Text(string="Decision Body - Articles")
    decision_date = fields.Date(string="Decision Date", required=True)
    effective_date = fields.Date(string="Effective Date")
    signatory_id = fields.Many2one('res.partner', string="Signatory (President/Vice-President)")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('signed', 'Signed'),
        ('notified', 'Notified'),
    ], string="Status", default='draft')

    def action_approve(self):
        """Approve the decision"""
        self.write({'state': 'approved'})
