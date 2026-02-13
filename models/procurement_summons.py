# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementSummons(models.Model):
    _name = 'procurement.summons'
    _description = 'Committee Summons'

    name = fields.Char(string="Reference", help="e.g. NXX/CM/YYYY")
    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    session_id = fields.Many2one('procurement.committee.session', string="Session")
    recipient_id = fields.Many2one('res.partner', string="Recipient", required=True)
    role = fields.Char(string="Role in Committee", help="Vice-President, Secretary, Member, etc.")
    organization = fields.Char(string="Affiliated Organization", help="e.g. DECC, DAG, DOF, CNR, FNPOS, CA, etc.")
    send_date = fields.Date(string="Sending Date")
    meeting_datetime = fields.Datetime(string="Meeting Date & Time")
    meeting_location = fields.Char(string="Meeting Location")
    subject = fields.Char(string="Summons Subject")
    agenda = fields.Text(string="Agenda")
    signatory_id = fields.Many2one('res.partner', string="Signatory")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('confirmed', 'Confirmed'),
    ], string="Status", default='draft')
