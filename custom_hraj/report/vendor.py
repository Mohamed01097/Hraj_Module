# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class Bills(models.TransientModel):
    _name = "hraj.bill"
    _description = "Invoice For Hraj Marketing"

    start_date = fields.Date('من تاريخ', store=True, tracking=True)
    end_date = fields.Date('إلى تاريخ', store=True, tracking=True)

    def hraj_bill(self):
        bill_dict = {}

        settelment_data = self.env['settlement'].search([])

        for settle in settelment_data:
            expenses_lines, receivables_lines = [], []

            for line in settle.expenses_ids:
                expenses_lines.append({
                    'partner': line.partner_id.id
                })

            for line in settle.receivables_ids:
                receivables_lines.append({
                    'subtotal': line.qty * line.price_unit
                })

            bill_dict[settle.id] = {
                'vendor': settle.vendor_id.name,
                'name': settle.name,
                'expense_ids': expenses_lines,
                'receivables_ids': receivables_lines,
            }

        print(bill_dict)

        data = {
            'form': self.read()[0],
            'bill_dict': bill_dict,
        }

        return self.env.ref('custom_hraj.action_report_hraj_bill').report_action(self, data=data)

