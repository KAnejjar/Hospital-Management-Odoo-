# -*- coding: utf-8 -*-
import json
from odoo import api, fields, models,modules, _
from odoo.exceptions import UserError, ValidationError

#from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError


class PosConfigInherit(models.Model):
    _inherit = 'pos.config'
    default_partner_id = fields.Many2one('res.partner', string="Client Par Defaut")

class Assurances(models.Model):
    _name = 'pos.assurance'
    #_sequence = None
    #_order = "sequence"
    assurance = fields.Char(name='assurance',string="Type d'assurance",required=True)
    _rec_name='assurance'
    sequence = fields.Integer(string='Sequence Assurance')
    
class Medecins(models.Model):
    _name = 'pos.medecin'
    medecin = fields.Char(name='medecin', string="Médecin",required=True)
    _rec_name='medecin'
    sequence = fields.Integer(string='Sequance Medecins')

class PosOrder(models.Model):
    _name = 'pos.order'
    _inherit ='pos.order'

    # _sql_constraints = [
    #     ('x_numCheque_unique', 'unique (order.partner_id.x_numCheque)','Le numéro doit être unique!')
    # ]
    
    def action_pos_order_invoice(self):
        moves = self.env['account.move']

        for order in self:
            if order.account_move:
                moves += order.account_move
                continue

            if not order.partner_id:
                raise UserError(_('Veuillez choisir un client pour la vente.'))

            move_vals = {
                'invoice_payment_ref': order.name,
                'invoice_origin': order.name,
                'journal_id': order.session_id.config_id.invoice_journal_id.id,
                'type': 'out_invoice' if order.amount_total >= 0 else 'out_refund',
                'ref': order.name,
                'partner_id': order.partner_id.id,
                'narration': order.note or '',
                # considering partner's sale pricelist's currency
                'currency_id': order.pricelist_id.currency_id.id,
                'invoice_user_id': order.user_id.id,
                'invoice_date': fields.Date.today(),
                'fiscal_position_id': order.fiscal_position_id.id,
                'invoice_line_ids': [(0, None, order._prepare_invoice_line(line)) for line in order.lines],
                'x_numCheque': order.partner_id.x_numCheque,
                'assurance2': order.partner_id.assurance2,
                'medecin2': order.partner_id.medecin2,
            }
            new_move = moves.sudo()\
                            .with_context(default_type=move_vals['type'], force_company=order.company_id.id)\
                            .create(move_vals)
            message = _("Cette facture a été créée à partir du point de vente de la session:<a href=# data-oe-model=pos.order data-oe-id=%d>%s</a>") % (order.id, order.name)
            new_move.message_post(body=message)
            order.write({'account_move': new_move.id, 'state': 'invoiced'})
            moves += new_move

        if not moves:
            return {}

        return {
            'name': _('Facture'),
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_model': 'account.move',
            'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': moves and moves.ids[0] or False,
        }


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit ='res.partner'
 
    x_numCheque = fields.Char(name='x_numCheque', string="Numéro d'assurance", required=True,index=True)
    assurance2 = fields.Many2one('pos.assurance', string="Type d'assurance")#,default=lambda self: self.env['pos.assurance'].search([]))
    medecin2 = fields.Many2one('pos.medecin', string='Médecin')#,default=lambda self: self.env['pos.medecin'].search([]))
    
    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        num = self.env['res.partner'].search([('x_numCheque','=',vals.get('x_numCheque'))])
        if len(num) > 1:
            raise ValidationError(_("Le numéro d'assurance doit être unique!"))
        else :
            return res
     
    @api.multi
    def write(self,vals):
        res = super(ResPartner, self).write(vals)
        new_value = vals.get('x_numCheque')
        num = self.search([('x_numCheque','=',new_value)])
        if len(num) > 1:
            raise ValidationError(_("Le numéro d'assurance doit être unique!"))
        else :
            return res
        # num = self.search([('x_numCheque','=',self.x_numCheque)])
        # if len(num) > 1:
        #     res = super(ResPartner, self).write(vals)
        #     return res
        # else :
        #     raise ValidationError(_("Le numéro d'assurance doit être unique!"))   
    @api.model 
    def get_medecs(self):
        L_medecs=[]
        meds = self.env['pos.medecin'].search([])
        for rec in meds:
            #pair = (rec.id,rec.medecin)
            L_medecs.append(rec.id)
            L_medecs.append(rec.medecin)
        return L_medecs

    @api.model 
    def get_assur(self):
        L_assur=[]
        assur = self.env['pos.assurance'].search([])
        for rec in assur:
            #pair = (rec.id,rec.medecin)
            L_assur.append(rec.id)
            L_assur.append(rec.assurance)
        return L_assur
 
class AccountInvoice(models.Model):
    _name = 'account.move'
    _inherit ='account.move'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        # OVERRIDE
        res = super(AccountInvoice, self)._onchange_partner_id()
        if self.partner_id:
            self.x_numCheque = self.partner_id.x_numCheque
            self.assurance2 = self.partner_id.assurance2
            self.medecin2 = self.partner_id.medecin2
        return res