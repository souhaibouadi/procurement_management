# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementCommittee(models.Model):
    _name = 'procurement.committee'
    _description = 'Procurement Committee'

    name = fields.Char(string="Committee Name", required=True)
    committee_type = fields.Selection([
        ('specs_review', 'Specifications Review Committee - Central (C.E.C.C)'),
        ('regional_specs_review', 'Regional Specifications Review Committee (C.R.E.C.C)'),
        ('consultation_eval', 'Consultation Bid Opening & Evaluation Committee (CCOPEO2)'),
        ('tender_eval', 'Tender Bid Opening & Evaluation Committee (COPEO)'),
        ('market_committee', 'Public Procurement Committee (C.M.)'),
    ], string="Committee Type")
    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    president_id = fields.Many2one('res.partner', string="President")
    vice_president_id = fields.Many2one('res.partner', string="Vice-President")
    secretary_id = fields.Many2one('res.partner', string="Secretary")
    reporter_id = fields.Many2one('res.partner', string="Reporter")
    member_ids = fields.Many2many('res.partner', string="Members")
    appointment_decision_ref = fields.Char(string="Ministerial Appointment Decision Reference")
    appointment_date = fields.Date(string="Appointment Date")
    active = fields.Boolean(default=True)
