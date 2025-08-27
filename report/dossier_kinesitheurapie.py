# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo import tools
from odoo.exceptions import UserError


class MzDosmedKineReadaptation(models.Model):
    _name = 'mz.dosmed.kine.readaptation'
    _description = "Dossier kine-readaptation"
    _auto = False
    _order = 'kine_dossier_id desc'

    kine_dossier_id = fields.Char('Id kine dossier',size=15)
    detail = fields.Html(u'Detail', compute='_get_detail')
    nombre_seances_prevues = fields.Integer('Nombre de séances prévues')
    noms_theurapeute = fields.Many2one('mz.medecin','Noms du thérapeute')

    @api.depends('kine_dossier_id')
    def _get_detail(self):
        for record in self:
            kine_dossier_id = int(record.kine_dossier_id)
            kine_dossier_obj = self.env['mz.kine.dossier.patient'].browse(kine_dossier_id)

            motif_consultation = kine_dossier_obj.motif_consultation_id.name if kine_dossier_obj.motif_consultation_id else ''
            anamnese = kine_dossier_obj.anamnese if kine_dossier_obj.anamnese else ''

            antecedants = self._get_antecedents(kine_dossier_obj)

            diagnostic_medical = kine_dossier_obj.diagnostic_medical_id.name if kine_dossier_obj.diagnostic_medical_id else ''
            resultats_examens_para_cliniques = kine_dossier_obj.resultats_examens_para_cliniques if kine_dossier_obj.resultats_examens_para_cliniques else ''
            traitement_en_cours = kine_dossier_obj.traitement_en_cours if kine_dossier_obj.traitement_en_cours else ''
            medecin_prescripteur = kine_dossier_obj.medecin_prescripteur if kine_dossier_obj.medecin_prescripteur else ''

            structure_prescription = kine_dossier_obj.structure_prescription if kine_dossier_obj.structure_prescription else ''
            service_prescription = kine_dossier_obj.service_prescription if kine_dossier_obj.service_prescription else ''
            attentes_patient = kine_dossier_obj.attentes_patient if kine_dossier_obj.attentes_patient else ''

            evaluation_deficiences = self._get_evaluation_deficiences(kine_dossier_id)
            evaluation_capacites_fonctionnelles = self._get_evaluation_capacites_fonctionnelles(kine_dossier_id)

            consignes_particulieres = kine_dossier_obj.consignes_particulieres if kine_dossier_obj.consignes_particulieres else ''
            diagnostic_kine = kine_dossier_obj.diagnostic_kine if kine_dossier_obj.diagnostic_kine else ''

            orientation_patient = self._get_orientation_patient(kine_dossier_obj)

            directives_traitement = kine_dossier_obj.directives_traitement if kine_dossier_obj.directives_traitement else ''
            objectif_prise_encharge_court_terme = kine_dossier_obj.objectif_prise_encharge_court_terme if kine_dossier_obj.objectif_prise_encharge_court_terme else ''
            objectif_prise_encharge_moyen_terme = kine_dossier_obj.objectif_prise_encharge_moyen_terme if kine_dossier_obj.objectif_prise_encharge_moyen_terme else ''
            objectif_prise_encharge_fin_traitement = kine_dossier_obj.objectif_prise_encharge_fin_traitement if kine_dossier_obj.objectif_prise_encharge_fin_traitement else ''
            nombre_seances_prevues = str(kine_dossier_obj.nombre_seances_prevues) if kine_dossier_obj.nombre_seances_prevues else ''

            traitement_kinesitherapique = self._get_traitement_kinesitherapique(kine_dossier_obj)
            evaluation_globale = kine_dossier_obj.evaluation_globale if kine_dossier_obj.evaluation_globale else ''

            detail = '''
                        
                <div class="row">   
                    <div class="col-lg-9">

                        <h2>RENSEIGNEMENTS MEDICO-TECHNIQUES </h2>
                        <br/>

                        <div style="margin-left:20px;">
                            
                            <h5>Motifs de consultation :</h5>	
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + motif_consultation + ''' </td>
                                </tr>
                            </table>
                            
                            <br/>
                            <h5>Anamnèse :</h5>	
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + anamnese + ''' </td>
                                </tr>
                            </table>

                            <br/>
                            <h5>Antécédents :</h5>
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + antecedants + ''' </td>
                                </tr>
                            </table>

                            <br/>
                            <h5>Diagnostic médical :</h5>	
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + diagnostic_medical + ''' </td>
                                </tr>
                            </table>

                            <br/>
                            <h5>Résultats des examens para cliniques (imagerie, explorations fonctionnelles, biologiques etc.) :</h5>	
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + resultats_examens_para_cliniques + ''' </td>
                                </tr>
                            </table>

                            <br/>
                            <h5>Traitement(s) médical en cours :</h5>	
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + traitement_en_cours + ''' </td>
                                </tr>
                            </table>


                            <br/>
                            <h5>Prescription médicale du traitement kinésithérapique :</h5>	
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + traitement_en_cours + ''' </td>
                                </tr>
                            </table>

                            <br/>
                            <h5>Médecin prescripteur :</h5>	
                            <table>
                                <tr>
                                    <td colspan="2" style="width:920;height:25px;"> ''' + medecin_prescripteur + ''' </td>
                                </tr>
                                <tr>
                                    <td>Structure : </td>
                                    <td style="width:920;height:25px;"> ''' + structure_prescription + ''' </td>
                                </tr>
                                <tr>
                                    <td>Service : </td>
                                    <td style="width:920;height:25px;"> ''' + service_prescription + ''' </td>
                                </tr>
                            </table>

                            <hr/><h3>ATTENTES DU PATIENT OU DES SES PROCHES </h3>
                            <br/>
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + attentes_patient + ''' </td>
                                </tr>
                            </table>

                            <hr/><h5>Evaluation des déficiences </h5>
                            <br/>
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + evaluation_deficiences + ''' </td>
                                </tr>
                            </table>

                            <h5>Evaluation des capacités fonctionnelles (MIF)</h5>
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + evaluation_capacites_fonctionnelles + ''' </td>
                                </tr>
                            </table>

                            <h5>Consignes particulières :</h5>	
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + consignes_particulieres + ''' </td>
                                </tr>
                            </table>

                            <h5>Diagnostic kinésithérapique :</h5>	
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + diagnostic_kine + ''' </td>
                                </tr>
                            </table>

                            <h5>Orientation du patient :</h5>	
                            <table style="margin-left:10px;margin-top:10px;">
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + orientation_patient + ''' </td>
                                </tr>
                            </table>

                        </div>

                        <hr/><h2>DIRECTIVES DE TRAITEMENT </h2>
                        <br/>
                        
                        <div style="margin-left:20px;">

                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + directives_traitement + ''' </td>
                                </tr>
                            </table>
                            <br/>

                            <h3>OBJECTIFS DE LA PRISE EN CHARGE KINESITHERAPIQUE </h3>	
                            <h5>Objectif(s) à court terme :</h5>	
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + objectif_prise_encharge_court_terme + ''' </td>
                                </tr>
                            </table>

                            <h5>Objectif(s) à moyen terme :</h5>	
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + objectif_prise_encharge_moyen_terme + ''' </td>
                                </tr>
                            </table>

                            <h5>Objectif(s) de fin traitement ou sortie d'établissement :</h5>	
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + objectif_prise_encharge_fin_traitement + ''' </td>
                                </tr>
                            </table>

                            <hr/><h2>TRAITEMENT KINESITHERAPIQUE </h2>
                            <br/>
                            <table>
                                <tr>
                                    <td>Le temps préconisé pour le suivi thérapeutique (nombre de séances prévues) : </td><td> ''' + nombre_seances_prevues + ''' </td>
                                </tr>
                            </table>
                            <br/>
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + traitement_kinesitherapique + ''' </td>
                                </tr>
                            </table>

                            <hr/><h2>EVALUATION GLOBALE EN FIN DE TRAITEMENT </h2>
                            <table>
                                <tr>
                                    <td style="width:920;height:25px;"> ''' + evaluation_globale + ''' </td>
                                </tr>
                            </table>
                            <br/>

                            <br/>

                        </div>
                                
                    </div>
                </div>
                
                        '''
                        
            record.detail = detail

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
                SELECT MIN(ki.id) as id,
                    ki.id as kine_dossier_id,
                    ki.nombre_seances_prevues,
                    ki.noms_theurapeute
                FROM mz_kine_dossier_patient ki
                GROUP BY ki.id 
                    )"""%(self._table))
        
    
    def _get_antecedents(self, kine_dossier_obj):

        antecedent_familiaux_ids = ''
        antecedent_medicaux_ids = ''
        antecedent_chirurgicaux_ids = ''
        i = 0
        for antecedent_familial in kine_dossier_obj.antecedent_familiaux_ids:
            antecedent_familiaux_ids += antecedent_familial.name if i == 0 else ', ' + antecedent_familial.name
            i += 1

        i = 0
        for antecedent_medical in kine_dossier_obj.antecedent_medicaux_ids:
            antecedent_medicaux_ids += antecedent_medical.name if i == 0 else ', ' + antecedent_medical.name
            i += 1

        i = 0
        for antecedent_chirurgical in kine_dossier_obj.antecedent_chirurgicaux_ids:
            antecedent_chirurgicaux_ids += antecedent_chirurgical.name if i == 0 else ', ' + antecedent_chirurgical.name
            i += 1

        allergiques = kine_dossier_obj.allergiques if kine_dossier_obj.allergiques else ''

        antecedents_str = '<ul><li>médicaux : ' + antecedent_medicaux_ids + '</li><li>chirurgicaux : ' + antecedent_chirurgicaux_ids + '</li><li>familiaux : ' + antecedent_familiaux_ids + '</li><li>allergiques : ' + allergiques + '</li></ul>'

        return antecedents_str
    
    def _get_evaluation_deficiences(self, kine_dossier_id):

        evaluation_deficiences_obj = self.env['mz.kine.evaluation.deficiences']
        evaluation_deficiences_str = ' '

        evaluation_deficiences_objs = evaluation_deficiences_obj.search([('dossier_patient_kine_id','=',kine_dossier_id)])
        if evaluation_deficiences_objs:
            evaluation_deficiences_str += '<table class="table"><tr><td><b>Initiale</b> </td><td><b>Date</b> </td></tr>'
            for evaluation_deficiences_line in evaluation_deficiences_objs[0].evaluation_deficiences_line_ids:
                initale = evaluation_deficiences_line.name if evaluation_deficiences_line.name else ''
                date = evaluation_deficiences_line.date.strftime('%d/%m/%Y') if evaluation_deficiences_line.date else ''
                evaluation_deficiences_str += '<tr><td>' + initale + '</td><td>' + date + '</td></tr>'
            evaluation_deficiences_str += '</table>'

        return evaluation_deficiences_str
    
    def _get_evaluation_capacites_fonctionnelles(self, kine_dossier_id):

        evaluation_deficiences_obj = self.env['mz.kine.evaluation.deficiences']
        evaluation_deficiences_str = ''

        return evaluation_deficiences_str
    
    def _get_orientation_patient(self, kine_dossier_obj):

        transfert = kine_dossier_obj.transfert if kine_dossier_obj.transfert else ''
        lieu_transfert = kine_dossier_obj.lieu_transfert if kine_dossier_obj.lieu_transfert else ''
        referencement = kine_dossier_obj.referencement if kine_dossier_obj.referencement else ''
        motif_referencement = kine_dossier_obj.motif_referencement if kine_dossier_obj.motif_referencement else ''
        lieu_referencement = kine_dossier_obj.lieu_referencement if kine_dossier_obj.lieu_referencement else ''

        orientation_patient_str = '<table class="table"><tr><td><b>A base communautaire</b></td> <td><b>Hospitalisation</b></td> <td><b>Ambulatoire</b></td> </tr>'
        orientation_patient_str += '<tr><td>Transfert : ' + transfert + '</td><td colspan="2">Référencement : ' + referencement + '</td> </tr>'
        orientation_patient_str += '<tr><td>Lieu : ' + lieu_transfert + '</td><td colspan="2">Motif : ' + motif_referencement + ' <br/> Lieu : ' + lieu_referencement + '</td> </tr>'
        orientation_patient_str += '</table>'

        return orientation_patient_str
    

    def _get_traitement_kinesitherapique(self, kine_dossier_obj):

        traitement_kinesitherapique_str = '<table class="table"><tr><td><b>Date Séance kiné</b></td> <td><b>Evolution</b></td> <td><b>Traitement/Technique</b></td> <td><b>Observations</b></td> <td><b>Noms du kiné</b></td></tr>'
        for traitement_line in kine_dossier_obj.traitement_line_ids:
            date = traitement_line.date_seance_kine.strftime('%d/%m/%Y') if traitement_line.date_seance_kine else ''
            evolution = traitement_line.evolution if traitement_line.evolution else ''
            traitement = traitement_line.traitement if traitement_line.traitement else ''
            observations = traitement_line.observations if traitement_line.observations else ''
            noms_kine = traitement_line.noms_kine.name if traitement_line.noms_kine else ''
            
            traitement_kinesitherapique_str += '<tr><td>' + date + '</td><td>' + evolution + '</td><td>' + traitement + '</td><td>' + observations + '</td><td>' + noms_kine + '</td> </tr>'
        traitement_kinesitherapique_str += '</table>'

        return traitement_kinesitherapique_str


    # def name_get(self):
    #     result = []
    #     for record in self:
    #         if record.patient_id.prenom:
    #             result.append((record.id, "{} {}".format(record.patient_id.partner_id.name, record.patient_id.prenom)))
    #         else:
    #             result.append((record.id, record.patient_id.partner_id.name))
    #     return result
