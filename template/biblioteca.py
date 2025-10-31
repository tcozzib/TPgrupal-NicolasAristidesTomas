from typing import Any
from enum import Enum


class Celda(Enum):
    VACÍO = 100
    BARCO = 200
    AGUA = 300
    def __str__(self):
        return " " if self == VACÍO else ("X" if self == BARCO else "~")
    def __repr__(self):
        return self.__str__()

VACÍO = Celda.VACÍO
BARCO = Celda.BARCO
AGUA = Celda.AGUA

class ResultadoDisparo(Enum):
    TOCADO = 10
    NADA = 20

TOCADO = ResultadoDisparo.TOCADO
NADA = ResultadoDisparo.NADA


class Jugador(Enum):
    UNO = "UNO"
    DOS = "DOS"

UNO = Jugador.UNO
DOS = Jugador.DOS

def jugadorQueEmpieza():
    return [Jugador.UNO]

class Dirección(Enum):
    ARRIBA = 8
    ABAJO = 12
    IZQUIERDA = 53
    DERECHA = -6

ARRIBA = Dirección.ARRIBA
ABAJO = Dirección.ABAJO
IZQUIERDA = Dirección.IZQUIERDA
DERECHA = Dirección.DERECHA

# Tipos (los que están comentados se definen en un módulo auxiliar)
# Celda = VACÍO | AGUA | BARCO  # contenido de una celda
Grilla = list[list[Celda]]      # una grilla, dada por una matriz de celdas
Tablero = tuple[Grilla,Grilla]       # un tablero, dado por la grilla local y la grilla del oponente
Dimensiones = tuple[int,int]         # cantidad de filas (alto) y cantidad de columnas (ancho) de las grillas
Posición = tuple[str,int]            # una ubicación de una grilla, dada por una letra y un número
# Jugador = UNO | DOS           # identificador de jugador
Barco = int                     # definición de barco (sólo su tamaño)
BarcoEnGrilla = list[Posición]      # un barco ubicado en la grilla (lista de posiciones que ocupa en la grilla)
# Dirección = ARRIBA | ABAJO | IZQUIERDA | DERECHA
EstadoJuego = tuple[
    Dimensiones,                # dimensiones de las grillas
    list[Barco],                # barcos disponibles
    list[Jugador],              # turno
    Tablero,                    # tablero jugador 1
    Tablero                     # tablero jugador 2
]

# Procedimientos y funciones auxiliares

def esLetraVálida(letra: str) -> bool:
    """ Indica si la letra *letra* es válida como indicador de fila.
        Para eso, debe ser una letra entre A y Z.
    """
    # Validación adicional en Python:
        # como no existe el tipo Char, hay que verificar que la longitud sea exactamente 1
    return len(letra) == 1 and ord('A') <= ord(letra) and ord(letra) <= ord('Z')

def númeroDeFila(letra: str) -> int:
    """ Describe el número de fila correspondiente a la letra *letra*.
        PRE: esLetraVálida(letra)
    """
    return ord(letra) - ord('A') + 1

def siguienteLetra(letra: str) -> str:
    """ Describe la letra siguiente a *letra*.
        PRE: esLetraVálida(letra)
        PRE: ord(letra) < ord('Z')
    """
    return chr(ord(letra) + 1)

def anteriorLetra(letra: str) -> str:
    """ Describe la letra anterior a *letra*.
        PRE: esLetraVálida(letra)
        PRE: ord(letra) > ord('A')
    """
    return chr(ord(letra) - 1)

def direccionesOrtogonales() -> list[Dirección]:
    """ Describe una lista con las cuatro direcciones ortogonales. """
    return [ARRIBA, ABAJO, IZQUIERDA, DERECHA]

def cantidadDeApariciones(elementoBuscado: Any, lista: list[Any]) -> int:
    """ Describe la cantidad de apariciones del elemento *elementoBuscado* en la lista *lista*. """
    cantidadPorAhora = 0
    for elementoDeLista in lista:
        cantidadPorAhora += unoSiCeroSiNo(elementoDeLista == elementoBuscado)
    return cantidadPorAhora

def unoSiCeroSiNo(condición: bool) -> int:
    """ Describe uno si se cumple la condición *condición* y cero si no. """
    return 1 if condición else 0

