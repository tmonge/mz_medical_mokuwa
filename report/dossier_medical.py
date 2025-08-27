# -*- coding: utf-8 -*-
from odoo import models


class MzDosmedFicheAmbulatoire(models.Model):

    _inherit = "mz.dosmed.fiche.ambulatoire"

    def _get_consultation_specialiste(self, episode_medical_id):
        consultation_specialiste = super(MzDosmedFicheAmbulatoire, self)._get_consultation_specialiste(episode_medical_id)
        if consultation_specialiste == '':
            consultation_medical_objs = self.env['mz.consultation.medical'].search([('episode_medical_id','=',episode_medical_id)])
            if consultation_medical_objs:
                consultation_medical_obj = consultation_medical_objs[0]

                examen_radiologique = consultation_medical_obj.examen_radiologique if consultation_medical_obj.examen_radiologique else ''
                examen_complementaire = consultation_medical_obj.examen_complementaire if consultation_medical_obj.examen_complementaire else ''

                inspection = self._get_inspection(consultation_medical_obj.id)
                traitement = self._get_traitement(consultation_medical_obj.id)
                demande_traitement_kine = self._get_demande_traitement_kine(consultation_medical_obj.id)
      
                return '''

                    <hr/><h3>EXAMEN RADIOLOGIQUE </h3>
                    <br/>
                    <div class="row">
                        <div class="col-12">
                            ''' + examen_radiologique +'''
                        </div>
                    </div>

                    <hr/><h3>EXAMEN COMPLEMENTAIRE </h3>
                    <br/>
                    <div class="row">
                        <div class="col-12">
                            ''' + examen_complementaire +'''
                        </div>
                    </div>

                    <hr/><h3>INSPECTION </h3>
                    <br/>
                    <div style="margin-left:20px;">
                        ''' + inspection +'''
                    </div>

                    <hr/><h3>TRAITEMENT </h3>
                    <br/>
                    <div>
                        ''' + traitement +'''
                    </div>

                    <hr/><h3>DEMANDE TRAITEMENT KINESITHEURAPIE</h3>
                    <br/>
                    <div style="margin-left:20px;">
                        ''' + demande_traitement_kine +'''
                    </div>

                '''
            return ''
        else:
            return consultation_specialiste
        
    def _get_inspection(self, consultation_medical_id):

        inspection_str = ''

        consultation_medical_inspection_obj = self.env['mz.consultation.medical.inspection'].sudo().search([('consultation_medical_id','=',consultation_medical_id)])
        if consultation_medical_inspection_obj:

            rachis = consultation_medical_inspection_obj.rachis if consultation_medical_inspection_obj.rachis else ''
            epaule_membre_superieur = consultation_medical_inspection_obj.epaule_membre_superieur if consultation_medical_inspection_obj.epaule_membre_superieur else ''
            bassin_membre_inferieur = consultation_medical_inspection_obj.bassin_membre_inferieur if consultation_medical_inspection_obj.bassin_membre_inferieur else ''
            station_debout = consultation_medical_inspection_obj.station_debout if consultation_medical_inspection_obj.station_debout else ''
            deambulation = consultation_medical_inspection_obj.deambulation if consultation_medical_inspection_obj.deambulation else ''
            colonne_vertebrale = consultation_medical_inspection_obj.colonne_vertebrale if consultation_medical_inspection_obj.colonne_vertebrale else ''
            palpi_membres_superieurs = consultation_medical_inspection_obj.palpi_membres_superieurs if consultation_medical_inspection_obj.palpi_membres_superieurs else ''
            palpi_bassin_membre_inferieur = consultation_medical_inspection_obj.palpi_bassin_membre_inferieur if consultation_medical_inspection_obj.palpi_bassin_membre_inferieur else ''
            mensurations_longitudinales = consultation_medical_inspection_obj.mensurations_longitudinales if consultation_medical_inspection_obj.mensurations_longitudinales else ''
            mensurations_perimetriques = consultation_medical_inspection_obj.mensurations_perimetriques if consultation_medical_inspection_obj.mensurations_perimetriques else ''
            mobile_passive = consultation_medical_inspection_obj.mobile_passive if consultation_medical_inspection_obj.mobile_passive else ''

            stade_mobile_passive = ''
            i = 0
            for stade in consultation_medical_inspection_obj.stade_mobile_passive_ids:
                stade_mobile_passive += stade.name if i == 0 else ', ' + stade.name
                i += 1

            examen_sensibilite = consultation_medical_inspection_obj.examen_sensibilite if consultation_medical_inspection_obj.examen_sensibilite else ''
            examen_reflexes = consultation_medical_inspection_obj.examen_reflexes if consultation_medical_inspection_obj.examen_reflexes else ''

            inspection_str = '''
                <h4>Rachis :</h4>	
                <table>
                    <tr>
                        <td style="width:920;height:25px;"> ''' + rachis + ''' </td>
                    </tr>
                </table>
                
                <br/>
                <h4>Lépaule et le membre supérieur :</h4>
                <table>
                    <tr> <td> ''' + epaule_membre_superieur + ''' </td></tr>
                </table>

                <br/>
                <h4>Le bassin et les membres inférieurs :</h4>	
                <table>
                    <tr> <td> ''' + bassin_membre_inferieur + ''' </td></tr>
                </table>

                <br/>
                <h4>La station débout :</h4>	
                <table>
                    <tr> <td> ''' + station_debout + ''' </td></tr>
                </table>

                <br/>
                <h4>La déambulation :</h4>	
                <table>
                    <tr> <td> ''' + deambulation + ''' </td></tr>
                </table>

                <br/>
                <h4>PALPATION</h4>

                <div style="margin-left:20px;">
                    <br/>
                    <h5>La colonne vertébrale :</h5>
                    <table>
                        <tr> <td> ''' + colonne_vertebrale + ''' </td></tr>
                    </table>

                    <br/>
                    <h5>Les membre supérieurs :</h5>	
                    <table>
                        <tr> <td> ''' + palpi_membres_superieurs + ''' </td></tr>
                    </table>

                    <br/>
                    <h5>Le bassin et les membres inférieurs :</h5>	
                    <table>
                        <tr> <td> ''' + palpi_bassin_membre_inferieur + ''' </td></tr>
                    </table>
                </div>

                <br/>
                <h4>MENSURATIONS</h4>

                <div style="margin-left:20px;">
                    <br/>
                    <h5>Les mensurations longitudinales :</h5>
                    <table>
                        <tr> <td> ''' + mensurations_longitudinales + ''' </td></tr>
                    </table>

                    <br/>
                    <h5>Les mensurations périmétriques :</h5>
                    <table>
                        <tr> <td> ''' + mensurations_perimetriques + ''' </td></tr>
                    </table>
                </div>

                <br/>
                <h4>MOBILITE PASSIVE :</h4>	
                <table>
                    <tr> <td> ''' + mobile_passive + ''' </td></tr>
                </table>

                <br/>	
                <table>
                    <tr> <td> ''' + stade_mobile_passive + ''' </td></tr>
                </table>

                <br/>
                <h4>SENSIBILITE ET REFLEXES</h4>

                <div style="margin-left:20px;">
                    <br/>
                    <h5>Examen de la sensibilité :</h5>	
                    <table>
                        <tr> <td> ''' + examen_sensibilite + ''' </td></tr>
                    </table>

                    <br/>
                    <h5>Examen des réflexes ostéo-tendineux :</h5>	
                    <table>
                        <tr> <td> ''' + examen_reflexes + ''' </td></tr>
                    </table>
                </div>
            '''

        return inspection_str
    
    def _get_traitement(self, consultation_medical_id):

        traitement_str = ''
        consultation_medical_traitement_obj = self.env['mz.consultation.medical.traitement'].sudo().search([('consultation_medical_id','=',consultation_medical_id)])
        if consultation_medical_traitement_obj:

            traitement_str += '<ul>'
            for traitement in consultation_medical_traitement_obj.consultation_medical_traitement_ids:
                traitement_str += '<li>' + traitement.name + '</li>'
            traitement_str += '</ul>'

            methode_chirurgicales_interention_os = consultation_medical_traitement_obj.methode_chirurgicales_interention_os if consultation_medical_traitement_obj.methode_chirurgicales_interention_os else ''
            methode_chirurgicales_interention_arti = consultation_medical_traitement_obj.methode_chirurgicales_interention_arti if consultation_medical_traitement_obj.methode_chirurgicales_interention_arti else ''
            methode_chirurgicales_interention_tendons = consultation_medical_traitement_obj.methode_chirurgicales_interention_tendons if consultation_medical_traitement_obj.methode_chirurgicales_interention_tendons else ''
            methode_chirurgicales_interventin_nerfs = consultation_medical_traitement_obj.methode_chirurgicales_interventin_nerfs if consultation_medical_traitement_obj.methode_chirurgicales_interventin_nerfs else ''

            traitement_str += '''
                <ul>
                    <li>Intervention sur les Os : ''' + methode_chirurgicales_interention_os + '''</li>
                    <li>Intervention sur les articulations : ''' + methode_chirurgicales_interention_arti + '''</li>
                    <li>Intervention sur les tendons : ''' + methode_chirurgicales_interention_tendons + '''</li>
                    <li>Intervention sur les nerfs : ''' + methode_chirurgicales_interventin_nerfs + '''</li>
                </ul>
            '''

        return traitement_str
    
    def _get_demande_traitement_kine(self, consultation_medical_id):

        demande_traitement_kine_str = ''
        demande_traitement_kine_objs = self.env['mz.kine.demande.traitement'].sudo().search([('consultation_medical_id','=',consultation_medical_id)])
        if demande_traitement_kine_objs:
            demande_traitement_kine_str += '<table class="table"><tr><td><b>Traitement prescris</b> </td><td><b>Nombre de séances</b> </td><td><b>Demandé par</b></td> <td><b>Date demande</b></td> </tr>'
            for demande_traitement_kine in demande_traitement_kine_objs:
                traitement_prescris = demande_traitement_kine.traitement_prescris_id.name if demande_traitement_kine.traitement_prescris_id else ''
                nombre_seances = str(demande_traitement_kine.nombre_seances) if demande_traitement_kine.nombre_seances else ''
                demande_par = demande_traitement_kine.demande_par.name if demande_traitement_kine.demande_par else ''
                date_demande = demande_traitement_kine.date_demande.strftime('%d/%m/%Y') if demande_traitement_kine.date_demande else ''

                demande_traitement_kine_str += '<tr><td>' + traitement_prescris + '</td><td>' + nombre_seances + '</td><td>' + demande_par + '</td><td>' + date_demande + '</td></tr>'
            demande_traitement_kine_str += '</table>'

        return demande_traitement_kine_str
