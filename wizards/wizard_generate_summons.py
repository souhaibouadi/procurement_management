# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class WizardGenerateSummons(models.TransientModel):
    _name = 'procurement.wizard.generate.summons'
    _description = 'Generate Summons Wizard'

    session_id = fields.Many2one(
        'procurement.committee.session',        string='Session',
        required=True,
        default=lambda self: self.env.context.get('active_id')
    )
    session_date = fields.Datetime(
        related='session_id.session_date',
        string='Session Date',
        readonly=True
    )
    session_type = fields.Selection(
        related='session_id.session_type',
        string='Session Type',
        readonly=True
    )
    summons_date = fields.Date(
        string='Summons Date',
        required=True,
        default=fields.Date.today
    )
    send_email = fields.Boolean(
        string='Send Email',
        default=True,
        help='Send summons by email to committee members'
    )
    include_agenda = fields.Boolean(
        string='Include Agenda',
        default=True,
        help='Include session agenda in the summons'
    )
    member_ids = fields.Many2many(
        'procurement.committee.member',
        string='Members to Summon',
        compute='_compute_member_ids',
        store=True,
        readonly=False
    )
    additional_message = fields.Text(
        string='Additional Message',
        help='Additional message to include in the summons'
    )

    @api.depends('session_id')
    def _compute_member_ids(self):
        for wizard in self:
            if wizard.session_id and wizard.session_id.committee_id:
                wizard.member_ids = wizard.session_id.committee_id.member_ids
            else:
                wizard.member_ids = False

    def action_generate(self):
        self.ensure_one()
        
        if not self.member_ids:
            raise UserError(_('Please select at least one member to summon.'))
        
        summons_vals = []
        for member in self.member_ids:
            vals = {
                'session_id': self.session_id.id,
                'member_id': member.id,
                'summons_date': self.summons_date,
                'state': 'draft',
            }
            if self.additional_message:
                vals['notes'] = self.additional_message
            summons_vals.append(vals)
        
        summons = self.env['procurement.summons'].create(summons_vals)
        
        # Send emails if requested
        if self.send_email:
            for s in summons:
                s.action_send()
        
        # Return action to view created summons
        return {
            'name': _('Generated Summons'),
            'type': 'ir.actions.act_window',
            'res_model': 'procurement.summons',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', summons.ids)],
            'context': {'create': False},
        }