def esMatrizVálida(matriz: list[list[Any]]) -> bool:
    """ Indica si la matriz *matriz* es una matriz válida.
        Para ser una matriz válida, todas las filas deben tener la misma longitud.
    """
    if len(matriz) == 0:
        return True
    largoFila = len(matriz[0])
    filaActual = 1
    while filaActual < len(matriz) and len(matriz[filaActual]) == largoFila:
        filaActual += 1
    return filaActual == len(matriz)

## Dimensiones

def anchoDimensiones(dimensiones: Dimensiones) -> int:
    """ Describe el ancho (la cantidad de columnas) de las dimensiones *dimensiones*. """
    return dimensiones[1]

def altoDimensiones(dimensiones: Dimensiones) -> int:
    """ Describe el alto (la cantidad de filas) de las dimensiones *dimensiones*. """
    return dimensiones[0]

def mismasDimensiones(dimensiones1: Dimensiones, dimensiones2: Dimensiones) -> bool:
    """ Indica si las dimensiones *dimensiones1* coinciden con las dimensiones *dimensiones2*. """
    return anchoDimensiones(dimensiones1) == anchoDimensiones(dimensiones2) and \
        altoDimensiones(dimensiones1) == altoDimensiones(dimensiones2)

## Grilla

def esGrillaVálida(grilla: Grilla) -> bool:
    """ Indica si la grilla *grilla* es una grilla válida.
        Para ser una grilla válida, debe ser una matriz válida, tener entre una y 26 filas y tener al menos una columna.
    """
    return esMatrizVálida(grilla) and \
        len(grilla) > 0 and len(grilla) <= 26 and \
        len(grilla[0]) > 0

def dimensionesGrilla(grilla: Grilla) -> Dimensiones:
    """ Describe las dimensiones (cantidad de filas y cantidad de columnas) de la grilla *grilla*.
        PRE: esGrillaVálida(grilla)
    """
    return (len(grilla), len(grilla[0]))

def cantidadDeFilasGrilla(grilla: Grilla) -> int:
    """ Describe la cantidad de filas de la grilla *grilla*.
        PRE: esGrillaVálida(grilla)
    """
    return altoDimensiones(dimensionesGrilla(grilla))

def cantidadDeColumnasGrilla(grilla: Grilla) -> int:
    """ Describe la cantidad de columnas de la grilla *grilla*.
        PRE: esGrillaVálida(grilla)
    """
    return anchoDimensiones(dimensionesGrilla(grilla))

def grillaVálidaEnJuego(grilla: Grilla, estadoDeJuego: EstadoJuego) -> bool:
    """ Indica la grilla *grilla* es válida para el juego *estadoDeJuego*.
        Para eso, debe ser una grilla válida y dimensiones coincidir con las del juego.
    """
    return esGrillaVálida(grilla) and \
        mismasDimensiones(dimensionesGrilla(grilla), dimensionesEstadoJuego(estadoDeJuego))

# Tablero

def grillaLocal(tablero: Tablero) -> Grilla:
    """ Describe la grilla local del tablero *tablero*. """
    return tablero[0]

def grillaOponente(tablero: Tablero) -> Grilla:
    """ Describe la grilla del oponente del tablero *tablero*. """
    return tablero[1]

## EstadoJuego

def dimensionesEstadoJuego(estadoDeJuego: EstadoJuego) -> Dimensiones:
    """ Describe las dimensiones (cantidad de filas y cantidad de columnas) de las grillas
            en el estado de juego *estadoDeJuego*.
    """
    return estadoDeJuego[0]

def cantidadDeFilasEstadoJuego(estadoDeJuego: EstadoJuego) -> int:
    """ Describe la cantidad de filas del estado de juego *estadoDeJuego*. """
    return altoDimensiones(dimensionesEstadoJuego(estadoDeJuego))

def cantidadDeColumnasEstadoJuego(estadoDeJuego: EstadoJuego) -> int:
    """ Describe la cantidad de columnas del estado de juego *estadoDeJuego*. """
    return anchoDimensiones(dimensionesEstadoJuego(estadoDeJuego))

