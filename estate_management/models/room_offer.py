from odoo import models, fields, api
from . import room
from datetime import timedelta, datetime
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"
    
    offer_price = fields.Float(string="Buyer's Offer")
    status = fields.Selection([('accepted','Accepted'),
                               ('refused', 'Refused')], copy=False, readonly=True, string="Status")
    partner_id = fields.Many2one("res.partner", required=True, string="Buyer")
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(compute="_compute_deadline", string="Deadline")
    #inverse="_inverse_deadline",
    
    
    
    _sql_constraints = [('offer_check', 'CHECK(offer_price > 0)', 'An offer price must be strictly positive')]

    @api.depends("create_date")
    def _compute_deadline(self):
        for rec in self:
            rec.date_deadline = rec.create_date + timedelta(days=rec.validity)
            return rec.date_deadline
    
    # def _inverse_deadline(self):
    #     for rec in self:
    #         start_date = datetime.strptime(str(rec.create_date), "%Y-%m-%d")
    #         end_date = datetime.strptime(str(rec.date_deadline), "%Y-%m-%d")
    #         day_diff = end_date - start_date
    #         rec.validity = str(day_diff.days)
    #
    #         return rec.validity
    
    #button to accept an offer (Only one offer can be accepted for a property)
    def action_accepted(self):
        for rec in self:
            rec.status = 'accepted'
            rec.property_id.state = 'offer accepted'
            rec.property_id.sell_price = rec.offer_price
            rec.property_id.buyer_id = rec.partner_id
        return rec.status
    
    #button to refuse an offer
    def action_refused(self):
        for rec in self:
            rec.status = 'refused'
        return rec.status
    
    @api.model 
    def create(self, vals):
        rec = super(EstatePropertyOffer, self).create(vals)
        property = self.env['estate.property'].browse(vals['property_id'])
        if not float_is_zero(property.best_price, 2):
            if float_compare(rec.offer_price, property.best_price, precision_digits=2) < 0:
                raise UserError(f"The offer must be higher than {property.best_price}")
        if property.state == 'new':
            property.state = 'offer received'
        return rec
        
    