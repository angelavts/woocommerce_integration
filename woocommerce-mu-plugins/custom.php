<?php 
 /* 
 Plugin Name: Personalización de woocommerce
 Plugin URI: locahost/wordpress 
 Description: Plugin con las funciones personalizadas para la tienda en woocommerce
 Version: 1.0.0 
 Author: Angela 
 Author URI: 
 License: GPL 2+ 
 License URI: 
 */ 
//* Personalización de la página de tienda de WooCommerce
add_action( 'after_setup_theme', 'angela_custom_shop_woocommmerce' );

function angela_custom_shop_woocommmerce() {

    remove_action( 'woocommerce_before_checkout_form', 'woocommerce_checkout_coupon_form', 10 );
    //remove_action( 'woocommerce_checkout_order_review', 'woocommerce_checkout_payment', 20 );
    //remove_action( 'woocommerce_checkout_order_review', 'wc_payment_methods', 20 );
    // evitar que se pueda enviar a una dirección diferente
    add_filter( 'woocommerce_cart_needs_shipping_address', '__return_false');
    add_action( 'woocommerce_thankyou', 'send_order_details' );
    function send_order_details( $order_id ){
        // enviar petición a odoo para actualizar las ordenes

        // ruta de odoo
        $url = "http://localhost:8070/odoo_controller/odoo_controller/order_created";
        //$url = "https://5204a286-d9a6-4022-8ddc-4244ffb927b4.mock.pstmn.io/test";

        // obtener los datos de la orden que se acaba de realizar
        $order = wc_get_order( $order_id );
        // acomodar el arreglo de items con el item_id y la cantidad
        $items = [];
        foreach ($order->get_items() as $item_key => $item ){
            $item_data = [
                "product_id" => $item->get_product()->get_id(),
                "sku" => $item->get_product()->get_sku(),
                "quantity" => $item->get_quantity()
            ];
            // agregar item al arreglo
            $items[] = $item_data;
        }
        $billing = [
            "customer_id" => $order->get_customer_id(),
            "first_name" => $order->get_billing_first_name(),
            "last_name" => $order->get_billing_last_name(),
            "email" => $order->get_billing_email(),
            "phone" => $order->get_billing_phone(),
            "address_1" => $order->get_billing_address_1(),
            "address_2" => $order->get_billing_address_2(),
            "city" => $order->get_billing_city(),
            "country" => $order->get_billing_country(),
        ];

        // Los datos del cliente y el pedido realizado
        $datos = [
            "order_id" => $order->get_id(),
            "order_number" => $order->get_order_number(),
            "billing" => $billing,
            "line_items" => $items						
        ];
        $odoo_api_key = "API-KEY-ODOO";
        // Crear opciones de la petición HTTP
        $opciones = array(
            "http" => array(
                "header"=>array(
                    "Content-type: application/json",
                    "Authorization: " . $odoo_api_key
                ),
                "method" => "POST",
                "content" => json_encode($datos), # Agregar el contenido definido antes
                
                "ssl"=>array(
                    "verify_peer"=>false,
                    "verify_peer_name"=>false,
                )
            ),
        );

        # Preparar petición
        $contexto = stream_context_create($opciones);
        # Hacerla
        $resultado = file_get_contents($url, false, $contexto);

        //$resultado = http_get($url_get, [], $info);

        if ($resultado === false) {
            echo "Error haciendo petición";
        }

        # si no salimos allá arriba, todo va bien
        var_dump($resultado);
        // do something
        echo "ENVIAR ORDEN A ODOO!!";
        echo $order_id;
    }

}


