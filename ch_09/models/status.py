# -*- coding: utf-8 -*-
from openerp import models, fields, api
class bookStatus(models.TransientModel):
    _name = 'library.book.status'
    book_ids = fields.Many2many('library.book')
    @api.multi
    def toggle_availability(self):
        for r in self:
            for book in r.book_ids:
                book.state=not book.state

