# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
from datetime import *
import unicodedata
from odoo.tools.translate import _
from odoo.exceptions import UserError
import time
from time import mktime






class mz_chambre(models.Model):

    _inherit = 'mz.chambre'
    type_chambre = fields.Selection((('sejours_normale', 'séjours Hospitalisation normale'),
                                         ('sejours_VIP', 'séjours Hospitalisation VIP'),
                                         ('sejours_super_VIP', 'séjours Hospitalisation Super VIP')), 'Type de Chambre')
        
 
