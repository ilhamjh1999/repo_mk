from odoo import api, fields, models, tools, _


class PhotoGalery(models.Model):
    _name = 'photo.galery'
    

    name = fields.Char('Photo Name')
    image = fields.Binary(
        "Photo", help="Image of the product variant (Big-sized image of product template if false). It is automatically "
             "resized as a 1024x1024px image, with aspect ratio preserved.")
    image_small = fields.Binary(
        "Small-sized image", compute='_compute_images', inverse='_set_image_small',
        help="Image of the product variant (Small-sized image of product template if false).")
    image_medium = fields.Binary(
        "Medium-sized image", compute='_compute_images', inverse='_set_image_medium',
        help="Image of the product variant (Medium-sized image of product template if false).")
    descrip = fields.Char('Description')
    picture_date = fields.Date(string='Picture Date')
    project_id = fields.Many2one('project.project', string='Project',required=True)
    task_id = fields.Many2one('project.task', string='Task', required=True,)
    
    @api.one
    def _compute_images(self):
        if self._context.get('bin_size'):
            self.image_medium = self.image
            self.image_small = self.image
            
        else:
            resized_images = tools.image_get_resized_images(self.image, return_big=True, avoid_resize_medium=True)
            self.image_medium = resized_images['image_medium']
            self.image_small = resized_images['image_small']
           
        if not self.image_medium:
            self.image_medium = self.image_medium
        if not self.image_small:
            self.image_small = self.image_small
        

    @api.one
    def _set_image_medium(self):
        self._set_image_value(self.image_medium)

    @api.one
    def _set_image_small(self):
        self._set_image_value(self.image_small)

    @api.one
    def _set_image_value(self, value):
        image = tools.image_resize_image_big(value)
        if self.image:
            self.image = image