def barcosDisponibles(estadoDeJuego: EstadoJuego) -> list[Barco]:
    """ Describe la lista de barcos disponibles en el juego *estadoDeJuego*. """
    return estadoDeJuego[1]

def turno(estadoDeJuego: EstadoJuego) -> Jugador:
    """ Describe el jugador al que le toca en el juego *estadoDeJuego*. """
    return estadoDeJuego[2][0]

def tableroDeJugador(estadoDeJuego: EstadoJuego, jugador: Jugador) -> Tablero:
    """ Describe el tablero del jugador *jugador* en el juego *estadoDeJuego*. """
    return estadoDeJuego[3] if jugador == UNO else estadoDeJuego[4]

def cambiarTurno(estadoDeJuego: EstadoJuego):
    """ Alterna el turno actual en el juego *estadoDeJuego*. """
    jugador_actual = estadoDeJuego[2][0]
    estadoDeJuego[2][0] = DOS if jugador_actual == UNO else UNO


# Posición

def esPosiciónVálida(posición: Posición) -> bool:
    """ Indica si la posición *posición* es una posición válida.
        Para ser una posición válida, la letra debe ser una letra entre A y Z y el número debe ser mayor a 0.
    """
    return esLetraVálida(letraDePosición(posición)) and númeroDePosición(posición) > 0

def letraDePosición(posición: Posición) -> str:
    """ Describe la letra de la posición *posición*. """
    return posición[0]

def númeroDePosición(posición: Posición) -> int:
    """ Describe el número de la posición *posición*. """
    return posición[1]

def mismaPosición(posición1: Posición, posición2: Posición) -> bool:
    """ Indica si las posiciones *posición1* y *posición2* son la misma posición. """
    return letraDePosición(posición1) == letraDePosición(posición2) and \
        númeroDePosición(posición1) == númeroDePosición(posición2)

def hayPosiciónAdyacenteEn(posición: Posición, posiciones: list[Posición]) -> bool:
    """ Indica si en la lista *posiciones* hay alguna posición adyacente a la
            posición *posición*. """
    posiciónActualEnLista = 0
    while posiciónActualEnLista < len(posiciones) and \
        not sonPosicionesAdyecentes(posición, posiciones[posiciónActualEnLista]):
            posiciónActualEnLista += 1
    return posiciónActualEnLista < len(posiciones)

def sonPosicionesAdyecentes(posición1: Posición, posición2: Posición) -> bool:
    """ Indica si las posiciones *posición1* y *posición2* son adyacentes.
        Una forma de validarlo es usando la función esBarcoVálido que determina
            justamente si una lista de posiciones consiste en posiciones contíguas.
    """
    return esBarcoVálido([posición1,posición2])

# Posición en grilla

def esPosiciónVálidaEnGrilla(posición: Posición, grilla: Grilla) -> bool:
    """ Indica si la posición *posición* es válida en la grilla *grilla*.
        Para ser una posición válida en una grilla, debe ser una posición válida y
            caer dentro de las dimensiones de la grilla.
        PRE: esGrillaVálida(grilla)
    """
    return esPosiciónVálida(posición) and \
        númeroDeFila(letraDePosición(posición)) <= cantidadDeFilasGrilla(grilla) and \
        númeroDePosición(posición) <= cantidadDeColumnasGrilla(grilla)

def sonPosicionesVálidasEnGrilla(posiciones: list[Posición], grilla: Grilla) -> bool:
    """ Indica si todas las posiciones en *posiciones* son válidas en la grilla *grilla*.
        PRE: esGrillaVálida(grilla)
    """
    posiciónActual = 0
    while posiciónActual < len(posiciones) and \
        esPosiciónVálidaEnGrilla(posiciones[posiciónActual], grilla):
            posiciónActual += 1
    return posiciónActual == len(posiciones)

def celdaEnPosición(grilla: Grilla, posición: Posición) -> Celda:
    """ Describe la celda que se encuentra en la posición *posición* de la grilla *grilla*.
        PRE: esGrillaVálida(grilla)
        PRE: esPosiciónVálidaEnGrilla(posición, grilla)
    """
    return grilla[númeroDeFila(letraDePosición(posición))-1][númeroDePosición(posición)-1]

