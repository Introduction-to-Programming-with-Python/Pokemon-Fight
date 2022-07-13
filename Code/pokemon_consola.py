"""
Laboratorio N3: Pokemon.
Módulo de consola.

@author: da-naran
"""
import pokemon_funciones_solucion as poke
import random
from IPython.display import display, Image
from PIL import Image as PImage


def iniciar_aplicacion():
    """Inicia la ejecución de la aplicación por consola.
    Esta funcion primero carga los archivos y crea los diccionarios de pokemones.
    Luego la funcion le muestra el menu al usuario y espera a que seleccione una opcion.
    Esta operacion se repite hasta que el usuario seleccione la opcion de salir.
    """
    pokedex = poke.cargar_pokemones()
    poke.cargar_estadisticas(pokedex)
    poke.cargar_imagenes(pokedex)

    habilidades = poke.cargar_habilidades()
    habilidades_traducidas = poke.asignar_traducciones(habilidades)
    poke.asignar_habilidades(pokedex, habilidades_traducidas)

    ejecutando = True
    while ejecutando:
        print("\n\nBienvenido al Pokedex de IP!" + "\n" + ("-" * 50))
        print("Pokemon catalogados:", str(poke.dar_total_pokemones(pokedex)))
        print("-" * 50 + "\n")

        ejecutando = mostrar_menu_aplicacion(pokedex)


def ejecutar_navegar(pokedex: dict) -> None:
    ejecutando = True
    pagina_actual = 0
    pagina_max = poke.dar_total_pokemones(pokedex) // 10
    while ejecutando:
        print("-" * 50)
        print("\nNavegando el Pokedex" + "\n" + ("-" * 50))

        lista = dar_10_pokemones(pagina_actual * 10, pokedex)
        for i in range(0, len(lista)):
            pokemon = lista[i]
            print(str(i), " -", pokemon["identifier"].upper())
            # display(Image(filename=pokemon["imagen"]))

        print("-" * 50)
        print("Página", pagina_actual + 1, "de", pagina_max + 1)
        print("-" * 50)
        print("Menú de opciones")
        print(" 0-9 Consultar Pokemon")
        print(" X - Siguiente página")
        print(" Z - Página anterior")
        print(" M - Volver al Menú principal")
        print("-" * 50)

        opcion = input("Ingrese la opcion que desea ejecutar:").strip()

        if opcion in "0123456789" and len(opcion) == 1:
            pokemon = lista[int(opcion)]
            ejecutar_consultar_pokemon(pokemon, pokedex)
        elif opcion.upper() == "X":
            if pagina_actual == pagina_max:
                pagina_actual = 0
            else:
                pagina_actual += 1
        elif opcion.upper() == "Z":
            if pagina_actual == 0:
                pagina_actual = pagina_max
            else:
                pagina_actual -= 1
        elif opcion.upper() == "M":
            ejecutando = False
        else:
            print("La opcion " + opcion + " no es una opción válida.")


def dar_10_pokemones(comienzo: int, pokedex: dict) -> list:
    return list(pokedex.values())[comienzo : comienzo + 10]


