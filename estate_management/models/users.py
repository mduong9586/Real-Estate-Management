from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = "res.users"
    
    property_ids = fields.One2many("estate.property", "users_id", domain=['|', ('state', '=', 'new'), ('state', '=', 'offer received')])