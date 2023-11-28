# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class Invoice(models.TransientModel):
    _name = "hraj.invoice"
    _description = "Invoice For Hraj Marketing"

    start_date = fields.Date('من تاريخ', store=True, tracking=True)
    end_date = fields.Date('إلى تاريخ', store=True, tracking=True)
    office_customer = fields.Boolean(string="عميل مكتب",default=True)
    work_type = fields.Selection([
        ('hraj','خراج'),
        ('market','تسويق')
    ],string="نوع الخدمة")

    def hraj_invoice(self):
        pos_order_lines = self.env['pos.order.line'].search([
            ('order_id.date_order', '>=', self.start_date),
            ('order_id.date_order', '<=', self.end_date),
        ])
        invoice_dict = {}
        for pos in pos_order_lines:
            partner_id = pos.order_id.partner_id.id
            if f"order_{partner_id}" not in invoice_dict:
                invoice_dict[f"order_{partner_id}"] = {
                    'type': pos.order_id.partner_id.combine_type,
                    'name':pos.order_id.partner_id.name,
                    'pos_price_subtotal': 0,
                    'pos_tax': 0,
                    'inv': {
                        'total_tax_excldued': 0,
                        'tax': 0,
                    },
                    'settle': {
                        'sub_total_settle': 0,
                        'tax_settle': 0,
                    },
                }
            invoice_dict[f"order_{partner_id}"]['pos_price_subtotal'] += pos.price_subtotal_incl
            invoice_dict[f"order_{partner_id}"]['pos_tax'] += (pos.price_subtotal_incl - pos.price_subtotal)

        invoices = self.env['account.move'].search([
            ('partner_id','in',pos_order_lines.mapped('order_id.partner_id.id')),
            ('move_type','=','out_invoice')
        ])
        for invoice in invoices:
            partner_id = invoice.partner_id.id
            invoice_dict[f"order_{partner_id}"]['total_tax_excldued'] += invoice.amount_untaxed_signed
            invoice_dict[f"order_{partner_id}"]['tax'] += invoice.amount_tax_signed

            # Assuming a field named 'customer' in the 'settlement.line' model that refers to the partner
        settlement_invoices_lines = self.env['settlement.line'].search([('customer', 'in', pos_order_lines.mapped('order_id.partner_id.id'))])
        for settle in settlement_invoices_lines:
            partner_id = settle.customer.id
            invoice_dict[f"order_{partner_id}"]['settle']['sub_total_settle'] += settle.price_subtotal
            invoice_dict[f"order_{partner_id}"]['settle']['tax_settle'] += settle.price_subtotal * 0.15

        data = {
            'form': self.read()[0],
            'start_date': self.start_date,
            'end_date': self.end_date,
            'office_customer':self.office_customer,
            'work_type':self.work_type,
            'invoice_dict': invoice_dict,
        }
        return self.env.ref('custom_hraj.action_report_hraj_invoice').report_action(self, data=data)

    # def hraj_invoice(self):
    #     invoices = self.env['account.move'].search([
    #         ('invoice_date', '>=', self.start_date),
    #         ('invoice_date', '<=', self.end_date),
    #         ('move_type', '=', 'out_invoice')
    #     ])
    #
    #     invoice_dict = {}
    #     for invoice in invoices:
    #         partner_id = invoice.partner_id.id
    #         if f"invoice_{partner_id}" not in invoice_dict:
    #             invoice_dict[f"invoice_{partner_id}"] = {
    #                 'type': invoice.partner_id.combine_type,
    #                 'name': invoice.partner_id.name,
    #                 'total_tax_excldued': 0,
    #                 'tax': 0,
    #                 'settle': {
    #                     'sub_total_settle': 0,
    #                     'tax_settle': 0,
    #                 },
    #                 'pos':{
    #                   'pos_price_subtotal':0,
    #                   'pos_tax':0,
    #                 }
    #             }
    #         invoice_dict[f"invoice_{partner_id}"]['total_tax_excldued'] += invoice.amount_untaxed_signed
    #         invoice_dict[f"invoice_{partner_id}"]['tax'] += invoice.amount_tax_signed
    #
    #         # Assuming a field named 'customer' in the 'settlement.line' model that refers to the partner
    #     settlement_invoices_lines = self.env['settlement.line'].search([('customer', 'in', invoices.mapped('partner_id.id'))])
    #     for settle in settlement_invoices_lines:
    #         partner_id = settle.customer.id
    #         invoice_dict[f"invoice_{partner_id}"]['settle']['sub_total_settle'] += settle.price_subtotal
    #         invoice_dict[f"invoice_{partner_id}"]['settle']['tax_settle'] += settle.price_subtotal * 0.15
    #
    #     pos_order_lines = self.env['pos.order.line'].search([('order_id.partner_id', 'in', invoices.mapped('partner_id.id'))])
    #     for pos in pos_order_lines:
    #         partner_id = pos.order_id.partner_id.id
    #         invoice_dict[f"invoice_{partner_id}"]['pos']['pos_price_subtotal'] += pos.price_subtotal_inc
    #         invoice_dict[f"invoice_{partner_id}"]['pos']['pos_tax'] += (pos.price_subtotal_inc - pos.price_subtotal)
    #
    #     data = {
    #         'form': self.read()[0],
    #         'start_date': self.start_date,
    #         'end_date': self.end_date,
    #         'office_customer':self.office_customer,
    #         'work_type':self.work_type,
    #         'invoice_dict': invoice_dict,
    #     }
    #     return self.env.ref('custom_hraj.action_report_hraj_invoice').report_action(self, data=data)