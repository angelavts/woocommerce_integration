# -*- coding: utf-8 -*-
import json
import requests
import base64
from odoo import http
from odoo import models
from woocommerce import API
from odoo.addons.woocommerce_integration.models.tools import wcapi


class OdooController(http.Controller):
    @http.route('/odoo_controller/odoo_controller/', auth='public')
    def index(self, **kw):
        return '<h1>Hola Mundo</h1>'


    @http.route('/odoo_controller/odoo_controller/example_products', auth='public')
    def example_product(self, **kw):
        # traer la lista de productos de woocommerce para probar
        response = wcapi.get('products').json()
        # quedarse con el último produco
        last_product = response[0]
        html_list = '<ul>\n'
        for key, value in last_product.items():
            html_list += '<li>' +  str(key) + ': ' + str(value) + '</li>\n'
        html_list += '</ul>'
        return html_list
    

    @http.route('/odoo_controller/odoo_controller/add_last_order', auth='public')
    def add_last_order(self, **kw):
        last_order = wcapi.get('orders').json()[0]
        # extraer los datos del cliente
        billing = last_order['billing']
        partner = {
            'name': billing['first_name'] + ' ' + billing['last_name'],
            'phone': billing['phone'],
            'email': billing['email']
        }
        bd_partner = http.request.env['res.partner']

        
        # revisar si el cliente existe en la base de datos (correo)
        print('Buscar cliente')
        current_partner = bd_partner.search([('email', '=', partner['email'])])
        if not current_partner:
            print('No encontró al cliente, crear')
            # no existe el cliente, crear
            print(bd_partner.create(partner))
            # buscar el cliente a partir del correo
            current_partner = bd_partner.search([('email', '=', partner['email'])])
            print('Cliente creado')
            

        sku_list = []
        # extraer datos de productos
        # construir lista de objetos
        print('Crear lista de productos')
        # si da tiempo, verificar que no se cree  otra orden similar
        for wc_product in last_order['line_items']:
            order_line = {
                'product_id': http.request.env['product.template'].search([('default_code', '=', wc_product['sku'])])[0].id,
                'product_uom_qty': wc_product['quantity']
            }
            # agregar una tupla con los datos de la orden_line
            sku_list.append((0, False, order_line))
        print('Lista creada')
        # crear objeto con la orden
        order_data = {
            'partner_id': current_partner.id,
            'order_line': sku_list,
            'wc_order_id': last_order['id'],
            'wc_number': last_order['number']
        }

        print('Crear orden')
        http.request.env['sale.order'].create(order_data)
        print('Orden creada')
        # eliminar orden woomerce
        
        return '<h2>Orden creada exitosamente</h2>'

    @http.route('/odoo_controller/odoo_controller/order_created', type='json', auth='my_api_key', methods=['POST'])
    def order_created(self, **kw):        
        response = http.request.jsonrequest
        error = False
        message = 'OK'
        # revisar si la orden existe
        wc_order_id = response['order_id']
        sale_order = http.request.env['sale.order'].search([('wc_order_id', '=', wc_order_id)])
        # si no existe, se crea
        if not sale_order:
            # extraer id del cliente
            billing = response['billing']        
            wc_customer_id = billing['customer_id']
            # buscar este cliente en la base de datos de odoo
            current_partner = http.request.env['res.partner'].search([('wc_customer_id', '=', wc_customer_id)])
            # 3. Evaluar si el cliente ya existe, sino, se crea uno nuevo
            if not current_partner:
                # extraer los datos del cliente
                partner_data = {
                    'wc_customer_id': int(wc_customer_id),
                    'name': billing['first_name'] + ' ' + billing['last_name'],
                    'phone': billing['phone'],
                    'email': billing['email'],
                    'street': billing['address_1'],
                    "street2": billing["address_2"],
                }
                # crear al cliente y guardar su referencia
                current_partner = current_partner.create(partner_data)
            
            # 4. Crear la lista de productos que se añadirán al diccionario de la orden de venta
            # 4.1 Extraer los ids de los productos en el modelo product.template en relacion con el sku en Woocommerce (default_code en Odoo)
            sku_list = []
            i = 0
            for wc_product in response['line_items']:
                # incluir producto si se encuentra en la bd
                product = http.request.env['product.product'].search([('wc_id', '=', wc_product['product_id'])])
                if product:
                    i += 1
                    order_line = {
                        'product_id': product.id,
                        'product_uom_qty': wc_product['quantity']
                    }                    
                    # agregar una tupla con los datos de la orden_line
                    sku_list.append((0, False, order_line))


            if sku_list:
                order_data = {
                    'name': response['order_key'],
                    'partner_id': current_partner.id,
                    'order_line': sku_list,
                    'wc_order_id': wc_order_id,
                    'wc_number': response['order_number']
                }
                # crear orden
                http.request.env['sale.order'].create(order_data)
            else:
                error = True
                message = 'No existen los productos'
        else:
            error = True
            message = 'Ya existe orden de venta'
        
        if not error:
            responseDict = {
                    'success': True,
                    'status': 'OK',
                    'code': 200
                }
        else:
            responseDict = {
                    'success': False,
                    'error': message
                }
        return json.dumps(responseDict)

    @http.route('/odoo_controller/odoo_controller/send_image', auth='public')
    def send_image(self, **kw):
        # prueba para enviar una imagen a wordpress
        product = http.request.env['product.template'].search([('default_code', '=', 'E-COM09')])
        image = product.image_1920
        url = 'https://argemtshop.com/wp-json/wp/v2/posts'
        user = 'argemt08'
        password = 'JPSs unNz FFRj yghP 9MJc l5PG'
        credentials = user + ':' + password
        token = base64.b64encode(credentials.encode())
        header = {'Authorization': 'Basic ' + token.decode('utf-8')}
        # response = requests.get(url , headers=header)
        # print(response)
        return 'Imagen enviada'


        


