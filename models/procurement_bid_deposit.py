# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementBidDeposit(models.Model):
    _name = 'procurement.bid.deposit'
    _description = 'Bid Deposit Register'
    _order = 'sequence'

    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    sequence = fields.Integer(string="Order Number")
    bidder_id = fields.Many2one('procurement.bidder', string="Bidder")
    deposit_date = fields.Date(string="Deposit Date", required=True)
    deposit_time = fields.Char(string="Deposit Time", required=True)
    within_deadline = fields.Boolean(string="Submitted Within Regulatory Deadline", compute='_compute_within_deadline', store=True)
    envelope_count = fields.Integer(string="Number of Envelopes")
    envelope_contents = fields.Text(string="Contents (Candidacy + Technical + Financial)")
    notes = fields.Text(string="Notes")

    @api.depends('deposit_date', 'deposit_time', 'procedure_id.submission_deadline')
    def _compute_within_deadline(self):
        for rec in self:
            if rec.procedure_id.submission_deadline and rec.deposit_date:
                deadline_date = rec.procedure_id.submission_deadline.date()
                rec.within_deadline = rec.deposit_date <= deadline_date
            else:
                rec.within_deadline = True
