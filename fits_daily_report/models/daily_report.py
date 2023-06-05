# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, tools, _
from odoo.modules import get_module_resource
from itertools import groupby
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
import pytz

          

class ProjectDaily(models.Model):
    _name = 'project.daily'
    _description = "Daily Report"
    _order = "date_daily desc"
    _inherit = ['mail.thread']

    #Penambahan Field Baru
    no_urut = fields.Char('No Urut')
    kontrak_no_tgl = fields.Char('Kontrak No. Tanggal')
    smpk_no_tgl = fields.Char('SMPK No./Tanggal')
    personil_pelaksana_1 = fields.Char("Personil Pelaksanaan 1")
    personil_pelaksana_2 = fields.Char("Personil Pelaksanaan 2")

    project_id = fields.Many2one('project.project', string='Proyek', required=True)
    name = fields.Char('Nama Laporan')
    location = fields.Char(string='Lokasi',store=True,related='project_id.location', readonly=True)
    consultan = fields.Char('Konsultan')
    partner_id = fields.Many2one('res.partner',string='Penyedia Jasa')
    company_id = fields.Many2one('res.company',string='Konsultan Pengawas')
    description = fields.Char(string='Deskripsi Proyek',store=True,related='project_id.description', readonly=True)
    date_daily = fields.Date(string='Hari/Tanggal', default=fields.Date.context_today)
    start_time_jam = fields.Selection([
        ('1', '01'),('2', '02'),('3', '03'),('4', '04'),('5', '05'),('6', '06'),('7', '07'),
        ('8', '08'),('9', '09'),('10', '10'),('11', '11'),('12', '12'),('13', '13'),('14', '14'),
        ('15', '15'),('16', '16'),('17', '17'),('18', '18'),('19', '19'),('20', '20'),('21', '21'),
        ('22', '22'),('23', '23'),('24', '24')
        ], string='Start Time')
    start_time_menit = fields.Selection([
        ('00', '00'),('0.50', '30')
        ], string='Start Time', default='00')
    end_time_jam = fields.Selection([
        ('1', '01'),('2', '02'),('3', '03'),('4', '04'),('5', '05'),('6', '06'),('7', '07'),
        ('8', '08'),('9', '09'),('10', '10'),('11', '11'),('12', '12'),('13', '13'),('14', '14'),
        ('15', '15'),('16', '16'),('17', '17'),('18', '18'),('19', '19'),('20', '20'),('21', '21'),
        ('22', '22'),('23', '23'),('24', '24')
        ], string='End Time')
    end_time_menit = fields.Selection([
        ('00', '00'),('0.50', '30')
        ], string='End Time', default='00')
    start = fields.Float(string='Start Time', compute='_compute_duration', store=True, readonly=True)
    end = fields.Float(string='End Time', compute='_compute_duration', store=True, readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validate', 'Validate'),
        ('sent', 'Sent'),
        
        ], string='Status', readonly=True,  default='draft')
    total_person = fields.Integer(string='Total Person', store=True, readonly=True, compute='_person_all')
    total_person_tma = fields.Integer(string='Total Orang', store=True, readonly=True, compute='_person_all_tma')
    total_durasi = fields.Float(string='Total Duration', store=True, readonly=True, compute='_durasi_all')
    notes = fields.Html(string='Notes')
    user_id = fields.Many2one('res.users','Project Manager',readonly = True, default=lambda self: self.env.user.id)
    lampiran_ttd_pm = fields.Binary('TTD Project Manager')
    filename_ttd_pm = fields.Char('Nama Lampiran TTD PM')
    galery_ids = fields.One2many('project.galery', 'daily_id', string='Photo Galery', copy=True)
    lampiran_dokumen_ids = fields.One2many('lampiran.dokumen', 'daily_id', string='Lampiran Dokumen', copy=True)
    # manpower_ids = fields.One2many('project.manpower', 'daily_id', string='Manpower', copy=True)
    # material_ids = fields.One2many('project.material', 'daily_id', string='Material & Equipment', copy=True)
    # activies_ids = fields.One2many('project.activity', 'daily_id', string='Activity', copy=True)
    # issue_ids = fields.One2many('project.problem', 'daily_id', string='Problem', copy=True)
    # weather_ids = fields.One2many('project.weather', 'daily_id', string='Weather', copy=True)

    #New Field Many to One
    site_manager = fields.Many2one('res.users', 'Site Manager')
    lampiran_ttd_sm = fields.Binary('TTD Site Manager')
    filename_ttd_sm = fields.Char('Nama Lampiran TTD SM')
    #New Field One To Many
    total_person_tma = fields.Integer(string='Total Orang', store=True, readonly=True, compute='_person_all_tma')
    pekerjaan_ids = fields.One2many('pekerjaan.activity', 'daily_id', string='Pekerjaan', copy=True)
    pemakaian_peralatan_ids = fields.One2many('pemakaian.peralatan', 'daily_id', string='Pemakaian Peralatan',
                                              copy=True)
    bahan_konstruksi_ids = fields.One2many('bahan.konstruksi', 'daily_id', string='Bahan Konstruksi', copy=True)
    personil_pelaksanaan_ids = fields.One2many('personil.pelaksanaan', 'daily_id',
                                               string='Personil Pelaksanaan FUJICON', copy=True)
    personil_pelaksanaan_tma_ids = fields.One2many('personil.pelaksanaan.tma', 'daily_id',
                                                   string='Personil Pelaksanaan TMA', copy=True)
    penghambat_pekerjaan_ids = fields.One2many('penghambat.pekerjaan', 'daily_id', string='Penghambat Pekerjaan',
                                               copy=True)
    laporan_ids = fields.One2many('laporan', 'daily_id', string='Penghambat Pekerjaan', copy=True)
    total_progress_aktual = fields.Float(string='Total Progress Aktual', store=True, readonly=True,
                                         compute='_total_progress_aktual')
    total_progress_rencana = fields.Float(string='Total Progress Rencana', store=True, readonly=True,
                                          compute='_total_progress_rencana')

    total_deviasi = fields.Float(string='Total Deviasi', store=True, readonly=True,compute='_total_deviasi')

    @api.multi
    def get_activity_line(self):
        format_tgl = "%Y-%m-%d %H:%M:%S"
        user_tz = self.env.user.tz or 'Asia/Jakarta'
        jam_now = datetime.now()
        jam_now = pytz.timezone('UTC').localize(jam_now)
        jam_now =jam_now.astimezone(pytz.timezone(user_tz))
        tgl_jam = jam_now.strftime(format_tgl)
        task_obj = self.env['project.task'].search([('user_id', '=', self.user_id.id),('stage_id.name', 'not in', ['Done','Cancelled']),
                                                    ('project_id', '>=', self.project_id.id),
                                                    ('date_start', '<=', tgl_jam),'|',('date_end', '>=', tgl_jam),
                                                    ('date_deadline', '>=',self.date_daily)])   
        
        
        line_list = []
        for x in task_obj :
            vals = {
                    'daily_id'       : self.id,
                    'task_id'       : x.id,
                }
            line_list.append((0, 0, vals))
           
        self.activity_ids = line_list
        
    @api.onchange('project_id')
    def _onchange_project_id(self):
        self.partner_id = self.project_id.partner_id.id
        self.company_id = self.user_id.company_id.id
        self.get_activity_line()
        
    
    @api.depends('start_time_jam','start_time_menit','end_time_jam','end_time_menit')
    def _compute_duration(self):
        for o in self:
            start = float(int(o.start_time_jam)+float(o.start_time_menit))
            end = float(int(o.end_time_jam)+float(o.end_time_menit))
            o.start = start
            o.end = end
            
    # @api.depends('manpower_ids.person')
    # def _person_all(self):
    #     for order in self:
    #         for line in order.manpower_ids:
    #             order.total_person += line.person

    # BARU
    @api.depends('pekerjaan_ids.actual')
    def _total_progress_aktual(self):
       for order in self:
           for line in order.pekerjaan_ids:
                 order.total_progress_aktual += line.actual

    # BARU
    @api.depends('pekerjaan_ids.plan')
    def _total_progress_rencana(self):
        for order in self:
            for line in order.pekerjaan_ids:
                 order.total_progress_rencana += line.plan

    @api.depends('total_progress_aktual','total_progress_rencana')
    def _total_deviasi(self):
        for line in self:
             line.total_deviasi = line.total_progress_aktual - line.total_progress_rencana

    # BARU
    @api.depends('personil_pelaksanaan_ids.person')
    def _person_all(self):
        for order in self:
          for line in order.personil_pelaksanaan_ids:
              order.total_person += line.person

    # BARU
    @api.depends('personil_pelaksanaan_tma_ids.person')
    def _person_all_tma(self):
       for order in self:
            for line in order.personil_pelaksanaan_tma_ids:
                 order.total_person_tma += line.person

    # BARU
    @api.depends('penghambat_pekerjaan_ids.duration')
    def _durasi_all(self):
        for order in self:
            for line in order.penghambat_pekerjaan_ids:
                 order.total_durasi += line.duration



                
    # @api.depends('weather_ids.duration')
    # def _durasi_all(self):
    #     for order in self:
    #         for line in order.weather_ids:
    #             order.total_durasi += line.duration

    # BARU
    @api.depends('penghambat_pekerjaan_ids.duration')
    def _durasi_all(self):
        for order in self:
            for line in order.penghambat_pekerjaan_ids:
                order.total_durasi += line.duration

    @api.multi
    def action_valid(self):
        self.write({'state': 'validate'})
        
        
    @api.multi
    def project_lines_layouted(self):
        """
        Returns this order lines classified by sale_layout_category and separated in
        pages according to the category pagebreaks. Used to render the report.
        """
        self.ensure_one()
        report_pages = [[]]
        for category, lines in groupby(self.manpower_ids, lambda l: l.parent_id):
           
            # Append category to current report page
            report_pages[-1].append({
                'name': category and category.name or 'Uncategorized',
                'lines': list(lines)
            })

        return report_pages
    
    @api.multi
    def project_weather_layouted(self):
        """
        Returns this order lines classified by sale_layout_category and separated in
        pages according to the category pagebreaks. Used to render the report.
        """
        self.ensure_one()
        report_pages = [[]]
        for category, lines in groupby(self.weather_ids, lambda l: l.categ_weather_id):
           
            # Append category to current report page
            report_pages[-1].append({
                'name': category and category.name or 'Uncategorized',
                'lines': list(lines)
            })

        return report_pages
            
