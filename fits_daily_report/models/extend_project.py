from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

class Task(models.Model):
    _inherit = 'project.task'

    progres_ids = fields.One2many('project.progres', 'task_id', 'Progress')
    total_actual = fields.Float(
        compute='_progres_get', store=True, string=' Total Actual (%)')

    @api.depends('progres_ids.progres')
    def _progres_get(self):
        for task in self:
            for line in task.progres_ids:
                task.total_actual += line.progres
                if task.total_actual > 100:
                    raise ValidationError(
                        'You cannot input progress actual more than 100%')

    @api.constrains('planned_hours')
    def _planned_hours(self):
        if self.planned_hours == 0:
            raise exceptions.ValidationError(
                "Initially Planned Hours should not be 0.....!!")


class Project(models.Model):
    _inherit = 'project.project'

    total_planned = fields.Float(
        string='Total Planned Hours', compute='_get_total')
    total_efective = fields.Float(
        string='Total Actual Hours', compute='_get_total')

    @api.multi
    @api.depends('task_ids.planned_hours', 'task_ids.effective_hours')
    def _get_total(self):
        for project in self:
            task = self.env['project.task'].search(
                [('project_id', '=', project.id)])
            for x in task:
                project.total_planned += x.planned_hours
                project.total_efective += x.effective_hours


class Progress(models.Model):
    _name = "project.progres"
    _order = 'date desc'

    date = fields.Date('Date', required=True, index=True,
                       default=fields.Date.context_today)
    progres = fields.Float('Progress (%)')
    task_id = fields.Many2one('project.task', string='Task')

    @api.onchange('date')
    def _chek_date(self):
        if self.date:
            for task in self:
                if self.date == task.date:
                    self.date = datetime.now()
                    return {'value': {}, 'warning': {'title': 'Warning', 'message': 'You cannot input a progress recorded on the same date'}}
