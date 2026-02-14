# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProcurementCommitteeMember(models.Model):
    _name = 'procurement.committee.member'
    _description = 'Committee Member'

    committee_id = fields.Many2one('procurement.committee', string="Committee", required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string="Member", required=True)
    role = fields.Selection([
        ('president', 'President'),
        ('vice_president', 'Vice-President'),
        ('secretary', 'Secretary'),
        ('reporter', 'Reporter'),
        ('member', 'Member'),
    ], string="Role", default='member')
    is_active = fields.Boolean(string="Active", default=True)
    appointment_date = fields.Date(string="Appointment Date")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
