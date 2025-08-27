# -*- coding: utf-8 -*-
from odoo import models, fields


class MzMedFactureLine(models.Model):

    _inherit='mz.med.facture.line'
    
    mode_validation = fields.Selection(selection_add=[('Don','Don')])
    type_apurement = fields.Selection(selection_add=[('Don','Don')])
