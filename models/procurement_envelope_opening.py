# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProcurementEnvelopeOpening(models.Model):
    _name = 'procurement.envelope.opening'
    _description = 'Envelope Opening Session'

    procedure_id = fields.Many2one('procurement.procedure', string="Procedure")
    committee_id = fields.Many2one('procurement.committee', string="Committee")
    opening_date = fields.Datetime(string="Opening Date & Time", required=True)
    location = fields.Char(string="Location")
    is_public = fields.Boolean(string="Public Session", default=True)
    envelope_detail_ids = fields.One2many('procurement.envelope.detail', 'opening_id', string="Envelope Details")
    minutes_id = fields.Many2one('procurement.minutes', string="Minutes")
    notes = fields.Text(string="Notes")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('opened', 'Opened'),
        ('validated', 'Validated'),
    ], string="Status", default='draft')
            name = fields.Char(string="Opening Name", required=True)
    session_id = fields.Many2one('procurement.committee.session', string="Session")
    envelope_type = fields.Selection([
        ('candidacy', 'Candidacy'),
        ('technical', 'Technical'),
        ('financial', 'Financial'),
    ], string="Envelope Type")
    bidder_id = fields.Many2one('procurement.bidder', string="Bidder")
    content_details = fields.Text(string="Content Details")
    missing_documents = fields.Text(string="Missing Documents")


class ProcurementEnvelopeDetail(models.Model):
    _name = 'procurement.envelope.detail'
    _description = 'Envelope Detail'

    opening_id = fields.Many2one('procurement.envelope.opening', string="Opening Session")
    bidder_id = fields.Many2one('procurement.bidder', string="Bidder")
    candidacy_file_present = fields.Boolean(string="Candidacy File Present")
    technical_offer_present = fields.Boolean(string="Technical Offer Present")
    financial_offer_present = fields.Boolean(string="Financial Offer Present")
    envelope_sealed = fields.Boolean(string="Envelope Sealed")
    notes = fields.Text(string="Notes")
