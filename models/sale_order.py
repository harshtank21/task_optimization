from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "task"

    def action_confirm(self):
        context = {'active_model': 'sale.order', 'active_id': self.id}
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
        if self.partner_id.untrustworthy and self.env.context.get('warning_number', 0) < 1:
            context.update({'warning_msg': "This customer is untrustworthy. Are you sure you want to proceed?",
                            'warning_number': 1})
            return warning
        elif not self.opportunity_id and self.env.context.get('warning_number', 0) < 2:
            context.update({'warning_msg': "The quotation is not related to any opportunity",
                            'warning_number': 2})
            return warning
        elif self.amount_total == float(0.0) and self.env.context.get('warning_number', 0) < 3:
            context.update({'warning_msg': "The total amount is Zero.",
                            'warning_number': 3})
            return warning
        return super(SaleOrder, self).action_confirm()
