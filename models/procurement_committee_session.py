# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementCommitteeSession(models.Model):
    _name = 'procurement.committee.session'
    _description = 'Committee Session'

    name = fields.Char(string="Session Number", help="e.g. Session N01/2026")
    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    committee_id = fields.Many2one('procurement.committee', string="Committee")
    session_date = fields.Datetime(string="Session Date & Time", required=True)
    location = fields.Char(string="Meeting Location")
    session_type = fields.Selection([('envelope_opening', 'Envelope Opening'), ('evaluation', 'Evaluation'), ('award', 'Award'), ('other', 'Other')], string="Session Type")
    agenda_item_ids = fields.One2many('procurement.session.agenda', 'session_id', string="Agenda Items")
    summons_ids = fields.One2many('procurement.summons', 'session_id', string="Summons")
    minutes_id = fields.Many2one('procurement.minutes', string="Session Minutes")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('summoned', 'Summoned'),
        ('held', 'Held'),
        ('closed', 'Closed'),
    ], string="Status", default='draft')

    def action_summon(self):
        """Send summons to committee members"""
        self.write({'state': 'summoned'})

    def action_hold(self):
        """Mark session as held"""
        self.write({'state': 'held'})

    def action_close(self):
        """Close the session"""
        self.write({'state': 'closed'})


class ProcurementSessionAgenda(models.Model):
    _name = 'procurement.session.agenda'
    _description = 'Session Agenda Item'
    _order = 'sequence'

    session_id = fields.Many2one('procurement.committee.session', string="Session")
    sequence = fields.Integer(string="Order Number")
    description = fields.Text(string="Agenda Item Description")
    reporter_id = fields.Many2one('res.partner', string="Item Reporter")
    linked_procedure_id = fields.Many2one('procurement.procedure', string="Linked Procedure")
