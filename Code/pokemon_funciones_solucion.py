"""
Laboratorio N3: Pokemon.
Módulo de funciones.

@author: da-naran
"""
import random,math

def cargar_pokemones() -> dict:
    """
    Carga el archivo pokemon.csv

    Returns
    -------
    dict
        diccionario que contiene los 964 pokemones. Cada llave es un
        string que es el nombre de cada pokemon, y cada valor
        es un diccionario que representa a cada pokemon.

    """
    dicc_pokemon = {}
    # cargar archivo de pokemones
    archivo_pokemones = open("./Data/data/pokemon.csv")

    # leer el encabezado y guardarlo en una variable llamada atributos
    primera_linea = archivo_pokemones.readline()
    atributos = primera_linea.replace("\n", "").split(",")

    # crear los pokemones y meterlos en la lista
    linea = archivo_pokemones.readline()
    while len(linea) > 0:
        datos = linea.replace("\n", "").split(",")
        pokemon = {"imagen":"./Data/imgs/pokemon/main-sprites/black-white/0.png"}
        for i, a in enumerate(atributos):
            pokemon[a] = datos[i]
        dicc_pokemon[pokemon["identifier"]] = pokemon
        linea = archivo_pokemones.readline()

    # cerrar el archivo
    archivo_pokemones.close()

    return dicc_pokemon

def cargar_imagenes(pokedex: dict) -> None:
    """
    Procesa el archivo pokemon_imagenes.csv, y asigna una ruta
    de imagen a cada pokemon.

    Parameters
    ----------
    pokedex : dict
        diccionario que contiene los 964 pokemones. Cada llave es un
        string que es el nombre de cada pokemon, y cada valor
        es un diccionario que representa a cada pokemon.

    Returns
    -------
    None

    """
    archivo_habilidades = open("./Data/data/pokemon_imagenes.csv")
    linea = archivo_habilidades.readline()
    linea = archivo_habilidades.readline()

    while len(linea) > 0:
        datos = linea.replace("\n", "").split(",")
        pokemon = buscar_pokemon_por_ID(pokedex,datos[0])
        pokemon["imagen"] = "./Data/imgs/"+datos[1]
        linea = archivo_habilidades.readline()
    return


def cargar_estadisticas(pokedex: dict) -> None:
    """
    Procesa el archivo pokemon_estadisticas y las asigna a
    cada pokemon.

    Parameters
    ----------
    pokedex : dict
        diccionario que contiene los 964 pokemones. Cada llave es un
        string que es el nombre de cada pokemon, y cada valor
        es un diccionario que representa a cada pokemon.

    Returns
    -------
    None

    """
    nombres_estadisticas = {
        "1": "hp",
        "2": "attack",
        "3": "defense",
        "4": "special-attack",
        "5": "special-defense",
        "6": "speed",
        "7": "accuracy",
        "8": "evasion",
    }

    archivo_estadisticas = open("./Data/data/pokemon_estadisticas.csv")
    linea = archivo_estadisticas.readline()
    linea = archivo_estadisticas.readline()

    while len(linea) > 0:
        datos = linea.replace("\n", "").split(",")
        id_pokemon = datos[0]
        id_estadistica = datos[1]
        valor_estadistica = int(datos[2])
        estadistica = nombres_estadisticas[id_estadistica]
        pokemon = buscar_pokemon_por_ID(pokedex, id_pokemon)
        pokemon[estadistica] = valor_estadistica
        linea = archivo_estadisticas.readline()

    archivo_estadisticas.close()


def cargar_habilidades() -> dict:
    """
    Procesa el archivo abilities.csv, guardando los datos en un 
    diccionario.

    Returns
    -------
    dict
        Diccionario cuya llave es un string, el nombre de la habilidad,
        y como valores tiene diccionarios que representan cada
        habilidad.
    """
    archivo_habilidades = open("./Data/data/abilities.csv")
    linea = archivo_habilidades.readline()
    linea = archivo_habilidades.readline()

    habilidades = {}

    while len(linea) > 0:
        datos = linea.replace("\n", "").split(",")
        habilidades[datos[0]] = {"nombre": datos[1]}
        linea = archivo_habilidades.readline()

    return habilidades


def asignar_traducciones(habilidades: dict) -> dict:
    """
    Procesa el archivo ability_names.csv, que contiene las traducciones
    de cada habilidad.
    
    Parameters
    ----------
    habilidades : dict
        DESCRIPTION.

    Returns
    -------
    dict
        DESCRIPTION.

    """
    archivo_traducciones = open("./Data/data/ability_names.csv")
    linea = archivo_traducciones.readline()
    linea = archivo_traducciones.readline()

    while len(linea) > 0:
        datos = linea.replace("\n", "").split(",")
        habilidad = habilidades[datos[0]]
        habilidad["traducciones"] = habilidad.get("traducciones", [])
        habilidad["traducciones"].append(datos[2])
        linea = archivo_traducciones.readline()
    return habilidades