def primeraPosiciónEnGrilla(grilla: Grilla) -> Posición:
    """ Describe la primera posición de la grilla *grilla*.
        PRE: esGrillaVálida(grilla)
    """
    return ('A',1)

def esLaÚltimaPosiciónEnGrilla(posición: Posición, grilla: Grilla) -> bool:
    """ Indica si la posición *posición* es la última posición de la grilla *grilla*.
        PRE: esGrillaVálida(grilla)
        PRE: esPosiciónVálidaEnGrilla(posición, grilla)
    """
    return númeroDeFila(letraDePosición(posición)) == cantidadDeFilasGrilla(grilla) and \
        númeroDePosición(posición) == cantidadDeColumnasGrilla(grilla)

def posiciónSiguienteEnGrilla(posición: Posición, grilla: Grilla) -> Posición:
    """ Describe la posición siguiente a *posición* en la grilla *grilla*.
        PRE: esGrillaVálida(grilla)
        PRE: esPosiciónVálidaEnGrilla(posición, grilla)
        PRE: not esLaÚltimaPosiciónEnGrilla(posición, grilla)
    """
    return (siguienteLetra(letraDePosición(posición)), 1) \
        if númeroDePosición(posición) == cantidadDeColumnasGrilla(grilla) \
        else (letraDePosición(posición), númeroDePosición(posición) + 1)

def hayPosiciónAdyacenteAl(grilla: Grilla, posición: Posición, dirección: Dirección) -> bool:
    """ Indica si hay una posición adyacente a *posición* en la grilla *grilla* hacia *dirección*.
        PRE: esGrillaVálida(grilla)
        PRE: esPosiciónVálidaEnGrilla(posición, grilla)
    """
    if dirección == ARRIBA:
        return númeroDeFila(letraDePosición(posición)) < cantidadDeFilasGrilla(grilla)
    elif dirección == DERECHA:
        return númeroDePosición(posición) < cantidadDeColumnasGrilla(grilla)
    elif dirección == ABAJO:
        return númeroDeFila(letraDePosición(posición)) > 1
    else: # dirección == IZQUIERDA:
        return númeroDePosición(posición) > 1

def posiciónAdyacenteAl(grilla: Grilla, posición: Posición, dirección: Dirección) -> Posición:
    """ Describe la posición adyacente a *posición* en la grilla *grilla* hacia *dirección*.
        PRE: esGrillaVálida(grilla)
        PRE: esPosiciónVálidaEnGrilla(posición, grilla)
        PRE: hayPosiciónAdyacenteAl(grilla, posición, dirección)
    """
    if dirección == ARRIBA:
        return (siguienteLetra(letraDePosición(posición)), númeroDePosición(posición))
    elif dirección == DERECHA:
        return (letraDePosición(posición), númeroDePosición(posición)+1)
    elif dirección == ABAJO:
        return (anteriorLetra(letraDePosición(posición)), númeroDePosición(posición))
    else: # dirección == IZQUIERDA:
        return (letraDePosición(posición), númeroDePosición(posición)-1)

def cambiarCeldaGrilla(grilla: Grilla, posición: Posición, contenido: Celda):
    """ Cambia la posición *posición* de la grilla *grilla* por *posición*.
        PRE: esGrillaVálida(grilla)
        PRE: esPosiciónVálidaEnGrilla(posición, grilla)
    """
    grilla[númeroDeFila(letraDePosición(posición))-1][númeroDePosición(posición)-1] = contenido

# Lista de posiciones

def sonPosicionesVálidas(posiciones: list[Posición]) -> bool:
    """ Indica si todas las posiciones en *posiciones* son válidas. """
    posiciónActual = 0
    while posiciónActual < len(posiciones) and \
        esPosiciónVálida(posiciones[posiciónActual]):
            posiciónActual += 1
    return posiciónActual == len(posiciones)

def pertenecePosición(posiciónBuscada: Posición, posiciones: list[Posición]) -> bool:
    """ Indica si la posición *posiciónBuscada* pertenece a la lista *posiciones*. """
    posiciónActualEnLista = 0
    while posiciónActualEnLista < len(posiciones) and \
        not mismaPosición(posiciónBuscada, posiciones[posiciónActualEnLista]):
            posiciónActualEnLista += 1
    return posiciónActualEnLista < len(posiciones)

