 # -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.addons import decimal_precision as dp
from openerp.fields import Date as fDate
from datetime import datetime
class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'
    name = fields.Char('Title', required=True)
    notes = fields.Text('Internal Notes')
    author_ids = fields.Many2many('res.partner', string='Authors')

    short_name = fields.Char(        string='Short Title',     size=100,  # For Char only
        translate=False,  # also for Text fields
    )
    state = fields.Selection(
        [('draft', 'Not Available'),
         ('available', 'Available'),
         ('lost', 'Lost')],
        'State')
    description = fields.Html(string='Description')
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date')
    reader_rating = fields.Float('Reader Average Rating',(14, 4))
    pages = fields.Integer(
        string='Number of Pages',
        default=20,
        help='Total book page count',
        groups='base.group_user',
        states={'draft': [('readonly', True)]},
        copy=True,
        company_dependent=False,
    )
    active = fields.Boolean('Active', default=True)
    cost_price = fields.Float('Book Cost', dp.get_precision('Book Price'))
    publisher= fields.Many2one('res.partner', 'Publisher', domain=[('publisher', '=', True)])

    min_pages=50
    _sql_constraints = [
                         ('names', 'unique(name)','Error ! Name can\'t repeat.')
                        ,('pages', 'check(pages>={0} )'.format(min_pages),'Error ! Pages must be more than {0}.'.format(min_pages))
                        ]

    @api.constrains('date_release')
    def check_release_date(self):
        for this_record in self:
            if this_record.date_release > fields.Date.today():
                raise models.ValidationError('Release date must be in the past')

    hours_to_read= fields.Float(
        string='Hours Needed to read',
        compute='_compute_hours_to_read',
        inverse='_inverse_hours',
        # search='_search_age',
        store=False,
        compute_sudo=False,
    )

    @api.depends('pages')
    def _compute_hours_to_read(self):
        for book in self:
            book.hours_to_read = book.pages*2

    def _inverse_hours(self):
        for book in self:
            book.pages=book.hours_to_read /2




class publishers(models.Model):
    _inherit='res.partner'
    publisher=fields.Boolean()