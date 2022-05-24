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
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime ,timedelta
import logging






class ResUsers(models.Model):
    
    _inherit = 'res.users'
    
    access_token = fields.Char('Access Token')
    


    def action_generate_password(self):
        self.access_token=str(uuid.uuid4())


class ResPartner(models.Model):
    
    _inherit = 'res.partner'
    
    dupli_mobile =  fields.Char("Mobile number",compute="_compute_duplicate_mobile",store=True)




    @api.depends('mobile')
    def _compute_duplicate_mobile(self):
        for rec in self:
            if rec.mobile:
                number=rec.mobile
                number = number.replace("+", "").replace(" ", "")
                rec.dupli_mobile=number
            else:
                rec.dupli_mobile=''

class SyncDataWizard(models.Model):
    
    _name = 'sync.data.wizard'
    _description = "Server configuration and data"


    name = fields.Char(string="Server Name")
    customer_count = fields.Integer(default=1)
    url = fields.Char('URL')
    api_key = fields.Char('API KEY')
    state = fields.Selection([
            ('connect','Connect'),
            ('disconnect','Disconnect'),
            ],string="Status",default="disconnect")


    def button_update_product(self):
        product_ids = self.env['product.product'].search([])
        for product_id in product_ids:
            product_id.write({'invoice_policy':'order'})



    def button_map_existing_customer(self):
        conn =  http.client.HTTPSConnection(self.url)


        headers = {
            'Content-Type': "application/json",
             
            'Authorization':'Bearer '+str(self.api_key)
            }

        conn.request("GET", "/admin/v2/customers", headers=headers)

        res = conn.getresponse()
        data = res.read()
        cust_env=self.env['res.partner']
        cust_mapping = self.env['customermap.customermap']
        record=json.loads(data.decode('utf-8'))
        count=self.customer_count
        loop_one_time=100
        loop_count=1
        print("---------------------------------",record)
        for i in range(count,record['pagination']['total']+1):

            conn.request("GET", "/admin/v2/customers?page="+str(i), headers=headers)
            
            res = conn.getresponse()
            customer_data=json.loads(res.read().decode('utf-8'))
        
            for rec in customer_data['data']:
                if rec['mobile'] and rec['email']:
                    odoo_cust_id = cust_env.search([('dupli_mobile','=',str(rec['mobile'])),('email','=',rec['email']),('salla_id','=',False)])
                elif not rec['mobile'] and rec['email']:
                    odoo_cust_id = cust_env.search([('email','=',rec['email']),('salla_id','=',False)])
                elif rec['mobile'] and not rec['email']:
                    odoo_cust_id = cust_env.search([('dupli_mobile','=',str(rec['mobile'])),('salla_id','=',False)])
                print("---------------->>>>>>>>>>>>",odoo_cust_id,odoo_cust_id.salla_id,str(rec['mobile']),rec['email'])
                if odoo_cust_id:
                
                    vals={
                    'name':rec['first_name']+' '+rec['last_name'],
                    'salla_id':rec['id'],
                    'customer_rank': 1

                    }
                    if rec['mobile']:
                        vals['mobile']=rec['mobile']
                    if rec['email']:
                        vals['email']=rec['email']
                    if rec['email']:
                        vals['email']=rec['email']
                    if rec['avatar']:
                        try:
                            response = requests.get(rec['avatar'])
                            img = Image.open(BytesIO(response.content))
                            img.save('url_img.png')
                            imgfile = Image.open('url_img.png')
                            f = open('url_img.png' , 'rb') 
                            img1 = base64.encodestring(f.read()) 
                            f.close()
                            os.remove('url_img.png')
                            vals['image_1920'] = img1
                        except:
                            vals['image_1920']=False
                    if rec['city']:
                        vals['city']=rec['city']
                    odoo_cust_id.write(vals)
                    customer_map_val={
                        'partner_id':odoo_cust_id.id,
                        'odoo_id':odoo_cust_id.id,
                        'ecom_id':rec['id']
                        }
                    cust_mapping.create(customer_map_val)
            loop_count=loop_count+1
            if loop_one_time == loop_count:
                self.customer_count=self.customer_count+100
                break



    def button_sync_customer(self):
        conn =  http.client.HTTPSConnection(self.url)


        headers = {
            'Content-Type': "application/json",
             
            'Authorization':'Bearer '+str(self.api_key)
            }

        conn.request("GET", "/admin/v2/customers", headers=headers)

        res = conn.getresponse()
        data = res.read()
        cust_env=self.env['res.partner']
        cust_mapping = self.env['customermap.customermap']
        record=json.loads(data.decode('utf-8'))
        count=self.customer_count
        loop_one_time=100
        loop_count=1

        for i in range(count,record['pagination']['total']+1):

            conn.request("GET", "/admin/v2/customers?page="+str(i), headers=headers)
            
            res = conn.getresponse()
            customer_data=json.loads(res.read().decode('utf-8'))
        
            for rec in customer_data['data']:
                salla_cust_id = cust_env.search([('salla_id','=',str(rec['id']))])
                if not salla_cust_id:
                
                    vals={
                    'name':rec['first_name']+' '+rec['last_name'],
                    'salla_id':rec['id'],
                    'customer_rank': 1

                    }
                    if rec['mobile']:
                        vals['mobile']=rec['mobile']
                    if rec['email']:
                        vals['email']=rec['email']
                    if rec['email']:
                        vals['email']=rec['email']
                    if rec['avatar']:
                        try:
                            response = requests.get(rec['avatar'])
                            img = Image.open(BytesIO(response.content))
                            img.save('url_img.png')
                            imgfile = Image.open('url_img.png')
                            f = open('url_img.png' , 'rb') 
                            img1 = base64.encodestring(f.read()) 
                            f.close()
                            os.remove('url_img.png')
                            vals['image_1920'] = img1
                        except:
                            vals['image_1920']=False
                    if rec['city']:
                        vals['city']=rec['city']
                    customer_id = cust_env.create(vals)
                    customer_map_val={
                        'partner_id':customer_id.id,
                        'odoo_id':customer_id.id,
                        'ecom_id':rec['id']
                        }
                    cust_mapping.create(customer_map_val)
            loop_count=loop_count+1
            if loop_one_time == loop_count:
                self.customer_count=self.customer_count+100
                break


    def button_sync_tax(self):

        conn =  http.client.HTTPSConnection(self.url)


        headers = {
            'Content-Type': "application/json",
             
            'Authorization':'Bearer '+str(self.api_key),
            }

        conn.request("GET", "/admin/v2/taxes", headers=headers)


        res = conn.getresponse()
        data = res.read()
        tax_env=self.env['account.tax']
        record=json.loads(data.decode('utf-8'))
        for rec in record['data']:
            tax_id = tax_env.search([('salla_id','=',rec['id'])])
            if not tax_id:

                tax_val = tax_env.default_get(list(tax_env.fields_get()))
                tax_val.update({
                    'salla_id':rec['id'],
                    'amount':rec['tax'],
                    'active':rec['status'],
                    'name':'tax '+str(rec['tax'])
                })
                new_tax_id=tax_env.create(tax_val)
                # new_tax_id.default_get()





    def button_sync_orders(self):
        conn =  http.client.HTTPSConnection(self.url)


        headers = {
            'Content-Type': "application/json",
             
            'Authorization':'Bearer '+str(self.api_key),
            }

        conn.request("GET", "/admin/v2/orders", headers=headers)


        res = conn.getresponse()
        data = res.read()
        order_env=self.env['sale.order']
        cust_env=self.env['res.partner']
        order_status_env=self.env['order.status']
        product_env=self.env['product.template']
        product_env_map=self.env['producttempmap.producttempmap']
        product_attr_env=self.env['attributemap.attributemap']
        product_attr_val_env_map=self.env['attributeval.attributeval']
        product_attr_val_env=self.env['product.attribute.value']
        product_variant_env=self.env['product.product']

        product_variant_env_map=self.env['productmap.productmap']
        website_categ_env=self.env['product.public.category']
        promotion_val_env=self.env['promotion.promotion']
        sale_order_env=self.env['sale.order']
        sale_mapping= self.env['sale.order.map']
        record=json.loads(data.decode('utf-8'))
        logging.info("ASS----------%s",str(record))
        for rec in record['data']:
            
            order_id = order_env.search([('salla_id','=',rec['id'])])
            if not order_id:
                order_val={
                    'salla_id':rec['id'],
                    'reference':rec['reference_id'],

                }
                if rec['status']:
                    order_status_id = order_status_env.search([('salla_id','=',rec['status']['id'])])
                    if not order_status_id:
                        order_status_val={
                            'salla_id':rec['status']['id'],
                            'name':rec['status']['name']
                        }
                        order_status_id=order_status_env.create(order_status_val)
                        order_val['order_status_id']=order_status_id.id
                    else:
                        order_val['order_status_id']=order_status_id.id
                conn.request("GET", "/admin/v2/orders/"+str(rec['id'])+"?expanded=true", headers=headers)

                order_data = conn.getresponse()
                order_detail = order_data.read()
                record_order_details=json.loads(order_detail.decode('utf-8'))
                order_data=[]
                for item_data in record_order_details['data']['items']:
                    tax_id =self.env['account.tax'].sudo().search([('amount','=',float(item_data['amounts']['tax']['percent']))],limit=1)
                    if tax_id:
                        order_line={
                            'product_uom_qty':item_data['quantity'],
                            'weight':item_data['weight'],
                            # 'price_unit':item_data['product']['price']['amount'],
                            'price_unit':item_data['amounts']['price_without_tax']['amount'],
                            'tax_id':[(6,0,[tax_id.id])],
                            # 'is_tax_fixed':True,
                            # 'custom_tax_amount':item_data['amounts']['tax']['amount']['amount'],
                            'name':item_data['name'],
                            'salla_id':item_data['id'],

                            }
                    else:
                        order_line={
                            'product_uom_qty':item_data['quantity'],
                            'weight':item_data['weight'],
                            # 'price_unit':item_data['product']['price']['amount'],
                            'price_unit':item_data['amounts']['price_without_tax']['amount'],
                            'tax_id':[(6,0,[])],
                            # 'is_tax_fixed':True,
                            # 'custom_tax_amount':item_data['amounts']['tax']['amount']['amount'],
                            'name':item_data['name'],
                            'salla_id':item_data['id'],

                            }
                    # order_line={
                    # 'product_uom_qty':item_data['quantity'],
                    # 'weight':item_data['weight'],
                    # 'price_unit':item_data['amounts']['price_without_tax']['amount'],
                    # 'tax_id':[(6,0,[])],
                    # 'is_tax_fixed':True,
                    # 'custom_tax_amount':item_data['amounts']['tax']['amount']['amount'],

                    # }
                    product_tmpl_id = product_env.sudo().search([('salla_id','=',item_data['product']['id'])])
                    product_variant_ids = product_variant_env.sudo().search([('product_tmpl_id','=',product_tmpl_id.id)])
                    value_ids =[]
                    if len(item_data['options'])>0:
                        for option_data in item_data['options']:
                            value_id = product_attr_val_env.search([('salla_id','=',option_data['value']['id'])])
                            if value_id:
                                value_ids.append(value_id.id)
                        if len(value_ids) >0:
                            value_ids.sort()
                            for product in product_variant_ids:
                                attr_value_ids=[]
                                for product_attr_value in product.product_template_attribute_value_ids:
                                    attr_value_ids.append(int(product_attr_value.product_attribute_value_id.id))
                                attr_value_ids.sort()
                                if attr_value_ids == value_ids:
                                    order_line['product_id']=product.id
                                    order_line['name']=product.name
                                    order_data.append((0,0,order_line))
                    else:
                        if len(product_variant_ids.ids) == 1:
                            order_line['product_id']=product_variant_ids.id
                            order_line['name']=product_variant_ids.name
                            order_data.append((0,0,order_line))
                if len(order_data)<=0:
                    continue
                else:
                    (dt, mSecs) = rec['date']['date'].strip().split(".") 
                    date_time_obj = datetime.strptime('2022-3-31 13:28:43', '%Y-%m-%d %H:%M:%S')

                    cust_id = self.env['res.partner'].search([('salla_id','=',record_order_details['data']['customer']['id'])])
                    if cust_id:
                        order_val['date_order']=date_time_obj
                        order_val['partner_id']=cust_id.id
                        order_val['order_line']=order_data
                        sale_id=sale_order_env.create(order_val)
                        sale_map_val={
                        'sale_id':sale_id.id,
                        'odoo_id':sale_id.id,
                        'ecom_id':rec['id']
                        }
                        sale_mapping.create(sale_map_val)
                        if record_order_details['data']['amounts']['shipping_cost']['amount'] >0:
                            carrier_id=request.env['delivery.carrier'].sudo().search([('delivery_type','=','fixed')],limit=1)
                            sale_id.set_delivery_line(carrier_id, record_order_details['data']['amounts']['shipping_cost']['amount'])
                            sale_id.write({
                                'recompute_delivery_price': False,
                                'delivery_message': '',
                            })
                        
                break





            
    def button_update_odoo_product(self):
        conn =  http.client.HTTPSConnection(self.url)


        headers = {
            'Content-Type': "application/json",
             
            'Authorization':'Bearer '+str(self.api_key)
            }

        conn.request("GET", "/admin/v2/products", headers=headers)

        res = conn.getresponse()
        data = res.read()
        product_env=self.env['product.template']
        product_env_map=self.env['producttempmap.producttempmap']
        product_attr_env=self.env['attributemap.attributemap']
        product_attr_val_env_map=self.env['attributeval.attributeval']
        product_attr_val_env=self.env['product.attribute.value']
        product_variant_env=self.env['product.product']
        product_variant_env_map=self.env['productmap.productmap']
        website_categ_env=self.env['product.public.category']
        promotion_val_env=self.env['promotion.promotion']
        adj_obj = self.env['stock.inventory']
        adj_line_obj = self.env['stock.inventory.line']
        
        record=json.loads(data.decode('utf-8'))
        for i in range(1,record['pagination']['total']+1):
            conn.request("GET", "/admin/v2/products?page="+str(i), headers=headers)
            record=json.loads(data.decode('utf-8'))
            res = conn.getresponse()
            data = res.read()
            for rec in record['data']:
                if rec['sku']:
                    product_id = product_env.search([('salla_id','=',False),('default_code','=',rec['sku'])])
                    if product_id:
                        vals={
                            'salla_id':rec['id'],
                            'name':rec['name'],
                            'type':'product',
                            'default_code':rec['sku'],
                            'barcode':rec['sku'],
                            'lst_price':rec['price']['amount'],
                            'standard_price':rec['price']['amount'],
                            'weight':rec['weight'],
                            'description':rec['description'],
                            'invoice_policy':'order'


                           
                            }
                        if rec['promotion']:
                            if rec['promotion']['title'] != None:
                                promotion_val={
                                'name':rec['promotion']['title'],
                                'title':rec['promotion']['title'],
                                'sub_title':rec['promotion']['sub_title'],
                                }
                                promotion_id=promotion_val_env.create(promotion_val)
                                vals['promotion_id']=promotion_id.id
                        option_list=[]
                        for option in rec['options']:
                            attribute_id = self.env['product.attribute'].search([('salla_id','=',option['id'])])
                            if not attribute_id:
                                attribute_id = self.env['product.attribute'].create({
                                    'salla_id':option['id'],
                                    'name':option['name'],
                                    'display_type':option['type'],
                                    })
                                option_val={
                                    'attribute_id':attribute_id.id

                                }
                                product_attr_env.create({
                                    'attribute_id':attribute_id.id,
                                    'odoo_id':attribute_id.id,
                                    'ecom_id':option['id']
                                    })
                            else:
                                option_val={
                                    'attribute_id':attribute_id.id
                                    }
                            
                            value_list=[]
                            for value in option['values']:
                                value_attribute_id = self.env['product.attribute.value'].search([('salla_id','=',value['id']),('attribute_id','=',attribute_id.id)])
                                if value_attribute_id:

                                    value_list.append((4,value_attribute_id.id))
                                else:
                                    value_dict={
                                        'salla_id':value['id'],
                                        'name':value['name'],
                                        'attribute_id':attribute_id.id
                                    }
                                    value_attribute_id=product_attr_val_env.create(value_dict)
                                    product_attr_val_env_map.create({
                                        'attribute_value_id':value_attribute_id.id,
                                        'odoo_id':value_attribute_id.id,
                                        'ecom_id':value['id'],
                                        })
                                    value_list.append((4,value_attribute_id.id))

                            option_val['value_ids']=value_list
                            option_list.append((0,0,option_val))
                        vals['attribute_line_ids']=option_list
                        website_categ_ids=[]
                        for categ in rec['categories']:
                            categ_id=website_categ_env.search([('salla_id','=',categ['id'])])
                            if categ_id:
                                website_categ_ids.append(categ_id.id)
                        vals['public_categ_ids']=[(6,0,website_categ_ids)]
                        img_data=[]
                        for image in rec['images']:
                            if image['type'] == 'image':
                                image_val={
                                    'file_link':image['url'],
                                    'name':image['id'],

                                }
                                image_data=product_env.convert_url_image_data(image['url'])
                                image_val['image'] = image_data
                                if image['main'] == True:
                                    image_val['main']=True
                                    vals['image_1920']=image_data
                                img_data.append((0,0,image_val))
                            elif image['type'] == 'image':
                                image_val={
                                    'file_link':image['url'],
                                    'name':image['id'],
                                }
                                img_data.append((0,0,image_val))
                        vals['product_image_ids']=img_data
                        

                        product_id.write(vals)
                        tmpl_id = product_id
                        if len(rec['options']) ==0:
                            product_id = product_variant_env.sudo().search([('product_tmpl_id','=',tmpl_id.id)])
                            date_time_format = DEFAULT_SERVER_DATETIME_FORMAT
                            wl_adjust_id = adj_obj.sudo().create({
                               'name':datetime.today().strftime(date_time_format),
                               'location_ids':[(6,0,[8])], 
                                          })
                            wl_res = wl_adjust_id.sudo().write({'product_ids':[(6,0,product_id.ids)]})
                            wl_adjust_id.sudo().action_start()

                            available_product=adj_line_obj.sudo().search([('inventory_id','=',wl_adjust_id.id),('product_id','=',product_id.id)])
                            if available_product:
                                if rec['quantity'] != None:
                                    available_product.sudo().write({'product_qty':int(rec['quantity'])})
                            else:
                                if rec['quantity'] != None:
                                    adj_line_obj.sudo().create({
                                                'product_id':product_id.id,
                                                'product_qty':int(rec['quantity']),
                                                'inventory_id':wl_adjust_id.id, 
                                                'location_id':8,
                                                      })
                            wl_adjust_id.sudo().custom_action_validate()
                        product_env_map.create({
                            'product_template_id':tmpl_id.id,
                            'odoo_id':tmpl_id.id,
                            'ecom_id':rec['id']
                            })
                        
                        product_ids = product_variant_env.search([('product_tmpl_id','=',tmpl_id.id)])
                        for product_variant_data in rec['skus']:
                            for product in product_ids:
                                attr_value_ids=[]
                                for product_attr_value in product.product_template_attribute_value_ids:
                                    attr_value_ids.append(int(product_attr_value.product_attribute_value_id.salla_id))
                                attr_value_ids.sort()
                                product_variant_data['related_options'].sort()
                                if attr_value_ids == product_variant_data['related_options']:
                                    val={
                                    'salla_id':product_variant_data['id'],
                                    # 'lst_price':product_variant_data['sale_price']['amount'],
                                    # 'standard_price':product_variant_data['price']['amount'],
                                    }
                                    # if product_variant_data['sale_price'] != None:
                                    #     val['lst_price']=product_variant_data['sale_price']['amount']
                                    if product_variant_data['price'] != None:
                                        val['standard_price']=product_variant_data['price']['amount']
                                        val['lst_price']=product_variant_data['price']['amount']
                                    if product_variant_data['sku'] != None:
                                        val['default_code']=product_variant_data['sku']
                                        val['barcode']=product_variant_data['sku']
                                    product.sudo().write(val)
                                    if product_variant_data['stock_quantity'] > 0:
                                        date_time_format = DEFAULT_SERVER_DATETIME_FORMAT
                                        wl_adjust_id = adj_obj.sudo().create({
                                           'name':datetime.today().strftime(date_time_format),
                                           'location_ids':[(6,0,[8])], 
                                                      })
                                        wl_res = wl_adjust_id.sudo().write({'product_ids':[(6,0,product.ids)]})
                                        wl_adjust_id.sudo().action_start()

                                        available_product=adj_line_obj.sudo().search([('inventory_id','=',wl_adjust_id.id),('product_id','=',product.id)])
                                        quantity_count =0
                                        if available_product:
                                            if available_product.product_qty != int(product_variant_data['stock_quantity']):
                                                quantity_count=quantity_count+1
                                                available_product.sudo().write({'product_qty':int(product_variant_data['stock_quantity'])})
                                        else:
                                            quantity_count=quantity_count+1
                                            adj_line_obj.sudo().create({
                                                        'product_id':product.id,
                                                        'product_qty':int(product_variant_data['stock_quantity']),
                                                        'inventory_id':wl_adjust_id.id, 
                                                        'location_id':8,
                                                              })
                                        if quantity_count != 0:
                                            wl_adjust_id.sudo().custom_action_validate()
                                        else:
                                            wl_adjust_id.sudo().action_cancel_draft()
                                            wl_adjust_id.unlink()
                                    if product_variant_data['price'] != None:
                                        # for product_attr_value in product.product_template_attribute_value_ids:
                                        product.sudo().write({'salla_variant_price':product_variant_data['price']['amount']})
                                        
                                    product_variant_env_map.create({
                                        'product_id':product.id,
                                        'odoo_id':product.id,
                                        'ecom_id':product_variant_data['id'],
                                        })


                            
                






    def button_sync_products(self):
        conn =  http.client.HTTPSConnection(self.url)


        headers = {
            'Content-Type': "application/json",
             
            'Authorization':'Bearer '+str(self.api_key)
            }

        conn.request("GET", "/admin/v2/products", headers=headers)

        res = conn.getresponse()
        data = res.read()
        product_env=self.env['product.template']
        product_env_map=self.env['producttempmap.producttempmap']
        product_attr_env=self.env['attributemap.attributemap']
        product_attr_val_env_map=self.env['attributeval.attributeval']
        product_attr_val_env=self.env['product.attribute.value']
        product_variant_env=self.env['product.product']
        product_variant_env_map=self.env['productmap.productmap']
        website_categ_env=self.env['product.public.category']
        promotion_val_env=self.env['promotion.promotion']
        adj_obj = self.env['stock.inventory']
        adj_line_obj = self.env['stock.inventory.line']
        
        record=json.loads(data.decode('utf-8'))
        for i in range(1,record['pagination']['total']+1):
            conn.request("GET", "/admin/v2/products?page="+str(i), headers=headers)
            record=json.loads(data.decode('utf-8'))
            res = conn.getresponse()
            data = res.read()
            for rec in record['data']:
                product_id = product_env.search([('salla_id','=',rec['id'])])
                if not product_id:
                    vals={
                        'salla_id':rec['id'],
                        'name':rec['name'],
                        'type':'product',
                        'default_code':rec['sku'],
                        'barcode':rec['sku'],
                        'lst_price':rec['price']['amount'],
                        'standard_price':rec['price']['amount'],
                        'weight':rec['weight'],
                        'description':rec['description'],
                        'invoice_policy':'order'


                       
                        }
                    if rec['promotion']:
                        if rec['promotion']['title'] != None:
                            promotion_val={
                            'name':rec['promotion']['title'],
                            'title':rec['promotion']['title'],
                            'sub_title':rec['promotion']['sub_title'],
                            }
                            promotion_id=promotion_val_env.create(promotion_val)
                            vals['promotion_id']=promotion_id.id
                    option_list=[]
                    for option in rec['options']:
                        attribute_id = self.env['product.attribute'].search([('salla_id','=',option['id'])])
                        if not attribute_id:
                            attribute_id = self.env['product.attribute'].create({
                                'salla_id':option['id'],
                                'name':option['name'],
                                'display_type':option['type'],
                                })
                            option_val={
                                'attribute_id':attribute_id.id

                            }
                            product_attr_env.create({
                                'attribute_id':attribute_id.id,
                                'odoo_id':attribute_id.id,
                                'ecom_id':option['id']
                                })
                        else:
                            option_val={
                                'attribute_id':attribute_id.id
                                }
                        
                        value_list=[]
                        for value in option['values']:
                            value_attribute_id = self.env['product.attribute.value'].search([('salla_id','=',value['id']),('attribute_id','=',attribute_id.id)])
                            if value_attribute_id:

                                value_list.append((4,value_attribute_id.id))
                            else:
                                value_dict={
                                    'salla_id':value['id'],
                                    'name':value['name'],
                                    'attribute_id':attribute_id.id
                                }
                                value_attribute_id=product_attr_val_env.create(value_dict)
                                product_attr_val_env_map.create({
                                    'attribute_value_id':value_attribute_id.id,
                                    'odoo_id':value_attribute_id.id,
                                    'ecom_id':value['id'],
                                    })
                                value_list.append((4,value_attribute_id.id))

                        option_val['value_ids']=value_list
                        option_list.append((0,0,option_val))
                    vals['attribute_line_ids']=option_list
                    website_categ_ids=[]
                    for categ in rec['categories']:
                        categ_id=website_categ_env.search([('salla_id','=',categ['id'])])
                        if categ_id:
                            website_categ_ids.append(categ_id.id)
                    vals['public_categ_ids']=[(6,0,website_categ_ids)]
                    img_data=[]
                    for image in rec['images']:
                        if image['type'] == 'image':
                            image_val={
                                'file_link':image['url'],
                                'name':image['id'],

                            }
                            image_data=product_env.convert_url_image_data(image['url'])
                            image_val['image'] = image_data
                            if image['main'] == True:
                                image_val['main']=True
                                vals['image_1920']=image_data
                            img_data.append((0,0,image_val))
                        elif image['type'] == 'image':
                            image_val={
                                'file_link':image['url'],
                                'name':image['id'],
                            }
                            img_data.append((0,0,image_val))
                    vals['product_image_ids']=img_data
                    

                    tmpl_id = product_env.create(vals)
                    if len(rec['options']) ==0:
                        product_id = product_variant_env.sudo().search([('product_tmpl_id','=',tmpl_id.id)])
                        date_time_format = DEFAULT_SERVER_DATETIME_FORMAT
                        wl_adjust_id = adj_obj.sudo().create({
                           'name':datetime.today().strftime(date_time_format),
                           'location_ids':[(6,0,[8])], 
                                      })
                        wl_res = wl_adjust_id.sudo().write({'product_ids':[(6,0,product_id.ids)]})
                        wl_adjust_id.sudo().action_start()

                        available_product=adj_line_obj.sudo().search([('inventory_id','=',wl_adjust_id.id),('product_id','=',product_id.id)])
                        if available_product:
                            if rec['quantity'] != None:
                                available_product.sudo().write({'product_qty':int(rec['quantity'])})
                        else:
                            if rec['quantity'] != None:
                                adj_line_obj.sudo().create({
                                            'product_id':product_id.id,
                                            'product_qty':int(rec['quantity']),
                                            'inventory_id':wl_adjust_id.id, 
                                            'location_id':8,
                                                  })
                        wl_adjust_id.sudo().custom_action_validate()
                    product_env_map.create({
                        'product_template_id':tmpl_id.id,
                        'odoo_id':tmpl_id.id,
                        'ecom_id':rec['id']
                        })
                    
                    product_ids = product_variant_env.search([('product_tmpl_id','=',tmpl_id.id)])
                    for product_variant_data in rec['skus']:
                        for product in product_ids:
                            attr_value_ids=[]
                            for product_attr_value in product.product_template_attribute_value_ids:
                                attr_value_ids.append(int(product_attr_value.product_attribute_value_id.salla_id))
                            attr_value_ids.sort()
                            product_variant_data['related_options'].sort()
                            if attr_value_ids == product_variant_data['related_options']:
                                val={
                                'salla_id':product_variant_data['id'],
                                # 'lst_price':product_variant_data['sale_price']['amount'],
                                # 'standard_price':product_variant_data['price']['amount'],
                                }
                                # if product_variant_data['sale_price'] != None:
                                #     val['lst_price']=product_variant_data['sale_price']['amount']
                                if product_variant_data['price'] != None:
                                    val['standard_price']=product_variant_data['price']['amount']
                                    val['lst_price']=product_variant_data['price']['amount']
                                if product_variant_data['sku'] != None:
                                    val['default_code']=product_variant_data['sku']
                                    val['barcode']=product_variant_data['sku']
                                product.sudo().write(val)
                                if product_variant_data['stock_quantity'] > 0:
                                    date_time_format = DEFAULT_SERVER_DATETIME_FORMAT
                                    wl_adjust_id = adj_obj.sudo().create({
                                       'name':datetime.today().strftime(date_time_format),
                                       'location_ids':[(6,0,[8])], 
                                                  })
                                    wl_res = wl_adjust_id.sudo().write({'product_ids':[(6,0,product.ids)]})
                                    wl_adjust_id.sudo().action_start()

                                    available_product=adj_line_obj.sudo().search([('inventory_id','=',wl_adjust_id.id),('product_id','=',product.id)])
                                    quantity_count =0
                                    if available_product:
                                        if available_product.product_qty != int(product_variant_data['stock_quantity']):
                                            quantity_count=quantity_count+1
                                            available_product.sudo().write({'product_qty':int(product_variant_data['stock_quantity'])})
                                    else:
                                        quantity_count=quantity_count+1
                                        adj_line_obj.sudo().create({
                                                    'product_id':product.id,
                                                    'product_qty':int(product_variant_data['stock_quantity']),
                                                    'inventory_id':wl_adjust_id.id, 
                                                    'location_id':8,
                                                          })
                                    if quantity_count != 0:
                                        wl_adjust_id.sudo().custom_action_validate()
                                    else:
                                        wl_adjust_id.sudo().action_cancel_draft()
                                        wl_adjust_id.unlink()
                                if product_variant_data['price'] != None:
                                    # for product_attr_value in product.product_template_attribute_value_ids:
                                    product.sudo().write({'salla_variant_price':product_variant_data['price']['amount']})
                                    
                                product_variant_env_map.create({
                                    'product_id':product.id,
                                    'odoo_id':product.id,
                                    'ecom_id':product_variant_data['id'],
                                    })


                            
                











    def button_sync_categ(self):
        conn =  http.client.HTTPSConnection(self.url)


        headers = {
            'Content-Type': "application/json",
             
            'Authorization':'Bearer '+str(self.api_key)
            }

        conn.request("GET", "/admin/v2/categories", headers=headers)

        res = conn.getresponse()
        data = res.read()
        categ_env=self.env['product.public.category']
        categ_mapping = self.env['categorymap.categorymap']
        
        record=json.loads(data.decode('utf-8'))
        for rec in record['data']:
            salla_categ_id = categ_env.search([('salla_id','=',str(rec['id']))])
            if not salla_categ_id:

                vals={
                    'name':rec['name'],
                    'salla_id':rec['id']
                }
                categ_id=categ_env.create(vals)
                categ_mapping.create({
                    'category_id':categ_id.id,
                    'odoo_id':categ_id.id,
                    'ecom_id':rec['id']
                    })
            conn.request("GET", "/admin/v2/categories/"+str(rec['id'])+"/children", headers=headers)

            res = conn.getresponse()
            data = res.read()

            child_categ=json.loads(data.decode('utf-8'))
            for child in child_categ['data']:
                salla_categ_id = categ_env.search([('salla_id','=',str(child['id']))])
                if not salla_categ_id:
                    salla_first_child_categ_id = categ_env.search([('salla_id','=',str(child['parent_id']))])
                    vals={
                        'name':child['name'],
                        'salla_id':child['id'],
                        'parent_id':salla_first_child_categ_id.id
                    }
                    categ_id=categ_env.create(vals)
                    categ_mapping.create({
                        'category_id':categ_id.id,
                        'odoo_id':categ_id.id,
                        'ecom_id':child['id']
                        })
                conn.request("GET", "/admin/v2/categories/"+str(child['id'])+"/children", headers=headers)

                res = conn.getresponse()
                data = res.read()

                second_child_categ=json.loads(data.decode('utf-8'))
                for second_child in second_child_categ['data']:
                    salla_categ_id = categ_env.search([('salla_id','=',str(second_child['id']))])
                    if not salla_categ_id:
                        salla_second_child_categ_id = categ_env.search([('salla_id','=',str(child['parent_id']))])
                    
                        vals={
                            'name':second_child['name'],
                            'salla_id':second_child['id'],
                            'parent_id':salla_second_child_categ_id.id
                        }
                        categ_id=categ_env.create(vals)
                        categ_mapping.create({
                        'category_id':categ_id.id,
                        'odoo_id':categ_id.id,
                        'ecom_id':second_child['id']
                        })







           
        # print(record)

    
    def button_test_connection(self):
        try:
            conn = http.client.HTTPSConnection(self.url)

            headers = {
                'Content-Type': "application/json",
                'Authorization': self.api_key
                }

            conn.request("GET", "/mocks/salla/merchant/68673/products/tags", headers=headers)

            res = conn.getresponse()
            data = res.read()

            self.state='connect'
            return {'type': 'ir.actions.act_window',
                        'name': _('Connection Not Successful'),
                        'res_model': 'wizard.alert',
                        'target': 'new',
                        'view_id': self.env.ref('data_sync.wizard_form_view').id,
                        'view_mode': 'form',
                        'res_id': record_id.id,
                        'context': {'create': False,'edit':False},
                        'flags': {'mode': 'readonly'}  
                        }
            
        except Exception as err:
            record_id=self.env['wizard.alert'].create({'popup':'Test Connection Not Successfull. Please Try Again....'})
            return {'type': 'ir.actions.act_window',
                    'name': _('Connection Not Successful'),
                    'res_model': 'wizard.alert',
                    'target': 'new',
                    'view_id': self.env.ref('data_sync.wizard_form_view').id,
                    'view_mode': 'form',
                    'res_id': record_id.id,
                    'context': {'create': False,'edit':False},
                    'flags': {'mode': 'readonly'}  
                    }

        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.server_name))

    def sync_data(self):
        conn = http.client.HTTPSConnection(self.url)
        

    def button_set_customer_webhook(self):
        conn = http.client.HTTPSConnection(self.url)

        headers = {
            'Content-Type': "application/json",
            'Authorization': 'Bearer '+str(self.api_key)
            }

        conn.request("GET", "/mocks/salla/merchant/68673/products/tags", headers=headers)

        res = conn.getresponse()
        data = res.read()

        

        conn = http.client.HTTPSConnection("api.salla.dev")
        base_url = self.env['ir.config_parameter'].search([('key','=','web.base.url')])
        url=base_url.value+"/customer/update"+str(2)+'?access_token='+"009f9914-21a3-4dc4-b791-a8ee52ed53fc"
        str_url='"%s"' % (base_url.value+"/json-call/customer_update?user_id=2&token=009f9914-21a3-4dc4-b791-a8ee52ed53fc")

        payload = "{\n  \"name\": \"Salla Update Customer Event\",\n  \"event\": \"customer.updated\",\n  \"url\": "+str_url+",\n  \"version\": 2,\n  \"headers\": [\n    {\n      \"key\": \"Content-Type\",\n      \"value\": \"application/json\"\n    },\n    {\n      \"key\": \"Content-Length\",\n      \"value\": \"<calculated when request is sent>\"\n    }    ]\n}"
        headers = {
            'Content-Type': "application/json",
            'Authorization': 'Bearer '+str(self.api_key)
            }
        
        conn.request("POST", "/admin/v2/webhooks/subscribe", str(payload), headers)

        res = conn.getresponse()
        data = res.read()

        
