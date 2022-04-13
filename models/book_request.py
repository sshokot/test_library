from odoo import fields, models, _, api
from odoo.exceptions import ValidationError


class  BookRequest(models.Model):
    _name = 'book.request'
    _description = 'book.request'

    borrower_id = fields.Many2one('res.partner', string='Borrower', required=True)
    borrow_from = fields.Datetime(string='From', required=True)
    borrow_to = fields.Datetime(string='To', required=True)
    book_id = fields.Many2one('product.product', string='Book', required=True)
    state = fields.Selection([('borrowed', 'Borrowed'), ('returned', 'Returned'),('lost','Lost')], string='State')

    def make_borrowed(self):
        self.state = 'borrowed'
        self.create_return_event()
        self.create_sale_order()

    def make_returned(self):
        self.state = 'returned'

    def make_lost(self):
        self.state = 'lost'

    def create_return_event(self):

        user = self.env['res.users'].browse(self.env.uid)
        event = self.env['calendar.event'].create({
            'name': _("Return book from %s") % self.borrower_id.name,
            'start': self.borrow_from,
            'stop': self.borrow_to,
            'attendee_ids': [(0, 0, {'state': 'accepted', 'email': self.borrower_id.email, 'partner_id': self.borrower_id.id})],
            'partner_ids': [(4, user.partner_id.id)],
        })

    def create_sale_order(self):
        public_so = self.env['sale.order'].create({
           'partner_id': self.borrower_id.id,
           'order_line': [
               (0, 0, {
                   'product_id': self.book_id.id,
                   'product_uom_qty': 1,
               })
           ]
        })

