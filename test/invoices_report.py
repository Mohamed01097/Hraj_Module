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
        invoices = self.env['account.move'].search([
            ('invoice_date', '>=', self.start_date),
            ('invoice_date', '<=', self.end_date),
            ('move_type', '=', 'out_invoice')
        ])

        invoice_dict = {}
        for invoice in invoices:
            partner_id = invoice.partner_id.id
            if f"invoice_{partner_id}" not in invoice_dict:
                invoice_dict[f"invoice_{partner_id}"] = {
                    'type': invoice.partner_id.combine_type,
                    'name': invoice.partner_id.name,
                    'total_tax_excldued': 0,
                    'tax': 0,
                    'settle': {
                        'sub_total_settle': 0,
                        'tax_settle': 0,
                    }
                }
            invoice_dict[f"invoice_{partner_id}"]['total_tax_excldued'] += invoice.amount_untaxed_signed
            invoice_dict[f"invoice_{partner_id}"]['tax'] += invoice.amount_tax_signed

            # Assuming a field named 'customer' in the 'settlement.line' model that refers to the partner
        settlement_invoices = self.env['settlement.line'].search([('customer', 'in', invoices.mapped('partner_id.id'))])

        for settle in settlement_invoices:
            partner_id = settle.customer.id
            invoice_dict[f"invoice_{partner_id}"]['settle']['sub_total_settle'] += settle.price_subtotal
            invoice_dict[f"invoice_{partner_id}"]['settle']['tax_settle'] += settle.price_subtotal * 0.15

        # settlement_invoices = self.env['settlement.line'].search([('customer', '=', invoices.mapped('partner_id.id'))])
        # for settle in settlement_invoices:

        data = {
            'form': self.read()[0],
            'start_date': self.start_date,
            'end_date': self.end_date,
            'office_customer':self.office_customer,
            'work_type':self.work_type,
            'invoice_dict': invoice_dict,
        }
        return self.env.ref('custom_hraj.action_report_hraj_invoice').report_action(self, data=data)