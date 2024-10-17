from typing import Any, Generator, Iterable
import os
from itertools import cycle
from functools import reduce
from collections import defaultdict, Counter
from utilidades import Pizzas
from utilidades import Pedidos
from utilidades import Locales
import creador_de_named_tuples


# Carga de datos

def cargar_pizzas(path: str) -> Generator:
    with open(path, 'r', encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            datos = linea.strip("\n").split(",")
            yield creador_de_named_tuples.crear_pizza(datos)


def cargar_locales(path: str) -> Generator:
    with open(path, 'r', encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            datos = linea.strip("\n").split(",")
            yield creador_de_named_tuples.crear_local(datos)


def cargar_pedidos(path: str) -> Generator:
    with open(path, 'r', encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            datos = linea.strip("\n").split(",")
            yield creador_de_named_tuples.crear_pedidos(datos)


def cargar_contenido_pedidos(path: str) -> Generator:
    with open(path, 'r', encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            datos = linea.strip("\n").split(",")
            yield creador_de_named_tuples.crear_contenidopedidos(datos)


# Consultas que ocupan 1 generador

def pedidos_con_al_menos_esta_pizza(
        generador_contenido_pedidos: Generator,
        tipo_de_pizza: str
        ) -> Iterable:
    return filter(lambda contenido: tipo_de_pizza in contenido.nombre, generador_contenido_pedidos)


def cantidad_vendida_de_pizza_por_tipo(
        generador_contenido_pedidos: Generator,
        tipo_de_pizza: str
        ) -> int:
    return reduce(
        lambda acumulador, contenido: acumulador + contenido.cantidad
            if contenido.nombre.split("_")[0] == tipo_de_pizza else acumulador,
        generador_contenido_pedidos, 0)

def pedido_con_mayor_descuento_utilizado(
        generador_contenido_pedidos: Generator
) ->Iterable:
    pedidos = list(generador_contenido_pedidos)
    max_descuento = max(map(lambda pedido: pedido.descuento,pedidos))
    return (pedido for pedido in pedidos if pedido.descuento == max_descuento)

def ajustar_precio_segun_ingredientes(
        generador_pizzas: Generator,
        ingrediente: str,
        diferencia_precio: int
        ) -> Iterable:
    return(
        Pizzas(nombre=pizza.nombre,
               ingredientes=pizza.ingredientes,
               precio=max(pizza.precio + diferencia_precio, 7000)
            )
            for pizza in generador_pizzas
            if ingrediente in pizza.ingredientes
        )

def clientes_despues_hora(
        generador_pedidos: Generator,
        hora: str
        ) -> str:
    ids_clientes = (
        pedido.id_cliente
        for pedido in generador_pedidos
        if pedido.hora >= hora
    )
    return "".join(map(str, ids_clientes))

def cliente_indeciso(
        generador_pizzas: Generator,
        ingrediente_no_deseado: str,
        cantidad_pizzas: int
        ) -> Iterable:
    pizzas_sin_ingredientes = (
        pizza for pizza in generador_pizzas if ingrediente_no_deseado not in pizza.ingredientes
        )
    pizzas_sin_ingredientes_lst = list(pizzas_sin_ingredientes)
    if not pizzas_sin_ingredientes_lst:
        return iter([])
    
    return (pizza for pizza, i in zip(cycle(pizzas_sin_ingredientes_lst), range(cantidad_pizzas)))

def pizzas_con_ingrediente(
        generador_pizzas: Generator,
        ingrediente: str
        ) -> Iterable:
    return (pizza for pizza in generador_pizzas if ingrediente in pizza.ingrediente)

def pizzas_pagables_de_un_tamano(
        generador_pizzas: Generator,
        dinero: int,
        tamano: str
    ) -> Iterable:
    return (
        pizza for pizza in generador_pizzas
        if pizza.precio <= dinero and pizza.nombre.lower() == tamano.lower()
    )

def cantidad_empleados_pais(
        generador_locales: Generator,
        pais: str
        ) -> int:
    return sum(
        local.cantidad_trabajadores for local in generador_locales
        if local.pais.lower() == pais.lower()
    )

# Consultas que ocupan 2 Generadores

def ganancias_producidas_en_los_pedidos(
        generador_contenido_pedidos: Generator,
        generador_pizzas: Generator
        ) -> Iterable:
    pizzas_dict = {pizza.nombre: pizza.precio for pizza in generador_pizzas}
    contenidos_validos = filter(lambda c: c.nombre in pizzas_dict, generador_contenido_pedidos)

    ganancias_por_pedido = defaultdict(int)
    for id_pedido,ganancia in map(lambda c: (
        c.id_pedido,
        round(c.cantidad * pizzas_dict[c.nombre] * (1 - c.descuento))
    ), contenidos_validos):
        ganancias_por_pedido[id_pedido] += ganancia
    return ((id_pedido,ganancia) for id_pedido, ganancia in ganancias_por_pedido.items())

def pizza_mas_vendida_del_dia(
        generador_contenido_pedidos: Generator,
        generador_pedidos: Generator,
        fecha: str
        ) -> set:
    pedidos_en_fechas = {pedido.id_pedido for pedido in generador_pedidos if pedido.fecha == fecha}
    pizzas_vendidas = filter(lambda x: x.id_pedido in pedidos_en_fechas, generador_contenido_pedidos)
    conteo_pizzas = Counter()
    for pedido in pizzas_vendidas:
        nombre_base = pedido.nombre.rsplit('_',1)[0]
        conteo_pizzas[nombre_base] += pedido.cantidad
    
    max_ventas = max(conteo_pizzas.values(),default=0)
    pizzas_mas_vendidas = {pizza for pizza, cantidad in conteo_pizzas.items() if cantidad == max_ventas}

    return pizzas_mas_vendidas

def pizza_del_mes(
        generador_pedidos: Generator,
        generador_contenido_pedidos: Generator,
        mes: str
        ) -> str:
    pedidos_del_mes = filter(lambda pedido: pedido.fecha.split('-')[1] == mes, generador_pedidos)
    ids_pedidos_del_mes = {pedido.id_pedido for pedido in pedidos_del_mes} #Usando una compresion de conjunto para obtener IDs unicos
    contador_pizzas = defaultdict(int)

    for contenido in generador_contenido_pedidos:
        if contenido.id_pedido in  ids_pedidos_del_mes:
            nombre_sin_tamano = "".join(contenido.nombre.split('')[0:-1])
            contador_pizzas[nombre_sin_tamano] += contenido.cantidad
        
        if not contador_pizzas:
            return iter([])
        
        max_ventas = max(contador_pizzas.values())
        pizza_mas_vendidas = filter(lambda pizza: contador_pizzas[pizza] == max_ventas, contador_pizzas)

        return pizza_mas_vendidas

def popularidad_mezcla_de_ingredientes(
        generador_pizzas: Generator,
        generador_contenido_pedidos: Generator,
        ingredientes: set
        ) -> int:
    pass


def total_ahorrado_pedidos(
        generador_contenido_pedidos: Generator,
        generador_pizzas: Generator
        ) -> str:
    pass

def pizza_favorita_cliente(
        generador_pedidos: Generator,
        generador_contenido_pedidos: Generator,
        id_cliente: int,
        ) -> tuple:
    pass


# Consultas que ocupan 3 o mas Generadores

def local_mas_pizzas_vendidas_por_tipo_de_pizza(
        generador_contenido_pedidos: Generator,
        generador_pedidos: Generator,
        generador_locales: Generator,
        tipo_de_pizza: str
        ) -> Iterable:
    pass

def ganancia_total_de_un_local(
        generador_contenido_pedidos: Generator,
        generador_pedidos: Generator,
        generador_pizzas: Generator,
        id_local: int
        ) -> int:
    pass


def promedio_ventas_con_descuento_de_un_pais(
        generador_contenido_pedidos: Generator,
        generador_pedidos: Generator,
        generador_locales: Generator,
        pais: str
        ) -> float:
    pass


def gasto_cliente_por_mes(
        generador_contenido_pedidos: Generator,
        generador_pedidos: Generator,
        generador_pizzas: Generator,
        id_cliente: int,
        year: int,
        ) -> list:
    pass

def pizzas_vendidas_mes_pais(
        generador_contenido_pedidos: Generator,
        generador_pedidos: Generator,
        generador_locales: Generator,
        pais: str,
        mes: int,
        year: int,
        ) -> int:
    pass


# Consulta anidada

def consulta_anidada(instrucciones: dict) -> Any:
    pass
