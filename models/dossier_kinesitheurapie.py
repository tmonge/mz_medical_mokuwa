# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import *


liste_sexe = [('F', 'Feminin'), ('M', 'Masculin')]
liste_etat_civile = [('Celibataite', 'Celibataite'),('Marie', 'Marié(e)'),('Veuf(ve)', 'Veuf(ve)')]
liste_contrat_patient = [('prive', 'Privé'), ('conventionne', 'Conventionné')]
liste_mesure_independance_fonctionnelle = [('1', 'Aide totale - 1'),('2', 'Aide maximale - 2'),('3', 'Aide moyenne - 3'),
                                           ('4', 'Aide minimale - 4'),('5', 'Dépense modifiée - 5'),('6', 'Indépendance modifiée - 6'),
                                           ('7', 'Indépendance complete - 7')]

class MzKineDemandeTraitement(models.Model):
    _name = 'mz.kine.demande.traitement'

    consultation_medical_id = fields.Many2one('mz.consultation.medical','Consultation médicale')
    patient_id = fields.Many2one('mz.patient','Patient')
    num_fiche = fields.Char(related='patient_id.numero_fiche', readonly=True, string='Numero de fiche')
    sexe = fields.Selection(related='patient_id.sexe', selection=liste_sexe, readonly=True, string='Sexe')
    age = fields.Char(related='patient_id.age', readonly=True, string='Age')
    date_naissance = fields.Date(related='patient_id.date_naissance', readonly=True, string='Date naissance')
    etat_civile = fields.Selection(related='patient_id.etat_civile', selection=liste_etat_civile, readonly=True, string='Etat civile')
    telephone = fields.Char(related='patient_id.phone', readonly=True, string='Téléphone')
    # socièté et catégorie
    avenue = fields.Char(related='patient_id.avenue', readonly=True, string='Avenue')
    quartier = fields.Char(related='patient_id.quartier', readonly=True, string='Quartier')
    contrat = fields.Selection(related='patient_id.contrat', selection=liste_contrat_patient, readonly=True, string='Contrat')
    profession_id = fields.Many2one(related='patient_id.profession_id', relation='mz.profession', readonly=True, string='Profession')
    commune_id = fields.Many2one(related='patient_id.commune_id', relation='mz.commune', readonly=True, string='Commune')
    traitement_prescris_id = fields.Many2one('mz.acte','Traitement prescris')
    nombre_seances = fields.Integer('Nombre de séances')
    observation_medecin = fields.Text('Observation Medecin')
    demande_par = fields.Many2one('mz.medecin','Demandé par')
    date_demande = fields.Datetime('Date demande')
    state = fields.Selection([('nouveau', 'Nouveau'),('valide', 'Valide'),('prise_en_charge', 'Prise en charge')], 'Etat', default = 'nouveau')

    @api.model
    def create(self, vals):

        this_now = datetime.now()
        this_date = this_now.strftime('%Y-%m-%d %H:%M:%S')
        vals['patient_id'] = self.env['mz.consultation.medical'].browse(vals.get('consultation_medical_id')).patient_id.id
        vals['demande_par'] = self.env['mz.medecin'].utilisateur_en_cours().id
        vals['date_demande'] = this_date
        return super(MzKineDemandeTraitement, self).create(vals)

    def name_get(self):
        result = []
        for record in self:
            if record.patient_id.prenom:
                result.append((record.id, "{} {}".format(record.patient_id.partner_id.name, record.patient_id.prenom)))
            else:
                result.append((record.id, record.patient_id.partner_id.name))
        return result

    def valider(self):
        self.state = 'valide'

    def prendre_en_charge(self):
        self.state = 'prise_en_charge'

        # this_now = datetime.now()
        # this_date = this_now.strftime('%Y-%m-%d %H:%M:%S')
        # Il faut date debut

        dossier_patient_kine = self.env['mz.kine.dossier.patient'].create({'patient_id': self.patient_id.id, 'demande_traitement_id': self.id})
        res_id = dossier_patient_kine.id
        view_id = self.env.ref('mz_medical_mokuwa.view_kine_dossier_patient_form').id

        return {
            'name': 'Dossier patient kiné',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [view_id],
            'res_model': 'mz.kine.dossier.patient',
            'type': 'ir.actions.act_window',
            'res_id': res_id,
            'nodestroy': True,
            'target': 'current',
            'context': {},
            }


