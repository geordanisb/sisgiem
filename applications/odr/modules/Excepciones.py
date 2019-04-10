# -*- coding: utf-8 -*-
class NotCentral(Exception):
    def __init__(self,central):
        self.central = central

    def __str__(self):
        return """Se ha intentado insertar un record con central telefónica = {}, la cual no existe en el sistema. 
        Debe primero agregar las centrales necesarias para evitar este tipo de error.
        """.format(self.central)