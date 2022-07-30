from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    
    name = fields.Char(string="Property Name", required=True)
    number = fields.Integer(string="Property Number", required=True)
    postcode = fields.Char(string="Zipcode")
    date_avalability = fields.Date(string="Available From", copy=False, default=lambda self: fields.Date.today())
    
    description = fields.Text()
    bedrooms = fields.Integer("Beds", default=2)
    bathrooms = fields.Integer("Baths")
    living_area = fields.Float("Area(sqm)")
    garden_area = fields.Float("Garden Area(sqm)")
    garden = fields.Boolean(string="Gardens", default=False)
    garden_facing = fields.Selection([('north', 'North'),
                                      ('south', 'South'),
                                      ('east', 'East'),
                                      ('west', 'West')], string="Orientations")
    total_area = fields.Float(compute="_compute_total_area", string="Total Area(sqm)", readonly=True)
    
    expected_price = fields.Float(string="Expected Price", copy=False)
    sell_price = fields.Float(string="Selling Price", readonly=True, default=0)
    best_price = fields.Float(compute="_compute_highest_offer", string="Highest Offer")
    
    state =fields.Selection([('new','New'),
                             ('offer received', 'Offer Received'),
                             ('offer accepted', 'Offer Accepted'),
                             ('sold', 'Sold'),
                             ('cancelled', 'Cancelled')], string="Status", default="new")
    
    #Many2one fields for adding property types into the estate.room model (A property can have ONE type, but same type can be applied to MANY properties)
    property_type_id = fields.Many2one("estate.property.type", string="Types")
    
    #Same Many2one concept is applied to buyer_id and users_id
    buyer_id = fields.Many2one("res.partner", string="Buyers", copy=False)
    users_id = fields.Many2one("res.users", string="Sale Agents", default=lambda self: self.env.user)
    
    #Many2many fields for adding tags to properties (A property can have MANY tags and a tag can be applied to MANY properties)
    tag_ids = fields.Many2many("estate.property.tags", string="Tags")
    
    #One2many field for adding an offer to a property (An offer applies to ONE property and a property can have MANY offers)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    
    _sql_constraints = [('expected_price_check', 'CHECK(expected_price > 0)','The property expected price must be strictly positive'),
                        ('sell_price_check', 'CHECK(sell_price >= 0)', 'The property selling price must be positive')]
    
    #compute total area with and without garden
    @api.depends("garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area
    
    #compute highest offer to put in best price
    @api.depends("offer_ids.offer_price")
    def _compute_highest_offer(self):
        for rec in self:
            list_price = self.mapped("offer_ids.offer_price")
            list_price.sort()
            #print(list_price)
            if len(list_price) > 0:
                rec.best_price = list_price[-1]
            else:
                rec.best_price = 0
        return rec.best_price
    
    #onchange whether the property has garden or not
    @api.onchange("garden")
    def _onchange_garden(self):
        for rec in self:
            if rec.garden == True:
                rec.garden_area = 10
                rec.garden_facing = 'north'
            else:
                rec.garden_area = 0
                rec.garden_facing = ''
    
    #button action to declare sold a property (Sold property cannot be cancelled)
    def action_sold(self):
        if self.filtered(lambda x: x.state == 'cancelled'):
            raise UserError("Cancelled property cannot be sold")
        for rec in self:
            rec.state = 'sold'
        return rec.state
    
    #buttonn action to declare cancelled a property (Cancelled property cannot be sold
    def action_cancel(self):
        if self.filtered(lambda x: x.state == 'sold'):
            raise UserError("Sold property cannot be cancelled")
        for rec in self:
            rec.state = 'cancelled'
        return rec.state
    
    @api.constrains('sell_price', 'expected_price')
    def _check_offer_price(self):
        for rec in self:
            if not float_is_zero(rec.sell_price, 2):
                res = float_compare(rec.sell_price, ((rec.expected_price * 90) / 100), precision_digits=2) 
                if res < 0:
                    raise ValidationError("Offer cannot be lower than 90% of expected price")
    
    @api.ondelete(at_uninstall=False)
    def _check_deletion(self):
        for rec in self:
            if rec.state in ('new', 'cancelled'):
                raise UserError("Cannot delete new or cancelled property")
             
    
        