def ejecutar_consultar_pokemon(pokemon, pokedex):
    continuar_ejecutando = True
    while continuar_ejecutando:
        print("\n" + "-" * 50)
        nombre = pokemon["identifier"].upper().ljust(25)
        id = "Lvl " + str(pokemon.get("nivel", 1)) + "  ID: " + pokemon["id"]
        print(nombre + id.rjust(25))
        print("-" * 50)

        img = PImage.open(pokemon["imagen"])
        ancho = img.size[0]
        display(Image(filename=pokemon["imagen"], width=ancho * 2))

        excluir = {
            "id",
            "base_experience",
            "identifier",
            "habilidades",
            "habilidades_restantes",
            "hp_pelea",
            "nivel",
            "imagen",
            "species_id",
            "order",
            "is_default",
        }
        atributos = list(set(pokemon.keys()) - excluir)

        for i in range(0, len(atributos), 2):
            fila = ""
            prop = atributos[i]
            fila = prop.ljust(18) + str(pokemon[prop]).rjust(4)

            if (i + 1) < len(atributos):
                prop_2 = atributos[i + 1]
                fila += "\t" + prop_2.ljust(18) + str(pokemon[prop_2]).rjust(4)

            print(fila)

        print("\n" + "-" * 50)
        print("Menú de opciones")
        print("-" * 50)
        print(" H - Habilidades especiales")
        print(" P - Pelea con pokemon aleatorio")
        print(" Z - Anterior")
        print(" X o Enter - Siguiente")
        print(" Cualquier otra tecla - Regresar")
        opcion_elegida = input("Ingrese la opción que desea ejecutar: ").strip()
        if opcion_elegida.upper() == "P":
            ejecutar_pelea(pokemon, pokedex)
        elif opcion_elegida.upper() == "H":
            if "habilidades" in pokemon.keys():
                print("\n" + "*" * 50)
                print("Habilidades:")
                print("*" * 50 + "\n")
                for h in pokemon["habilidades"]:
                    print(h["nombre"].upper())
                    if "traducciones" in h.keys():
                        print(", ".join(h["traducciones"]), "\n")
            input("Presione una tecla para continuar...")
            # ejecutar_consultar_pokemon(pokemon,pokedex)
        elif opcion_elegida.upper() == "Z":
            anterior = poke.dar_pokemon_anterior(pokedex, pokemon["id"])
            if anterior is None:
                anterior = pokemon
            ejecutar_consultar_pokemon(anterior, pokedex)
            continuar_ejecutando = False
        elif opcion_elegida.upper() == "X" or opcion_elegida == "":
            siguiente = poke.dar_pokemon_siguiente(pokedex, pokemon["id"])
            if siguiente is None:
                siguiente = pokemon
            ejecutar_consultar_pokemon(siguiente, pokedex)
            continuar_ejecutando = False
        else:
            continuar_ejecutando = False


def ejecutar_buscar(pokedex: dict) -> None:
    nombre = input("Escriba el nombre a buscar:")
    encontrados = poke.buscar_pokemon_por_nombre(pokedex, nombre)

    if encontrados is None:
        print("Función no implementada!")
        return

    ejecutando = True
    pagina_actual = 0
    pagina_max = len(encontrados) // 10
    while ejecutando:
        print("-" * 50)
        print("\nResultados de la búsqueda" + "\n" + ("-" * 50))
        print(len(encontrados), "pokemon encontrados")
        print("-" * 50)

        idx = pagina_actual * 10
        lista = encontrados[idx : idx + 10]
        for i in range(0, len(lista)):
            pokemon = lista[i]
            print(str(i), " -", pokemon["identifier"].upper())

        print("-" * 50)
        print("Página", pagina_actual + 1, "de", pagina_max + 1)
        print("-" * 50)
        print("Menú de opciones")
        print(" 0-9 Consultar Pokemon")
        print(" X - Siguiente página")
        print(" Z - Página anterior")
        print(" M - Volver al Menú principal")
        print("-" * 50)

        opcion = input("Ingrese la opcion que desea ejecutar:").strip()

        if opcion in "0123456789" and len(opcion) == 1:
            pokemon = lista[int(opcion)]
            ejecutar_consultar_pokemon(pokemon, pokedex)
        elif opcion.upper() == "X":
            if pagina_actual == pagina_max:
                pagina_actual = 0
            else:
                pagina_actual += 1
        elif opcion.upper() == "Z":
            if pagina_actual == 0:
                pagina_actual = pagina_max
            else:
                pagina_actual -= 1
        elif opcion.upper() == "M":
            ejecutando = False
        else:
            print("La opcion " + opcion + " no es una opción válida.")


