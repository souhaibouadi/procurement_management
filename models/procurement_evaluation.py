# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementEvaluation(models.Model):
    _name = 'procurement.evaluation'
    _description = 'Bid Evaluation'

    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    committee_id = fields.Many2one('procurement.committee', string="Committee")
    evaluation_type = fields.Selection([
        ('preliminary', 'Preliminary Examination'),
        ('technical', 'Technical Evaluation'),
        ('financial', 'Financial Evaluation'),
    ], string="Evaluation Type")
    criterion_ids = fields.One2many('procurement.evaluation.criterion', 'evaluation_id', string="Criteria")
    score_ids = fields.One2many('procurement.evaluation.score', 'evaluation_id', string="Scores")
    minutes_id = fields.Many2one('procurement.minutes', string="Minutes")
    evaluation_date = fields.Date(string="Evaluation Date")
    notes = fields.Text(string="Notes")
        name = fields.Char(string="Evaluation Name", required=True)
    bidder_id = fields.Many2one('procurement.bidder', string="Bidder")
    technical_score = fields.Float(string="Technical Score")
    financial_score = fields.Float(string="Financial Score")
    total_score = fields.Float(string="Total Score")
    rank = fields.Integer(string="Rank")
    technical_notes = fields.Text(string="Technical Notes")
    financial_notes = fields.Text(string="Financial Notes")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validated', 'Validated'),
    ], string="State", default='draft')

    def action_validate(self):
        """Validate the evaluation"""
        self.write({'state': 'validated'})


class ProcurementEvaluationCriterion(models.Model):
    _name = 'procurement.evaluation.criterion'
    _description = 'Evaluation Criterion'
    _order = 'sequence'

    evaluation_id = fields.Many2one('procurement.evaluation', string="Evaluation")
    criterion_name = fields.Char(string="Criterion Name", required=True)
    description = fields.Text(string="Description and Scoring Formula")
    max_score = fields.Float(string="Maximum Score")
    sequence = fields.Integer(string="Order")


class ProcurementEvaluationScore(models.Model):
    _name = 'procurement.evaluation.score'
    _description = 'Evaluation Score'

    evaluation_id = fields.Many2one('procurement.evaluation', string="Evaluation")
    bidder_id = fields.Many2one('procurement.bidder', string="Bidder")
    criterion_id = fields.Many2one('procurement.evaluation.criterion', string="Criterion")
    proposed_value = fields.Char(string="Value Proposed by Bidder")
    score = fields.Float(string="Score Obtained")
