# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementNotice(models.Model):
    _name = 'procurement.notice'
    _description = 'Procurement Notice'

    name = fields.Char(string="Notice Title", required=True)
    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    notice_type = fields.Selection([
        ('tender_call', 'Tender Call Notice'),
        ('candidacy_call', 'Candidacy Call Notice'),
        ('competition', 'Competition Notice'),
        ('provisional_award', 'Provisional Award Notice'),
        ('final_award', 'Final Award Notice'),
        ('unsuccessful', 'Unsuccessful Notice'),
        ('cancellation', 'Cancellation Notice'),
    ], string="Notice Type")
    tender_subtype = fields.Selection([
        ('national_open', 'National Open with Minimum Capacity Requirements'),
        ('national_restricted', 'National Restricted'),
        ('international', 'International'),
    ], string="Tender Subtype")
    notice_reference = fields.Char(string="Notice Reference", help="e.g. N03/DG/2025")
    contract_subject = fields.Text(string="Contract Subject")
    eligibility_conditions = fields.Text(string="Eligibility Conditions")
    professional_capacity = fields.Text(string="Professional Capacity Requirements")
    financial_capacity = fields.Text(string="Financial Capacity Requirements", help="Average turnover required, fiscal years, minimum amount")
    technical_capacity = fields.Text(string="Technical Capacity Requirements")
    specs_price = fields.Float(string="Specifications Price (DZD)")
    submission_composition = fields.Text(string="Submission Composition", help="Candidacy file + Technical offer + Financial offer")
    outer_envelope_label = fields.Char(string="Outer Envelope Label", default="To be opened only by the Bid Opening and Evaluation Committee")
    preparation_days = fields.Integer(string="Preparation Duration (days)")
    submission_time_limit = fields.Char(string="Submission Time Limit", default="13:00")
    commitment_duration = fields.Char(string="Bidder Commitment Duration", help="Preparation period + 3 months")
    bomop_publication_date = fields.Date(string="BOMOP Publication Date")
    journal_line_ids = fields.One2many('procurement.notice.journal', 'notice_id', string="Publication Journals")
    language = fields.Selection([
        ('fr', 'French'),
        ('ar', 'Arabic'),
        ('fr_ar', 'French + Arabic'),
    ], string="Language")
    appeal_delay_days = fields.Integer(string="Appeal Period (days)", default=10)
    appeal_address = fields.Text(string="Appeal Address")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validated', 'Validated'),
        ('published', 'Published'),
    ], string="Status", default='draft')


class ProcurementNoticeJournal(models.Model):
    _name = 'procurement.notice.journal'
    _description = 'Notice Publication Journal'

    notice_id = fields.Many2one('procurement.notice', string="Notice")
    journal_name = fields.Char(string="Journal Name", help="El Chaab, El Moudjahid, BOMOP, etc.")
    publication_date = fields.Date(string="Publication Date")
