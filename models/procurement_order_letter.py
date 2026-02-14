# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementOrderLetter(models.Model):
    _name = 'procurement.order.letter'
    _description = 'Order Letter'

    name = fields.Char(string="Reference", required=True, copy=False, readonly=True, default='New')
    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    operation = fields.Char(string="Operation")
    contract_reference = fields.Char(string="Contract/Market Number and Subject")
    letter_subject = fields.Text(string="Letter Subject")
    service_line_ids = fields.One2many('procurement.order.letter.line', 'letter_id', string="Service Lines")
    recipient_id = fields.Many2one('res.partner', string="Recipient")
    signatory_id = fields.Many2one('res.partner', string="Signatory")
    letter_date = fields.Date(string="Letter Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('acknowledged', 'Acknowledged'),
        ('executed', 'Executed'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='draft')

    def action_draft(self):
        """Reset to draft state"""
        self.write({'state': 'draft'})

    def action_send(self):
        """Send the order letter"""
        self.write({'state': 'sent'})

    def action_acknowledge(self):
        """Acknowledge receipt of the order letter"""
        self.write({'state': 'acknowledged'})

    def action_execute(self):
        """Start execution"""
        self.write({'state': 'executed'})

    def action_cancel(self):
        """Cancel the order letter"""
        self.write({'state': 'cancelled'})


class ProcurementOrderLetterLine(models.Model):
    _name = 'procurement.order.letter.line'
    _description = 'Order Letter Service Line'
    _order = 'sequence'

    letter_id = fields.Many2one('procurement.order.letter', string="Order Letter")
    sequence = fields.Integer(string="Order Number")
    description = fields.Text(string="Service Description")
