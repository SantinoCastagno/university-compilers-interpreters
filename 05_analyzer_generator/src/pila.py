class Pila:
    items = []

    def __init__(self):
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def apilar(self, item):
        self.items.append(item)

    def desapilar(self):
        if not self.esta_vacia():
            return self.items.pop()
        else:
            return None

    def ver_cima(self):
        if not self.esta_vacia():            
            return self.items[-1]
        else:
            return None

    def recuperar_cima(self):
        if not self.esta_vacia():
            return self.items[-1].tabla
        else:
            return None

    def tamanio(self):
        return len(self.items)