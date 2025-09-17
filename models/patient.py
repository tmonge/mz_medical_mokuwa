# -*- coding: utf-8 -*-
from odoo import fields, models, _

class MzPatient(models.Model):
    
    _inherit='mz.patient'

    categorie = fields.Selection([('A', 'A'),('B', 'B') ,('C', 'C') ,('D', 'D')], 'Catégorie')

    # @api.model
    # def create(self, vals):

    #     vals['name'] = vals.get('name').upper()
    #     if vals.get('prenom'):
    #         vals['prenom'] = vals.get('prenom').upper()

    #     patient_ids = self.search([('name','=',vals.get('name')), ('prenom','=',vals.get('prenom')), ('date_naissance','=',vals.get('date_naissance'))])
    #     if patient_ids:
    #         raise UserError(_('Le patient que vous essayer d\'enregistrer existe déjà dans le système, veuillez le rechercher, Merci.'))

    #     vals['numero_fiche'] = self.env['ir.sequence'].next_by_code('patient')
    #     vals['est_patient'] = True
    #     return super(MzPatient, self).create(vals)
    
    def action_view_dossier_kine_readaptation(self):
        kine_dossier_ids = []
        sql = """SELECT id as kine_id FROM mz_kine_dossier_patient WHERE patient_id = %d """%(self.id)

        self.env.cr.execute(sql)
        res = self.env.cr.dictfetchall()

        for val in res:
            kine_dossier_ids.append(val['kine_id'])

        return {
            'name': _('Dossier kiné-readaptation'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model':'mz.dosmed.kine.readaptation',
            'domain': "[('kine_dossier_id','in',[" + ','.join(map(str, kine_dossier_ids)) + "])]",
            'type': 'ir.actions.act_window',
            }