def ejecutar_pelea(pokemon: dict, pokedex: dict) -> None:
    adversario = poke.dar_pokemon_aleatorio(pokedex)

    poke.preparar_para_pelea(pokemon)
    poke.preparar_para_pelea(adversario)

    versus = pokemon["identifier"].upper() + " vs " + adversario["identifier"].upper()
    info_pelea = {
        "mensajes": "PELEA!!!!;" + versus,
        "pokemon": pokemon,
        "adversario": adversario,
    }
    info_pelea = mostrar_info_pelea(info_pelea, True)
    mi_turno = False

    if "hp_pelea" not in pokemon:
        return

    while (
        pokemon["hp_pelea"] > 0
        and adversario["hp_pelea"] > 0
        and info_pelea.get("escapar", False) == False
    ):
        info_pelea = mostrar_info_pelea(info_pelea, mi_turno)
        mi_turno = not mi_turno

    mostrar_info_pelea(info_pelea, mi_turno)

    if pokemon["hp_pelea"] > 0 and info_pelea.get("escapar", False) == False:
        ganador = pokemon
        perdedor = adversario
    else:
        ganador = adversario
        perdedor = pokemon

    if info_pelea.get("escapar", False) == False:
        ganador["experiencia"] = ganador.get("experiencia", 0) + int(
            perdedor["base_experience"]
        )
        ganador["nivel"] = ganador["nivel"] + 1

    print("\n" + "*" * 50)
    txt_ganador = "GANADOR: " + ganador["identifier"].upper()
    print("*" + txt_ganador.center(48) + "*")
    print("*" * 50)
    if pokemon == ganador:
        print("Has subido de nivel!")
        print(
            pokemon["identifier"].upper(), "está ahora en Nivel", str(pokemon["nivel"])
        )

    input("Presione una tecla para continuar...")


def mostrar_info_pelea(info_pelea: dict, mi_turno: bool) -> dict:

    adversario = info_pelea["adversario"]
    pokemon = info_pelea["pokemon"]

    mostrar_pantalla_pelea(info_pelea)

    if (
        mi_turno
        and pokemon["hp_pelea"] > 0
        and adversario["hp_pelea"] > 0
        and info_pelea.get("escapar", False) == False
    ):
        continuar_ejecutando = True
        while continuar_ejecutando:
            opcion_elegida = input("Ingrese la opción que desea ejecutar: ").strip()
            if opcion_elegida.upper() == "A":
                info_pelea = poke.ejecutar_ataque(pokemon, adversario, None, mi_turno)
                continuar_ejecutando = False
            elif (
                opcion_elegida.upper() == "H"
                and len(pokemon["habilidades_restantes"]) > 0
            ):
                print("Habilidades:")
                no_escogida = True
                rest = pokemon["habilidades_restantes"]
                while no_escogida:
                    for i in range(0, len(rest)):
                        print(i, "-", rest[i])
                    habilidad_escogida = input("Escoja una habilidad:")
                    if (
                        habilidad_escogida in "0123456789"
                        and len(habilidad_escogida) == 1
                    ):
                        if int(habilidad_escogida) < len(rest):
                            no_escogida = False
                            continuar_ejecutando = False
                            info_pelea = poke.ejecutar_ataque(
                                pokemon,
                                adversario,
                                rest[int(habilidad_escogida)],
                                mi_turno,
                            )
                    else:
                        print(
                            "La opcion "
                            + habilidad_escogida
                            + " no es una opción válida."
                        )
            elif opcion_elegida.upper() == "E":
                mensajes = pokemon["identifier"].upper() + ";sale corriendo!"
                info_pelea = {
                    "mensajes": mensajes,
                    "pokemon": pokemon,
                    "adversario": adversario,
                    "escapar": True,
                }
                continuar_ejecutando = False
            else:
                print("La opcion " + opcion_elegida + " no es una opción válida.")
    elif mi_turno == False and adversario["hp_pelea"] > 0:
        usa_habilidad = random.random()
        if (
            usa_habilidad > 0.45
            and len(adversario.get("habilidades_restantes", [])) > 0
        ):
            habilidad = adversario["habilidades_restantes"][0]
        else:
            habilidad = None

        info_pelea = poke.ejecutar_ataque(pokemon, adversario, habilidad, mi_turno)
        input("Presione una tecla para continuar...")
    else:
        input("Presione una tecla para continuar...")
        info_pelea = poke.ejecutar_ataque(pokemon, adversario, None, mi_turno)
        mostrar_pantalla_pelea(info_pelea)
        input("Presione una tecla para continuar...")

    return info_pelea