class LampiranDokumen(models.Model):
    _name = 'lampiran.dokumen'
    _rec_name = 'lampiran_dokumen'

    daily_id = fields.Many2one('project.daily', string='Daily Reference')
    lampiran_dokumen = fields.Binary('Lampiran Dokumen')
    nama_lampiran = fields.Char('Nama Lampiran Dokumen')
    descrip = fields.Char(string='Description')
    date = fields.Date(string='Picture Date')




class ProjectGalery(models.Model):
    _name = 'project.galery'
    _rec_name = 'photo_id'
    _order = 'sequence'

    photo_id = fields.Many2one('photo.galery', string='Nama Kegiatan', required=True,)
    daily_id = fields.Many2one('project.daily', string='Daily Reference')
    descrip = fields.Char(string='Deskripsi Kegiatan',store=True,related='photo_id.descrip', readonly=True)
    date = fields.Date(string='Tgl Foto',store=True,related='photo_id.picture_date', readonly=True)
    project_id = fields.Many2one('project.project', string='Proyek',required=True)
    task_id = fields.Many2one('project.task', string='Task', required=True,)
    sequence = fields.Integer(string='Sequence', default=10)
    actual = fields.Float(compute='_actual_get', store=True, string='Actual (%)')
    plan = fields.Float(compute='_plan_get', store=True, string='Plan (%)')

    @api.multi
    @api.onchange('photo_id','task_id')
    def partner_id_onchange(self):
        for o in self:
            o.task_id= o.photo_id.task_id.id 
            o.project_id = o.photo_id.project_id.id
            

    @api.multi
    @api.depends('task_id.progres_ids')
    def _actual_get(self):
        for activity in self:  
            if activity.task_id:
                    domain = [('date', '<=', activity.daily_id.date_daily),('task_id', '=', activity.task_id.id)]
                    obj_prog = self.env['project.progres'].search(domain)
                    for o in obj_prog:
                        activity.actual += o.progres
                        
                        
    @api.multi
    @api.depends('task_id.progres_ids')
    def _plan_get(self):
        for activity in self:  
            if activity.task_id:
                    domain = [('date', '<=', activity.daily_id.date_daily),('task_id', '=', activity.task_id.id)]
                    obj_prog = self.env['project.progres'].search(domain)
                    for o in obj_prog:
                        activity.plan += o.plan

