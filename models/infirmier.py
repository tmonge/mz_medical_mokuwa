# -*- coding: utf-8 -*-
from odoo import fields, models
from datetime import *

class MzEpisodeMedical(models.Model):    
    _inherit = 'mz.episode.medical'

    state = fields.Selection([('nouveau', 'Nouveau'),
                                ('confirmee', 'Confirmée'),
                                ('triage', 'Triage'),
                                ('recu_salle_soins', 'Recu salle des soins'),
                                ('attente_reception_secretaire', 'Attente réception secrétaire'),
                                ('recu_secretaire', 'Recu chez secrétaire'),
                                ('attente_prise_encharge', 'Attente prise en charge'),
                                ('attente_consultation', 'Attente consultation'),
                                ('consulte', 'Consulté par médecin'),
                                ('prise_encharge', 'Prise en charge')], 'Etat de l\'episode', default='nouveau')

    def envoyer_chez_secretaire(self):   
        self.write({'state':'attente_reception_secretaire'})
        return True

    def recevoir_secretaire(self):   
        self.write({'state':'recu_secretaire'})
        return True
