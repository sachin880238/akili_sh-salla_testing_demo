# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import DataSet
import json
import logging
_logger = logging.getLogger(__name__)
import decimal
from datetime import date, datetime ,timedelta
import requests
from PIL import Image
from io import BytesIO
import urllib.request
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import logging




from math import radians, cos, sin, asin, sqrt

class OdooAPI(DataSet):
    @http.route(['/json-call/customer_update'], type='json', auth="public", csrf=False, cors='*')
    def customer_update(self, **post):
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('&token=')

        post=json.loads(request.httprequest.data)
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('?user_id=')
        before_keyword, keyword, after_keyword = str(after_keyword).partition('&token=')
        user_id = request.env['res.users'].sudo().browse(int(before_keyword))
        cust_env=request.env['res.partner']
        if user_id.access_token == after_keyword:
            
            salla_cust_id = cust_env.sudo().search([('salla_id','=',str(post['data']['id']))])
            if salla_cust_id:
            
                vals={
                'name':post['data']['first_name']+' '+post['data']['last_name'],
                'salla_id':post['data']['id'],
                'customer_rank': 1

                }
                if post['data']['mobile']:
                    vals['mobile']=post['data']['mobile']
                if post['data']['email']:
                    vals['email']=post['data']['email']
                if post['data']['email']:
                    vals['email']=post['data']['email']
                # if post['data']['avatar']:
                #     print("hhhhhhhhhhhhhhhhhhhh",post['data']['avatar'])
                #     response = requests.get(post['data']['avatar'])
                #     print("======================",response)
                #     img = Image.open(BytesIO(response.content))
                #     img.save('url_img.png')
                #     imgfile = Image.open('url_img.png')
                #     f = open('url_img.png' , 'rb') 
                #     img1 = base64.encodestring(f.read()) 
                #     f.close()
                #     os.remove('url_img.png')
                #     vals['image_1920'] = img1
                if post['data']['city']:
                    vals['city']=post['data']['city']
                salla_cust_id.sudo().write(vals)
                mapped_object=request.env['web.hooks'].sudo().search([('url.function_name','=',post['event']),('user_id','=',user_id.id)],limit=1)
                val={
                    'event_name':'Customer Response from Salla Update',
                    'request_type':'get',
                    'data':post['data'],
                    'status':'Success'
                }
                
                mapped_object.write({'logs':[(0,0,val)]})
                
        
        
        return json.dumps({'token': 'True', 'uid': True,'status':'Done'})
        return {'token': 'True', 'uid': True,'status':'Done'}


    @http.route(['/json-call/customer_create'], type='json', auth="public", csrf=False, cors='*')
    def customer_create(self, **post):
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('&token=')

        post=json.loads(request.httprequest.data)
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('?user_id=')
        before_keyword, keyword, after_keyword = str(after_keyword).partition('&token=')
        user_id = request.env['res.users'].sudo().browse(int(before_keyword))
        cust_mapping = request.env['customermap.customermap']
        cust_env=request.env['res.partner']
        if user_id.access_token == after_keyword:
            salla_cust_id = cust_env.search([('salla_id','=',str(post['data']['id']))])
            if not salla_cust_id:
            
                vals={
                'name':post['data']['first_name']+' '+post['data']['last_name'],
                'salla_id':post['data']['id'],
                'customer_rank': 1

                }
                if post['data']['mobile']:
                    vals['mobile']=post['data']['mobile']
                if post['data']['email']:
                    vals['email']=post['data']['email']
                if post['data']['email']:
                    vals['email']=post['data']['email']
                # if post['data']['avatar']:
                #     # response = requests.get(post['data']['avatar'])
                #     # img = Image.open(BytesIO(response.content))
                #     # img.save('url_img.png')
                #     # imgfile = Image.open('url_img.png')
                #     urllib.request.urlretrieve(post['data']['avatar'], "url_img.png")
                #     f = open('url_img.png' , 'rb') 
                #     img1 = base64.encodestring(f.read()) 
                #     f.close()
                #     os.remove('url_img.png')
                #     vals['image_1920'] = img1
                if post['data']['city']:
                    vals['city']=post['data']['city']
                customer_id = cust_env.sudo().create(vals)
                customer_map_val={
                    'partner_id':customer_id.id,
                    'odoo_id':customer_id.id,
                    'ecom_id':post['data']['id']
                    }
                customer_mapp_id=cust_mapping.sudo().create(customer_map_val)
                mapped_object=request.env['web.hooks'].sudo().search([('url.function_name','=',post['event']),('user_id','=',user_id.id)],limit=1)
                val={
                    'event_name':'Customer Response from Salla Update',
                    'request_type':'get',
                    'data':post['data'],
                    'status':'Success'
                }
                
                mapped_object.write({'logs':[(0,0,val)]})
            
            # salla_cust_id = cust_env.sudo().search([('salla_id','=',str(post['data']['id']))])
            # print("==================>>",salla_cust_id)
            # if salla_cust_id:
            
            #     vals={
            #     'name':post['data']['first_name']+' '+post['data']['last_name'],
            #     'salla_id':post['data']['id'],
            #     'customer_rank': 1

            #     }
            #     if post['data']['mobile']:
            #         vals['mobile']=post['data']['mobile']
            #     if post['data']['email']:
            #         vals['email']=post['data']['email']
            #     if post['data']['email']:
            #         vals['email']=post['data']['email']
            #     # if post['data']['avatar']:
            #     #     print("hhhhhhhhhhhhhhhhhhhh",post['data']['avatar'])
            #     #     response = requests.get(post['data']['avatar'])
            #     #     print("======================",response)
            #     #     img = Image.open(BytesIO(response.content))
            #     #     img.save('url_img.png')
            #     #     imgfile = Image.open('url_img.png')
            #     #     f = open('url_img.png' , 'rb') 
            #     #     img1 = base64.encodestring(f.read()) 
            #     #     f.close()
            #     #     os.remove('url_img.png')
            #     #     vals['image_1920'] = img1
            #     if post['data']['city']:
            #         vals['city']=post['data']['city']
            #     salla_cust_id.write(vals)
                
        
        
        return json.dumps({'token': 'True', 'uid': True,'status':'Done'})
        return {'token': 'True', 'uid': True,'status':'Done'}



    @http.route(['/json-call/categ_create'], type='json', auth="public", csrf=False, cors='*')
    def catgeg_create(self, **post):
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('&token=')

        post=json.loads(request.httprequest.data)
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('?user_id=')
        before_keyword, keyword, after_keyword = str(after_keyword).partition('&token=')
        user_id = request.env['res.users'].sudo().browse(int(before_keyword))
        categ_env=request.env['product.public.category']
        categ_mapping = request.env['categorymap.categorymap']
        if user_id.access_token == after_keyword:
            salla_categ_id = categ_env.search([('salla_id','=',str(post['data']['id']))])
            if not salla_categ_id:
                vals={
                    
                    'salla_id':post['data']['id']
                }
                if post['data']['name'] != None:
                    vals['name']=post['data']['name']
                else:
                    vals['name']='NullName'
                if post['data']['parent_id'] != 0:
                    parent_salla_categ_id = categ_env.search([('salla_id','=',str(post['data']['parent_id']))])
                    if parent_salla_categ_id:
                        vals['parent_id']=parent_salla_categ_id.id
                categ_id=categ_env.sudo().create(vals)
                categ_mapping.sudo().create({
                        'category_id':categ_id.id,
                        'odoo_id':categ_id.id,
                        'ecom_id':post['data']['id']
                        })
                mapped_object=request.env['web.hooks'].sudo().search([('url.function_name','=',post['event']),('user_id','=',user_id.id)],limit=1)
                val={
                    'event_name':'Customer Response from Salla Update',
                    'request_type':'get',
                    'data':post['data'],
                    'status':'Success'
                }
                
                mapped_object.write({'logs':[(0,0,val)]})
        
        
        return json.dumps({'token': 'True', 'uid': True,'status':'Done'})
        return {'token': 'True', 'uid': True,'status':'Done'}




    @http.route(['/json-call/categ_update'], type='json', auth="public", csrf=False, cors='*')
    def catgeg_update(self, **post):
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('&token=')

        post=json.loads(request.httprequest.data)
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('?user_id=')
        before_keyword, keyword, after_keyword = str(after_keyword).partition('&token=')
        user_id = request.env['res.users'].sudo().browse(int(before_keyword))
        categ_env=request.env['product.public.category']
        categ_mapping = request.env['categorymap.categorymap']
        if user_id.access_token == after_keyword:
            salla_categ_id = categ_env.search([('salla_id','=',str(post['data']['id']))])
            if salla_categ_id:
                vals={
                    
                    'salla_id':post['data']['id']
                }
                if post['data']['name'] != None:
                    vals['name']=post['data']['name']
                else:
                    vals['name']='NullName'
                if post['data']['parent_id'] != 0:
                    parent_salla_categ_id = categ_env.search([('salla_id','=',str(post['data']['parent_id']))])
                    if parent_salla_categ_id:
                        vals['parent_id']=parent_salla_categ_id.id
                categ_id=salla_categ_id.sudo().write(vals)
                # categ_mapping.sudo().create({
                #         'category_id':categ_id.id,
                #         'odoo_id':categ_id.id,
                #         'ecom_id':post['data']['id']
                #         })
                mapped_object=request.env['web.hooks'].sudo().search([('url.function_name','=',post['event']),('user_id','=',user_id.id)],limit=1)
                val={
                    'event_name':'Customer Response from Salla Update',
                    'request_type':'get',
                    'data':post['data'],
                    'status':'Success'
                }
                
                mapped_object.write({'logs':[(0,0,val)]})
        
        
        return json.dumps({'token': 'True', 'uid': True,'status':'Done'})
        return {'token': 'True', 'uid': True,'status':'Done'}




    @http.route(['/json-call/product_create'], type='json', auth="public", csrf=False, cors='*')
    def product_create(self, **post):
        import http
        api_key = request.env['ir.config_parameter'].sudo().search([('key','=','api_key')])
        headers = {
                'Content-Type': "application/json",
                'Authorization': 'Bearer '+str(api_key.value)
                }
        conn =  http.client.HTTPSConnection('api.salla.dev')
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('&token=')

        post=json.loads(request.httprequest.data)
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('?user_id=')
        before_keyword, keyword, after_keyword = str(after_keyword).partition('&token=')
        user_id = request.env['res.users'].sudo().browse(int(before_keyword))
        product_env=request.env['product.template']
        product_env_map=request.env['producttempmap.producttempmap']
        product_attr_env=request.env['attributemap.attributemap']
        product_attr_val_env_map=request.env['attributeval.attributeval']
        product_attr_val_env=request.env['product.attribute.value']
        product_variant_env=request.env['product.product']
        product_variant_env_map=request.env['productmap.productmap']
        website_categ_env=request.env['product.public.category']
        promotion_val_env=request.env['promotion.promotion']
        adj_obj = request.env['stock.inventory']
        adj_line_obj = request.env['stock.inventory.line']
        if user_id.access_token == after_keyword:
            product_id = product_env.sudo().search([('salla_id','=',post['data']['id'])])
            if not product_id:
                vals={
                    'salla_id':post['data']['id'],
                    'name':post['data']['name'],
                    'type':post['data']['type'],
                    'default_code':post['data']['sku'],
                    'barcode':post['data']['sku'],
                    'lst_price':post['data']['price']['amount'],
                    'standard_price':post['data']['price']['amount'],
                    'lst_price':post['data']['price']['amount'],
                    'weight':post['data']['weight'],
                    'description':post['data']['description'],
                    'type':'product',
                    'invoice_policy':'order'


                   
                    }
                if post['data']['promotion']:
                    if post['data']['promotion']['title'] != None:
                        promotion_val={
                        'name':post['data']['promotion']['title'],
                        'title':post['data']['promotion']['title'],
                        'sub_title':post['data']['promotion']['sub_title'],
                        }
                        promotion_id=promotion_val_env.sudo().create(promotion_val)
                        vals['promotion_id']=promotion_id.id
                option_list=[]
                for option in post['data']['options']:
                    attribute_id = request.env['product.attribute'].sudo().search([('salla_id','=',option['id'])])
                    if not attribute_id:
                        attribute_id = request.env['product.attribute'].sudo().create({
                            'salla_id':option['id'],
                            'name':option['name'],
                            'display_type':option['type'],
                            })
                        option_val={
                            'attribute_id':attribute_id.id

                        }
                        product_attr_env.sudo().create({
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
                        value_attribute_id = request.env['product.attribute.value'].sudo().search([('salla_id','=',value['id']),('attribute_id','=',attribute_id.id)])
                        if value_attribute_id:

                            value_list.append((4,value_attribute_id.id))
                        else:
                            value_dict={
                                'salla_id':value['id'],
                                'name':value['name'],
                                'attribute_id':attribute_id.id
                            }
                            value_attribute_id=product_attr_val_env.sudo().create(value_dict)
                            product_attr_val_env_map.sudo().create({
                                'attribute_value_id':value_attribute_id.id,
                                'odoo_id':value_attribute_id.id,
                                'ecom_id':value['id'],
                                })
                            value_list.append((4,value_attribute_id.id))

                    option_val['value_ids']=value_list
                    option_list.append((0,0,option_val))
                vals['attribute_line_ids']=option_list
                website_categ_ids=[]
                for categ in post['data']['categories']:
                    categ_id=website_categ_env.sudo().search([('salla_id','=',categ['id'])])
                    if categ_id:
                        website_categ_ids.append(categ_id.id)
                vals['public_categ_ids']=[(6,0,website_categ_ids)]
                img_data=[]
                for image in post['data']['images']:
                    if image['type'] == 'image':
                        image_val={
                            'file_link':image['url'],
                            'name':image['id'],

                        }
                        image_data=product_env.convert_url_image_data(image['url'])
                        # response = requests.get(image['url'])
                        # img = Image.open(BytesIO(response.content))
                        # img.save('url_img.png')
                        # imgfile = Image.open('url_img.png')
                        # f = open('url_img.png' , 'rb') 
                        # img1 = base64.encodestring(f.read()) 
                        # f.close()
                        # os.remove('url_img.png')
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
                

                tmpl_id = product_env.sudo().create(vals)
                if len(post['data']['options']) ==0:
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
                       available_product.sudo().write({'product_qty':int(post['data']['quantity'])})
                    else:
                        adj_line_obj.sudo().create({
                                    'product_id':product_id.id,
                                    'product_qty':int(post['data']['quantity']),
                                    'inventory_id':wl_adjust_id.id, 
                                    'location_id':8,
                                          })
                    wl_adjust_id.sudo().custom_action_validate()
                    
                map_id=product_env_map.sudo().create({
                    'product_template_id':tmpl_id.id,
                    'odoo_id':tmpl_id.id,
                    'ecom_id':post['data']['id']
                    })
                # conn.request("GET", "/admin/v2/products/"+str(post['data']['id'])+"/variants", headers=headers)

                # res = conn.getresponse()
                # data = res.read()
               
                # record=json.loads(data.decode('utf-8'))
                # print("-------------->>//////",record['data'])
                # product_ids = product_variant_env.search([('product_tmpl_id','=',tmpl_id.id)])
                # print("jjjjjjjjjjjjjjjjjjjjjj",product_ids)
                # for product_variant_data in post['data']['skus']:
                #     for product in product_ids:
                #         attr_value_ids=[]
                #         for product_attr_value in product.product_template_attribute_value_ids:
                #             print("====================",product_attr_value.product_attribute_value_id,product_attr_value.product_attribute_value_id.salla_id)
                #             attr_value_ids.append(int(product_attr_value.product_attribute_value_id.salla_id))
                #         attr_value_ids.sort()
                #         product_variant_data['related_options'].sort()
                #         print("444444444444444444444444444",attr_value_ids,product_variant_data['related_options'])
                #         if attr_value_ids == product_variant_data['related_options']:
                #             print("dddddddddddd>>>>")
                #             val={
                #             'salla_id':product_variant_data['id'],
                #             # 'lst_price':product_variant_data['sale_price']['amount'],
                #             # 'standard_price':product_variant_data['price']['amount'],
                #             }
                #             if product_variant_data['sale_price'] != None:
                #                 val['lst_price']=product_variant_data['sale_price']['amount']
                #             if product_variant_data['price'] != None:
                #                 val['standard_price']=product_variant_data['price']['amount']
                #             if product_variant_data['sku'] != None:
                #                 val['default_code']=product_variant_data['sku']
                #                 val['barcode']=product_variant_data['sku']
                #             product.sudo().write(val)
                #             product_variant_env_map.sudo().create({
                #                 'product_id':product.id,
                #                 'odoo_id':product.id,
                #                 'ecom_id':product_variant_data['id'],
                #                 })
                mapped_object=request.env['web.hooks'].sudo().search([('url.function_name','=',post['event']),('user_id','=',user_id.id)],limit=1)
                val={
                    'event_name':'Customer Response from Salla Update',
                    'request_type':'get',
                    'data':post['data'],
                    'status':'Success'
                }
                
                mapped_object.write({'logs':[(0,0,val)]})

    @http.route(['/json-call/order_create'], type='json', auth="public", csrf=False, cors='*')
    def order_create(self, **post):
        api_key = request.env['ir.config_parameter'].sudo().search([('key','=','api_key')])
        import http
        
        headers = {
                'Content-Type': "application/json",
                'Authorization': 'Bearer '+str(api_key.value)
                }
        conn =  http.client.HTTPSConnection('api.salla.dev')
        
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('&token=')

        post=json.loads(request.httprequest.data)
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('?user_id=')
        before_keyword, keyword, after_keyword = str(after_keyword).partition('&token=')
        user_id = request.env['res.users'].sudo().browse(int(before_keyword))
        order_env=request.env['sale.order'].sudo()
        cust_env=request.env['res.partner'].sudo()
        order_status_env=request.env['order.status'].sudo()
        product_env=request.env['product.template'].sudo()
        product_env_map=request.env['producttempmap.producttempmap'].sudo()
        product_attr_env=request.env['attributemap.attributemap'].sudo()
        product_attr_val_env_map=request.env['attributeval.attributeval'].sudo()
        product_attr_val_env=request.env['product.attribute.value'].sudo()
        product_variant_env=request.env['product.product'].sudo()
        currency_obj = request.env['res.currency'].sudo()
        product_variant_env_map=request.env['productmap.productmap'].sudo()
        website_categ_env=request.env['product.public.category'].sudo()
        promotion_val_env=request.env['promotion.promotion'].sudo()
        sale_order_env=request.env['sale.order'].sudo()
        sale_mapping= request.env['sale.order.map'].sudo()
        transection_obj = request.env['payment.transaction'].sudo()
        pricelist_obj = request.env['product.pricelist'].sudo()
        if user_id.access_token == after_keyword:
            order_id = order_env.search([('salla_id','=',post['data']['id'])])
            if not order_id:
                order_val={
                    'salla_id':post['data']['id'],
                    'reference':post['data']['reference_id'],

                }
                if post['data']['status']:
                    order_status_id = order_status_env.search([('salla_id','=',post['data']['status']['id'])])
                    if not order_status_id:
                        order_status_val={
                            'salla_id':post['data']['status']['id'],
                            'name':post['data']['status']['name']
                        }
                        order_status_id=order_status_env.create(order_status_val)
                        order_val['order_status_id']=order_status_id.id
                    else:
                        order_val['order_status_id']=order_status_id.id
                conn.request("GET", "/admin/v2/orders/"+str(post['data']['id'])+"?expanded=true", headers=headers)


                order_data = conn.getresponse()
                order_detail = order_data.read()
                record_order_details=json.loads(order_detail.decode('utf-8'))
                logging.info("Data from site =====>>>%s",str(record_order_details))
                logging.info("Data from site111 =====>>>%s",str(record_order_details['data']))
                logging.info("Data from site222 =====>>>%s",str(record_order_details['data']['payment_method']))
                logging.info("Data from site333 =====>>>%s",str(record_order_details['data']['amounts']['total']))
                logging.info("Data from site444 =====>>>%s",str(record_order_details['data']['shipping']))
                cust_id = request.env['res.partner'].sudo().search([('salla_id','=',record_order_details['data']['customer']['id'])])
                order_data=[]
                
                for item_data in record_order_details['data']['items']:
                    tax_id =request.env['account.tax'].sudo().search([('amount','=',float(item_data['amounts']['tax']['percent']))],limit=1)
                    logging.info("Data frttttttttttttaxxxxxom site444 =====>>>%s",str(tax_id))
                    logging.info("Data frttttttttttttaxxxxxom site444 =====>>>%s",str(item_data['amounts']['tax']['percent']))
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
                        order_data.append((0,0,order_line))
                    else:
                        if len(product_variant_ids.ids) == 1:
                            order_line['product_id']=product_variant_ids.id
                            order_line['name']=product_variant_ids.name
                            order_data.append((0,0,order_line))
                if len(order_data)>0:
                    logging.info("Data from site444 =====>>>%s",str(order_data))
                    logging.info("Data froddddddddddddddddddddddddm site444 =====>>>%s",str(post['data']['amounts']['shipping_cost']['amount']))
                    
                    if post['data']['amounts']['shipping_cost']['amount'] >=0:
                        logging.info("Data from site =====>>sssssssssshipping_id>%s",str(post['data']))
                
                        shipping_product_id=request.env['product.product'].sudo().search([('salla_id','=',post['data']['shipping']['id'])],limit=1)
                        logging.info("Data from site =====>>sssssssssshipping_id>%s",str(shipping_product_id))
                        # if int(post['data']['shipping']['id']) == 1026614558:
                        #     shipping_product_id =request.env.ref("ak_add_field.agent_shipment")
                        # elif int(post['data']['shipping']['id']) == 1723506348:
                        #     shipping_product_id =request.env.ref("ak_add_field.SmSa_shipment")
                        # elif int(post['data']['shipping']['id']) == 1492787992:
                        #     shipping_product_id =request.env.ref("ak_add_field.self_pickup")
                        # elif int(post['data']['shipping']['id']) == 1723506348:
                        #     shipping_product_id =request.env.ref("ak_add_field.dhl_shipment")
                        if shipping_product_id:
                            if post['data']['amounts']['tax']['percent'] != '0.00':
                                order_line={
                                    'product_uom_qty':1,
                                    
                                    # 'price_unit':item_data['product']['price']['amount'],
                                    'price_unit':post['data']['amounts']['shipping_cost']['amount'],
                                    'product_id':shipping_product_id.id,
                                    # 'tax_id':[(6,0,[])],
                                    # 'is_tax_fixed':True,
                                    # 'custom_tax_amount':item_data['amounts']['tax']['amount']['amount'],
                                    'name':shipping_product_id.name,
                                    # 'salla_id':item_data['id'],

                                    }
                                order_data.append((0,0,order_line))
                            else:
                                order_line={
                                    'product_uom_qty':1,
                                    
                                    # 'price_unit':item_data['product']['price']['amount'],
                                    'price_unit':post['data']['amounts']['shipping_cost']['amount'],
                                    'product_id':shipping_product_id.id,
                                    'tax_id':[(6,0,[])],
                                    # 'is_tax_fixed':True,
                                    # 'custom_tax_amount':item_data['amounts']['tax']['amount']['amount'],
                                    'name':shipping_product_id.name,
                                    # 'salla_id':item_data['id'],

                                    }
                                order_data.append((0,0,order_line))

                        # sale_id.set_delivery_line(carrier_id, post['data']['amounts']['shipping_cost']['amount'])
                        # sale_id.write({
                        #     'recompute_delivery_price': False,
                        #     'delivery_message': '',
                        # })
                    (dt, mSecs) = post['data']['date']['date'].strip().split(".") 
                    date_time_obj = datetime.strptime('2022-3-31 13:28:43', '%Y-%m-%d %H:%M:%S')
                    
                    currency_id = currency_obj.sudo().search([('name','=',record_order_details['data']['amounts']['total']['currency'])])
                    if cust_id:
                        order_val['date_order']=date_time_obj
                        order_val['partner_id']=cust_id.id
                        if currency_id:
                            pricelist_id = pricelist_obj.sudo().search([('currency_id','=',currency_id.id)],limit=1)
                            if pricelist_id:
                                order_val['pricelist_id']=pricelist_id.id
                            else:
                                order_val['currency_id']=currency_id.id
                        order_val['order_line']=order_data
                        sale_id=sale_order_env.create(order_val) 
                        if record_order_details['data']['amounts']['total']:
                            if record_order_details['data']['payment_method']:
                                payment_data = {
                                        'reference':record_order_details['data']['id'],
                                        'amount':record_order_details['data']['amounts']['total']['amount'],
                                        'partner_id':cust_id.id,
                                        'date':date.today(),
                                        'state':'done',
                                        'sale_id':sale_id.id
                                               }
                                if record_order_details['data']['payment_method'] == 'bank':
                                    payment_data['acquirer_id'] = 6
                                elif record_order_details['data']['payment_method'] == 'mada':
                                    payment_data['acquirer_id'] = 14
                                elif record_order_details['data']['payment_method'] == 'credit_card':
                                    payment_data['acquirer_id'] = 15
                                elif record_order_details['data']['payment_method'] == 'tamara_installment':
                                    payment_data['acquirer_id'] = 16
                                else:
                                    payment_data['acquirer_id'] = 6
                                if currency_id:
                                    payment_data['currency_id'] = currency_id.id
                                logging.info("Data to create payment Transection =====>>>%s",str(payment_data))
                                transection_obj.create(payment_data)
                                wizard_env=request.env['sale.advance.payment.inv']
                                sale_line_obj = request.env['sale.order.line']
                                invoice_lines = []
                                for line in sale_id.order_line:
                                    vals = {
                                        'name': line.name,
                                        'price_unit': line.price_unit,
                                        'quantity': line.product_uom_qty,
                                        'product_id': line.product_id.id,
                                        'product_uom_id': line.product_uom.id,
                                        'tax_ids': [(6, 0, line.tax_id.ids)],
                                        'sale_line_ids': [(6, 0, [line.id])],
                                    }
                                    invoice_lines.append((0, 0, vals))
                                invoice_id=request.env['account.move'].sudo().create({
                                    'ref': sale_id.client_order_ref,
                                    'move_type': 'out_invoice',
                                    'invoice_origin': sale_id.name,
                                    'invoice_user_id': sale_id.user_id.id,
                                    'partner_id': sale_id.partner_invoice_id.id,
                                    'currency_id': sale_id.pricelist_id.currency_id.id,
                                    'invoice_line_ids': invoice_lines
                                })
                                invoice_id.sudo().action_post()
                        sale_map_val={
                        'sale_id':sale_id.id,
                        'odoo_id':sale_id.id,
                        'ecom_id':post['data']['id']
                        }
                        sale_mapping.create(sale_map_val)
                        # if post['data']['amounts']['shipping_cost']['amount'] >0:
                        #     carrier_id=request.env['delivery.carrier'].sudo().search([('delivery_type','=','fixed')],limit=1)
                        #     sale_id.set_delivery_line(carrier_id, post['data']['amounts']['shipping_cost']['amount'])
                        #     sale_id.write({
                        #         'recompute_delivery_price': False,
                        #         'delivery_message': '',
                        #     })
                        
                        sale_id.action_confirm()
                        mapped_object=request.env['web.hooks'].sudo().search([('url.function_name','=',post['event']),('user_id','=',user_id.id)],limit=1)
                        val={
                            'event_name':'Customer Response from Salla Update',
                            'request_type':'get',
                            'data':post['data'],
                            'status':'Success'
                        }
                        
                        mapped_object.write({'logs':[(0,0,val)]})
            




    @http.route(['/json-call/product_update'], type='json', auth="public", csrf=False, cors='*')
    def product_update(self, **post):
        api_key = request.env['ir.config_parameter'].sudo().search([('key','=','api_key')])
        headers = {
                'Content-Type': "application/json",
                'Authorization': 'Bearer '+str(api_key.value)
                }
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('&token=')
        import http
        conn =  http.client.HTTPSConnection('api.salla.dev')
        
        post=json.loads(request.httprequest.data)
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('?user_id=')
        before_keyword, keyword, after_keyword = str(after_keyword).partition('&token=')
        user_id = request.env['res.users'].sudo().browse(int(before_keyword))
        product_env=request.env['product.template']
        product_env_map=request.env['producttempmap.producttempmap']
        product_attr_env=request.env['attributemap.attributemap']
        product_attr_val_env_map=request.env['attributeval.attributeval']
        product_attr_val_env=request.env['product.attribute.value']
        product_variant_env=request.env['product.product']
        product_variant_env_map=request.env['productmap.productmap']
        website_categ_env=request.env['product.public.category']
        promotion_val_env=request.env['promotion.promotion']
        adj_obj = request.env['stock.inventory']
        adj_line_obj = request.env['stock.inventory.line']
        if user_id.access_token == after_keyword:
            product_id = product_env.sudo().search([('salla_id','=',post['data']['id'])])
            if product_id:
                vals={
                    
                    'name':post['data']['name'],
                    'type':post['data']['type'],
                    'default_code':post['data']['sku'],
                    
                    'lst_price':post['data']['sale_price']['amount'],
                    'standard_price':post['data']['price']['amount'],
                    'lst_price':post['data']['price']['amount'],
                    'weight':post['data']['weight'],
                    'description':post['data']['description'],
                    'type':'product'


                   
                    }
                if post['data']['sku'] != '':
                    vals['barcode']=post['data']['sku']
                if post['data']['promotion']:
                    if post['data']['promotion']['title'] != None:
                        promotion_val={
                        'name':post['data']['promotion']['title'],
                        'title':post['data']['promotion']['title'],
                        'sub_title':post['data']['promotion']['sub_title'],
                        'salla_id':post['data']['id']
                        }
                        promotion_id=promotion_val_env.sudo().search([('salla_id','=',post['data']['id'])])
                        if promotion_id:
                            promotion_id.sudo().write(promotion_val)
                        else:

                            promotion_id=promotion_val_env.sudo().create(promotion_val)
                        vals['promotion_id']=promotion_id.id
                option_list=[]
                for option in post['data']['options']:
                    attribute_id = request.env['product.attribute'].sudo().search([('salla_id','=',option['id'])])
                    if not attribute_id:
                        attribute_id = request.env['product.attribute'].sudo().create({
                            'salla_id':option['id'],
                            'name':option['name'],
                            'display_type':option['type'],
                            })
                        option_val={
                            'attribute_id':attribute_id.id

                        }
                        product_attr_env.sudo().create({
                            'attribute_id':attribute_id.id,
                            'odoo_id':attribute_id.id,
                            'ecom_id':option['id']
                            })
                        value_list=[]
                        for value in option['values']:
                            value_attribute_id = request.env['product.attribute.value'].sudo().search([('salla_id','=',value['id']),('attribute_id','=',attribute_id.id)])
                            if value_attribute_id:

                                value_list.append((4,value_attribute_id.id))
                            else:
                                value_dict={
                                    'salla_id':value['id'],
                                    'name':value['name'],
                                    'attribute_id':attribute_id.id
                                }
                                value_attribute_id=product_attr_val_env.sudo().create(value_dict)
                                product_attr_val_env_map.sudo().create({
                                    'attribute_value_id':value_attribute_id.id,
                                    'odoo_id':value_attribute_id.id,
                                    'ecom_id':value['id'],
                                    })
                                value_list.append((4,value_attribute_id.id))
                        option_val['value_ids']=value_list
                        option_list.append((0,0,option_val))
                    else:
                        check_attr=0
                        for variant_lines in product_id.attribute_line_ids:
                            if variant_lines.attribute_id.id == attribute_id.id:
                                check_attr=check_attr+1
                                value_ids=[]
                                for value in option['values']:
                                    value_attribute_id = request.env['product.attribute.value'].sudo().search([('salla_id','=',value['id']),('attribute_id','=',attribute_id.id)])
                                    if value_attribute_id:
                                        for variant_value_line in variant_lines.value_ids:
                                            if value_attribute_id.id != variant_value_line.id:
                                                value_ids.append((4,value_attribute_id.id))
                                                break
                                    else:
                                        value_dict={
                                            'salla_id':value['id'],
                                            'name':value['name'],
                                            'attribute_id':attribute_id.id
                                        }
                                        value_attribute_id=product_attr_val_env.sudo().create(value_dict)
                                        value_ids.append((4,value_attribute_id.id))
                                variant_lines.write({'value_ids':value_ids})



                        if check_attr == 0:
                            

                            option_val={
                                'attribute_id':attribute_id.id
                                }
                            value_list=[]
                            for value in option['values']:
                                value_attribute_id = request.env['product.attribute.value'].sudo().search([('salla_id','=',value['id']),('attribute_id','=',attribute_id.id)])
                                if value_attribute_id:

                                    value_list.append((4,value_attribute_id.id))
                                else:
                                    value_dict={
                                        'salla_id':value['id'],
                                        'name':value['name'],
                                        'attribute_id':attribute_id.id
                                    }
                                    value_attribute_id=product_attr_val_env.sudo().create(value_dict)
                                    product_attr_val_env_map.sudo().create({
                                        'attribute_value_id':value_attribute_id.id,
                                        'odoo_id':value_attribute_id.id,
                                        'ecom_id':value['id'],
                                        })
                                    value_list.append((4,value_attribute_id.id))


                    
                    

                            option_val['value_ids']=value_list
                            option_list.append((0,0,option_val))
                vals['attribute_line_ids']=option_list
                website_categ_ids=[]
                for categ in post['data']['categories']:
                    categ_id=website_categ_env.sudo().search([('salla_id','=',categ['id'])])
                    if categ_id:
                        website_categ_ids.append(categ_id.id)
                vals['public_categ_ids']=[(6,0,website_categ_ids)]
                img_data=[]
                for image in post['data']['images']:
                    if image['type'] == 'image':
                        image_val={
                            'file_link':image['url'],
                            'name':image['id'],

                        }
                        image_data=product_id.convert_url_image_data(image['url'])
                        # response = requests.get(image['url'])
                        # img = Image.open(BytesIO(response.content))
                        # img.save('url_img.png')
                        # imgfile = Image.open('url_img.png')
                        # f = open('url_img.png' , 'rb') 
                        # img1 = base64.encodestring(f.read()) 
                        # f.close()
                        # os.remove('url_img.png')
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
                

                tmpl_id = product_id.sudo().write(vals)
                if len(post['data']['options']) ==0:
                    product_id = product_variant_env.sudo().search([('product_tmpl_id','=',product_id.id)])
                    date_time_format = DEFAULT_SERVER_DATETIME_FORMAT
                    wl_adjust_id = adj_obj.sudo().create({
                       'name':datetime.today().strftime(date_time_format),
                       'location_ids':[(6,0,[8])], 
                                  })
                    wl_res = wl_adjust_id.sudo().write({'product_ids':[(6,0,product_id.ids)]})
                    wl_adjust_id.sudo().action_start()

                    available_product=adj_line_obj.sudo().search([('inventory_id','=',wl_adjust_id.id),('product_id','=',product_id.id)])
                    if available_product:
                        if available_product.product_qty != int(post['data']['quantity']):
                            available_product.sudo().write({'product_qty':int(post['data']['quantity'])})
                    else:
                        adj_line_obj.sudo().create({
                                    'product_id':product_id.id,
                                    'product_qty':int(post['data']['quantity']),
                                    'inventory_id':wl_adjust_id.id, 
                                    'location_id':8,
                                          })
                    wl_adjust_id.sudo().custom_action_validate()
                    
                # map_id=product_env_map.sudo().create({
                #     'product_template_id':tmpl_id.id,
                #     'odoo_id':tmpl_id.id,
                #     'ecom_id':post['data']['id']
                #     })
                product_ids = product_variant_env.sudo().search([('product_tmpl_id','=',product_id.id)])
                for product_variant_data in post['data']['skus']:
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
                                extra_cost=(product_variant_data['price']['amount']-product_id.list_price)/(len(product.product_template_attribute_value_ids.ids)+1)
                                # for product_attr_value in product.product_template_attribute_value_ids:
                                product.sudo().write({'salla_variant_price':product_variant_data['price']['amount']})
                                #print("hhhhhhhhhhhhhhhhhh",extra_cost,product_attr_value.price_extra,product_attr_value.name,result)
                                # val['lst_price']=product_variant_data['price']['amount']
                            # product_variant_env_map.sudo().create({
                            #     'product_id':product.id,
                            #     'odoo_id':product.id,
                            #     'ecom_id':product_variant_data['id'],
                            #     })
                            break
                mapped_object=request.env['web.hooks'].sudo().search([('url.function_name','=',post['event']),('user_id','=',user_id.id)],limit=1)
                val={
                    'event_name':'Customer Response from Salla Update',
                    'request_type':'get',
                    'data':post['data'],
                    'status':'Success'
                }
                
                mapped_object.write({'logs':[(0,0,val)]})



    @http.route(['/json-call/payment_update'], type='json', auth="public", csrf=False, cors='*')
    def payment_update(self, **post):
        api_key = request.env['ir.config_parameter'].sudo().search([('key','=','api_key')])
        import http
        
        headers = {
                'Content-Type': "application/json",
                'Authorization': 'Bearer '+str(api_key.value)
                }
        conn =  http.client.HTTPSConnection('api.salla.dev')
        
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('&token=')

        post=json.loads(request.httprequest.data)
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('?user_id=')
        before_keyword, keyword, after_keyword = str(after_keyword).partition('&token=')
        user_id = request.env['res.users'].sudo().browse(int(before_keyword))
        order_env=request.env['sale.order'].sudo()
        cust_env=request.env['res.partner'].sudo()
        order_status_env=request.env['order.status'].sudo()
        product_env=request.env['product.template'].sudo()
        product_env_map=request.env['producttempmap.producttempmap'].sudo()
        product_attr_env=request.env['attributemap.attributemap'].sudo()
        product_attr_val_env_map=request.env['attributeval.attributeval'].sudo()
        product_attr_val_env=request.env['product.attribute.value'].sudo()
        product_variant_env=request.env['product.product'].sudo()

        product_variant_env_map=request.env['productmap.productmap'].sudo()
        website_categ_env=request.env['product.public.category'].sudo()
        promotion_val_env=request.env['promotion.promotion'].sudo()
        sale_order_env=request.env['sale.order'].sudo()
        sale_mapping= request.env['sale.order.map'].sudo()

        


    @http.route(['/json-call/order_deleted'], type='json', auth="public", csrf=False, cors='*')
    def order_delete(self, **post):
        api_key = request.env['ir.config_parameter'].sudo().search([('key','=','api_key')])
        import http
        
        headers = {
                'Content-Type': "application/json",
                'Authorization': 'Bearer '+str(api_key.value)
                }
        conn =  http.client.HTTPSConnection('api.salla.dev')
        
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('&token=')

        post=json.loads(request.httprequest.data)
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('?user_id=')
        before_keyword, keyword, after_keyword = str(after_keyword).partition('&token=')
        user_id = request.env['res.users'].sudo().browse(int(before_keyword))
        order_env=request.env['sale.order'].sudo()
        cust_env=request.env['res.partner'].sudo()
        order_status_env=request.env['order.status'].sudo()
        product_env=request.env['product.template'].sudo()
        product_env_map=request.env['producttempmap.producttempmap'].sudo()
        product_attr_env=request.env['attributemap.attributemap'].sudo()
        product_attr_val_env_map=request.env['attributeval.attributeval'].sudo()
        product_attr_val_env=request.env['product.attribute.value'].sudo()
        product_variant_env=request.env['product.product'].sudo()

        product_variant_env_map=request.env['productmap.productmap'].sudo()
        website_categ_env=request.env['product.public.category'].sudo()
        promotion_val_env=request.env['promotion.promotion'].sudo()
        sale_order_env=request.env['sale.order'].sudo()
        sale_mapping= request.env['sale.order.map'].sudo()

        


    @http.route(['/json-call/order_update'], type='json', auth="public", csrf=False, cors='*')
    def order_update(self, **post):
        api_key = request.env['ir.config_parameter'].sudo().search([('key','=','api_key')])
        import http
        
        headers = {
                'Content-Type': "application/json",
                'Authorization': 'Bearer '+str(api_key.value)
                }
        conn =  http.client.HTTPSConnection('api.salla.dev')
        
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('&token=')

        post=json.loads(request.httprequest.data)
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('?user_id=')
        before_keyword, keyword, after_keyword = str(after_keyword).partition('&token=')
        user_id = request.env['res.users'].sudo().browse(int(before_keyword))
        order_env=request.env['sale.order'].sudo()
        cust_env=request.env['res.partner'].sudo()
        order_status_env=request.env['order.status'].sudo()
        product_env=request.env['product.template'].sudo()
        product_env_map=request.env['producttempmap.producttempmap'].sudo()
        product_attr_env=request.env['attributemap.attributemap'].sudo()
        product_attr_val_env_map=request.env['attributeval.attributeval'].sudo()
        product_attr_val_env=request.env['product.attribute.value'].sudo()
        product_variant_env=request.env['product.product'].sudo()

        product_variant_env_map=request.env['productmap.productmap'].sudo()
        website_categ_env=request.env['product.public.category'].sudo()
        promotion_val_env=request.env['promotion.promotion'].sudo()
        sale_order_env=request.env['sale.order'].sudo()
        sale_mapping= request.env['sale.order.map'].sudo()
        sale_line_env= request.env['sale.order.line'].sudo()

        if user_id.access_token == after_keyword:
            order_id = order_env.search([('salla_id','=',post['data']['id'])])
            if order_id:
                order_val={
                    'salla_id':post['data']['id'],
                    'reference':post['data']['reference_id'],

                }
                if post['data']['status']:
                    order_status_id = order_status_env.search([('salla_id','=',post['data']['status']['id'])])
                    if not order_status_id:
                        order_status_val={
                            'salla_id':post['data']['status']['id'],
                            'name':post['data']['status']['name']
                        }
                        order_status_id=order_status_env.create(order_status_val)
                        order_val['order_status_id']=order_status_id.id
                    else:
                        order_val['order_status_id']=order_status_id.id
                conn.request("GET", "/admin/v2/orders/"+str(post['data']['id'])+"?expanded=true", headers=headers)

                order_data = conn.getresponse()
                order_detail = order_data.read()
                record_order_details=json.loads(order_detail.decode('utf-8'))
                line_ids = order_id.sudo().mapped('order_line')
                line_list=[]
                for line in line_ids:
                    line_list.append(line.salla_id)
                
                order_data=[]
                for item_data in record_order_details['data']['items']:
                    order_line={
                    'product_uom_qty':item_data['quantity'],
                    'weight':item_data['weight'],
                    # 'price_unit':item_data['product']['price']['amount'],
                    'name':item_data['name'],
                    'salla_id':item_data['id'],

                    }

                    product_tmpl_id = product_env.sudo().search([('salla_id','=',item_data['product']['id'])])
                    product_variant_ids = product_variant_env.sudo().search([('product_tmpl_id','=',product_tmpl_id.id)])
                    value_ids =[]
                    if len(item_data['options'])>0:
                        for option_data in item_data['options']:
                            value_id = product_attr_val_env.sudo().search([('salla_id','=',option_data['value']['id'])])
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
                                    sale_line_id = sale_line_env.search([('salla_id','=',item_data['id'])])
                                    if sale_line_id:
                                        if item_data['id'] in line_list:
                                            line_list.remove(item_data['id'])
                                        continue
                                    else:
                                        if item_data['id'] in line_list:
                                            line_list.remove(item_data['id'])
                                        order_data.append((0,0,order_line))
                    else:
                        if len(product_variant_ids.ids) == 1:
                            order_line['product_id']=product_variant_ids.id
                            order_line['name']=product_variant_ids.name
                            sale_line_id = sale_line_env.search([('salla_id','=',item_data['id'])])
                            if sale_line_id:
                                if item_data['id'] in line_list:
                                    line_list.remove(item_data['id'])
                                sale_line_id.sudo().write(order_line)
                            else:
                                if item_data['id'] in line_list:
                                    line_list.remove(item_data['id'])
                                order_data.append((0,0,order_line))
                for unlink_line in line_list:
                    sale_line_id = sale_line_env.search([('salla_id','=',unlink_line)])
                    sale_line_id.sudo().unlink()

                if len(order_data)<=0:
                    (dt, mSecs) = post['data']['date']['date'].strip().split(".") 
                    date_time_obj = datetime.strptime('2022-3-31 13:28:43', '%Y-%m-%d %H:%M:%S')

                    cust_id = request.env['res.partner'].sudo().search([('salla_id','=',record_order_details['data']['customer']['id'])])
                    if cust_id:
                        order_val['date_order']=date_time_obj
                        order_val['partner_id']=cust_id.id
                        order_val['order_line']=order_data
                        sale_id=order_id.sudo().write(order_val)
                        
                        mapped_object=request.env['web.hooks'].sudo().search([('url.function_name','=',post['event']),('user_id','=',user_id.id)],limit=1)
                        val={
                            'event_name':'Customer Response from Salla Update',
                            'request_type':'get',
                            'data':post['data'],
                            'status':'Success'
                        }
                        
                        mapped_object.sudo().write({'logs':[(0,0,val)]})
                else:
                    (dt, mSecs) = post['data']['date']['date'].strip().split(".") 
                    date_time_obj = datetime.strptime('2022-3-31 13:28:43', '%Y-%m-%d %H:%M:%S')

                    cust_id = request.env['res.partner'].sudo().search([('salla_id','=',record_order_details['data']['customer']['id'])])
                    if cust_id:
                        order_val['date_order']=date_time_obj
                        order_val['partner_id']=cust_id.id
                        order_val['order_line']=order_data
                        sale_id=order_id.sudo().write(order_val)
                        
                        mapped_object=request.env['web.hooks'].sudo().search([('url.function_name','=',post['event']),('user_id','=',user_id.id)],limit=1)
                        val={
                            'event_name':'Customer Response from Salla Update',
                            'request_type':'get',
                            'data':post['data'],
                            'status':'Success'
                        }
                        
                        mapped_object.sudo().write({'logs':[(0,0,val)]})
            




    @http.route(['/json-call/shipping_address_update'], type='json', auth="public", csrf=False, cors='*')
    def shipping_address_update(self, **post):
        api_key = request.env['ir.config_parameter'].sudo().search([('key','=','api_key')])
        import http
        
        headers = {
                'Content-Type': "application/json",
                'Authorization': 'Bearer '+str(api_key.value)
                }
        conn =  http.client.HTTPSConnection('api.salla.dev')
        
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('&token=')

        post=json.loads(request.httprequest.data)
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('?user_id=')
        before_keyword, keyword, after_keyword = str(after_keyword).partition('&token=')
        user_id = request.env['res.users'].sudo().browse(int(before_keyword))
        order_env=request.env['sale.order'].sudo()
        cust_env=request.env['res.partner'].sudo()
        order_status_env=request.env['order.status'].sudo()
        product_env=request.env['product.template'].sudo()
        product_env_map=request.env['producttempmap.producttempmap'].sudo()
        product_attr_env=request.env['attributemap.attributemap'].sudo()
        product_attr_val_env_map=request.env['attributeval.attributeval'].sudo()
        product_attr_val_env=request.env['product.attribute.value'].sudo()
        product_variant_env=request.env['product.product'].sudo()

        product_variant_env_map=request.env['productmap.productmap'].sudo()
        website_categ_env=request.env['product.public.category'].sudo()
        promotion_val_env=request.env['promotion.promotion'].sudo()
        sale_order_env=request.env['sale.order'].sudo()
        sale_mapping= request.env['sale.order.map'].sudo()

        


    @http.route(['/json-call/order_shipment_creating'], type='json', auth="public", csrf=False, cors='*')
    def order_shipment_creating(self, **post):
        api_key = request.env['ir.config_parameter'].sudo().search([('key','=','api_key')])
        import http
        
        headers = {
                'Content-Type': "application/json",
                'Authorization': 'Bearer '+str(api_key.value)
                }
        conn =  http.client.HTTPSConnection('api.salla.dev')
        
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('&token=')

        post=json.loads(request.httprequest.data)
        before_keyword, keyword, after_keyword = str(request.httprequest.url).partition('?user_id=')
        before_keyword, keyword, after_keyword = str(after_keyword).partition('&token=')
        user_id = request.env['res.users'].sudo().browse(int(before_keyword))
        order_env=request.env['sale.order'].sudo()
        cust_env=request.env['res.partner'].sudo()
        order_status_env=request.env['order.status'].sudo()
        product_env=request.env['product.template'].sudo()
        product_env_map=request.env['producttempmap.producttempmap'].sudo()
        product_attr_env=request.env['attributemap.attributemap'].sudo()
        product_attr_val_env_map=request.env['attributeval.attributeval'].sudo()
        product_attr_val_env=request.env['product.attribute.value'].sudo()
        product_variant_env=request.env['product.product'].sudo()

        product_variant_env_map=request.env['productmap.productmap'].sudo()
        website_categ_env=request.env['product.public.category'].sudo()
        promotion_val_env=request.env['promotion.promotion'].sudo()
        sale_order_env=request.env['sale.order'].sudo()
        sale_mapping= request.env['sale.order.map'].sudo()

        




    
    
    
    @http.route(['/json-call/user_logout'], type='json', auth="public", csrf=False, cors='*')
    def user_logout(self, **post):
        if not post:
            return {'error': 'Please send data to Odoo.'}
        if not post.get('token'):
            return {'error': 'Please send token.','status':'Failed'}

        check_token = request.env['jsonrpc.token'].sudo().search(
            [('token', '=', str(post.get('token')))])
        if check_token:
            check_token.sudo().unlink()

        return True

    @http.route(['/json-call'], type='json', auth="public", jsonrpctoken=True, csrf=False, cors='*')
    def jsonrpc_method(self, **post):
        post=json.loads(request.httprequest.data)
            
        model = ''
        method = ''
        if post.get('model') and post.get('method'):
            model = post.get('model')
            method = post.get('method')
        else:
            return {'error':'Model or Method is missing or wrong','status':'Failed'}
        res = self._call_kw(model, method, [post] or [[]], {})
        return res


