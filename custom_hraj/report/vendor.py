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
            expenses_lines,receivables_lines = [],[]
            for line in settle.expenses_ids:
                expenses_lines.append((0, 0,{
                    'card': round(line.card/59),
                    'partner': line.partner_id.id
                }))
            for line in settle.receivables_ids:
                receivables_lines.append((0, 0,{
                    'subtotal': line.qty * line.price_unit
                }))
            bill_dict[settle]={
                'vendor':settle.vendor_id,
                'name':settle.name,
                'expense_ids':expenses_lines,
                'receivables_ids':receivables_lines,
            }
        print(bill_dict)
        data = {
            'form': self.read()[0],
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
        return self.env.ref('custom_hraj.action_report_hraj_bill').report_action(self, data=data)

