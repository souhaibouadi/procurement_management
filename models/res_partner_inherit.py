# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Procurement Supplier Fields
    is_procurement_supplier = fields.Boolean(
        string="Is Procurement Supplier", default=False,
        help="Check if this partner is a qualified procurement supplier")
    supplier_registration_number = fields.Char(
        string="Supplier Registration Number",
        help="Official supplier registration number")
    supplier_qualification_date = fields.Date(
        string="Qualification Date",
        help="Date when the supplier was qualified")
    supplier_qualification_expiry = fields.Date(
        string="Qualification Expiry",
        help="Date when the supplier qualification expires")

    # Business Information for Algerian Suppliers
    fiscal_id = fields.Char(
        string="NIF (Fiscal ID)",
        help="Numéro d'Identification Fiscale")
    commerce_register = fields.Char(
        string="Commerce Register",
        help="Registre de Commerce")
    cnas_number = fields.Char(
        string="CNAS Number",
        help="Caisse Nationale des Assurances Sociales")
    casnos_number = fields.Char(
        string="CASNOS Number",
        help="Caisse Nationale de Sécurité Sociale des Non-Salariés")

    # Procurement Statistics (computed fields)
    procurement_bid_count = fields.Integer(
        string="Bid Count", compute='_compute_procurement_counts',
        help="Number of bids submitted by this partner")
    procurement_award_count = fields.Integer(
        string="Award Count", compute='_compute_procurement_counts',
        help="Number of procurement awards received")
    procurement_contract_count = fields.Integer(
        string="Contract Count", compute='_compute_procurement_counts',
        help="Number of procurement contracts")

    @api.depends('is_procurement_supplier')
    def _compute_procurement_counts(self):
        for partner in self:
            partner.procurement_bid_count = self.env['procurement.bidder'].search_count(
                [('partner_id', '=', partner.id)])
            partner.procurement_award_count = self.env['procurement.award'].search_count(
                [('partner_id', '=', partner.id)])
            # Count purchase orders linked to this partner with procurement references
            partner.procurement_contract_count = self.env['purchase.order'].search_count(
                [('partner_id', '=', partner.id), ('procurement_procedure_id', '!=', False)])
