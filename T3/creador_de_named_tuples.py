from utilidades import Pizzas, Locales, ContenidoPedidos, Pedidos

def crear_pizza(atributos_lst):
    nombre_p, ingredientes_str, precio_str = atributos_lst
    pizza = Pizzas(nombre=nombre_p, ingredientes=ingredientes_str, precio=int(precio_str))
    return pizza
    
def crear_local(atributos_lst):
    id_local_l, direccion_l, pais_l, ciudad_l, cantidad_l = atributos_lst
    local = Locales(id_local=int(id_local_l), direccion=direccion_l, ciudad=ciudad_l,
                    pais=pais_l, cantidad_trabajadores=int(cantidad_l))
    return local

def crear_contenidopedidos(atributos_lst):
    id_pedido_c, nombre_c, cantidad_c, descuento_c = atributos_lst
    contenido = ContenidoPedidos(id_pedido=int(id_pedido_c), nombre=nombre_c,
                                 cantidad=int(cantidad_c), descuento=float(descuento_c))
    return contenido

def crear_pedidos(atributos_lst):
    id_pedido_d, id_local_d, id_cliente_d, fecha_d, hora_d = atributos_lst
    pedido = Pedidos(id_pedido=int(id_pedido_d), id_local=int(id_local_d), 
                     id_cliente=int(id_cliente_d), fecha=fecha_d, hora=hora_d)
    return pedido