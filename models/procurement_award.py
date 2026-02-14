# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta


class ProcurementAward(models.Model):
    _name = 'procurement.award'
    _description = 'Procurement Award'

    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    award_type = fields.Selection([
        ('provisional', 'Provisional Award'),
        ('final', 'Final Award'),
    ], string="Award Type")
    bidder_id = fields.Many2one('procurement.bidder', string="Awardee")
    designation = fields.Text(string="Market Designation")
    award_amount_excl_tax = fields.Float(string="Award Amount Excl. Tax (DZD)")
    award_amount_incl_tax = fields.Float(string="Award Amount Incl. Tax (DZD)")
    obtained_score = fields.Float(string="Score Obtained")
    execution_delay = fields.Char(string="Execution / Activation Delay")
    ranking_label = fields.Char(string="Ranking", default="1st")
    award_date = fields.Date(string="Award Date")
    appeal_start_date = fields.Date(string="Appeal Period Start Date")
    appeal_end_date = fields.Date(string="Appeal Period End Date", compute='_compute_appeal_end_date', store=True)
    appeal_ids = fields.One2many('procurement.appeal', 'award_id', string="Appeals")
    notice_id = fields.Many2one('procurement.notice', string="Linked Award Notice")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('published', 'Published'),
        ('appeal', 'Under Appeal'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='draft')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    @api.depends('appeal_start_date')
    def _compute_appeal_end_date(self):
        for rec in self:
            if rec.appeal_start_date:
                rec.appeal_end_date = rec.appeal_start_date + timedelta(days=10)
            else:
                rec.appeal_end_date = False

    def action_confirm(self):
        """Confirm the award"""
        self.write({'state': 'confirmed'})

    def action_publish(self):
        """Publish the award"""
        self.write({'state': 'published'})


class ProcurementAppeal(models.Model):
    _name = 'procurement.appeal'
    _description = 'Award Appeal'

    award_id = fields.Many2one('procurement.award', string="Award")
    bidder_id = fields.Many2one('procurement.bidder', string="Appellant")
    appeal_date = fields.Date(string="Appeal Date")
    grounds = fields.Text(string="Appeal Grounds")
    appeal_decision = fields.Text(string="Appeal Decision")
    state = fields.Selection([
        ('received', 'Received'),
        ('examined', 'Examined'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], string="Status", default='received')
