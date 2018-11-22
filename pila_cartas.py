from carta import Carta
from carta import criterio, MISMO_PALO

class SolitarioError(Exception):
    """Tipo de Exception para todos los errores del Solitario."""
    # No tocar nada acá, el pass está bien como toda implementación :).
    pass


class PilaCartas:
    """Representa una pila de cartas en el tablero."""

    def __init__(self, pila_visible=False, valor_inicial=None, puede_desapilar=True, criterio_apilar=None, criterio_mover=None):
        """Se construye una pila vacía. El comportamiento estará regido por:
            pila_visible: Bool. ¿Al imprimir la pila se muestra sólo la carta
                del tope o son visibles todas las cartas de la pila?
            valor_inicial: Número 1 al 13. Si está presente sólo se puede
                apilar ese valor sobre una pila vacía.
            puede_desapilar: Bool. ¿En la pila se apila y se desapila o sólo
                se puede apilar?
            criterio_apilar: f(a, b). Si la pila no está vacía y tope() == a,
                f(a, b) indica si puede apilarse la carta b sobre la pila.
            criterio_mover: f(a, b). Siendo la pila una secuencia de cartas
                [cn, ..., c2, c1, c0], donde c0 es el tope, voy a poder mover
                en bloque parte de la pila siempre y cuando f(c1, c0),
                f(c2, c1), etc. hasta que la función falle.
        Todos los parámetros son optativos y tienen valores por omisión. En
        el caso de los parámetros que sean None, los mismos no se
        considerarán como restricciones (por ejemplo, si valor_inicial == None
        se desactivará el chequeo de valor_inicial)."""
        self.items = []
        self.pila_visible = pila_visible
        self.valor_inicial = valor_inicial
        self.puede_desapilar = puede_desapilar
        self.criterio_apilar = criterio_apilar
        self.criterio_mover = criterio_mover

    def es_vacia(self):
        """Indica si la pila se encuentra vacía."""
        return len(self.items) == 0

    def tope(self):
        """Devuelve la carta tope de la pila.
        Levanta SolitarioError en caso de error."""
        if not self.es_vacia():
            return self.items[-1]
        raise SolitarioError("La pila esta vacia.")

    def apilar(self, carta, forzar=False):
        """Apila una carta en la pila. Si forzar es True desactiva los chequeos
        sobre el valor_inicial y el criterio_apilar.
        Levanta SolitarioError en caso de no poder apilar."""
        if forzar or self.es_vacia() and not self.valor_inicial:
            self.items.append(carta)
        elif self.es_vacia():
            if carta.valor == self.valor_inicial:
                self.items.append(carta)
            else:
                raise SolitarioError("No se puede apilar la carta")
        elif not self.es_vacia():
            c = self.criterio_apilar
            if c(self.tope(), carta):
                self.items.append(carta)
            else:
                raise SolitarioError("No se puede apilar la carta")

    def desapilar(self):
        """Desapila una carta. Levanta SolitarioError en caso de no poder
        desapilar."""
        if self.es_vacia():
            raise SolitarioError("No hay mas cartas para desapilar")
        return self.items.pop()

    def mover(self, origen):
        """Siendo origen otra PilaCartas intenta mover un subpilón de cartas
        de origen sobre la pila.
        Las primera carta que se apile sobre la pila debe validar
        criterio_apilar mientras que la cantidad de cartas máxima a mover
        desde origen dependerá de criterio_mover.
        Independientemente del criterio_mover no podrán moverse cartas que se
        encuentren boca abajo y sobre una carta boca abajo puede apilarse
        cualquier valor.
        Debe levantarse SolitarioError en caso de no poder mover ninguna carta
        de origen a la pila."""
        aux = PilaCartas(pila_visible=True)
        try:
            while not origen.es_vacia() and not origen.tope().boca_abajo:
                aux.apilar(origen.tope(), forzar=True)
                origen.desapilar()
            while not aux.es_vacia():
                try:
                    self.apilar(aux.tope())
                    aux.desapilar()
                except SolitarioError:
                    origen.apilar(aux.tope(),forzar=True)
                    aux.desapilar()
                    try:
                        self.apilar(aux.tope())
                        aux.desapilar()
                    except SolitarioError:
                        origen.apilar(aux.tope())
                        aux.desapilar()
            if origen.tope().boca_abajo:
                origen.tope().voltear()
        except SolitarioError:
            if not origen.es_vacia():
                raise SolitarioError("No se puede mover la pila")
            return

    def __str__(self):
        """Devuelve una representación de la pila.
        La misma será una X si la pila estuviera vacía.
        Si pila_visible == True se representará a la pila como todas las
        cartas de base a tope separadas por espacios. Si no sólo se
        representará según el tope."""
        if self.es_vacia():
            return "X"
        elif self.pila_visible:
            mostrar =""
            for elemento in self.items:
                mostrar += "{} ".format(str(elemento))
            return mostrar
        return str(self.tope())

    def __repr__(self):
        """Ídem __str__."""
        pass
