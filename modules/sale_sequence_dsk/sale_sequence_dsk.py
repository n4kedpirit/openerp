# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv, orm

class sale_order(osv.osv):
    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if not default:
            default = {}
        saved_sale_order = self.browse(cr, uid, id, context=context)
        if saved_sale_order['is_cash_payment']:
            sale_order_sequence_code = 'sale.order.cash'
        else:
            sale_order_sequence_code = 'sale.order.bank'
        default.update({
            'state': 'draft',
            'invoice_ids': [],
            'date_confirm': False,
            'name': self.pool.get('ir.sequence').get(cr, uid, sale_order_sequence_code),
            })
        #Lines below are taken from the same method in BaseModel
        context = context.copy()
        data = self.copy_data(cr, uid, id, default, context)
        new_id = self.create(cr, uid, data, context)
        self.copy_translations(cr, uid, id, new_id, context)
        return new_id

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            if vals.get('is_cash_payment'):
                sale_order_sequence_code = 'sale.order.cash'
            else:
                sale_order_sequence_code = 'sale.order.bank'
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, sale_order_sequence_code) or '/'
        return super(sale_order, self).create(cr, uid, vals, context=context)


    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        if 'is_cash_payment' in vals and len(ids) == 1:
            for saved_sale_order in self.browse(cr, uid, ids, context=context):
                if saved_sale_order['is_cash_payment'] != vals['is_cash_payment']:
                    if vals['is_cash_payment']:
                        sale_order_sequence_code = 'sale.order.cash'
                    else:
                        sale_order_sequence_code = 'sale.order.bank'
                    vals['name'] = self.pool.get('ir.sequence').get(cr, uid, sale_order_sequence_code)
        return super(sale_order, self).write(cr, uid, ids, vals, context=context)

    _name = 'sale.order'
    _inherit = 'sale.order'
    _columns = {
        'is_cash_payment': fields.boolean('Cash Payment'),
    }
sale_order()