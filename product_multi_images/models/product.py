# -*- coding: utf-8 -*-
# Copyright 2018 Akili Systems
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp
import logging
from odoo import tools
import base64

from PIL import Image
import requests
from io import BytesIO
import urllib
import io

import urllib.request


from PIL import ImageDraw
from PIL import ImageFont
import os
import logging
import tempfile


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    # image_medium = fields.Binary(
    #     "Image", compute='_compute_main_images',
    #     help="This field holds the image used as image for the product, limited to 1024x1024px.")


    # image = fields.Binary(
    #     "Image", compute='_compute_main_images',
    #     help="This field holds the image used as image for the product, limited to 1024x1024px.")

    # @api.depends('product_image_ids.main')
    # def _compute_main_images(self):
    #     for rec in self:
    #         rec.image_medium = rec.get_main_images().image
    #         rec.image = rec.get_main_images().image

    product_image_ids = fields.One2many('product.image', 'product_tmpl_id', string='Images')
    main_change = fields.Boolean("main_change")
    line_change = fields.Boolean("line change")

    



    def get_main_images(self):
        return self.env['product.image'].search([('main','=',True),('id','in',self.product_image_ids.ids)],limit=1)

    def get_selector_images(self):
        return self.env['product.image'].search([('selector','=',True),('main','=',False),('id','in',self.product_image_ids.ids)])

    def get_line_images(self):
        return self.env['product.image'].search([('line','=',True),('id','in',self.product_image_ids.ids)],limit=1)


   

    



    
 
class ProductProduct(models.Model):
    _inherit = "product.product"


    salla_variant_price = fields.Float('Salla Price')



    @api.depends('list_price','salla_variant_price', 'price_extra')
    @api.depends_context('uom')
    def _compute_product_lst_price(self):
        res = super(ProductProduct, self)._compute_product_lst_price()
        for product in self:
            if product.salla_variant_price >0:
                product.lst_price = product.salla_variant_price
        


    # image_variant = fields.Binary(
    #     "Variant Image", compute='_compute_main_images',
    #     help="This field holds the image used as image for the product variant, limited to 1024x1024px.")

    product_image_ids = fields.One2many('product.image', 'product_variant_id', string='Images')
    main_change = fields.Boolean("main_change")


    temp_default = fields.Boolean(string='TDefault')
    

    

    # @api.depends('product_image_ids.main')
    # def _compute_main_images(self):
    #     for rec in self:
    #         rec.image_variant = rec.get_main_images().image

    @api.onchange('image_medium')
    def _onchange_image_medium(self):
        if not self.image_medium or self.main_change:
            self.main_change = False
            return False
        for image in self.product_image_ids:
            if image.main:
                image.main = False
        self.product_image_ids = [(0,0,{'main':True,'selector':True,'image':self.image_medium})]

    def get_main_images(self):
        return self.env['product.image'].search([('main','=',True),('id','in',self.product_image_ids.ids)],limit=1)

    def get_selector_images(self):
        return self.env['product.image'].search([('selector','=',True),('main','=',False),('id','in',self.product_image_ids.ids)])

    def get_line_images(self):
        return self.env['product.image'].search([('line','=',True),('id','in',self.product_image_ids.ids)],limit=1)

   


