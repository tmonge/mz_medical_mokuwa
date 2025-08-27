# -*- coding: utf-8 -*-
from odoo import fields, models, api
import unicodedata
from odoo.exceptions import UserError


def convert_unicode(obj_to_convert):
    if type(obj_to_convert) is unicode:
        return unicodedata.normalize('NFKD', obj_to_convert).encode('ascii', 'ignore')
    else:
        return obj_to_convert

class MzConsultationMedical(models.Model):

    _inherit = 'mz.consultation.medical'

    #EXAMEN RADIOLOGIQUE
    examen_radiologique = fields.Text('Examen Radiologique')

    #EXAMEN COMPLEMENTAIRE
    examen_complementaire = fields.Text('Examens Complementaires')

    def inspection(self):

        mod_obj = self.env['ir.model.data']
        res = mod_obj.get_object_reference('mz_medical_mokuwa', 'view_consultation_medical_inspection')
        view_id = res and res[1] or False,
        view_id = view_id[0]

        inspection_ids = self.env['mz.consultation.medical.inspection'].search([('consultation_medical_id','=',self.id)])    
        if inspection_ids:
            res_id = inspection_ids[0].id
        else:
            inspection_id = self.env['mz.consultation.medical.inspection'].create({'consultation_medical_id': self.id})
            res_id = inspection_id.id

        return {
            'name': 'Inspection',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mz.consultation.medical.inspection',
            'view_id': [view_id],
            'type': 'ir.actions.act_window',
            'res_id': res_id,
            'context': {},
            'target': 'new'
            }

    def resumeanciendossier(self):

        mod_obj = self.env['ir.model.data']
        res = mod_obj.get_object_reference('mz_medical_mokuwa', 'view_consultation_medical_resumeancien')
        view_id = res and res[1] or False,
        view_id = view_id[0]

        inspection_ids = self.env['mz.consultation.resume.anciendossier'].search([('consultation_medical_id','=',self.id)])    
        if inspection_ids:
            res_id = inspection_ids[0].id
        else:
            inspection_id = self.env['mz.consultation.resume.anciendossier'].create({'consultation_medical_id': self.id})
            res_id = inspection_id.id

        return {
            'name': 'Résumé Ancien Dosier',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mz.consultation.resume.anciendossier',
            'view_id': [view_id],
            'type': 'ir.actions.act_window',
            'res_id': res_id,
            'context': {},
            'target': 'new'
            }

    def traitement(self):

        mod_obj = self.env['ir.model.data']
        res = mod_obj.get_object_reference('mz_medical_mokuwa', 'view_consultation_medical_traitement')
        view_id = res and res[1] or False,
        view_id = view_id[0]

        traitement_ids = self.env['mz.consultation.medical.traitement'].search([('consultation_medical_id','=',self.id)])    
        if traitement_ids:
            res_id = traitement_ids[0].id
        else:
            traitement_id = self.env['mz.consultation.medical.traitement'].create({'consultation_medical_id': self.id})
            res_id = traitement_id.id

        return {
            'name': 'Traitement',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mz.consultation.medical.traitement',
            'view_id': [view_id],
            'type': 'ir.actions.act_window',
            'res_id': res_id,
            'context': {},
            'target': 'new'
            }

    def action_view_demande_traitement_kine(self):
        action = self.env.ref('mz_medical_mokuwa.action_demande_traitement_kine').read()[0]
        action['domain'] = [('consultation_medical_id', '=', self.id)]
        action['context'] = {'default_consultation_medical_id': self.id, 'default_patient_id': self.patient_id.id, 'search_default_consultation_medical_id': self.id}
        return action