class PersonilPelaksanaan(models.Model):
    _name = 'personil.pelaksanaan'
    _rec_name = 'designation_id'
    _order = 'sequence'

    designation_id = fields.Many2one('project.designation', string='Tugas/jabatan')
    partner_id = fields.Many2one('res.partner', string='Nama')
    parent_id = fields.Many2one('res.partner', string='Company')
    person = fields.Integer(string='Jumlah')
    lokasi = fields.Char(string='Lokasi')
    daily_id = fields.Many2one('project.daily', string='Daily Reference')
    sequence = fields.Integer(string='Sequence', default=10)
    project_id = fields.Many2one('project.project', string='Project', required=False)
    ref_project_id = fields.Many2one('project.project', string='Ref', related='daily_id.project_id')
    date_daily = fields.Date(string='Ref Date', related='daily_id.date_daily')
    date = fields.Date(string='Date')

    @api.multi
    @api.onchange('partner_id','parent_id','person','designation_id')
    def partner_id_onchange(self):
        for o in self:
            o.parent_id= o.partner_id.parent_id.id
            o.project_id = o.daily_id.project_id.id
            o.date = o.daily_id.date_daily

class PersonilPelaksanaanTma(models.Model):
    _name = 'personil.pelaksanaan.tma'
    _rec_name = 'designation_id'
    _order = 'sequence'

    designation_id = fields.Many2one('project.designation', string='Tugas/Jabatan')
    partner_id = fields.Many2one('res.partner', string='Nama')
    parent_id = fields.Many2one('res.partner', string='Company')
    person = fields.Integer(string='Jumlah')
    lokasi = fields.Char(string='Lokasi')
    daily_id = fields.Many2one('project.daily', string='Daily Reference')
    sequence = fields.Integer(string='Sequence', default=10)
    project_id = fields.Many2one('project.project', string='Project', required=False)
    ref_project_id = fields.Many2one('project.project', string='Ref', related='daily_id.project_id')
    date_daily = fields.Date(string='Ref Date', related='daily_id.date_daily')
    date = fields.Date(string='Date')

    @api.multi
    @api.onchange('partner_id','parent_id','person','designation_id')
    def partner_id_onchange(self):
        for o in self:
            o.parent_id= o.partner_id.parent_id.id
            o.project_id = o.daily_id.project_id.id
            o.date = o.daily_id.date_daily

