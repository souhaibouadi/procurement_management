# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class WizardGenerateSummons(models.TransientModel):
    _name = 'procurement.wizard.generate.summons'
    _description = 'Generate Summons Wizard'

    session_id = fields.Many2one(
        'procurement.committee.session',
        string='Session',
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
        relation='wizard_summons_member_rel',
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
                committee = wizard.session_id.committee_id
                members = self.env['procurement.committee.member'].search([
                    ('committee_id', '=', committee.id),
                    ('is_active', '=', True)
                ])
                wizard.member_ids = members
            else:
                wizard.member_ids = False

    def action_generate(self):
        self.ensure_one()
        if not self.member_ids:
            raise UserError(_('Please select at least one member to summon.'))

        session = self.session_id
        procedure = session.procedure_id

        summons_vals = []
        for member in self.member_ids:
            vals = {
                'procedure_id': procedure.id if procedure else False,
                'session_id': session.id,
                'recipient_id': member.partner_id.id,
                'member_id': member.id,
                'role': member.role or '',
                'send_date': self.summons_date,
                'meeting_datetime': session.session_date,
                'meeting_location': session.location or '',
                'subject': 'Summons - %s' % (session.name or ''),
                'state': 'draft',
            }
            if self.additional_message:
                vals['content'] = self.additional_message
            if self.include_agenda and session.agenda_item_ids:
                agenda_text = '\n'.join(
                    ['- %s' % item.description for item in session.agenda_item_ids if item.description]
                )
                vals['agenda'] = agenda_text
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