class MzKineDossierPatient(models.Model):
    _name = 'mz.kine.dossier.patient'

    demande_traitement_id = fields.Many2one('mz.kine.demande.traitement','demande traitement')
    # renseignements socio-administratifs
    patient_id = fields.Many2one('mz.patient','Patient')
    num_fiche = fields.Char(related='patient_id.numero_fiche', readonly=True, string='Numero de fiche')
    sexe = fields.Selection(related='patient_id.sexe', selection=liste_sexe, readonly=True, string='Sexe')
    age = fields.Char(related='patient_id.age', readonly=True, string='Age')
    date_naissance = fields.Date(related='patient_id.date_naissance', readonly=True, string='Date naissance')
    etat_civile = fields.Selection(related='patient_id.etat_civile', selection=liste_etat_civile, readonly=True, string='Etat civile')
    telephone = fields.Char(related='patient_id.phone', readonly=True, string='Téléphone')
    # socièté et catégorie
    avenue = fields.Char(related='patient_id.avenue', readonly=True, string='Avenue')
    quartier = fields.Char(related='patient_id.quartier', readonly=True, string='Quartier')
    contrat = fields.Selection(related='patient_id.contrat', selection=liste_contrat_patient, readonly=True, string='Contrat')
    profession_id = fields.Many2one(related='patient_id.profession_id', relation='mz.profession', readonly=True, string='Profession')
    commune_id = fields.Many2one(related='patient_id.commune_id', relation='mz.commune', readonly=True, string='Commune')

    # Renseignements medico-techniques
    motif_consultation_id = fields.Many2one('mz.kine.motif.consultation','Motif consultation')
    anamnese = fields.Text('Anamnèse')
    antecedent_familiaux_ids = fields.Many2many(related='patient_id.antecedent_familiaux_ids', relation='mz.med.antecedent', string='Antécédents familiaux', domain="[('type', '=', 'familial')]")
    antecedent_medicaux_ids = fields.Many2many(related='patient_id.antecedent_medicaux_ids', relation='mz.med.antecedent', string='Antécédents medicaux', domain="[('type', '=', 'medical')]")
    antecedent_chirurgicaux_ids = fields.Many2many(related='patient_id.antecedent_chirurgicaux_ids', relation='mz.med.antecedent', string='Antécédents chirurgicaux', domain="[('type', '=', 'chirurgical')]")
    allergiques = fields.Text('Allergiques')
    diagnostic_medical_id = fields.Many2one('mz.kine.diagnostic.medical','Diagnostic médical')

    resultats_examens_para_cliniques = fields.Text('Résultats des examens para cliniques')
    traitement_en_cours = fields.Char('Traitement en cours', size=255)
    prescription_medicale_trait_kine = fields.Char('Prescription medicale traitement kiné', size=255)
    medecin_prescripteur = fields.Char('Médecin prescripteur', size=255)
    structure_prescription = fields.Char('Structure prescription', size=255)
    service_prescription = fields.Char('Service prescription', size=255)
    attentes_patient = fields.Text('Attentes du patient')
    examen_kine_ids = fields.Many2many('mz.kine.examen','mz_kine_dossier_patient_examen_rel','dossier_patient_id','examen_id','Examen kinésitherapique')

    consignes_particulieres = fields.Text('Consignes particulières')
    bilan = fields.Text('Bilan')
    diagnostic_kine = fields.Text('Diagnostic kinesitherapique')

    transfert = fields.Selection([('Oui','Oui'),('Non','Non')], 'Transfert')
    lieu_transfert = fields.Char('Lieu transfert', size=255)
    referencement = fields.Selection([('Oui','Oui'),('Non','Non')], 'Référencement')
    motif_referencement = fields.Char('Motif référencement', size=255)
    lieu_referencement = fields.Char('Lieu référencement', size=255)

    directives_traitement = fields.Text('Directives de traitement')

    objectif_prise_encharge_court_terme = fields.Text('Objectif prise en charge court terme')
    objectif_prise_encharge_moyen_terme = fields.Text('Objectif prise en charge moyen terme')
    objectif_prise_encharge_fin_traitement = fields.Text('Objectif prise en charge fin traitement')

    # Traitement kinesitherapique
    nombre_seances_prevues = fields.Integer('Nombre de séances prévues')
    traitement_line_ids = fields.One2many('mz.kine.traitement','kine_dossier_id','Traitements')
    evaluation_globale = fields.Text('Evaluation globale')
    noms_theurapeute = fields.Many2one('mz.medecin','Noms du thérapeute')
    correspondance_prof = fields.Char('Correspondance professionnelle')



    def evaluation_deficiences(self):
        
        mod_obj = self.env['ir.model.data']
        res = mod_obj.get_object_reference('mz_medical_mokuwa', 'view_kine_evaluation_deficiences_form')
        view_id = res and res[1] or False,
        view_id = view_id[0]

        evaluation_deficiences = self.env['mz.kine.evaluation.deficiences'].search([('dossier_patient_kine_id','=',self.id)])    
        if evaluation_deficiences:
            res_id = evaluation_deficiences[0].id
        else:
            evaluation_deficiences = self.env['mz.kine.evaluation.deficiences'].create({'dossier_patient_kine_id': self.id})
            res_id = evaluation_deficiences.id

        return {
                'name': 'Evaluation déficiences',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mz.kine.evaluation.deficiences',
                'view_id': [view_id],
                'type': 'ir.actions.act_window',
                'res_id': res_id,
                'context': {},
                'target': 'new',
                # 'nodestroy': True,
            }

    def evaluation_capa_fonctionnelles(self):
        
        mod_obj = self.env['ir.model.data']
        res = mod_obj.get_object_reference('mz_medical_mokuwa', 'view_kine_evaluation_capa_fonctionnelles_form')
        view_id = res and res[1] or False,
        view_id = view_id[0]

        evaluation_capa_fonctionnelles = self.env['mz.kine.evaluation.capacites.fonctionnelles'].search([('dossier_patient_kine_id','=',self.id)])    
        if evaluation_capa_fonctionnelles:
            res_id = evaluation_capa_fonctionnelles[0].id
        else:
            evaluation_capa_fonctionnelles = self.env['mz.kine.evaluation.capacites.fonctionnelles'].create({'dossier_patient_kine_id': self.id})
            res_id = evaluation_capa_fonctionnelles.id

        return {
                'name': 'Evaluation des capacités fonctionnelles',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mz.kine.evaluation.capacites.fonctionnelles',
                'view_id': [view_id],
                'type': 'ir.actions.act_window',
                'res_id': res_id,
                'context': {},
                'target': 'new',
                # 'nodestroy': True,
            }

    def name_get(self):
        result = []
        for record in self:
            if record.patient_id.prenom:
                result.append((record.id, "{} {}".format(record.patient_id.partner_id.name, record.patient_id.prenom)))
            else:
                result.append((record.id, record.patient_id.partner_id.name))
        return result

