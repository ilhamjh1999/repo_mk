from odoo import api, fields, models, tools, _

class ProjectProject(models.Model):
    _inherit = 'project.project'

    location = fields.Char('Location')
    description = fields.Char('Project Description')
    nilai = fields.Float(compute='_compute_nilai', string='Total Cost') 
    
    @api.one
    @api.depends('task_ids.nilai_kegiatan')
    def _compute_nilai(self):
        task = self.env['project.task'].search([('project_id','=',self.id)])
        for x in task:
            self.nilai += x.nilai_kegiatan