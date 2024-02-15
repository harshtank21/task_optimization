from odoo import api, fields, models


class SaleConfirmWizard(models.TransientModel):
    _name = 'sale.confirm.wizard'

    name = fields.Char(string='Warning')

    def sale_order_submit_button(self):
        context_get = self.env.context
        record = self.env['sale.order'].browse(context_get.get('active_id'))
        context = {'active_model': 'sale.order', 'active_id': record.id}
        warning = {
            'name': 'warning',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.confirm.wizard',
            'view_id': self.env.ref('task_optimization.sale_order_confirm_wizard_form_view').id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': context
        }
        if not record.opportunity_id and self.env.context.get('warning_number', 0) < 2:
            context.update({'warning_msg': "The quotation is not related to any opportunity",
                            'warning_number': 2})
            return warning
        elif record.amount_total == float(0.0) and self.env.context.get('warning_number', 0) < 3:
            context.update({'warning_msg': "The total amount is Zero.",
                            'warning_number': 3})
            return warning
        else:
            record.with_context({'warning_number': 3}).action_confirm()

    @api.model
    def default_get(self, fields):
        context_get = self.env.context
        res = super(SaleConfirmWizard, self).default_get(fields)
        res['name'] = context_get.get('warning_msg')
        return res