def todasEnLaMismaFila(posiciones: list[Posición]) -> bool:
    """ Indica si todas las posiciones en *posiciones* pertenecen a la misma fila.
        PRE: sonPosicionesVálidas(posiciones)
    """
    if len(posiciones) == 0:
        return True
    letraDeFila = letraDePosición(posiciones[0])
    posiciónActual = 1
    while posiciónActual < len(posiciones) and letraDePosición(posiciones[posiciónActual]) == letraDeFila:
        posiciónActual += 1
    return posiciónActual == len(posiciones)

def todasEnLaMismaColumna(posiciones: list[Posición]) -> bool:
    """ Indica si todas las posiciones en *posiciones* pertenecen a la misma columna.
        PRE: sonPosicionesVálidas(posiciones)
    """
    if len(posiciones) == 0:
        return True
    númeroDeColumna = númeroDePosición(posiciones[0])
    posiciónActual = 1
    while posiciónActual < len(posiciones) and númeroDePosición(posiciones[posiciónActual]) == númeroDeColumna:
        posiciónActual += 1
    return posiciónActual == len(posiciones)

def columnasConsecutivasAscendentes(posiciones: list[Posición]) -> bool:
    """ Indica si las columnas de las posiciones en *posiciones* son consecutivas de forma ascendente.
        PRE: sonPosicionesVálidas(posiciones)
    """
    if len(posiciones) == 0:
        return True
    columnaActual = númeroDePosición(posiciones[0])
    posiciónActual = 1
    while posiciónActual < len(posiciones) and númeroDePosición(posiciones[posiciónActual]) == columnaActual + 1:
        posiciónActual += 1
        columnaActual += 1
    return posiciónActual == len(posiciones)

def columnasConsecutivasDescendentes(posiciones: list[Posición]) -> bool:
    """ Indica si las columnas de las posiciones en *posiciones* son consecutivas de forma descendente.
        PRE: sonPosicionesVálidas(posiciones)
    """
    if len(posiciones) == 0:
        return True
    columnaActual = númeroDePosición(posiciones[0])
    posiciónActual = 1
    while posiciónActual < len(posiciones) and númeroDePosición(posiciones[posiciónActual]) == columnaActual - 1:
        posiciónActual += 1
        columnaActual -= 1
    return posiciónActual == len(posiciones)

def filasConsecutivasAscendentes(posiciones: list[Posición]) -> bool:
    """ Indica si las filas de las posiciones en *posiciones* son consecutivas de forma ascendente.
        PRE: sonPosicionesVálidas(posiciones)
    """
    if len(posiciones) == 0:
        return True
    filaActual = númeroDeFila(letraDePosición(posiciones[0]))
    posiciónActual = 1
    while posiciónActual < len(posiciones) and \
        númeroDeFila(letraDePosición(posiciones[posiciónActual])) == filaActual + 1:
            posiciónActual += 1
            filaActual += 1
    return posiciónActual == len(posiciones)

def filasConsecutivasDescendentes(posiciones: list[Posición]) -> bool:
    """ Indica si las filas de las posiciones en *posiciones* son consecutivas de forma descendente.
        PRE: sonPosicionesVálidas(posiciones)
    """
    if len(posiciones) == 0:
        return True
    filaActual = númeroDeFila(letraDePosición(posiciones[0]))
    posiciónActual = 1
    while posiciónActual < len(posiciones) and \
        númeroDeFila(letraDePosición(posiciones[posiciónActual])) == filaActual - 1:
            posiciónActual += 1
            filaActual -= 1
    return posiciónActual == len(posiciones)

def posicionesOrdenadas(posiciones: list[Posición]) -> list[Posición]:
    """ Describe una lista de posiciones con las posiciones en *posiciones* pero ordenadas. """
    return sorted(posiciones)

# BarcoEnGrilla

def tamañoBarco(barco: BarcoEnGrilla) -> int:
    """ Describe el tamaño del barco *barco*.
        PRE: esBarcoVálido(barco)
    """
    return len(barco)

