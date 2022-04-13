from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    book_request_count = fields.Integer(compute="_count_book_requests")

    def _count_book_requests(self):
        for contact in self:
            contact.book_request_count = self.env['book.request'].search_count([('borrower_id','=',self.id)])

    def action_view_book_requests(self):
        action = self.env['ir.actions.act_window']._for_xml_id("library.act_window_book_request")
        action['domain'] =  [('borrower_id.id','=',self.id)]
        action['context'] = {'default_borrower_id': self.id}
        return action
