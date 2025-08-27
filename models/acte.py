# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import UserError


class MzPrixActeCategoriePatient(models.Model):

    _inherit = 'mz.prix.acte.categorie.patient'

    prix_enfant = fields.Float('Prix enfant', digits=(16, 2))

class MzActe(models.Model):
    
    _inherit = 'mz.acte'

    def get_prix_acte(self, patient_obj, acte_obj):
        
        prix_acte_categorie_patient_objs = self.env['mz.prix.acte.categorie.patient'].search([('acte_id','=',acte_obj.id),('categorie_id','=',patient_obj.categorie_id.id)])
        if not prix_acte_categorie_patient_objs:
            raise UserError(('Le prix de cet acte n\'est pas configuré pour la catégorie de ce patient'))
        
        try:
            age = int(patient_obj.age[0:2])
        except:
            age = 0

        if age > 14:
            prix_acte = prix_acte_categorie_patient_objs[0].prix
        else:
            if prix_acte_categorie_patient_objs[0].prix_enfant:
                prix_acte = prix_acte_categorie_patient_objs[0].prix_enfant
            else:
                prix_acte = prix_acte_categorie_patient_objs[0].prix
            
        return prix_acte