class MzKineEvaluationDeficiences(models.Model):

    _name = 'mz.kine.evaluation.deficiences'
    _description = 'Evaluation deficiences'
    
    dossier_patient_kine_id = fields.Many2one('mz.kine.dossier.patient','Consultation médical')
    evaluation_deficiences_line_ids = fields.One2many('mz.kine.evaluation.deficiences.line','evaluation_deficiences_id','Evaluation déficience line')
    # state = fields.Selection([('nouveau', 'Nouveau'),('acheve', 'Acheve')], 'Etat', default = 'nouveau')

    def write_success(self):
        return True

class MzKineEvaluationDeficiencesLine(models.Model):

    _name = 'mz.kine.evaluation.deficiences.line'
    _description = 'Evaluation deficiences line'
    
    name = fields.Char('Initiale', size=255)
    date = fields.Date('Date', default=datetime.today())
    evaluation_deficiences_id = fields.Many2one('mz.kine.evaluation.deficiences','Evaluation déficience')


class MzKineEvaluationCapacitesFonctionnelles(models.Model):

    _name = 'mz.kine.evaluation.capacites.fonctionnelles'
    _description = 'Evaluation capacites fonctionnelles'
    
    dossier_patient_kine_id = fields.Many2one('mz.kine.dossier.patient','Consultation médical')
    alimentation_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Alimentation entrée')
    alimentation_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Alimentation séjour')
    alimentation_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Alimentation sortie')
    alimentation_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Alimentation suivi')

    soins_apparence_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Soins de l\'apparence entrée')
    soins_apparence_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Soins de l\'apparence séjour')
    soins_apparence_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Soins de l\'apparence sortie')
    soins_apparence_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Soins de l\'apparence suivi')

    toilette_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Toilette entrée')
    toilette_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Toilette séjour')
    toilette_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Toilette sortie')
    toilette_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Toilette suivi')

    habillage_partie_sup_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Habillage partie supérieure entrée')
    habillage_partie_sup_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Habillage partie supérieure séjour')
    habillage_partie_sup_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Habillage partie supérieure sortie')
    habillage_partie_sup_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Habillage partie supérieure suivi')

    habillage_partie_inf_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Habillage partie inférieure entrée')
    habillage_partie_inf_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Habillage partie inférieure séjour')
    habillage_partie_inf_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Habillage partie inférieure sortie')
    habillage_partie_inf_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Habillage partie inférieure suivi')

    utilisatioon_toilette_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Utilisatioon des toilettes entrée')
    utilisatioon_toilette_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Utilisatioon des toilettes séjour')
    utilisatioon_toilette_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Utilisatioon des toilettes sortie')
    utilisatioon_toilette_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Utilisatioon des toilettes suivi')

    vessie_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Vessie entrée')
    vessie_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Vessie séjour')
    vessie_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Vessie sortie')
    vessie_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Vessie suivi')

    intestin_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Intestin entrée')
    intestin_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Intestin séjour')
    intestin_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Intestin sortie')
    intestin_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Intestin suivi')

    mobilite_lit_chaisse_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Mobilité (lit,chaisse, fauteuil roulant) entrée')
    mobilite_lit_chaisse_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Mobilité (lit,chaisse, fauteuil roulant) séjour')
    mobilite_lit_chaisse_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Mobilité (lit,chaisse, fauteuil roulant) sortie')
    mobilite_lit_chaisse_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Mobilité (lit,chaisse, fauteuil roulant) suivi')

    mobilite_wc_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Mobilite (W.C) entrée')
    mobilite_wc_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Mobilité (W.C) séjour')
    mobilite_wc_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Mobilité (W.C) sortie')
    mobilite_wc_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Mobilité (W.C) suivi')

    mobilite_baignoire_douche_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Mobilité (Baignoire, douche) entrée')
    mobilite_baignoire_douche_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Mobilité (Baignoire, douche) séjour')
    mobilite_baignoire_douche_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Mobilité (Baignoire, douche) sortie')
    mobilite_baignoire_douche_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Mobilité (Baignoire, douche) suivi')

    locomotion_marche_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Locomotion (Marche) entrée')
    locomotion_marche_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Locomotion (Marche) séjour')
    locomotion_marche_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Locomotion (Marche) sortie')
    locomotion_marche_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Locomotion (Marche) suivi')

    locomotion_fauteuil_roulant_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Locomotion (Fauteuil roulant) entrée')
    locomotion_fauteuil_roulant_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Locomotion (Fauteuil roulant) séjour')
    locomotion_fauteuil_roulant_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Locomotion (Fauteuil roulant) sortie')
    locomotion_fauteuil_roulant_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Locomotion (Fauteuil roulant) suivi')

    locomotion_toilette_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Locomotion (Toilette) entrée')
    locomotion_toilette_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Locomotion (Toilette) séjour')
    locomotion_toilette_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Locomotion (Toilette) sortie')
    locomotion_toilette_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Locomotion (Toilette) suivi')

    communication_comprehension_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Comprehension) entrée')
    communication_comprehension_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Comprehension) séjour')
    communication_comprehension_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Comprehension) sortie')
    communication_comprehension_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Comprehension) suivi')

    communication_expression_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Expression) entrée')
    communication_expression_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Expression) séjour')
    communication_expression_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Expression) sortie')
    communication_expression_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Expression) suivi')

    conscience_monde_ext_interaction_sociale_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Interactions sociales) entrée')
    conscience_monde_ext_interaction_sociale_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Interactions sociales) séjour')
    conscience_monde_ext_interaction_sociale_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Interactions sociales) sortie')
    conscience_monde_ext_interaction_sociale_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Interactions sociales) suivi')

    conscience_resolution_pb_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Résolution des problèmes) entrée')
    conscience_resolution_pb_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Résolution des problèmes) séjour')
    conscience_resolution_pb_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Résolution des problèmes) sortie')
    conscience_resolution_pb_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (Résolution des problèmes) suivi')

    conscience_memoire_entree = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (mémoire) entrée')
    conscience_memoire_sejour = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (mémoire) séjour')
    conscience_memoire_sortie = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (mémoire) sortie')
    conscience_memoire_suivi = fields.Selection(liste_mesure_independance_fonctionnelle, 'Communication (mémoire) suivi')

    total_entree = fields.Char('Total entrée', size=10, store=True, compute='_compute_total_entree')
    total_sejour = fields.Char('Total séjour', size=10, store=True, compute='_compute_total_sejour')
    total_sortie = fields.Char('Total sortie', size=10, store=True, compute='_compute_total_sortie')
    total_suivi = fields.Char('Total suivi', size=10, store=True, compute='_compute_total_suivi')
    # state = fields.Selection([('nouveau', 'Nouveau'),('acheve', 'Acheve')], 'Etat', default = 'nouveau')

    def write_success(self):
        return True

    @api.depends('alimentation_entree','soins_apparence_entree','toilette_entree','habillage_partie_sup_entree','habillage_partie_inf_entree','utilisatioon_toilette_entree','vessie_entree','intestin_entree','mobilite_lit_chaisse_entree','mobilite_wc_entree','mobilite_baignoire_douche_entree','locomotion_marche_entree','locomotion_fauteuil_roulant_entree','locomotion_toilette_entree','communication_comprehension_entree','communication_expression_entree','conscience_monde_ext_interaction_sociale_entree','conscience_resolution_pb_entree','conscience_memoire_entree')
    def _compute_total_entree(self):
        tot1 = int(self.alimentation_entree) + int(self.soins_apparence_entree) + int(self.toilette_entree) + int(self.habillage_partie_sup_entree) + int(self.habillage_partie_inf_entree) + int(self.utilisatioon_toilette_entree) + int(self.vessie_entree) + int(self.intestin_entree)
        tot2 = int(self.mobilite_lit_chaisse_entree) + int(self.mobilite_wc_entree) + int(self.mobilite_baignoire_douche_entree)
        tot3 = int(self.locomotion_marche_entree) + int(self.locomotion_fauteuil_roulant_entree) + int(self.locomotion_toilette_entree)
        tot4 = int(self.communication_comprehension_entree) + int(self.communication_expression_entree)
        tot5 = int(self.conscience_monde_ext_interaction_sociale_entree) + int(self.conscience_resolution_pb_entree) + int(self.conscience_memoire_entree)
        self.total_entree = tot1 + tot2 + tot3 + tot4 + tot5

    @api.depends('alimentation_sejour','soins_apparence_sejour','toilette_sejour','habillage_partie_sup_sejour','habillage_partie_inf_sejour','utilisatioon_toilette_sejour','vessie_sejour','intestin_sejour','mobilite_lit_chaisse_sejour','mobilite_wc_sejour','mobilite_baignoire_douche_sejour','locomotion_marche_sejour','locomotion_fauteuil_roulant_sejour','locomotion_toilette_sejour','communication_comprehension_sejour','communication_expression_sejour','conscience_monde_ext_interaction_sociale_sejour','conscience_resolution_pb_sejour','conscience_memoire_sejour')
    def _compute_total_sejour(self):
        tot1 = int(self.alimentation_sejour) + int(self.soins_apparence_sejour) + int(self.toilette_sejour) + int(self.habillage_partie_sup_sejour) + int(self.habillage_partie_inf_sejour) + int(self.utilisatioon_toilette_sejour) + int(self.vessie_sejour) + int(self.intestin_sejour)
        tot2 = int(self.mobilite_lit_chaisse_sejour) +int( self.mobilite_wc_sejour) + int(self.mobilite_baignoire_douche_sejour)
        tot3 = int(self.locomotion_marche_sejour) + int(self.locomotion_fauteuil_roulant_sejour) + int(self.locomotion_toilette_sejour)
        tot4 = int(self.communication_comprehension_sejour) + int(self.communication_expression_sejour)
        tot5 = int(self.conscience_monde_ext_interaction_sociale_sejour) + int(self.conscience_resolution_pb_sejour) + int(self.conscience_memoire_sejour)
        self.total_sejour = tot1 + tot2 + tot3 + tot4 + tot5

    @api.depends('alimentation_sortie','soins_apparence_sortie','toilette_sortie','habillage_partie_sup_sortie','habillage_partie_inf_sortie','utilisatioon_toilette_sortie','vessie_sortie','intestin_sortie','mobilite_lit_chaisse_sortie','mobilite_wc_sortie','mobilite_baignoire_douche_sortie','locomotion_marche_sortie','locomotion_fauteuil_roulant_sortie','locomotion_toilette_sortie','communication_comprehension_sortie','communication_expression_sortie','conscience_monde_ext_interaction_sociale_sortie','conscience_resolution_pb_sortie','conscience_memoire_sortie')
    def _compute_total_sortie(self):
        tot1 = int(self.alimentation_sortie) + int(self.soins_apparence_sortie) + int(self.toilette_sortie) + int(self.habillage_partie_sup_sortie) + int(self.habillage_partie_inf_sortie) + int(self.utilisatioon_toilette_sortie) + int(self.vessie_sortie) + int(self.intestin_sortie)
        tot2 = int(self.mobilite_lit_chaisse_sortie) + int(self.mobilite_wc_sortie) + int(self.mobilite_baignoire_douche_sortie)
        tot3 = int(self.locomotion_marche_sortie) + int(self.locomotion_fauteuil_roulant_sortie) + int(self.locomotion_toilette_sortie)
        tot4 = int(self.communication_comprehension_sortie) + int(self.communication_expression_sortie)
        tot5 = int(self.conscience_monde_ext_interaction_sociale_sortie) + int(self.conscience_resolution_pb_sortie) + int(self.conscience_memoire_sortie)
        self.total_sortie = tot1 + tot2 + tot3 + tot4 + tot5

    @api.depends('alimentation_suivi','soins_apparence_suivi','toilette_suivi','habillage_partie_sup_suivi','habillage_partie_inf_suivi','utilisatioon_toilette_suivi','vessie_suivi','intestin_suivi','mobilite_lit_chaisse_suivi','mobilite_wc_suivi','mobilite_baignoire_douche_suivi','locomotion_marche_suivi','locomotion_fauteuil_roulant_suivi','locomotion_toilette_suivi','communication_comprehension_suivi','communication_expression_suivi','conscience_monde_ext_interaction_sociale_suivi','conscience_resolution_pb_suivi','conscience_memoire_suivi')
    def _compute_total_suivi(self):
        tot1 = int(self.alimentation_suivi) + int(self.soins_apparence_suivi) + int(self.toilette_suivi) + int(self.habillage_partie_sup_suivi) + int(self.habillage_partie_inf_suivi) + int(self.utilisatioon_toilette_suivi) + int(self.vessie_suivi) + int(self.intestin_suivi)
        tot2 = int(self.mobilite_lit_chaisse_suivi) + int(self.mobilite_wc_suivi) + int(self.mobilite_baignoire_douche_suivi)
        tot3 = int(self.locomotion_marche_suivi) + int(self.locomotion_fauteuil_roulant_suivi) + int(self.locomotion_toilette_suivi)
        tot4 = int(self.communication_comprehension_suivi) + int(self.communication_expression_suivi)
        tot5 = int(self.conscience_monde_ext_interaction_sociale_suivi) + int(self.conscience_resolution_pb_suivi) + int(self.conscience_memoire_suivi)
        self.total_suivi = tot1 + tot2 + tot3 + tot4 + tot5

