import random
import os

soles_iniciales = 1000
temperatura_inicial = random.randint(-10,35)
dia_actual = 1
ciclo = 0
tablero_jardin = [["X","X","X","X","X"],["X","X","X","X","X"],["X","X","X","X","X"]]

while ciclo == 0:
    print(f"""
            --------------------------------
                    Menu de inicio
            --------------------------------
        
            Soles disponibles:{soles_iniciales}
            Temeperatura:{temperatura_inicial} °C
            Dia actual:{dia_actual}

            [1] Menu Jardin
            [2] Laboratorio
            [3] Pasar Dia
            
            [0] Salir Del Programa
            
            Opcion:                        """)

    opcion = int(input())
    lista_opciones = [1,2,3]

    os.system("cls")

    if opcion in lista_opciones:
        if opcion == 1:
            print(f"""---------------------------------
                                Jardín
                    ---------------------------------
                        {tablero_jardin[0]}
                        {tablero_jardin[1]}
                        {tablero_jardin[2]}
                
                            [1] Intercambiar
                            [2] Cultivar
                            [3] Regar
                            [0] Volver al Menú de inicio
                
                    Indique su opción:""")
            
            opcion_menu_jardin = int(input())
            lista_opciones_menu_jardin = [0,1,2,3]

            if  opcion_menu_jardin in lista_opciones_menu_jardin:
                if opcion_menu_jardin == 1:

                    os.system("cls")

                    print(f"""
                        ------------
                        Intercambiar
                        ------------
                    {tablero_jardin[0]}
                    {tablero_jardin[1]}
                    {tablero_jardin[2]}

    Ingrese la coordenadas de el intercambio en formato x1,y1;x2,y2
                        
                        """)
                    
                    coordenadas_intercambio = str(input())
                    coordenadas_intercambio[]
                else:

                    os.system("cls")

                    print("""
                    -------------------------------------------------------------
                    Opcion no valida prsione cualquier tecla y intente nuevamente
                    -------------------------------------------------------------""")
                    
                    tecla_cualquiera = input()
                    os.system("cls")

                    print(f"""---------------------------------
                                    Jardín
                        ---------------------------------
                            {tablero_jardin[0]}
                            {tablero_jardin[1]}
                            {tablero_jardin[2]}
                    
                                [1] Intercambiar
                                [2] Cultivar
                                [3] Regar
                                [0] Volver al Menú de inicio
                    
                        Indique su opción:""")
                
    else:
        print("""
                -------------------------------------------------------------
                Opcion no valida prsione cualquier tecla y intente nuevamente
                -------------------------------------------------------------""")

