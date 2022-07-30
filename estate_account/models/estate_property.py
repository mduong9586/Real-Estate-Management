from odoo import api, models


class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    def action_sold(self):
        res = super(EstateProperty, self).action_sold()
        invoice = self.env['account.move'].create(
            )
        
        return res
    