class MzKineTraitement(models.Model):
    _name = 'mz.kine.traitement'

    @api.model
    def _get_partner(self):
        return self.env['res.partner'].utilisateur_en_cours()

    date_seance_kine = fields.Date('Date séance kiné', default=datetime.today())
    evolution = fields.Text('Evolution')
    traitement = fields.Text('Traitement/Technique')
    observations = fields.Text('Observations')
    noms_kine = fields.Many2one('res.partner','Noms kiné', default=_get_partner)
    kine_dossier_id = fields.Many2one('mz.kine.dossier.patient','Traitement')


# class MzKineTraitement(models.Model):
#     _name = 'mz.kine.traitement'

#     nombre_seances_prevues = fields.Integer('Nombre de séances prévues')
#     traitement_line_ids = fields.One2many('mz.kine.traitement.line','traitement_id','Traitement line')
#     patient_id = fields.Many2one('mz.patient','Patient')
#     num_fiche = fields.Char('N° fiche', size=20)
#     evaluation_globale = fields.Text('Evaluation globale')
#     noms_theurapeute = fields.Many2one('mz.medecin','Demandé par')
#     correspondance_prof = fields.Char('Correspondance professionnelle')


# class MzKineTraitementLine(models.Model):
#     _name = 'mz.kine.traitement.line'

#     date_seance_kine = fields.Date('Date séance kiné')
#     evolution = fields.Text('Evolution')
#     traitement = fields.Text('Traitement/Technique')
#     observations = fields.Text('Observations')
#     noms_kine = fields.Many2one('mz.medecin','Noms kiné')
#     traitement_id = fields.Many2one('mz.kine.traitement','Traitement')


class MzKineMotifConsultation(models.Model):
    _name = 'mz.kine.motif.consultation'

    name = fields.Char('Mofif consultation', size=100)

class MzKineExamen(models.Model):
    _name = 'mz.kine.examen'

    name = fields.Char('Examen', size=100)

class MzKineDiagnosticMedical(models.Model):
    _name = 'mz.kine.diagnostic.medical'

    name = fields.Char('Diagnostic médical', size=150)