def asignar_habilidades(pokedex: dict, habilidades: dict) -> None:
    """
    Asigna los diccionarios de habilidad a cada uno de los pokemon 
    que la usan.

    Parameters
    ----------
    pokedex : dict
        diccionario que contiene los 964 pokemones. Cada llave es un
        string que es el nombre de cada pokemon, y cada valor
        es un diccionario que representa a cada pokemon.
    habilidades : dict
        DESCRIPTION.

    """
    archivo_habilidades = open("./Data/data/pokemon_abilities.csv")
    linea = archivo_habilidades.readline()
    linea = archivo_habilidades.readline()
    while len(linea) > 0:
        datos = linea.replace("\n", "").split(",")
        pokemon = buscar_pokemon_por_ID(pokedex, datos[0])
        pokemon["habilidades"] = pokemon.get("habilidades", [])
        pokemon["habilidades"].append(habilidades[datos[1]])
        linea = archivo_habilidades.readline()

def dar_total_pokemones(pokedex: dict) -> int:
    """
    Retorna el número total de pokemones en el pokedex.

    Parameters
    ----------
    pokedex : dict
        diccionario que contiene los 964 pokemones. Cada llave es un
        string que es el nombre de cada pokemon, y cada valor
        es un diccionario que representa a cada pokemon.

    Returns
    -------
    int
        número total

    """
    return len(pokedex)


def buscar_pokemon_por_ID(pokedex: dict, id: str) -> dict:
    """
    Retorna el diccionario de un pokemon dado su ID.

    Parameters
    ----------
    pokedex : dict
        diccionario que contiene los 964 pokemones. Cada llave es un
        string que es el nombre de cada pokemon, y cada valor
        es un diccionario que representa a cada pokemon.
    id : str
        número identificador del pokemon a buscar

    Returns
    -------
    dict
        diccionario del pokemon, o None si no existe pokemon con
        el ID recibido como parámetro.

    """
    pokemon = None
    for p in pokedex.values():
        if p["id"] == id:
            pokemon = p
    return pokemon


def buscar_pokemon_por_nombre(pokedex: dict, nombre: str) -> list:
    """
    Retorna una lista con los diccionarios de pokemones que tienen en su nombre 
    (identifier) la cadena recibida como parámetro.

    Parameters
    ----------
    pokedex : dict
        diccionario que contiene los 964 pokemones. Cada llave es un
        string que es el nombre de cada pokemon, y cada valor
        es un diccionario que representa a cada pokemon.
    nombre : str
        cadena a buscar.

    Returns
    -------
    list
        lista de los pokemon que tienen en su nombre (identifier)
        la cadena recibida como parámetro

    """
    encontrados = []
    for k in pokedex.keys():
        if nombre.lower() in k:
            encontrados.append(pokedex[k])
    return encontrados

def dar_pokemon_siguiente(pokedex:dict,id:str)->dict:
    """
    Dado el id de un pokemon, retorna el siguiente pokemon que
    aparece en el pokedex. La función debe hacer un recorrido
    parcial por el pokedex. Si el id corresponde al último pokemon,
    la función retorna el primero del pokedex.

    Parameters
    ----------
    pokedex : dict
        diccionario que contiene los 964 pokemones. Cada llave es un
        string que es el nombre de cada pokemon, y cada valor
        es un diccionario que representa a cada pokemon.
    id : str
        cadena que contiene el número identificador (id) del pokemon.

    Returns
    -------
    dict
        diccionario del siguiente pokemon, o None si no existe
        pokemon con un ID igual al recibido como parámetro.

    """
    siguiente = None;
    i=0
    llaves = list(pokedex.keys())
    while i<len(llaves) and siguiente is None:
        if pokedex[llaves[i]]["id"] == id:
            idx = 0 if i==len(llaves)-1 else i+1
            siguiente = pokedex[llaves[idx]]
        i+=1
        
    return siguiente

def dar_pokemon_anterior(pokedex:dict,id:str)->dict:
    """
    Dado el id de un pokemon, retorna el pokemon que aparece
    inmediatamente antes. La función debe hacer un recorrido
    parcial por el pokedex. Si el id corresponde al primer pokemon,
    la función retorna el último del pokedex.

    Parameters
    ----------
    pokedex : dict
        diccionario que contiene los 964 pokemones. Cada llave es un
        string que es el nombre de cada pokemon, y cada valor
        es un diccionario que representa a cada pokemon.
    id : str
        cadena que contiene el número identificador (id) del pokemon.

    Returns
    -------
    dict
        diccionario del pokemon anterior, o None si no existe
        pokemon con un ID igual al recibido como parámetro.

    """
    anterior = None;
    i=0
    llaves = list(pokedex.keys())
    while i<len(llaves) and anterior is None:
        if pokedex[llaves[i]]["id"] == id:
            idx = i-1 if i>0 else len(llaves)-1
            anterior = pokedex[llaves[idx]]
        i+=1
        
    return anterior