def esBarcoVálido(barco: BarcoEnGrilla) -> bool:
    """ Indica si el barco *barco* es válido.
        Para ser un barco válido, debe tener al menos una sección y todas las posiciones que
            lo componen deben estar en la misma fila o en la misma columna y ser contíguas.
    """
    return tamañoBarco(barco) > 0 and sonPosicionesVálidas(barco) and \
        (esBarcoVálidoHorizontal(barco) or esBarcoVálidoVertical(barco))

def sonBarcosVálidos(barcos: list[BarcoEnGrilla]) -> bool:
    """ Indica si todos los barcos en *barcos* son barcos válidos. """
    barcoActual = 0
    while barcoActual < len(barcos) and esBarcoVálido(barcos[barcoActual]):
        barcoActual += 1
    return barcoActual == len(barcos) and not hayBarcosSuperpuestosOAdyacentes(barcos)

def esBarcoVálidoHorizontal(barco: BarcoEnGrilla) -> bool:
    """ Indica si el barco *barco* es válido en horizontal.
        Para ser un barco válido en horizontal, todas las posiciones que lo componen deben estar
            en la misma fila y sus columnas ser consecutivas en forma ascendente o descendente.
        PRE: sonPosicionesVálidas(barco)
    """
    return todasEnLaMismaFila(barco) and columnasConsecutivasAscendentes(sorted(barco))

def esBarcoVálidoVertical(barco: BarcoEnGrilla) -> bool:
    """ Indica si el barco *barco* es válido en vertical.
        Para ser un barco válido en vertical, todas las posiciones que lo componen deben estar
            en la misma columna y sus filas ser consecutivas en forma ascendente o descendente.
        PRE: sonPosicionesVálidas(barco)
    """
    return todasEnLaMismaColumna(barco) and filasConsecutivasAscendentes(sorted(barco))

def hayBarcosSuperpuestosOAdyacentes(barcos: list[BarcoEnGrilla]) -> bool:
    """ Indica si algún barco en *barcos* tiene una posición adyacente a una
            posición ocupada por otro barco de *barcos* o una posición compartida
            con otro barco de *barcos*.
    """
    barcoActual = 0
    while barcoActual < len(barcos) and \
        not colisionaBarco(barcos[barcoActual], barcos[barcoActual+1:]) and \
        not hayBarcoAdyacente(barcos[barcoActual], barcos[barcoActual+1:]):
        barcoActual += 1
    return barcoActual == len(barcos)

def colisionaBarco(barco: BarcoEnGrilla, barcos: list[BarcoEnGrilla]):
    """ Indica si el barco *barco* comparte alguna posición con un barco de *barcos*. """
    barcoActual = 0
    while barcoActual < len(barcos) and not colisionaBarcoCon(barco, barcos[barcoActual]):
        barcoActual += 1
    return barcoActual == len(barcos)

def hayBarcoAdyacente(barco: BarcoEnGrilla, barcos: list[BarcoEnGrilla]):
    """ Indica si el barco *barco* tiene una posición adyacente a una posición
            ocupada por un barco de *barcos*. """
    barcoActual = 0
    while barcoActual < len(barcos) and not sonAdyecentesEnAlgunaPosición(barco, barcos[barcoActual]):
        barcoActual += 1
    return barcoActual == len(barcos)

def colisionaBarcoCon(barco1: BarcoEnGrilla, barco2: BarcoEnGrilla):
    """ Indica si los barcos *barco1* y *barco2* tienen alguna posición compartida. """
    posiciónActual = 0
    while posiciónActual < tamañoBarco(barco1) and \
        not pertenecePosición(barco1[posiciónActual], barco2):
            posiciónActual += 1
    return posiciónActual == len(barco1)

def sonAdyecentesEnAlgunaPosición(barco1: BarcoEnGrilla, barco2: BarcoEnGrilla):
    """ Indica si el barco *barco1* tiene alguna posición adyacente a alguna posición
            de *barco2*. """
    posiciónActual = 0
    while posiciónActual < tamañoBarco(barco1) and \
        not hayPosiciónAdyacenteEn(barco1[posiciónActual], barco2):
            posiciónActual += 1
    return posiciónActual == len(barco1)

# BarcoEnGrilla en Grilla