class MzConsultationMedicalInspection(models.Model):

    _name = 'mz.consultation.medical.inspection'
    _description = 'Consultation medical Inspection'

    consultation_medical_id = fields.Many2one('mz.consultation.medical','Consultation médical')
    consultation_medical_stade_id = fields.Many2many('mz.consultation.medical.stade','Stade')
    #'patient_id':fields.many2one('mz.patient','Patient')
    rachis = fields.Text('Rachis')
    epaule_membre_superieur = fields.Text('Lépaule et le membre supérieur')
    bassin_membre_inferieur = fields.Text('Le bassin et les membres inférieurs')
    station_debout = fields.Text('La station débout')
    deambulation = fields.Text('La déambulation')
    
    #Palpation
    colonne_vertebrale = fields.Text('La colonne vertébrale')
    palpi_membres_superieurs = fields.Text('Les membre supérieurs')
    palpi_bassin_membre_inferieur = fields.Text('Le bassin et les membres inférieurs')

    #Mensurations
    mensurations_longitudinales = fields.Text('Les mensurations longitudinales')
    mensurations_perimetriques = fields.Text('Les mensurations périmétriques')

    #Mobile Passive
    mobile_passive = fields.Text('Mobile Passive')
    stade_mobile_passive_ids = fields.Many2many('mz.inspection.mobilite.passive.stade','mz_inspection_mobilite_passive_stade_rel','inspection_id','stade_id','Stade mobilité passive')

    #EXAMEN DE SENSIBILITE ET REFLEXES
    examen_sensibilite = fields.Text('Examen de la sensibilité')
    examen_reflexes = fields.Text('Examen des réflexes ostéo-tendineux')

    state = fields.Selection(related='consultation_medical_id.state', readonly=True, string='Etat')

    def write_success(self):
        return True


class MzInspectionMobilitePassiveStade(models.Model):

    _name = 'mz.inspection.mobilite.passive.stade'
    _description = 'Stade mobilite passive' 

    name = fields.Char('Stade', size=250)
    
    
     
class MzConsultationMedicalTraitement(models.Model):

    _name = 'mz.consultation.medical.traitement'
    _description = 'Consultation medical traitement'

    consultation_medical_id = fields.Many2one('mz.consultation.medical','Consultation médical')
    consultation_medical_traitement_ids = fields.One2many('mz.consultation.medical.traitement.nonsanglantes','traitement_id','Méthodes non sanglantes')

    methode_chirurgicales_interention_os = fields.Selection([('L\'Ostéotomie', 'L\'Ostéotomie'), ('L\'Ostéotosynthèse', 'L\'Ostéotosynthèse'),
                                                             ('La résection', 'La résection'),('La greffe osseuse', 'La greffe osseuse'),
                                                             ('L\'épiphysiodèse', 'L\'épiphysiodèse')], 'Intervention sur les Os')

    methode_chirurgicales_interention_arti = fields.Selection([('La ponction articulaire', 'La ponction articulaire'), ('L\'arthrodèse', 'L\'arthrodèse'),
                                                              ('L\'arthoplastie prothétique', 'L\'arthoplastie prothétique')], 'Intervention sur les articulations')
    methode_chirurgicales_interention_tendons = fields.Selection([('Les sutures', 'Les sutures'), ('Les incision ou ténotomies', 'Les incision ou ténotomies'),
                                                                  ('Les transplantations', 'Les transplantations'),
                                                                  ('Les tenodèses ou fixation de tendons sur le squelette', 'Les tenodèses ou fixation de tendons sur le squelette')], 'Intervention sur les tendons')

    methode_chirurgicales_interventin_nerfs = fields.Selection([('La transposition d\'un nerf hors dela place normale', 'La transposition d\'un nerf hors dela place normale'),
                                                                ('La neurolyse', 'la neurolyse'), ('La neurotomie', 'la neurotomie'),
                                                                ('La greffe nerveuse autologue', 'La greffe nerveuse autologue')], 'Intervention sur les nerfs')
    state = fields.Selection(related='consultation_medical_id.state', readonly=True, string='Etat')

    def write_success(self):
        return True

class MzConsultationMedicalTraitementNonsanglantes(models.Model):

    _name = 'mz.consultation.medical.traitement.nonsanglantes'
    _description = 'Traitement non sanglante'

    traitement_id = fields.Many2one('mz.consultation.medical.traitement','Traitement')
    name = fields.Char('Méthode non sanglante')


class MzConsultationMedicalResumerAncienDossier(models.Model):

    _name = 'mz.consultation.resume.anciendossier'
    _description = 'Consultation medical Resumer Ancien Dossier'

    consultation_medical_id = fields.Many2one('mz.consultation.medical','Consultation médical')
    resume_ancien_dossier = fields.Text('Résume Ancien Dossier')
    resume_ancien_dossier_radio = fields.Text('Ancien Résume Radiologie')
    state = fields.Selection(related='consultation_medical_id.state', readonly=True, string='Etat')
    
    def write_success(self):
        return True