def capturar_10_pokemones(pokedex: list):
    """
    Retorna una lista con 10 pokemones escogidos aleatoriamente.

    Parameters
    ----------
    pokedex : list
        diccionario que contiene los 964 pokemones. Cada llave es un
        string que es el nombre de cada pokemon, y cada valor
        es un diccionario que representa a cada pokemon.

    Returns
    -------
    capturados : list
        Lista que contiene los 10 diccionarios de pokemones

    """
    capturados = []
    lista = list(pokedex.values())
    for i in range(0, 10):
        indice_aleatorio = random.randint(0, len(lista))
        capturados.append(lista[indice_aleatorio])
    return capturados


def dar_maximo_pokemon(pokedex: dict, caracteristica: str) -> dict:
    """
    Retorna el pokemon que tiene el mayor valor para una característica.
    Si existe más de uno con el mismo valor mayor, retorna
    el último que se encuentre.

    Parameters
    ----------
    pokedex : dict
        diccionario que contiene los 964 pokemones. Cada llave es un
        string que es el nombre de cada pokemon, y cada valor
        es un diccionario que representa a cada pokemon.
    caracteristica : str
        característica numérica a buscar

    Returns
    -------
    dict
        diccionario del pokemon

    """
    lista_pokemon = list(pokedex.values())
    poke = lista_pokemon[0]
    for p in lista_pokemon:
        if int(p[caracteristica]) > int(poke[caracteristica]):
            poke = p
    return poke


def dar_minimo_pokemon(pokedex: dict, caracteristica: str) -> dict:
    """
    Retorna el pokemon que tiene el menor valor para una característica.
    Si existe más de uno con el mismo valor menor, retorna
    el último que se encuentre.

    Parameters
    ----------
    pokedex : dict
        diccionario que contiene los 964 pokemones. Cada llave es un
        string que es el nombre de cada pokemon, y cada valor
        es un diccionario que representa a cada pokemon.
    caracteristica : str
        característica numérica a buscar

    Returns
    -------
    dict
        diccionario del pokemon

    """
    lista_pokemon = list(pokedex.values())
    poke = lista_pokemon[0]
    for p in lista_pokemon:
        if int(poke[caracteristica]) > int(p[caracteristica]):
            poke = p
    return poke


def hacer_equipo_balanceado(pokedex: dict) -> list:
    """
    arma un equipo de 10 pokemones.

    Parameters
    ----------
    pokedex : dict
        diccionario que contiene los 964 pokemones. Cada llave es un
        string que es el nombre de cada pokemon, y cada valor
        es un diccionario que representa a cada pokemon.

    Returns
    -------
    list
        lista con los 10 pokemones. 

    """
    equipo = []

    equipo.append(dar_maximo_pokemon(pokedex, "attack"))
    equipo.append(dar_minimo_pokemon(pokedex, "attack"))
    equipo.append(dar_maximo_pokemon(pokedex, "defense"))
    equipo.append(dar_minimo_pokemon(pokedex, "defense"))
    equipo.append(dar_maximo_pokemon(pokedex, "hp"))
    equipo.append(dar_minimo_pokemon(pokedex, "hp"))
    equipo.append(dar_maximo_pokemon(pokedex, "speed"))
    equipo.append(dar_minimo_pokemon(pokedex, "speed"))
    equipo.append(dar_minimo_pokemon(pokedex, "weight"))
    equipo.append(dar_maximo_pokemon(pokedex, "weight"))
    return equipo


def dar_tabla_equipo(equipo: list) -> str:
    """
    Devuelve una cadena que resume ciertas estadísticas del
    equipo en una tabla ASCII: identifier, hp, attack, 
    defense, speed.
    
    Parameters
    ----------
    equipo : list
        Equipo a analizar

    Returns
    -------
    str
        tabla con las cinco columnas mencionadas, y datos de los 10
        pokemones como filas.

    """
    encabezado = (
        "nombre".center(15)
        + "HP".center(5)
        + "ataque".center(6)
        + "defensa".center(10)
        + "velocidad".center(11)
    )

    plantilla = "{}{}{}{}{}"

    tabla = encabezado + "\n"
    for p in equipo:
        tabla += (
            plantilla.format(
                p["identifier"][:15].center(15),
                str(p["hp"]).center(5),
                str(p["attack"]).center(6),
                str(p["defense"]).center(10),
                str(p["speed"]).center(11),
            )
            + "\n"
        )
    return tabla

