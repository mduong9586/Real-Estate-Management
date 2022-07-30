from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"
    
    
    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    
    sequence = fields.Integer(string="Sequence", default=1)
    
    _sql_constraints = [('type_unique', 'UNIQUE(name)', 'A property type must be unique')]
    
    