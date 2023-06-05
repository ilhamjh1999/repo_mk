from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta

class ProjectProgress(models.Model):
    _inherit = 'project.progres'

    plan = fields.Float('Plan (%)')
    plan_b = fields.Float('Plan B (%)')
    project_id = fields.Many2one('project.project', related='task_id.project_id',string='Project')
    bobot_actual_line = fields.Float(compute='_compute_bobot_actual_line', string='Actual Weight (%)',  store=True)
    bobot_plan_line = fields.Float(compute='_compute_bobot_plan_line', string='Plan Weight (%)',  store=True)
    bobot_plan_b_line = fields.Float(compute='_compute_bobot_plan_b_line', string='Plan Weight B (%)',  store=True)
    
    @api.onchange('plan')                     
    def _onchange_plan(self):
        for p in self :
            if p.plan:
                p.plan_b = p.plan 
    
    @api.onchange('date')                     
    def _chek_date(self):
        if self.date : 
            for task in self :
                obj_progres = self.env['project.progres'].search([('task_id','=',task.task_id.id)])
                for date in obj_progres:  
                    if task.date in date.date :
                        self.date = datetime.now()
                        return {'value':{},'warning':{'title':'Warning','message':'You cannot input a progress recorded on the same date'}} 
                
                
                
    @api.one
    @api.depends('task_id.nilai_kegiatan','task_id.project_id.nilai', 'progres')
    def _compute_bobot_actual_line(self):
        prj = self.env['project.project'].search([('id','=',self.task_id.project_id.id)])
        for progres in self :
            for obj in prj:
                if obj.nilai == 0 :
                    progres.bobot_actual_line = 0
                else :   
                    progres.bobot_actual_line = (progres.task_id.nilai_kegiatan / obj.nilai) * progres.progres
                    
        
    @api.one
    @api.depends('task_id.nilai_kegiatan','task_id.project_id.nilai', 'plan')
    def _compute_bobot_plan_line(self):
        prj = self.env['project.project'].search([('id','=',self.task_id.project_id.id)])
        for progres in self :
            for obj in prj:
                if obj.nilai == 0 :
                    progres.bobot_plan_line = 0
                else :   
                    progres.bobot_plan_line = (progres.task_id.nilai_kegiatan / obj.nilai) * progres.plan  
                    
                    
    @api.one
    @api.depends('task_id.nilai_kegiatan','task_id.project_id.nilai', 'plan_b')
    def _compute_bobot_plan_b_line(self):
        prj = self.env['project.project'].search([('id','=',self.task_id.project_id.id)])
        for progres in self :
            for obj in prj:
                if obj.nilai == 0 :
                    progres.bobot_plan_b_line = 0
                else :   
                    progres.bobot_plan_b_line = (progres.task_id.nilai_kegiatan / obj.nilai) * progres.plan_b  