from mazo import crear_mazo
from carta import criterio, CONSECUTIVA, ASCENDENTE, MISMO_PALO, DESCENDENTE, DISTINTO_COLOR
from mesa import SALIR, FUNDACION, PILA_TABLERO, MAZO, DESCARTE
from pila_cartas import PilaCartas, SolitarioError

class SolitarioClasico:
    """Interfaz para implementar un solitario."""

    def __init__(self, mesa):
        """Inicializa con una mesa creada y vacía."""
        self.mesa = mesa

    def armar(self):
        """Arma el tablero con la configuración inicial."""
        self.mesa.mazo = crear_mazo(mazos=1, palos=4)
        self.mesa.descarte = PilaCartas()

        for i in range(4):
            self.mesa.fundaciones.append(PilaCartas(criterio_apilar=criterio(palo=MISMO_PALO, orden=ASCENDENTE), valor_inicial=1))

        for i in range(4):
            self.mesa.pilas_tablero.append(PilaCartas(pila_visible=True, criterio_apilar=criterio(palo=DISTINTO_COLOR, orden=DESCENDENTE), criterio_mover=0))
            self.mesa.pilas_tablero[i].apilar(self.mesa.mazo.desapilar(), forzar=True)
            self.mesa.pilas_tablero[i].tope().voltear()

    def termino(self):
        """Avisa si el juego se terminó."""
        if not self.gano() and self.existen_movimientos():
            return False
        else:
            return True

    def gano(self):
        """Devuelve True si gano, False en caso contrario"""
        for fundacion in self.mesa.fundaciones:
            if fundacion.tope().valor != 13:
                return False
        return True

    def existen_movimientos(self):
        """Analiza si existen movimientos válidos para seguir jugando. Devuelve True si existen y False en caso contrario"""
        no = 0
        if self.mesa.mazo.es_vacia():
            for fundacion in self.mesa.fundaciones:
                try:
                    for pila in self.mesa.pilas_tablero:
                        fundacion.mover(pila)
                    fundacion.apilar(self.mesa.descarte.tope())
                except SolitarioError:
                    no += 1
            for pila in self.mesa.pilas_tablero:
                try:
                    pila.apilar(self.mesa.descarte.tope())
                except SolitarioError:
                    no += 1
        if not self.mesa.mazo.es_vacia() or no != 2:
            return True
        return False




    def jugar(self, jugada):
        """Efectúa una movida.
            La jugada es una lista de pares (PILA, numero). (Ver mesa.)
            Si no puede realizarse la jugada se levanta una excepción SolitarioError *descriptiva*."""

        if len(jugada) == 1 and jugada[0][0] == PILA_TABLERO:
            for fundacion in self.mesa.fundaciones:
                try:
                    fundacion.apilar(self.mesa.pilas_tablero[jugada[0][1]].tope())
                    self.mesa.pilas_tablero[jugada[0][1]].desapilar()
                    return
                except SolitarioError:
                    pass
            raise SolitarioError("Esa carta no se puede mover a ninguna pila o fundacion")

        elif len(jugada) == 1 and jugada[0][0] == DESCARTE:
            for fundacion in self.mesa.fundaciones:
                try:
                    fundacion.apilar(self.mesa.descarte.tope())
                    self.mesa.descarte.desapilar()
                    return
                except SolitarioError:
                    pass
            raise SolitarioError("Esa carta no se puede mover a ninguna pila o fundacion")


        elif len(jugada) == 1 and jugada[0][0] == MAZO:
            if not self.mesa.mazo.es_vacia():
                self.mesa.descarte.apilar(self.mesa.mazo.desapilar(), forzar=True)
                self.mesa.descarte.tope().voltear()
            else:
                raise SolitarioError("No hay mas cartas que sacar del mazo")

        elif len(jugada) == 2:
            origen, en = jugada[0]
            destino, hasta = jugada[1]

            if origen == PILA_TABLERO and destino == FUNDACION:
                if self.mesa.pilas_tablero[en].es_vacia():
                    raise SolitarioError("La pila esta vacia, no hay elementos para mover")
                else:
                    self.mesa.fundaciones[hasta].apilar(self.mesa.pilas_tablero[en].tope())
                    self.mesa.pilas_tablero[en].desapilar()

            elif origen == PILA_TABLERO and destino == PILA_TABLERO:
                if self.mesa.pilas_tablero[en].es_vacia():
                    raise SolitarioError("La pila esta vacia, no hay elementos para mover")
                else:
                    self.mesa.pilas_tablero[hasta].mover(self.mesa.pilas_tablero[en])

            elif origen == FUNDACION and destino == PILA_TABLERO:
                if self.mesa.fundaciones[en].es_vacia():
                    raise SolitarioError("La pila esta vacia, no hay elementos para mover")
                else:
                    self.mesa.pilas_tablero[hasta].apilar(self.mesa.fundaciones[en].tope())

            elif origen == DESCARTE and (destino == FUNDACION or destino == PILA_TABLERO):
                if self.mesa.descarte.es_vacia():
                    raise SolitarioError("La pila esta vacia, no hay elementos para mover")
                else:
                    if destino == FUNDACION:
                        self.mesa.fundaciones[hasta].apilar(self.mesa.descarte.tope())
                    else:
                        self.mesa.pilas_tablero[hasta].apilar(self.mesa.descarte.tope())
                    self.mesa.descarte.desapilar()

        elif len(jugada) > 2:
            origen, en = jugada[0]
            if origen == PILA_TABLERO:
                for i in range(1,len(jugada)-1):
                    if jugada[i] == jugada[0]:
                        self.mesa.pilas_tablero[en].criterio_mover += 1
                    else:
                        raise SolitarioError("Movimiento incorrecto")