class ProductImage(models.Model):
    _inherit = 'product.image'
    _order = 'sequence'

    @api.onchange('main','image')
    def _onchange_main(self):
        self.sequence_selected = True
        if self.main:
            self.main_change = True

    @api.onchange('line')
    def _change_line_image(self):
        if self.line:
            self.line_change = True
        else:
            self.line_change = False    

    @api.model
    def create(self,vals):
        date_list = []
        res = super(ProductImage, self).create(vals)
        if vals.get('main'):
            if res.product_variant_id:
                temp_image_ids = res.product_variant_id.product_image_ids
                for variant_image in temp_image_ids:
                    date_list.append(variant_image.create_date)
                for variant_image in temp_image_ids:
                    if variant_image.create_date != max(date_list):
                        variant_image.main = False
                res.product_variant_id.write({'image_variant':res.image}) 
            if res.product_tmpl_id:
                self.product_tmpl_id.write({'image':self.image})
        if vals.get('line'):
            if res.product_variant_id:
                temp_image_ids = res.product_variant_id.product_image_ids
                for variant_image in temp_image_ids:
                    date_list.append(variant_image.create_date)
                for variant_image in temp_image_ids:
                    if variant_image.create_date != max(date_list):
                        variant_image.line = False 
            if res.product_tmpl_id:
                temp_image_ids = res.product_tmpl_id.product_image_ids
                for template_image in temp_image_ids:
                    date_list.append(template_image.create_date)
                for template_image in temp_image_ids:
                    if template_image.create_date != max(date_list):
                        template_image.line = False
        return res

    def unlink(self):
        for product_images in self:
            if product_images.is_product_template and product_images._context['params']['model']=='product.product':
                raise ValidationError(_('We can not unlink template record.'))
            if product_images.main:
                raise ValidationError(_('We can not unlink main record.')) 
            if 'sale_multi_pricelist_product_template' in product_images._context:
                for variant in product_images.product_tmpl_id.product_variant_ids:
                    for image in variant.product_image_ids:
                        if product_images.id == image.parent_id.id:
                            image.unlink()
            # product_images._context['params']['model']=='product.product'
            if product_images.parent_id and 'sale_multi_pricelist_product_template' not in product_images._context:
                raise ValidationError(_('We can not unlink record from Product.'))
        res = super(ProductImage, self).unlink()
        return res     
 
    parent_id = fields.Many2one('product.image', string='Parent Image')    
    product_tmpl_id = fields.Many2one('product.template', 'Related Product', copy=True) 
    product_variant_id = fields.Many2one('product.product', 'Related Product', copy=True)    
    image = fields.Binary('Image', attachment=True)
    # miduam_image = fields.Binary('Image',  compute='_compute_images' )
    main = fields.Boolean("Main")
    selector = fields.Boolean("Selector")
    line = fields.Boolean("Line")
    main_change = fields.Boolean("main_change")
    line_change = fields.Boolean("line_change")
    desc = fields.Text("Description")
    file_link = fields.Char("File/Link")
    sequence = fields.Integer(string='Sequence', default=10)
    sequence_selected = fields.Boolean(string='Sequence Selected')
    product_variant_image = fields.Binary(string='Image', compute='get_product_variant_image',store=False)
    virtual_image = fields.Binary(string='Image', compute='get_virtual_image',store=False)
    is_product_template = fields.Boolean(string='Is Template')
    type_url = fields.Selection([
                ('image', 'Image'),
                ('video', 'Video'),
                
            ], string='URL Type', readonly=True)


    def get_product_variant_image(self):
        for rec in self:
            if rec.parent_id:
                rec.product_variant_image = rec.parent_id.image

    def get_virtual_image(self):
        for rec in self:
            if rec.parent_id:
                rec.virtual_image = rec.parent_id.image
            else:
                 rec.virtual_image = rec.image

    @api.onchange('file_link')
    def get_file_link(self):
        img1 = False
        var_img = False
        try:
            if self.file_link:
                response = requests.get(self.file_link)
                img = Image.open(BytesIO(response.content))
                img.save('url_img.png')
                imgfile = Image.open('url_img.png')
                f = open('url_img.png' , 'rb') 
                img1 = base64.encodestring(f.read()) 
                f.close()
                os.remove('url_img.png')
                self.image = img1
        except:
            return {'warning': {
                            'title': _('Wrong url'),
                            'message': _('Please provide correct URL or check your image size.!')
                        }}        


    # @api.onchange('image')
    # def onchange_image(self):
    #     self.ensure_one()
    #     # if not self.image:
    #     #     raise UserError("no image on this record")
    #     # decode the base64 encoded data
    #     data = base64.decodestring(self.image)
    #     # create a temporary file, and save the image
    #     fobj = tempfile.NamedTemporaryFile(delete=False)
    #     fname = fobj.name
    #     fobj.write(data)
    #     fobj.close()
    #     self.file_link = fname
    #     # open the image with PIL
    #     try:
    #         image = Image.open(fname)
    #         # do stuff here
    #     finally:
    #         # delete the file when done
    #         os.unlink(fname)    
         

class ProductImageExtra(models.Model):
    _name = 'product.image.extra'
    _description = 'Product Image'

    name = fields.Char('Name')
    image = fields.Binary('Image', attachment=True)
