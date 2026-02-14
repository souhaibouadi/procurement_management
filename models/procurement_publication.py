# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementPublication(models.Model):
    _name = 'procurement.publication'
    _description = 'Publication Record'

    name = fields.Char(string="Publication Name", required=True)
    media_type = fields.Selection([
        ('newspaper', 'Newspaper'),
        ('website', 'Website'),
        ('bulletin', 'Official Bulletin'),
        ('other', 'Other'),
    ], string="Media Type")
    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    publication_type = fields.Selection([
        ('press', 'National Press'),
        ('bomop', 'BOMOP'),
        ('posting', 'Public Posting'),
        ('website', 'Website'),
        ('consultation_letter', 'Consultation Letter'),
    ], string="Publication Type")
    publication_date = fields.Date(string="Publication Date")
    journal_name = fields.Char(string="Journal Name")
    publication_reference = fields.Char(string="Publication Reference")
    anep_order_number = fields.Char(string="ANEP Order Number")
    publication_cost = fields.Float(string="Publication Cost (DZD)")
    notes = fields.Text(string="Notes")
