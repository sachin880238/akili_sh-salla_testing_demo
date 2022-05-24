from odoo import models, api, fields, _
import http.client
import json
import numpy as np
import urllib.request
import cv2
import requests
from PIL import Image
import base64
import os
from io import BytesIO
import uuid

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    salla_id = fields.Char('Salla Id')
    promotion_id = fields.Many2one('promotion.promotion',string="Promotion")

    def convert_url_image_data(self,url):
        print("-------------->>>",url)
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.save('url_img.png')
        imgfile = Image.open('url_img.png')
        f = open('url_img.png' , 'rb') 
        img1 = base64.encodestring(f.read()) 
        f.close()
        os.remove('url_img.png')
        return img1


class ProductProduct(models.Model):
    _inherit = 'product.product'

    salla_id = fields.Char('Salla Id')


    

class ProductTemplateAttributeline(models.Model):
    _inherit = 'product.template.attribute.line'

    salla_id = fields.Char('Salla Id')

class ProductAttributeline(models.Model):
    _inherit = 'product.attribute'

    salla_id = fields.Char('Salla Id')

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    salla_id = fields.Char('Salla Id')