class Material(models.Model):
    _name = 'bahan.konstruksi'
    _rec_name = 'product_id'
    _order = 'sequence'

    product_id = fields.Many2one('product.product', string='Jenis', change_default=True, ondelete='restrict',
                                 required=True)
    product_uom = fields.Many2one('uom.uom', string='Satuan', required=True)
    vol = fields.Float(string='Cacah/Vol', required=True, default=1.0)
    daily_id = fields.Many2one('project.daily', string='Daily Reference')
    lokasi_asal = fields.Char(string='Lokasi Asal')
    lokasi_tujuan = fields.Char(string='Lokasi Tujuan')
    sequence = fields.Integer(string='Sequence', default=10)
    project_id = fields.Many2one('project.project', string='Project', required=False)
    ref_project_id = fields.Many2one('project.project', string='Ref', related='daily_id.project_id')
    date_daily = fields.Date(string='Ref Date', related='daily_id.date_daily')
    date = fields.Date(string='Date')
    sequence = fields.Integer(string='Sequence', default=10)

    @api.multi
    @api.onchange('product_id', 'product_uom', 'qty')
    def product_id_onchange(self):
        for o in self:
            o.product_uom = o.product_id.uom_id.id
            o.project_id = o.daily_id.project_id.id
            o.date = o.daily_id.date_daily

class PemakaianPeralatan(models.Model):
    _name = 'pemakaian.peralatan'
    _rec_name = 'product_id'
    _order = 'sequence'

    product_id = fields.Many2one('product.product', string='Jenis Peralatan', change_default=True, ondelete='restrict',
                                 required=True)
    qty = fields.Float(string='Jumlah', required=True, default=1.0)
    daily_id = fields.Many2one('project.daily', string='Daily Reference')
    sequence = fields.Integer(string='Sequence', default=10)
    lokasi = fields.Char(string='Lokasi')

