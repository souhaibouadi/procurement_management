# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementBidder(models.Model):
    _name = 'procurement.bidder'
    _description = 'Bidder'

    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    partner_id = fields.Many2one('res.partner', string="Bidder", required=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    tax_id_number = fields.Char(string="Tax Identification Number (NIF)")
    legal_form = fields.Selection([
        ('sarl', 'SARL'), ('eurl', 'EURL'), ('spa', 'SPA'),
        ('snc', 'SNC'), ('individual', 'Individual'), ('other', 'Other'),
    ], string="Legal Form")
    envelope_number = fields.Integer(string="Envelope Number")
    bid_amount_excl_tax = fields.Float(string="Bid Amount Excl. Tax (DZD)")
    bid_amount_incl_tax = fields.Float(string="Bid Amount Incl. Tax (DZD)")
    corrected_amount_incl_tax = fields.Float(string="Corrected Amount Incl. Tax (DZD)")
    technical_score = fields.Float(string="Technical Score")
    financial_score = fields.Float(string="Financial Score")
    total_score = fields.Float(string="Total Score", compute='_compute_total_score', store=True)
    ranking = fields.Integer(string="Ranking")
    passed_preliminary = fields.Boolean(string="Passed Preliminary Examination")
    exclusion_reason = fields.Text(string="Exclusion Reason")
    excluded_over_budget = fields.Boolean(string="Excluded (Amount Exceeds Allocated Budget)")
    proposed_delay = fields.Char(string="Proposed Delay", help="e.g. 07 days")
    bidder_state = fields.Selection([
        ('submitted', 'Bid Submitted'),
        ('eligible', 'Eligible'),
        ('excluded', 'Excluded'),
        ('retained', 'Retained'),
        ('provisional_awardee', 'Provisional Awardee'),
        ('final_awardee', 'Final Awardee'),
    ], string="Bidder Status")

    @api.depends('technical_score', 'financial_score')
    def _compute_total_score(self):
        for rec in self:
            rec.total_score = rec.technical_score + rec.financial_score


    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('qualified', 'Qualified'),
        ('awarded', 'Awarded'),
        ('rejected', 'Rejected'),
    ], string="State", default='draft')
    registration_date = fields.Date(string="Registration Date")
    bid_amount = fields.Float(string="Bid Amount")
    discount_percentage = fields.Float(string="Discount Percentage")
    final_amount = fields.Float(string="Final Amount")
    document_ids = fields.Many2many('ir.attachment', string="Documents")
    notes = fields.Text(string="Notes")
