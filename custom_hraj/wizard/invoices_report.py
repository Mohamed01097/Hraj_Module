# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class Invoice(models.TransientModel):
    _name = "hraj.invoice"
    _description = "Invoice For Hraj Marketing"

    start_date = fields.Date('من تاريخ', store=True, tracking=True)
    end_date = fields.Date('إلى تاريخ', store=True, tracking=True)

    def hraj_invoice(self):
        invoices = self.env['account.move'].search([
            ('invoice_date', '>=', self.start_date),
            ('invoice_date', '<=', self.end_date),
            ('move_type', '=', 'out_invoice')
        ])
        settlement_invoices = self.env['settlement.line'].search([])

        invoice_dict = {}
        for invoice in invoices:
            invoice_dict[invoice.id] = {
                'name': invoice.partner_id.name,
                'total_tax_excldued': invoice.amount_untaxed_signed,
                'tax': invoice.amount_tax_signed,
            }
        for settle in settlement_invoices:
            invoice_dict[settle.id] = {
                'customer':settle.customer,
                'sub_total_settle': settle.price_unit * settle.qty,
                'tax_settle': settle.price_unit * settle.qty * .15
            }
        print(invoice_dict)
        data = {
            'form': self.read()[0],
            'start_date': self.start_date,
            'end_date': self.end_date,
            'invoice_dict': invoice_dict
        }
        return self.env.ref('custom_hraj.action_report_hraj_invoice').report_action(self, data=data)
