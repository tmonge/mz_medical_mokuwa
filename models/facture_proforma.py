# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError



class MzMedFactureProforma(models.Model):

    _inherit='mz.med.facture.proforma'

    categorie_id = fields.Many2one('mz.patient.categorie', 'Catégorie patient')


class MzMedFactureLine(models.Model):

    _inherit='mz.med.facture.proforma.line'
    
    @api.onchange('facture_id.categorie_id', 'acte_id', 'quantite')
    def onchange_acte(self):
        if self.acte_id:
            if not self.facture_id.categorie_id:
                raise UserError(('Veuillez d\'abord selectionner la catégorie avant de continuer svp, merci.'))
            
            prix_unitaire =  self.get_prix_acte(self.facture_id.categorie_id.id, self.acte_id.id)
            self.prix_unitaire = prix_unitaire
            self.prix_total = prix_unitaire * self.quantite

    @api.onchange('facture_id.categorie_id', 'acte_id', 'quantite')
    def onchange_quantite(self):
        if self.acte_id:
            if not self.facture_id.categorie_id:
                raise UserError(('Veuillez d\'abord selectionner la catégorie avant de continuer svp, merci.'))
            
            prix_unitaire =  self.get_prix_acte(self.facture_id.categorie_id.id, self.acte_id.id)
            self.prix_total = prix_unitaire * self.quantite

    def get_prix_acte(self, categorie_id, acte_id):
        
        prix_acte_categorie_patient_objs = self.env['mz.prix.acte.categorie.patient'].search([('acte_id','=',acte_id),('categorie_id','=',categorie_id)])
        if not prix_acte_categorie_patient_objs:
            raise UserError(('Le prix de cet acte n\'est pas configuré pour la catégorie de ce patient'))
        
        return prix_acte_categorie_patient_objs[0].prix
