# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProcurementProcedure(models.Model):
    _name = 'procurement.procedure'
    _description = 'Procurement Procedure'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string="Reference", required=True, readonly=True, default="New", copy=False)
    procedure_reference = fields.Char(string="Procedure Number", help="e.g. N03/DG/2025")
    subject = fields.Text(string="Procurement Subject", required=True)
    service_type = fields.Selection([
        ('works', 'Works Execution'),
        ('supplies', 'Supplies Acquisition'),
        ('studies', 'Studies'),
        ('services', 'Service Delivery'),
    ], string="Service Type")
    structure_level = fields.Selection([
        ('central', 'General Directorate (Central)'),
        ('regional', 'Regional Agency'),
    ], string="Structure Level")
    procedure_type = fields.Selection([
        ('direct_order', 'Direct Purchase Order / Service Order'),
        ('comparative_table', 'Comparative Offer Table (COT)'),
        ('consultation', 'Consultation'),
        ('tender', 'Tender / Call for Competition'),
        ('competition', 'Competition'),
    ], string="Procedure Type", compute='_compute_procedure_type', store=True)
    estimated_amount_excl_tax = fields.Float(string="Administrative Estimate Excl. Tax (DZD)")
    estimated_amount_incl_tax = fields.Float(string="Administrative Estimate Incl. Tax (DZD)", compute='_compute_incl_tax', store=True)
    vat_rate = fields.Float(string="VAT Rate (%)", default=19.0)
    allocated_budget = fields.Float(string="Allocated Budget (DZD)")
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.ref('base.DZD', raise_if_not_found=False))
    lot_type = fields.Selection([('single', 'Single Lot'), ('separate', 'Separate Lots')], string="Lot Type")
    lot_justification = fields.Text(string="Justification for Separate Lots")
    specs_withdrawn_count = fields.Integer(string="Number of Specifications Withdrawn")
    bids_received_count = fields.Integer(string="Number of Bids Received")
    preparation_duration = fields.Integer(string="Offer Preparation Duration (days)", default=15)
    creation_date = fields.Date(string="Creation Date", default=fields.Date.today)
    launch_date = fields.Date(string="Launch Date")
    submission_deadline = fields.Datetime(string="Submission Deadline (date & time)")
    envelope_opening_date = fields.Datetime(string="Envelope Opening Date")
    submission_address = fields.Char(string="Submission Address")
    opening_location = fields.Char(string="Opening Location")
    fax_number = fields.Char(string="Fax Number")
    tax_id_number = fields.Char(string="Contracting Authority Tax ID (NIF)", default="41202 5000 14 00 49")
    contracting_authority_name = fields.Char(string="Contracting Authority Name", default="CACOBATPH")
    contracting_authority_address = fields.Text(string="Contracting Authority Address")
    authorizing_officer_id = fields.Many2one('res.users', string="Authorizing Officer")
    delegation_note = fields.Char(string="Delegated By")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('needs_assessment', 'Needs Assessment'),
        ('estimation', 'Administrative Estimation'),
        ('specs_drafting', 'Specifications Drafting'),
        ('specs_review', 'Specifications Review by Committee'),
        ('specs_correction', 'Specifications Correction'),
        ('specs_approval', 'Specifications Approval'),
        ('publication', 'Publication / Launch'),
        ('specs_withdrawal', 'Specifications Withdrawal'),
        ('bid_submission', 'Bid Submission'),
        ('envelope_opening', 'Envelope Opening'),
        ('evaluation', 'Bid Evaluation'),
        ('result', 'Results'),
        ('provisional_award', 'Provisional Award'),
        ('appeal_period', 'Appeal Period (10 days)'),
        ('final_award', 'Final Award'),
        ('contract_approval', 'Contract Approval by Market Committee'),
        ('contract_setup', 'Contract / Market Establishment'),
        ('execution', 'Execution'),
        ('provisional_acceptance', 'Provisional Acceptance'),
        ('final_acceptance', 'Final Acceptance'),
        ('closed', 'Closed'),
        ('unsuccessful', 'Unsuccessful'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='draft', tracking=True)

    purchase_order_ids = fields.One2many('purchase.order', 'procurement_procedure_id', string="Purchase Orders")
    committee_ids = fields.One2many('procurement.committee', 'procedure_id', string="Committees")
    session_ids = fields.One2many('procurement.committee.session', 'procedure_id', string="Sessions")
    notice_ids = fields.One2many('procurement.notice', 'procedure_id', string="Notices")
    publication_ids = fields.One2many('procurement.publication', 'procedure_id', string="Publications")
    specs_withdrawal_ids = fields.One2many('procurement.specs.withdrawal', 'procedure_id', string="Specs Withdrawals")
    bid_deposit_ids = fields.One2many('procurement.bid.deposit', 'procedure_id', string="Bid Deposits")
    envelope_opening_ids = fields.One2many('procurement.envelope.opening', 'procedure_id', string="Envelope Openings")
    evaluation_ids = fields.One2many('procurement.evaluation', 'procedure_id', string="Evaluations")
    bidder_ids = fields.One2many('procurement.bidder', 'procedure_id', string="Bidders")
    decision_ids = fields.One2many('procurement.decision', 'procedure_id', string="Decisions")
    minutes_ids = fields.One2many('procurement.minutes', 'procedure_id', string="Minutes")
    summons_ids = fields.One2many('procurement.summons', 'procedure_id', string="Summons")
    document_ids = fields.One2many('procurement.document', 'procedure_id', string="Documents")
    service_order_ids = fields.One2many('procurement.service.order', 'procedure_id', string="Service Orders")
    order_letter_ids = fields.One2many('procurement.order.letter', 'procedure_id', string="Order Letters")
    analytical_sheet_id = fields.Many2one('procurement.analytical.sheet', string="Analytical Sheet")
    provisional_award_id = fields.Many2one('procurement.award', string="Provisional Award")
    final_award_id = fields.Many2one('procurement.award', string="Final Award")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('procurement.procedure') or 'New'
        return super().create(vals_list)

    @api.depends('estimated_amount_excl_tax', 'vat_rate')
    def _compute_incl_tax(self):
        for rec in self:
            rec.estimated_amount_incl_tax = rec.estimated_amount_excl_tax * (1 + rec.vat_rate / 100)

    @api.depends('estimated_amount_incl_tax', 'service_type', 'structure_level')
    def _compute_procedure_type(self):
        for rec in self:
            amount = rec.estimated_amount_incl_tax or 0.0
            stype = rec.service_type
            level = rec.structure_level
            ptype = False
            if level == 'central':
                if stype in ('works', 'supplies'):
                    if amount < 50000:
                        ptype = 'direct_order'
                    elif amount < 1000000:
                        ptype = 'comparative_table'
                    elif amount <= 12000000:
                        ptype = 'consultation'
                    elif amount <= 30000000:
                        ptype = 'tender'
                    else:
                        ptype = 'tender'
                elif stype in ('studies', 'services'):
                    if amount < 50000:
                        ptype = 'direct_order'
                    elif amount < 500000:
                        ptype = 'comparative_table'
                    elif amount <= 6000000:
                        ptype = 'consultation'
                    elif amount <= 15000000:
                        ptype = 'tender'
                    else:
                        ptype = 'tender'
            elif level == 'regional':
                if stype in ('works', 'supplies'):
                    if amount < 50000:
                        ptype = 'direct_order'
                    elif amount < 1000000:
                        ptype = 'comparative_table'
                    elif amount <= 12000000:
                        ptype = 'consultation'
                    else:
                        ptype = 'consultation'
                elif stype in ('studies', 'services'):
                    if amount < 50000:
                        ptype = 'direct_order'
                    elif amount < 500000:
                        ptype = 'comparative_table'
                    elif amount <= 6000000:
                        ptype = 'consultation'
                    else:
                        ptype = 'consultation'
            rec.procedure_type = ptype

    def action_needs_assessment(self):
        self.write({'state': 'needs_assessment'})

    def action_estimation(self):
        self.write({'state': 'estimation'})

    def action_specs_drafting(self):
        self.write({'state': 'specs_drafting'})

    def action_specs_review(self):
        self.write({'state': 'specs_review'})

    def action_specs_correction(self):
        self.write({'state': 'specs_correction'})

    def action_specs_approval(self):
        self.write({'state': 'specs_approval'})

    def action_publication(self):
        self.write({'state': 'publication'})

    def action_specs_withdrawal(self):
        self.write({'state': 'specs_withdrawal'})

    def action_bid_submission(self):
        self.write({'state': 'bid_submission'})

    def action_envelope_opening(self):
        self.write({'state': 'envelope_opening'})

    def action_evaluation(self):
        self.write({'state': 'evaluation'})

    def action_result(self):
        self.write({'state': 'result'})

    def action_provisional_award(self):
        self.write({'state': 'provisional_award'})

    def action_appeal_period(self):
        self.write({'state': 'appeal_period'})

    def action_final_award(self):
        self.write({'state': 'final_award'})

    def action_contract_approval(self):
        self.write({'state': 'contract_approval'})

    def action_contract_setup(self):
        self.write({'state': 'contract_setup'})

    def action_execution(self):
        self.write({'state': 'execution'})

    def action_provisional_acceptance(self):
        self.write({'state': 'provisional_acceptance'})

    def action_final_acceptance(self):
        self.write({'state': 'final_acceptance'})

    def action_closed(self):
        self.write({'state': 'closed'})

    def action_unsuccessful(self):
        self.write({'state': 'unsuccessful'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})
