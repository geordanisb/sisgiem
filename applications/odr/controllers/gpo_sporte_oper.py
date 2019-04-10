from ParteGSO import SIPREC
siprec = SIPREC()

@auth.requires(auth.has_membership("administrador") or auth.has_membership("editor_odr"))
def importar_interrupciones_desde_siprec():
    #session.forget(response)
    return siprec.importar()

def index():
    titulo = "Grupo de Soporte a la Operación - Acciones"
    contenido = MENU(response.menu[1:])
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

def centros_telefonicos():
    titulo = "Centros telefónicos (CTLC)"

    contenido = grid("ctlc")
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

def centrales_telefonicas():
    titulo = "Centrales telefónicas"
    contenido = grid("central_telefonica")
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

def grid(tabla):
    db[tabla].id.readable = False
    return SQLFORM.grid(db[tabla])