from odoo import models, fields, api

class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"
    _order = "name"
    
    name = fields.Char(string="Tags", required=True)
    color = fields.Integer(string="Tag Colors")
    
    
    _sql_constraints = [('property_tag_unique', 'UNIQUE(name)', 'A property tag must be unique')]