class PekerjaaanActivity(models.Model):
    _name = 'pekerjaan.activity'
    _rec_name = 'task_id'
    _order = 'sequence'

    daily_id = fields.Many2one('project.daily', string='Daily Reference')
    task_id = fields.Many2one('project.task', string='Task', required=True, )
    progres_ids = fields.One2many('project.progres', 'task_id', 'Progress')
    sequence = fields.Integer(string='Sequence', default=10)
    actual = fields.Float(compute='_actual_get', store=True, string='Actual (%)')
    plan = fields.Float(compute='_plan_get', store=True, string='Plan (%)')
    total_progress = fields.Float(compute='_progress_get',string='Total Progres (%)')
    kegiatan_hari_ini = fields.Boolean('Kegiatan Hari Ini')

    @api.depends('task_id.total_actual')
    def _progress_get(self):
        for rec in self:
            rec.total_progress += rec.task_id.total_actual

    @api.depends('task_id.total_plan_weight')
    def _plan_get(self):
        for rec in self:
            rec.plan += rec.task_id.total_plan_weight

    @api.depends('task_id.total_actual_weight')
    def _actual_get(self):
        for rec in self:
            rec.actual += rec.task_id.total_actual_weight

class PenghambatPekerjaan(models.Model):
    _name = 'penghambat.pekerjaan'
    _order = 'sequence'

    start_time_jam = fields.Selection([
        ('1', '01'), ('2', '02'), ('3', '03'), ('4', '04'), ('5', '05'), ('6', '06'), ('7', '07'),
        ('8', '08'), ('9', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'),
        ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'),
        ('22', '22'), ('23', '23'), ('24', '24')
    ], string='Start Time')
    start_time_menit = fields.Selection([
        ('00', '00'), ('0.50', '30')
    ], string='Start Time', default='00')
    end_time_jam = fields.Selection([
        ('1', '01'), ('2', '02'), ('3', '03'), ('4', '04'), ('5', '05'), ('6', '06'), ('7', '07'),
        ('8', '08'), ('9', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'),
        ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'),
        ('22', '22'), ('23', '23'), ('24', '24')
    ], string='End Time')
    end_time_menit = fields.Selection([
        ('00', '00'), ('0.50', '30')
    ], string='End Time', default='00')
    daily_id = fields.Many2one('project.daily', string='Daily Reference')
    duration = fields.Float(string='Durasi', compute='_compute_duration', store=True, readonly=True)
    categ_weather_id = fields.Many2one('project.weather.categ', string='Jenis')
    lokasi = fields.Char(string='Lokasi')
    akibat = fields.Text(string='Akibat')
    start = fields.Float(string='Jam Mulai', compute='_compute_duration', store=True, readonly=True)
    end = fields.Float(string='Jam Selesai', compute='_compute_duration', store=True, readonly=True)
    sequence = fields.Integer(string='Sequence', default=10)
    project_id = fields.Many2one('project.project', string='Project', required=False)
    ref_project_id = fields.Many2one('project.project', string='Ref', related='daily_id.project_id')
    date_daily = fields.Date(string='Ref Date', related='daily_id.date_daily')
    date = fields.Date(string='Date')

    @api.multi
    @api.onchange('start_time_jam', 'categ_weather_id')
    def start_time_jam_onchange(self):
        for o in self:
            o.project_id = o.daily_id.project_id.id
            o.date = o.daily_id.date_daily

    @api.depends('start_time_jam', 'start_time_menit', 'end_time_jam', 'end_time_menit')
    def _compute_duration(self):
        for o in self:
            start = float(int(o.start_time_jam) + float(o.start_time_menit))
            end = float(int(o.end_time_jam) + float(o.end_time_menit))
            o.start = start
            o.end = end
            o.duration = end - start

class Laporan(models.Model):
    _name = 'laporan'

    daily_id = fields.Many2one('project.daily', string='Daily Reference')
    point_catatan = fields.Char(string='Point Catatan')
    uraian = fields.Text(string='Uraian')
    ttd_nama = fields.Binary(string='Tanda Tangan dan Nama Jelas')
    filename_ttd = fields.Char('Filename TTD')

class CategoryWeather(models.Model):
    _name = "project.weather.categ"

    name = fields.Char(string="Weather",required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Weather name already exists !"),
    ]
    
class ProjectDesignation(models.Model):
    _name = "project.designation"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Designation name already exists !"),
    ]            
            
            
    