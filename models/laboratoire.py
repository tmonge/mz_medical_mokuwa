# -*- coding: utf-8 -*-
from odoo import fields, models


class MzAnalyseBiologiqueLine(models.Model):
    
    _inherit='mz.analyse.biologique.line'

    observations_medecin = fields.Text('Observations médecin')