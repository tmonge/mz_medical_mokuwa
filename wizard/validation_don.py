# -*- coding: utf-8 -*-
from odoo import models


class MzWizardValidationPharmacieDon(models.TransientModel):

    _name = 'mz.wizard.validation.pharmacie.don'
    _description = 'Wizard validation pharmacie don'

    def valider(self):

        active_id = self._context.get('active_id', False)
        facture_line_obj = self.env['mz.med.facture.line']
        facture_line = facture_line_obj.browse(active_id)
        
        facture_line.type_apurement = 'Don'
        facture_line.mode_validation = 'Don'
        facture_line.mode_paiement = 'Don'
        facture_line.valider()
        
        return {'type': 'ir.actions.act_window_close'}