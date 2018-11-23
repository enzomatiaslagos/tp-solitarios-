from mazo import crear_mazo
from carta import criterio, CONSECUTIVA, ASCENDENTE, MISMO_PALO, DESCENDENTE, DISTINTO_COLOR
from mesa import SALIR, FUNDACION, PILA_TABLERO, MAZO, DESCARTE
from pila_cartas import PilaCartas, SolitarioError

class SolitarioEliminador:
    """Interfaz para implementar un solitario."""

    def __init__(self, mesa):
        """Inicializa con una mesa creada y vacía."""
        self.mesa = mesa

    def armar(self):
        """Arma el tablero con la configuración inicial."""
        self.mesa.mazo = crear_mazo()

        for i in range(6):
            self.mesa.fundaciones.append(PilaCartas(criterio_apilar=criterio(orden=CONSECUTIVA)))

        for i in range(4):
            self.mesa.pilas_tablero.append(PilaCartas(pila_visible=True))
            for j in range(13):
                carta = self.mesa.mazo.desapilar()
                carta.boca_abajo = False
                self.mesa.pilas_tablero[i].apilar(carta, forzar=True)

    def termino(self):
        """Avisa si el juego se terminó."""
        for pila in self.mesa.pilas_tablero:
            if not pila.es_vacia():
                return False
        return self.mesa.mazo.es_vacia() and self.mesa.descarte.es_vacia()




    def jugar(self, jugada):
        """Efectúa una movida.
            La jugada es una lista de pares (PILA, numero). (Ver mesa.)
            Si no puede realizarse la jugada se levanta una excepción SolitarioError *descriptiva*."""
        pila1, cual1 = jugada[0]
        pila2, cual2 = jugada[1] if len(jugada) == 2 else (SALIR, 0)

        if len(jugada) == 1 and pila1 == MAZO:
            raise SolitarioError("No puede sacar cartas del maso")

        if len(jugada) == 1 and pila1 == PILA_TABLERO:
            for fundacion in self.mesa.fundaciones:
                try:
                    fundacion.apilar(self.mesa.pilas_tablero[cual1].tope())
                    self.mesa.pilas_tablero[cual1].desapilar()
                    return
                except SolitarioError:
                    pass
            #raise SolitarioError("No puede moverse esa carta a ninguna fundación")

        if pila1 == FUNDACION:
            raise SolitarioError("Solo se pueden mover cartas del tablero a las fundaciones. \nUna vez en la fundacion, la carta no se puede mover mas")
        elif pila1 == PILA_TABLERO and pila2 == FUNDACION:
            if self.mesa.pilas_tablero[cual1].es_vacia():
                raise SolitarioError("La pila está vacía")
            self.mesa.fundaciones[cual2].apilar(self.mesa.pilas_tablero[cual1].tope())
            self.mesa.pilas_tablero[cual1].desapilar()

        else:
            raise SolitarioError("Movimiento invalido")

