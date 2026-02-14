# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementServiceOrder(models.Model):
    _name = 'procurement.service.order'
    _description = 'Service Order (ODS)'

    name = fields.Char(string="Service Order Reference", help="e.g. ODS/2026/0001")
    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    operation = fields.Char(string="Operation")
    contractor_id = fields.Many2one('res.partner', string="Contractor Partner")
    contract_reference = fields.Char(string="Contract/Market Reference", help="e.g. n.../DG/...")
    contract_date = fields.Date(string="Contract Date")
    execution_delay = fields.Char(string="Execution Delay")
    order_subject = fields.Text(string="Service Order Subject")
    order_body = fields.Text(string="Service Order Content")
    register_number = fields.Char(string="CACOBATPH Register Number")
    notification_date = fields.Date(string="Notification Date")
    notification_address = fields.Text(string="Notification Address")
    service_signatory_id = fields.Many2one('res.partner', string="Contracting Authority Signatory")
    handover_date = fields.Date(string="Handover Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('signed', 'Signed'),
        ('notified', 'Notified'),
    ], string="Status", default='draft')
