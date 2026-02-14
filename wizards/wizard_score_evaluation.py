# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class WizardScoreEvaluation(models.TransientModel):
    _name = 'procurement.wizard.score.evaluation'
    _description = 'Score Evaluation Wizard'

    evaluation_id = fields.Many2one(
        'procurement.evaluation',
        string='Evaluation',
        required=True,
        default=lambda self: self.env.context.get('active_id')
    )
    evaluation_type = fields.Selection(
        related='evaluation_id.evaluation_type',
        string='Evaluation Type',
        readonly=True
    )
    procedure_id = fields.Many2one(
        related='evaluation_id.procedure_id',
        string='Procedure',
        readonly=True
    )
    auto_calculate = fields.Boolean(
        string='Auto Calculate',
        default=True,
        help='Automatically calculate scores based on criteria'
    )
    apply_weights = fields.Boolean(
        string='Apply Weights',
        default=True,
        help='Apply criteria weights in score calculation'
    )
    recalculate_existing = fields.Boolean(
        string='Recalculate Existing',
        default=False,
        help='Recalculate scores for bidders with existing scores'
    )
    bidder_ids = fields.One2many(
        'procurement.wizard.score.evaluation.line',
        'wizard_id',
        string='Bidders',
        compute='_compute_bidder_ids',
        store=True,
        readonly=False
    )
    criterion_ids = fields.One2many(
        related='evaluation_id.criterion_ids',
        string='Criteria'
    )
    total_bidders = fields.Integer(
        string='Total Bidders',
        compute='_compute_statistics'
    )
    qualified_bidders = fields.Integer(
        string='Qualified',
        compute='_compute_statistics'
    )
    disqualified_bidders = fields.Integer(
        string='Disqualified',
        compute='_compute_statistics'
    )
    highest_score = fields.Float(
        string='Highest Score',
        compute='_compute_statistics'
    )
    lowest_score = fields.Float(
        string='Lowest Score',
        compute='_compute_statistics'
    )
    average_score = fields.Float(
        string='Average Score',
        compute='_compute_statistics'
    )

    @api.depends('evaluation_id')
    def _compute_bidder_ids(self):
        for wizard in self:
            lines = []
            if wizard.evaluation_id:
                for bidder in wizard.evaluation_id.bidder_ids:
                    lines.append((0, 0, {
                        'bidder_id': bidder.id,
                        'technical_score': bidder.technical_score,
                        'financial_score': bidder.financial_score,
                    }))
            wizard.bidder_ids = lines

    @api.depends('bidder_ids', 'bidder_ids.combined_score', 'bidder_ids.is_selected')
    def _compute_statistics(self):
        for wizard in self:
            bidders = wizard.bidder_ids
            wizard.total_bidders = len(bidders)
            wizard.qualified_bidders = len(bidders.filtered('is_selected'))
            wizard.disqualified_bidders = wizard.total_bidders - wizard.qualified_bidders
            scores = bidders.mapped('combined_score')
            wizard.highest_score = max(scores) if scores else 0.0
            wizard.lowest_score = min(scores) if scores else 0.0
            wizard.average_score = sum(scores) / len(scores) if scores else 0.0

    def action_calculate_scores(self):
        self.ensure_one()
        for line in self.bidder_ids:
            if self.apply_weights:
                line.combined_score = (line.technical_score * 0.7) + (line.financial_score * 0.3)
            else:
                line.combined_score = (line.technical_score + line.financial_score) / 2
        
        # Update ranks
        sorted_lines = self.bidder_ids.sorted(key=lambda x: x.combined_score, reverse=True)
        for rank, line in enumerate(sorted_lines, 1):
            line.rank = rank
        
        return {'type': 'ir.actions.act_window_close'}

    def action_apply_selection(self):
        self.ensure_one()
        for line in self.bidder_ids:
            if line.bidder_id:
                line.bidder_id.write({
                    'technical_score': line.technical_score,
                    'financial_score': line.financial_score,
                    'is_qualified': line.is_selected,
                })
        return {'type': 'ir.actions.act_window_close'}


class WizardScoreEvaluationLine(models.TransientModel):
    _name = 'procurement.wizard.score.evaluation.line'
    _description = 'Score Evaluation Wizard Line'

    wizard_id = fields.Many2one(
        'procurement.wizard.score.evaluation',
        string='Wizard',
        ondelete='cascade'
    )
    bidder_id = fields.Many2one(
        'procurement.bidder',
        string='Bidder',
        required=True
    )
    technical_score = fields.Float(
        string='Technical Score',
        default=0.0
    )
    financial_score = fields.Float(
        string='Financial Score',
        default=0.0
    )
    combined_score = fields.Float(
        string='Combined Score',
        default=0.0
    )
    rank = fields.Integer(
        string='Rank',
        default=0
    )
    is_selected = fields.Boolean(
        string='Selected',
        default=False
    )
