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
        print("PRINT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!...")
        return "fuciona 1"

    @http.route('/odoo_controller/odoo_controller/import_products_test/', auth='public')
    def import_products_test(self, **kw):    
        # m = request.env['product.product']
        # p = m.create({ 'name': filter_product["name"]})    
        # obtener los productos de woocommerce  
        all_products = http.request.env['product.product'].search([('default_code', '=', 'E-COM09')])
        wc_products = []
        data_product = {}
        # recorrer la lista de productos
        for product in all_products:
            print("-------------------------------------------------------")
            print(product.name)
            print(product.default_code)
            print(product.list_price)
            print(product.description)
            print(product.purchase_ok)
            print("-------------------------------------------------------")
            if product.default_code:
                data_product = {
                    "name": str(product.name),
                    "sku": str(product.default_code),
                    "regular_price": str(product.list_price),
                    "description": str(product.description),
                    "images": [
                        {
                            "src": "http://localhost/wordpress/wp-content/uploads/2022/02/Tarjeta_grafica_1.png"
                        }
                    ]
                }
                print(wcapi.post("products", data_product).json())        
        return "<h2>Los productos se han importado exitosamente</h2>"

    @http.route('/odoo_controller/odoo_controller/show_products/', auth='public')
    def show_products(self, **kw):    
        productList = http.request.env['product.product'].search([])
        for product in productList:
            print(product.name)
            print(product.description)

        return "Ready 2"

    @http.route('/odoo_controller/odoo_controller/example_products', auth='public')
    def example_product(self, **kw):
        response = wcapi.get("products").json()
        print(response)
        last_product = response[0]
        html_list = "<ul>\n"
        for key, value in last_product.items():
            html_list += "<li>" +  str(key) + ": " + str(value) + "</li>\n"
        html_list += "</ul>"
        return html_list
    

    @http.route('/odoo_controller/odoo_controller/add_order', auth='public')
    def add_order(self, **kw):
        last_order = wcapi.get("orders").json()[0]
        # extraer los datos del cliente
        # Recordar: rebajar stock
        billing = last_order["billing"]
        partner = {
            "name": billing["first_name"] + " " + billing["last_name"],
            "phone": billing["phone"],
            "email": billing["email"]
        }
        bd_partner = http.request.env['res.partner']

        
        # revisar si el cliente existe en la base de datos (correo)
        print("Buscar cliente")
        current_partner = bd_partner.search([('email', '=', partner['email'])])
        if not current_partner:
            print("No encontró al cliente, crear")
            # no existe el cliente, crear
            print(bd_partner.create(partner))
            # buscar el cliente a partir del correo
            current_partner = bd_partner.search([('email', '=', partner['email'])])
            print("Cliente creado")
            

        sku_list = []
        # extraer datos de productos
        # construir lista de objetos
        i = 0
        print("Crear lista de productos")
        # si da tiempo, verificar que no se cree  otra orden similar
        for wc_product in last_order["line_items"]:
            order_line = {
                "product_id": http.request.env['product.product'].search([('default_code', '=', wc_product["sku"])])[0].id,
                "product_uom_qty": wc_product["quantity"]
            }
            # agregar una tupla con los datos de la orden_line
            sku_list.append((i, False, order_line))
            i += 0
        print("Lista creada")
        # crear objeto con la orden
        order_data = {
            "partner_id": current_partner.id,
            "order_line": sku_list
        }
        print("Crear orden")
        http.request.env['sale.order'].create(order_data)
        print("Orden creada")
        # eliminar orden woomerce
        
        return "<h2>Orden creada exitosamente</h2>"

    @http.route('/odoo_controller/odoo_controller/order_created', type="json", auth='public', methods=['POST'])
    def order_created(self, **kw):
        print("AN ORDER HAS BEEN CREATED!") 
        response = http.request.jsonrequest
        print(response)
        print("READY") 
        appDict = {
            'success': True,
            'status': 'OK',
            'code': 200
        }

        return json.dumps(appDict)

    @http.route('/odoo_controller/odoo_controller/send_image', auth='public')
    def send_image(self, **kw):
        product = http.request.env['product.product'].search([('default_code', '=', 'E-COM09')])
        image = product.image_1920
        url = "https://argemtshop.com/wp-json/wp/v2/posts"
        user = "argemt08"
        password = "JPSs unNz FFRj yghP 9MJc l5PG"
        credentials = user + ':' + password
        token = base64.b64encode(credentials.encode())
        header = {'Authorization': 'Basic ' + token.decode('utf-8')}

        

        # response = requests.get(url , headers=header)
        # print(response)
        return "Imagen creada"

    @http.route('/odoo_controller/odoo_controller/import_product_test/', auth='public')
    def import_product_test(self, **kw):    
        data_product = {
            "name": "Producto prueba 1",
            "regular_price": "200",
            "description": "Pruebita",
            "images": [
                {
                    "src": "https://i.pinimg.com/564x/cc/1b/28/cc1b2803113900bea8a67f4e553bdf6e.jpg"
                }
            ]
        }
        print(wcapi.post("products", data_product).json())        
        return "<h2>Los productos se han importado exitosamente</h2>"


        


