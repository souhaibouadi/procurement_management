# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementSpecsWithdrawal(models.Model):
    _name = 'procurement.specs.withdrawal'
    _description = 'Specifications Withdrawal Register'
    _order = 'sequence'

    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    sequence = fields.Integer(string="Order Number")
    bidder_id = fields.Many2one('procurement.bidder', string="Bidder")
    withdrawn_by = fields.Char(string="Withdrawn By (Person Name)")
    withdrawal_date = fields.Date(string="Withdrawal Date", required=True)
    withdrawal_time = fields.Char(string="Withdrawal Time")
    amount_paid = fields.Float(string="Amount Paid for Specifications (DZD)")
    receipt_number = fields.Char(string="Payment Receipt Number")
    notes = fields.Text(string="Notes")