def sePuedeColocarBarco(barco: BarcoEnGrilla, grilla: Grilla) -> bool:
    """ Indica si el barco *barco* se puede colocar en la grilla *grilla*.
        Para eso, el barco debe ser válido, debe caer dentro de las dimensiones de la grilla y
            no haber en la grilla otro barco que colisione con él ni que quede adyacente a él.
        PRE: esGrillaVálida(grilla)
    """
    return esBarcoVálido(barco) and \
        sonPosicionesVálidasEnGrilla(barco, grilla) and \
        not colisionaBarcoEnGrilla(barco, grilla) and \
        not quedaBarcoAdyacenteAOtroBarcoEnGrilla(barco, grilla)

def colisionaBarcoEnGrilla(barco: BarcoEnGrilla, grilla: Grilla) -> bool:
    """ Indica si el barco *barco* colisiona con otro barco en la grilla *grilla*.
        PRE: esGrillaVálida(grilla)
        PRE: esBarcoVálido(barco)
        PRE: sonPosicionesVálidasEnGrilla(barco, grilla)
    """
    posiciónActual = 0
    while posiciónActual < len(barco) and celdaEnPosición(grilla, barco[posiciónActual]) != BARCO:
        posiciónActual += 1
    return posiciónActual == len(barco)

def quedaBarcoAdyacenteAOtroBarcoEnGrilla(barco: BarcoEnGrilla, grilla: Grilla) -> bool:
    """ Indica si el barco *barco* queda adyacente con otro barco en la grilla *grilla*.
        PRE: esGrillaVálida(grilla)
        PRE: esBarcoVálido(barco)
        PRE: sonPosicionesVálidasEnGrilla(barco, grilla)
    """
    posiciónActual = 0
    while posiciónActual < len(barco) and not hayBarcoAdyacenteEnGrilla(barco[posiciónActual], grilla):
        posiciónActual += 1
    return posiciónActual == len(barco)

def hayBarcoAdyacenteEnGrilla(grilla: Grilla, posición: Posición) -> bool:
    """ Indica si la posición *posición* de la grilla *grilla* es adyacente a una posición ocupada por un barco.
        PRE: esGrillaVálida(grilla)
        PRE: esPosiciónVálidaEnGrilla(posición, grilla)
    """
    direcciónActual = 0
    while direcciónActual < len(direccionesOrtogonales()) and \
        not hayBarcoAl(grilla, posición, direccionesOrtogonales()[direcciónActual]):
            direcciónActual += 1
    return direcciónActual < len(direccionesOrtogonales())

def hayBarcoAl(grilla, posición, dirección) -> bool:
    """ Indica si hay una posición adyacente a *posición* hacia *dirección* en la grilla *grilla* que tenga barco.
        PRE: esGrillaVálida(grilla)
        PRE: esPosiciónVálidaEnGrilla(posición, grilla)
    """
    return hayPosiciónAdyacenteAl(grilla, posición, dirección) and \
        celdaEnPosición(grilla, posiciónAdyacenteAl(grilla, posición, dirección)) == BARCO

def colocarBarcos(estadoDeJuego: EstadoJuego, barcosAColocar: list[BarcoEnGrilla], jugador: Jugador):
    """ Coloca los barcos *barcosAColocar* en el tablero del jugador *jugador* del juego *estadoDeJuego*.
        PRE: esEstadoDeJuegoVálido(estadoDeJuego)
        PRE: sonBarcosVálidos(barcos)
        PRE: esGrillaVacía(grillaLocal(tableroDeJugador(estadoDeJuego, jugador)))
        PRE: para todo barco *barco* de tipo BarcoEnGrilla en *barcosAColocar* se cumple:
          sePuedeColocarBarco(barco, grillaLocal(tableroDeJugador(estadoDeJuego, jugador)))
    """
    for barco in barcosAColocar:
        colocarBarco(barco, grillaLocal(tableroDeJugador(estadoDeJuego, jugador)))

def colocarBarco(barco: BarcoEnGrilla, grilla: Grilla):
    """ Coloca el barco *barco* en la grilla *grilla*.
        PRE: esGrillaVálida(grilla)
        PRE: sePuedeColocarBarco(barco, grilla)
    """
    for posición in barco:
        cambiarCeldaGrilla(grilla, posición, BARCO)