def mostrar_pantalla_pelea(info_pelea: dict) -> None:
    adversario = info_pelea["adversario"]
    pokemon = info_pelea["pokemon"]

    print("\n" + "*" * 50 + "\n")

    nivel = "Lvl " + str(adversario.get("nivel", 0)) + "--"
    linea = "+" + (nivel.rjust(23, "-")) + "+"
    print(linea.rjust(50))
    linea = (
        adversario["identifier"].upper()[:20]
        + "   "
        + "*" * len(adversario.get("habilidades_restantes", []))
    )
    linea = "|" + linea.ljust(23) + "|"
    print(linea.rjust(50))
    linea = "HP: " + str(adversario.get("hp_pelea", 0))
    linea = "|" + linea.ljust(23) + "|"
    print(linea.rjust(50))
    linea = "+" + ("-" * 23) + "+"
    print(linea.rjust(50))

    im_2 = PImage.open(adversario["imagen"])
    im_1 = PImage.new("RGBA", (600 - im_2.width, im_2.height))

    img_adv = PImage.new("RGBA", (im_1.width + im_2.width, im_1.height))
    img_adv.paste(im_1, (0, 0))
    img_adv.paste(im_2, (im_1.width, 0))

    if adversario.get("hp_pelea", 0) <= 0:
        img_adv = img_adv.convert("LA")

    display(img_adv)

    mensajes = info_pelea["mensajes"].split(";")
    for m in mensajes:
        print(m.center(50))

    im_2 = PImage.open(pokemon["imagen"])
    im_1 = PImage.new("RGBA", (50, im_2.height))

    img_poke = PImage.new("RGBA", (im_1.width + im_2.width, im_1.height))
    img_poke.paste(im_1, (0, 0))
    img_poke.paste(im_2, (im_1.width, 0))

    if pokemon.get("hp_pelea", 0) <= 0:
        img_poke = img_poke.convert("LA")

    display(img_poke)

    nivel = "Lvl " + str(pokemon.get("nivel", 0)) + "--"
    linea = "+" + (nivel.rjust(23, "-")) + "+" + "\t Opciones:"
    print(linea.ljust(50))
    linea = (
        pokemon["identifier"].upper()[:20]
        + "   "
        + "*" * len(pokemon.get("habilidades_restantes", []))
    )
    linea = "|" + linea.ljust(23) + "|" + " A - Ataque"
    print(linea.ljust(50))
    linea = "HP: " + str(pokemon.get("hp_pelea", 0))
    linea = "|" + linea.ljust(23) + "|"
    if len(pokemon.get("habilidades_restantes", [])) > 0:
        linea += " H - Habilidad"
    print(linea.ljust(50))
    linea = "+" + ("-" * 23) + "+" + " E - Escapar"
    print(linea.ljust(50))

    print("\n" + "*" * 50)


def ejecutar_equipo_aleatorio(pokedex: dict) -> None:
    capturados = poke.capturar_10_pokemones(pokedex)
    print(poke.dar_tabla_equipo(capturados))
    input("Presione cualquier tecla para continuar ... ")


def ejecutar_equipo_balanceado(pokedex: dict) -> None:
    equipo = poke.hacer_equipo_balanceado(pokedex)
    print(poke.dar_tabla_equipo(equipo))
    input("Presione cualquier tecla para continuar ... ")


def mostrar_menu_aplicacion(pokedex: dict) -> bool:
    """Le muestra al usuario las opciones de ejecución disponibles.
    Parametros:
        p1 (dict): Diccionario de Pokemones.
    Retorno:
        Esta funcion retorna True si el usuario selecciono una opcion diferente
        a la opcion que le permite salir de la aplicacion.
        Esta funcion retorna False si el usuario selecciono la opción para salir
        de la aplicacion.
    """
    print("Menú de opciones")
    print(" 1 - Navegar Pokedex")
    print(" 2 - Buscar Pokemon")
    print(" 3 - Crear equipo aleatorio")
    print(" 4 - Crear equipo balanceado")
    print(" S - Salir de la aplicacion")

    opcion_elegida = input("Ingrese la opción que desea ejecutar: ").strip()

    continuar_ejecutando = True

    if opcion_elegida == "1":
        ejecutar_navegar(pokedex)
    elif opcion_elegida == "2":
        ejecutar_buscar(pokedex)
    elif opcion_elegida == "3":
        ejecutar_equipo_aleatorio(pokedex)
    elif opcion_elegida == "4":
        ejecutar_equipo_balanceado(pokedex)
    elif opcion_elegida.upper() == "S":
        continuar_ejecutando = False
    else:
        print("La opcion " + opcion_elegida + " no es una opción válida.")

    return continuar_ejecutando


iniciar_aplicacion()