def dar_pokemon_aleatorio(pokedex:dict)->dict:
    """
    Retorna un pokemon escogido aleatoriamente de los 946 en total.

    Parameters
    ----------
    pokedex : dict
        diccionario que contiene los 964 pokemones. Cada llave es un
        string que es el nombre de cada pokemon, y cada valor
        es un diccionario que representa a cada pokemon.

    Returns
    -------
    dict
        el diccionario de un pokemon escogido aleatoriamente

    """
    return list(pokedex.values())[random.randint(0,len(pokedex))]

def preparar_para_pelea(pokemon:dict)->None:
    """
    Asigna (o reinicia) las siguientes entradas del diccionario del
    pokemon que entra como parámetro:
        * hp_pelea: el mismo valor que está bajo la llave "hp"
            (el pokemon inicia la pelea con el 100% de vida)
        * habilidades_restantes: es una lista de los nombres de las
            habilidades del pokemon en español (índice 5 de las traducciones).
        * nivel: todos los pokemones suben de nivel con cada pelea que
            ganan. Si la entrada nivel no existe en el diccionario,
            se asigna el valor de 1.

    Parameters
    ----------
    pokemon : dict
        diccionario del pokemon.

    """
    pokemon["hp_pelea"] = pokemon["hp"]
    pokemon["habilidades_restantes"] = []
    for h in pokemon["habilidades"]:
        pokemon["habilidades_restantes"].append(h["traducciones"][5])
    pokemon["nivel"] = pokemon.get("nivel",1)

def ejecutar_ataque(
    pokemon: dict, adversario: dict, habilidad: str, mi_turno: bool
) -> dict:
    """
    Esta función aplica el daño de un pokemon atacante a un atacado,
    y retorna un diccionario con el formato especificado. Hay dos
    posibilidades de ataque, dependiendo del valor de mi_turno:
        
        * El pokemon del jugador ataca
        * El adversario ataca
    
    El daño se calcula con la fórmula del enunciado, y se debe aplicar
    siempre y cuando los dos pokemones tengan "hp_pelea" mayor a cero.
    Si alguno de los dos llegó a un hp_pelea menor que 1, se informa
    el siguiente mensaje: "<NOMBRE> se ha desmayado!;Has <resultado>.",
    donde se remplaza <NOMBRE> por el nombre del pokemon que ha sido
    vencido (en mayúsculas), y <resultado> por "ganado" o "perdido", 
    dependiendo de quién ganó.
    
    Cuando se realiza daño al pokemon atacado, se informa el siguiente
    mensaje: <ATACANTE> usa <MOVIDA>;DAÑO A <ATACADO>: <DAÑO>, donde
    <ATACANTE> y <ATACADO> corresponden a los nombres (en mayúsculas)
    de los respectivos pokemones, <MOVIDA> es "ATAQUE" si habilidad es
    None, de lo contrario es el nombre de la habilidad usada en mayúsculas.
    
    Parameters
    ----------
    pokemon : dict
        Pokemon del jugador.
    adversario : dict
        Adversario controlado por la computadora.
    habilidad : str
        Nombre (en español) de la habilidad que se va a usar, 
        o None si se hace un ataque normal.
    mi_turno : bool
        True si es turno del jugador, False si es turno de la
        computadora.

    Returns
    -------
    dict
        Diccionario con el pokemon del jugador, su adversario,
        y una cadena de mensajes del ataque, separados por ;.

    """
    info = {"pokemon": pokemon, "adversario": adversario, "mensajes":""}
    if pokemon["hp_pelea"] <= 0:
        info["mensajes"] = pokemon["identifier"].upper() + " se ha desmayado!;Has perdido."
    elif adversario["hp_pelea"] <= 0:
        info["mensajes"] = adversario["identifier"].upper() + " se ha desmayado!;Has ganado."
    else:
        if mi_turno == True:
            atacante = pokemon
            atacado = adversario
        else:
            atacante = adversario
            atacado = pokemon
        
        nivel = atacante["nivel"]
        ataque = atacante["attack"]
        defensa = atacado["defense"]
        restantes = atacante["habilidades_restantes"]
        
        if habilidad is None:
            poder = 70
            movimiento = "ATAQUE"
        elif len(restantes) > 0:
            poder = 120
            restantes.pop(restantes.index(habilidad))
            movimiento = habilidad.upper()
            
        modifier = random.uniform(0.85,1.0)
        damage = math.ceil((math.floor(math.floor(math.floor(2 * nivel / 5 + 2) * poder * ataque / defensa) / 50) + 2) * modifier)
        
        atacado["hp_pelea"] -= damage
        
        mensajes = atacante["identifier"].upper() + " usa " + movimiento + "!;"
        mensajes += "Daño a " + atacado["identifier"].upper() + ": " + str(damage)
        info["mensajes"] = mensajes
    
    return info
